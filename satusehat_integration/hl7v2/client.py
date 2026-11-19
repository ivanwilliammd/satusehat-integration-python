"""MLLP client for analyzers and LIS endpoints.

Two rules that matter operationally:

* transport failures retry, application verdicts do not — retrying an ``AE`` turns one bad message
  into a thousand;
* ``MSA-2`` must echo ``MSH-10``, otherwise the ACK is stale or misrouted and must not count as
  success.
"""

from __future__ import annotations

import socket
import time
from dataclasses import dataclass

from .ack import ACCEPT, ERROR
from .message import Message
from .mllp import MllpReader, frame


@dataclass
class SendResult:
    code: str
    control_id: str
    text: str
    attempts: int = 1
    latency_ms: int = 0
    accepted: bool = False


class Client:
    def __init__(self, address: str, timeout: float = 10.0, retries: int = 2) -> None:
        host, _, port = address.rpartition(":")
        self.address = address
        self.host = host
        self.port = int(port)
        self.timeout = timeout
        self.retries = retries

    def send(self, message: Message) -> SendResult:
        return self.session([message])[0]

    def session(self, messages: list[Message]) -> list[SendResult]:
        """Sends several messages over one connection, one result per message, in order."""
        results: list[SendResult] = []
        sock: socket.socket | None = None
        reader = MllpReader()
        try:
            for message in messages:
                last_error: Exception | None = None
                for attempt in range(1, self.retries + 2):
                    try:
                        if sock is None:
                            sock = socket.create_connection((self.host, self.port), timeout=self.timeout)
                            reader = MllpReader()
                        results.append(self._exchange(sock, reader, message))
                        last_error = None
                        break
                    except OSError as exc:
                        last_error = exc
                        if sock is not None:
                            sock.close()
                            sock = None
                        if attempt > self.retries:
                            break
                        time.sleep(0.2 * attempt)
                if last_error is not None:
                    raise RuntimeError(
                        f"MLLP send failed at message {len(results) + 1} after {self.retries} retries: "
                        f"{last_error}"
                    ) from last_error
        finally:
            if sock is not None:
                sock.close()
        return results

    def interpret(self, sent: Message, ack_raw: str) -> SendResult:
        """Parses an ACK received out-of-band; daemons that own their socket can reuse it."""
        ack = Message.parse(ack_raw)
        if ack.message_type() != "ACK":
            raise ValueError(f"reply is not an ACK but {ack.message_type()}")
        echo = ack.get("MSA.2")
        if echo and echo != sent.control_id():
            raise ValueError(
                f"MSA-2 ({echo}) does not match MSH-10 ({sent.control_id()}) — stale or misrouted ACK"
            )
        code = (ack.get("MSA.1") or ERROR).upper()
        return SendResult(code=code, control_id=echo, text=ack.get("MSA.3"), accepted=code == ACCEPT)

    def _exchange(self, sock: socket.socket, reader: MllpReader, message: Message) -> SendResult:
        started = time.monotonic()
        sock.sendall(frame(str(message)).encode("latin-1"))
        raw = self._read_ack(sock, reader)
        result = self.interpret(message, raw)
        result.latency_ms = int((time.monotonic() - started) * 1000)
        return result

    def _read_ack(self, sock: socket.socket, reader: MllpReader) -> str:
        buffered = reader.take()
        if buffered:
            return buffered
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                raise ConnectionError("peer closed the connection before sending an ACK")
            reader.push(chunk.decode("latin-1"))
            message = reader.take()
            if message:
                return message

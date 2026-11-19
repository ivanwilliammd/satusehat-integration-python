"""HL7 v2 tests.

The corpus in ``fixtures/`` is copied byte-for-byte from the PHP SDK: ten messages a hospital sends
and ten that must be refused. Parity between the five SDKs is a test, not a claim.
"""

from __future__ import annotations

import json
import socket
import socketserver
import threading
from pathlib import Path

import pytest

from .ack import ACCEPT, ERROR, Ack
from .client import Client
from .encoding import charset_of, decode, encode
from .message import HL7Error, Message
from .mllp import MllpReader, frame, shift, split, unframe
from .profiles import PROFILES

ADT = (
    "MSH|^~\\&|SIMRS|RS-01|SATUSEHAT|KEMKES|20261118120000||ADT^A01^ADT_A01|MSG00001|P|2.5.1\r"
    "EVN|A01|20261118115900\r"
    "PID|1||0001234567890^^^NIK^NIK||ANGGRAENI^SITI^^^\r"
    "PV1|1|I|WARD01^101^A\r"
    "OBX|1|NM|8867-4^Heart rate^LN||78|/min|||||F\r"
)

FIXTURES = Path(__file__).parent / "fixtures"


class TestMessage:
    def test_parses_segments_and_paths(self) -> None:
        msg = Message.parse(ADT)
        assert len(msg.all()) == 5
        assert msg.message_type() == "ADT"
        assert msg.trigger_event() == "A01"
        assert msg.control_id() == "MSG00001"
        assert msg.get("PID.5.1") == "ANGGRAENI"
        assert msg.get("OBX.5") == "78"

    def test_round_trips_byte_for_byte(self) -> None:
        assert str(Message.parse(ADT)) == ADT

    def test_decodes_and_reencodes_escapes(self) -> None:
        msg = Message.parse(
            "MSH|^~\\&|A|B|C|D|20260101||ADT^A08|1|P|2.5.1\r"
            "PID|1||123||SMITH\\S\\JOHN\\F\\JR\\T\\II\r"
        )
        assert msg.get("PID.5.1") == "SMITH^JOHN|JR&II"
        msg.set("PID.5.2", "O'BRIEN&SONS")
        assert Message.parse(str(msg)).get("PID.5.2") == "O'BRIEN&SONS"

    def test_rejects_message_without_msh(self) -> None:
        with pytest.raises(HL7Error, match="MSH"):
            Message.parse("PID|1||123\r")

    def test_reports_charset_without_reencoding(self) -> None:
        assert Message.parse(ADT).charset() == "ASCII"
        assert charset_of("UNICODE UTF-8") == "UTF-8"
        assert charset_of("8859/1") == "ISO-8859-1"

    def test_escape_helpers_are_inverse(self) -> None:
        raw = "a|b^c~d&e\\f"
        assert decode(encode(raw)) == raw


class TestMllp:
    def test_frames_and_unframes(self) -> None:
        assert "ADT^A01" in unframe(frame(ADT))

    def test_never_emits_truncated_message_at_a_chunk_boundary(self) -> None:
        stream = frame(ADT) + frame(ADT.replace("ADT^A01", "ADT^A08"))
        complete = {ADT, ADT.replace("ADT^A01", "ADT^A08")}
        for cut in range(1, len(stream), 7):
            partial = split(stream[:cut])
            assert len(partial) <= 1
            for message in partial:
                assert message in complete
        assert len(split(stream)) == 2

    def test_reader_keeps_the_second_frame_in_the_same_chunk(self) -> None:
        reader = MllpReader()
        reader.push(frame("MSG-A") + frame("MSG-B"))
        assert reader.take() == "MSG-A"
        assert reader.take() == "MSG-B"
        assert reader.take() is None

    def test_shift_returns_buffer_untouched_when_incomplete(self) -> None:
        assert shift("\x0bpartial") == ("", "\x0bpartial")


class TestAck:
    def test_echoes_control_id_and_verdict(self) -> None:
        ack = Ack.build(Message.parse(ADT))
        assert ack.message_type() == "ACK"
        assert ack.get("MSA.1") == ACCEPT
        assert ack.get("MSA.2") == "MSG00001"

    def test_error_carries_the_reason(self) -> None:
        ack = Ack.error(Message.parse(ADT), "PID missing")
        assert ack.get("MSA.1") == ERROR
        assert ack.get("MSA.3") == "PID missing"


class TestCorpus:
    @pytest.mark.parametrize("name", sorted(json.loads((FIXTURES / "manifest.json").read_text())["valid"]))
    def test_accepts_messages_a_hospital_sends(self, name: str) -> None:
        manifest = json.loads((FIXTURES / "manifest.json").read_text())
        profile = PROFILES[manifest["valid"][name]["profile"]]()
        msg = Message.parse((FIXTURES / "valid" / f"{name}.hl7").read_text())
        errors = [i for i in profile.validate(msg) if i.severity == "error"]
        assert errors == []

    @pytest.mark.parametrize("name", sorted(json.loads((FIXTURES / "manifest.json").read_text())["invalid"]))
    def test_refuses_messages_that_must_not_reach_a_database(self, name: str) -> None:
        manifest = json.loads((FIXTURES / "manifest.json").read_text())
        spec = manifest["invalid"][name]
        raw = (FIXTURES / "invalid" / f"{name}.hl7").read_text()
        if spec.get("exception"):
            with pytest.raises(HL7Error):
                Message.parse(raw)
            return
        profile = PROFILES[spec["profile"]]()
        paths = [i.path for i in profile.validate(Message.parse(raw))]
        for expected in spec["issues"]:
            assert expected in paths


class _Handler(socketserver.BaseRequestHandler):
    def handle(self) -> None:  # pragma: no cover - exercised through Client
        reader = MllpReader()
        while True:
            chunk = self.request.recv(8192)
            if not chunk:
                return
            reader.push(chunk.decode("latin-1"))
            while True:
                raw = reader.take()
                if raw is None:
                    break
                ack = Ack.build(Message.parse(raw))
                self.request.sendall(frame(str(ack)).encode("latin-1"))


class TestClient:
    @pytest.fixture()
    def server(self):
        srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), _Handler)
        srv.daemon_threads = True
        thread = threading.Thread(target=srv.serve_forever, daemon=True)
        thread.start()
        try:
            yield srv.server_address[1]
        finally:
            srv.shutdown()
            srv.server_close()

    def test_sends_over_a_real_socket(self, server: int) -> None:
        result = Client(f"127.0.0.1:{server}").send(Message.parse(ADT))
        assert result.code == ACCEPT
        assert result.control_id == "MSG00001"
        assert result.accepted is True

    def test_sends_three_messages_over_one_connection(self, server: int) -> None:
        messages = [Message.parse(ADT.replace("MSG00001", cid)) for cid in ("S1", "S2", "S3")]
        results = Client(f"127.0.0.1:{server}").session(messages)
        assert [r.control_id for r in results] == ["S1", "S2", "S3"]

    def test_rejects_a_stale_ack(self) -> None:
        msg = Message.parse(ADT)
        stale = str(Ack.build(msg).set("MSA.2", "OTHER123"))
        with pytest.raises(ValueError, match="does not match"):
            Client("127.0.0.1:1").interpret(msg, stale)

    def test_retries_the_transport_then_fails_clearly(self) -> None:
        closed = socket.socket()
        closed.bind(("127.0.0.1", 0))
        port = closed.getsockname()[1]
        closed.close()
        with pytest.raises(RuntimeError, match="MLLP send failed"):
            Client(f"127.0.0.1:{port}", timeout=0.3, retries=1).send(Message.parse(ADT))

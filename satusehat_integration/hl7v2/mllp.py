"""Minimal Lower Layer Protocol framing: VT ... FS CR.

The string helpers are trivial; the stateful reader is not. MLLP arrives in arbitrary TCP chunks and
one ``recv()`` routinely returns several frames, so a stateless reader hands back the first message and
silently discards the rest.
"""

from __future__ import annotations

VT = "\x0b"
FS = "\x1c"
CR = "\x0d"
MAX_BYTES = 4 * 1024 * 1024


def frame(message: str) -> str:
    return f"{VT}{message}{FS}{CR}"


def unframe(framed: str) -> str:
    return framed.replace(VT, "").replace(FS + CR, "").strip()


def shift(buffer: str) -> tuple[str, str]:
    """Extracts one frame: ``(message, remaining)``; ``("", buffer)`` when incomplete."""
    start = buffer.find(VT)
    if start == -1:
        return "", buffer
    end = buffer.find(FS, start)
    if end == -1:
        return "", buffer
    return buffer[start + 1 : end], buffer[end + 2 :]


def split(stream: str) -> list[str]:
    out: list[str] = []
    buffer = stream
    while True:
        message, buffer = shift(buffer)
        if not message:
            return out
        out.append(message)


class MllpReader:
    """Keeps the bytes that arrived after the last complete frame."""

    def __init__(self, max_bytes: int = MAX_BYTES) -> None:
        self._buffer = ""
        self._max = max_bytes

    def push(self, chunk: str) -> None:
        self._buffer += chunk
        if len(self._buffer) > self._max:
            raise ValueError("MLLP frame exceeds the 4 MB limit.")

    def take(self) -> str | None:
        message, rest = shift(self._buffer)
        if not message:
            return None
        self._buffer = rest
        return message

r"""HL7 v2 escape sequences (chapter 2).

A naive ``split("|")`` corrupts real messages: a pipe inside a name arrives as ``\F\``, a caret inside
an address as ``\S\``. Decoding happens on read and encoding on write, so what is stored is what went
over the wire.
"""

from __future__ import annotations

_DECODE = (
    ("\\F\\", "|"),
    ("\\S\\", "^"),
    ("\\R\\", "~"),
    ("\\E\\", "\\"),
    ("\\T\\", "&"),
)

import re

_HEX = re.compile(r"\\X([0-9A-Fa-f]+)\\")
_CHARSETS = {
    "": "ASCII",
    "ASCII": "ASCII",
    "8859/1": "ISO-8859-1",
    "ISO IR6": "ISO-8859-1",
    "ISO IR100": "ISO-8859-1",
    "UNICODE UTF-8": "UTF-8",
    "UNICODE UTF8": "UTF-8",
    "UTF-8": "UTF-8",
}


def decode(value: str) -> str:
    """Decodes escape sequences. ``\\Z..\\`` (locally defined) and ``\\.br\\`` are left untouched."""
    if "\\" not in value:
        return value
    value = _HEX.sub(lambda m: bytes.fromhex(m.group(1)).decode("latin-1"), value)
    for seq, char in _DECODE:
        value = value.replace(seq, char)
    return value


def encode(value: str) -> str:
    return (
        value.replace("\\", "\\E\\")
        .replace("|", "\\F\\")
        .replace("^", "\\S\\")
        .replace("~", "\\R\\")
        .replace("&", "\\T\\")
    )


def charset_of(msh18: str | None) -> str:
    """MSH-18 declares the charset; it is reported, never used to re-encode bytes."""
    return _CHARSETS.get((msh18 or "").strip().upper(), (msh18 or "").strip().upper())

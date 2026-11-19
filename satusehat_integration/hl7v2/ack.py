"""Acknowledgement builder.

MSA-1 is the verdict (AA accepted, AE error, AR rejected) and MSA-2 echoes MSH-10, which is how the
sender correlates the ACK with what it sent. An ACK without that echo is indistinguishable from a
stale one.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from .message import Message
from .segment import Segment

ACCEPT = "AA"
ERROR = "AE"
REJECT = "AR"


class Ack:
    ACCEPT = ACCEPT
    ERROR = ERROR
    REJECT = REJECT

    @staticmethod
    def build(inbound: Message, code: str = ACCEPT, text: str = "") -> Message:
        msh = inbound.segment("MSH")
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        control_id = uuid.uuid4().hex[:16].upper()
        fields = [
            "MSH",
            "|",
            "^~\\&",
            msh.get("5") if msh else "",
            msh.get("6") if msh else "",
            msh.get("3") if msh else "",
            msh.get("4") if msh else "",
            stamp,
            "",
            "ACK",
            control_id,
            "P",
            (msh.get("12.1") if msh else "") or "2.5.1",
        ]
        msa = Segment("MSA", {1: code, 2: inbound.control_id(), 3: text})
        return Message.from_segments([Segment.from_parts(["MSH"] + fields[2:]), msa])

    @staticmethod
    def error(inbound: Message, reason: str) -> Message:
        return Ack.build(inbound, ERROR, reason[:200])

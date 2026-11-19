"""The profiles that cover most hospital traffic: transfer and results."""

from __future__ import annotations

from .profile import Profile


def adt_a01() -> Profile:
    return Profile(
        name="ADT_A01",
        message_type="ADT",
        trigger="A01",
        required_segments=["MSH", "EVN", "PID", "PV1"],
        required_fields={
            "MSH.10": "Message control ID",
            "PID.3": "Patient identifier",
            "PID.5.1": "Patient family name",
            "PV1.2": "Patient class (I/O/E)",
        },
        allowed_values={
            "PID.8.1": ["F", "M", "O", "U", "A", "N"],
            "PV1.2": ["I", "O", "E", "P", "R", "B", "C", "N"],
        },
    )


def adt_a08() -> Profile:
    """A08 is "update patient information"; PV1 is often absent, so it is not required."""
    return Profile(
        name="ADT_A08",
        message_type="ADT",
        trigger="A08",
        required_segments=["MSH", "EVN", "PID"],
        required_fields={
            "MSH.10": "Message control ID",
            "PID.3": "Patient identifier",
            "PID.5.1": "Patient family name",
        },
        allowed_values={"PID.8.1": ["F", "M", "O", "U", "A", "N"]},
    )


def oru_r01() -> Profile:
    return Profile(
        name="ORU_R01",
        message_type="ORU",
        trigger="R01",
        required_segments=["MSH", "PID", "OBR", "OBX"],
        required_fields={
            "MSH.10": "Message control ID",
            "PID.3": "Patient identifier",
            "OBR.4.1": "Universal service identifier",
            "OBX.5": "Observation value",
        },
        allowed_values={"OBX.11": ["F", "P", "C", "X"]},
    )


PROFILES = {"adtA01": adt_a01, "adtA08": adt_a08, "oruR01": oru_r01}

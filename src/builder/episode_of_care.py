"""EpisodeOfCare resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderEpisodeOfCare.php. Versi sebelumnya berbeda pada empat hal:

- `type` menulis satu elemen daftar (menimpa), padahal kanon menumpuk (0..*);
- `diagnosis` tidak menerima `role`, padahal R4 mewajibkan diagnosis.role 1..1 dan
  kanon menulisnya;
- `status` dan `status_history` tidak divalidasi terhadap tujuh nilai yang sah;
- `status_history` menerima objek Period, bukan (start, end) seperti kanon.

Ditambah: setId, addTeam, addAccount.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _rujukan(nilai: Any) -> Dict[str, Any]:
    return nilai if isinstance(nilai, dict) else {"reference": nilai}


class EpisodeOfCareBuilder(BaseBuilder):
    """Builder for EpisodeOfCare resource."""

    VALID_STATUSES = ["planned", "waitlist", "active", "onhold", "finished", "cancelled", "entered-in-error"]

    def __init__(self) -> None:
        super().__init__("EpisodeOfCare")

    def _cek_status(self, status: str) -> None:
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status: {status}")

    def set_id(self, id: str) -> "EpisodeOfCareBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "EpisodeOfCareBuilder":
        if isinstance(identifier, dict):
            return self._push("identifier", identifier)
        return self._push("identifier", {"system": identifier, "value": value})

    def set_status(self, status: str) -> "EpisodeOfCareBuilder":
        self._cek_status(status)
        self.data["status"] = status
        return self

    def add_status_history(self, status: str, start: str, end: Optional[str] = None) -> "EpisodeOfCareBuilder":
        self._cek_status(status)
        period: Dict[str, Any] = {"start": start}
        if end is not None:
            period["end"] = end
        return self._push("statusHistory", {"status": status, "period": period})

    def set_patient(self, patient: Any) -> "EpisodeOfCareBuilder":
        self.data["patient"] = _rujukan(patient)
        return self

    def set_managing_organization(self, organization: Any) -> "EpisodeOfCareBuilder":
        self.data["managingOrganization"] = _rujukan(organization)
        return self

    def add_type(self, konsep: Dict[str, Any]) -> "EpisodeOfCareBuilder":
        return self._push("type", konsep)

    def set_period(self, period: Any, end: Optional[str] = None) -> "EpisodeOfCareBuilder":
        if isinstance(period, dict):
            self.data["period"] = period
            return self
        hasil: Dict[str, Any] = {"start": period}
        if end:
            hasil["end"] = end
        self.data["period"] = hasil
        return self

    def add_diagnosis(self, condition: Any, role: Dict[str, Any], rank: Optional[int] = None) -> "EpisodeOfCareBuilder":
        diagnosis: Dict[str, Any] = {"condition": _rujukan(condition), "role": role}
        if rank is not None:
            diagnosis["rank"] = rank
        return self._push("diagnosis", diagnosis)

    def add_referral_request(self, referral_request: Any) -> "EpisodeOfCareBuilder":
        return self._push("referralRequest", _rujukan(referral_request))

    def set_care_manager(self, care_manager: Any) -> "EpisodeOfCareBuilder":
        self.data["careManager"] = _rujukan(care_manager)
        return self

    def add_team(self, team: Any) -> "EpisodeOfCareBuilder":
        return self._push("team", _rujukan(team))

    def add_account(self, account: Any) -> "EpisodeOfCareBuilder":
        return self._push("account", _rujukan(account))

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "EpisodeOfCareBuilder":
        return self.set_status(value)

    def status_history(self, status: str, period: Dict[str, Any]) -> "EpisodeOfCareBuilder":
        """Alias lama: menerima objek Period; kini meneruskan start/end seperti kanon."""
        return self.add_status_history(status, period.get("start", ""), period.get("end"))

    def type(self, konsep: Dict[str, Any]) -> "EpisodeOfCareBuilder":
        """Alias lama: dulu menimpa; kini menumpuk seperti kanon."""
        return self.add_type(konsep)

    def diagnosis(
        self,
        condition_reference: Optional[str] = None,
        condition_codeable_concept: Optional[Dict[str, Any]] = None,
        rank: Optional[int] = None,
        role: Optional[Dict[str, Any]] = None,
    ) -> "EpisodeOfCareBuilder":
        """Alias lama: tanpa `role` kanon tidak bisa dipanggil; default peran 'principal'. """
        kondisi = condition_codeable_concept or (
            {"reference": condition_reference} if condition_reference else {}
        )
        peran = role or {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/diagnosis-role", "code": "AD", "display": "Admission diagnosis"}]}
        return self.add_diagnosis(kondisi, peran, rank)

    def patient(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        self.set_patient(reference)
        if display:
            self.data["patient"]["display"] = display
        return self

    def managing_organization(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        self.set_managing_organization(reference)
        if display:
            self.data["managingOrganization"]["display"] = display
        return self

    def period(self, start: Optional[str] = None, end: Optional[str] = None) -> "EpisodeOfCareBuilder":
        p: Dict[str, Any] = {}
        if start:
            p["start"] = start
        if end:
            p["end"] = end
        return self._set("period", p) if p else self

    def referral_request(self, reference: str) -> "EpisodeOfCareBuilder":
        return self.add_referral_request(reference)

    def care_manager(self, reference: str, display: Optional[str] = None) -> "EpisodeOfCareBuilder":
        self.set_care_manager(reference)
        if display:
            self.data["careManager"]["display"] = display
        return self

    def identifier(self, system: str, value: str) -> "EpisodeOfCareBuilder":
        return self.add_identifier(system, value)

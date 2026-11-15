from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


class FamilyMemberHistoryBuilder(BaseBuilder):
    """Setara PayloadBuilderFamilyMemberHistory.php.

    Versi sebelumnya hanya punya enam method tanpa awalan `set_`; 16 setter PHP
    belum ada. Nama lama dipertahankan sebagai alias.

    Quirk PHP ditiru dan ditandai: `setAgeAge` menulis `ageAge` sebagai angka plus
    `ageUnit` terpisah, padahal R4 menuntut Age (value + unit) di dalam satu objek.
    """

    def __init__(self) -> None:
        super().__init__("FamilyMemberHistory")

    def set_id(self, id: str) -> "FamilyMemberHistoryBuilder":
        return self._set("id", id)

    def add_identifier(self, system: Any, value: str = "") -> "FamilyMemberHistoryBuilder":
        """PHP menerima objek Identifier; di sini bentuk (system, value) juga diterima."""
        if isinstance(system, dict):
            return self._push("identifier", system)
        return self._push("identifier", {"system": system, "value": value})

    def set_instantiates_canonical(self, canonical: str) -> "FamilyMemberHistoryBuilder":
        return self._set("instantiatesCanonical", canonical)

    def set_status(self, status: str) -> "FamilyMemberHistoryBuilder":
        sah = ["partial", "completed", "entered-in-error", "health-unknown"]
        if status not in sah:
            raise ValueError(f"Invalid status: {status}")
        return self._set("status", status)

    def set_data_absent_reason(self, alasan: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("dataAbsentReason", alasan)

    def set_patient(self, reference: Any, display: Optional[str] = None) -> "FamilyMemberHistoryBuilder":
        if isinstance(reference, dict):
            return self._set("patient", reference)
        patient: Dict[str, Any] = {"reference": reference}
        if display:
            patient["display"] = display
        return self._set("patient", patient)

    def set_date(self, date: str) -> "FamilyMemberHistoryBuilder":
        return self._set("date", date)

    def set_name(self, name: Optional[str]) -> "FamilyMemberHistoryBuilder":
        if name is not None:
            self._set("name", name)
        return self

    def set_relationship(self, hubungan: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("relationship", hubungan)

    def set_sex(self, sex: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("sex", sex)

    def set_born_period(self, period: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("bornPeriod", period)

    def set_born_date(self, tanggal: str) -> "FamilyMemberHistoryBuilder":
        return self._set("bornDate", tanggal)

    def set_born_string(self, teks: str) -> "FamilyMemberHistoryBuilder":
        return self._set("bornString", teks)

    def set_age_age(self, value: int, unit: str) -> "FamilyMemberHistoryBuilder":
        """Quirk PHP: angka dan satuan ditulis di dua elemen terpisah, bukan satu Age."""
        self._set("ageAge", value)
        self._set("ageUnit", unit)
        return self

    def set_age_range(self, value: int, low: str, high: str) -> "FamilyMemberHistoryBuilder":
        return self._set("ageRange", {"value": value, "low": {"value": low}, "high": {"value": high}})

    def set_age_string(self, teks: str) -> "FamilyMemberHistoryBuilder":
        return self._set("ageString", teks)

    def set_deceased_boolean(self, meninggal: bool) -> "FamilyMemberHistoryBuilder":
        return self._set("deceasedBoolean", meninggal)

    def set_deceased_age(self, value: int, unit: str) -> "FamilyMemberHistoryBuilder":
        """Quirk PHP: sama seperti ageAge — angka dan satuan terpisah."""
        self._set("deceasedAge", value)
        self._set("deceasedAgeUnit", unit)
        return self

    def set_deceased_range(self, value: int, low: str, high: str) -> "FamilyMemberHistoryBuilder":
        return self._set("deceasedRange", {"value": value, "low": {"value": low}, "high": {"value": high}})

    def set_deceased_date(self, tanggal: str) -> "FamilyMemberHistoryBuilder":
        return self._set("deceasedDate", tanggal)

    def set_deceased_string(self, teks: str) -> "FamilyMemberHistoryBuilder":
        return self._set("deceasedString", teks)

    def set_deceased_codeable_concept(self, konsep: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("deceasedCodeableConcept", konsep)

    def set_reason_code(self, konsep: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("reasonCode", konsep)

    def add_reason_code(self, konsep: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._push("reasonCode", konsep)

    def add_reason_reference(self, reference: Any) -> "FamilyMemberHistoryBuilder":
        ref = reference if isinstance(reference, dict) else {"reference": reference}
        return self._push("reasonReference", ref)

    def set_note(self, teks: str) -> "FamilyMemberHistoryBuilder":
        """Quirk PHP: dinamai set, tetapi MENUMPUK ke daftar note."""
        return self._push("note", {"text": teks})

    def add_condition(
        self,
        code: Dict[str, Any],
        onset_string: Optional[str] = None,
        outcome: Optional[Dict[str, Any]] = None,
        contributed_to_death: Optional[bool] = None,
    ) -> "FamilyMemberHistoryBuilder":
        kondisi: Dict[str, Any] = {"code": code}
        if onset_string is not None:
            kondisi["onsetString"] = onset_string
        if outcome is not None:
            kondisi["outcome"] = outcome
        if contributed_to_death is not None:
            kondisi["contributedToDeath"] = contributed_to_death
        return self._push("condition", kondisi)

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "FamilyMemberHistoryBuilder":
        return self.set_status(value)

    def patient(self, reference: str) -> "FamilyMemberHistoryBuilder":
        return self.set_patient(reference)

    def relationship(self, konsep: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self.set_relationship(konsep)

    def code(self, konsep: Dict[str, Any]) -> "FamilyMemberHistoryBuilder":
        return self._set("code", konsep)

    def date(self, value: str) -> "FamilyMemberHistoryBuilder":
        return self.set_date(value)

    def note(self, text: str) -> "FamilyMemberHistoryBuilder":
        return self.set_note(text)

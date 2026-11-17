"""ImagingStudy resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderImagingStudy.php. Versi sebelumnya berbeda pada dua tanda tangan
yang membuat payload tidak bisa dibandingkan:

- add_series(uid, modality_code, modality_system, …) — kanon (uid, system, code,
  display, status, description, number);
- add_series_instance(idx, uid, sop_class, sop_system) — kanon (idx, uid,
  dicomClassSystem, dicomClassCode, dicomClassDisplay).

Ditambah yang belum ada: identifier, ended, location, partOf, referrer (menimpa),
series/<i>/started, series/<i>/bodySite, series/<i>/instance/<j>/number.

Tiga quirk kanon ditiru dan ditandai:
- add_referrer dinamai "add" tetapi MENIMPA `referrer` (R4 0..1, jadi namanya salah);
- series.modality ditulis sebagai Coding rata, sementara series.bodySite dibungkus
  CodeableConcept di resource yang sama;
- add_series menulis `status` di dalam series, padahal R4 tidak punya elemen itu.
"""
from typing import Any, Dict, Optional

from satusehat_integration.builder.base_builder import BaseBuilder


class ImagingStudyBuilder(BaseBuilder):
    """Builder for ImagingStudy resource."""

    def __init__(self):
        super().__init__("ImagingStudy")

    # --- jalur bersarang ------------------------------------------------------

    @staticmethod
    def _is_index(seg: str) -> bool:
        return seg.isdigit()

    def _titik(self, path: str):
        segs = path.split("/")
        cur: Any = self.data
        for i, seg in enumerate(segs[:-1]):
            kunci: Any = int(seg) if self._is_index(seg) else seg
            if isinstance(cur, list):
                while len(cur) <= kunci:
                    cur.append({})
                cur = cur[kunci]
                continue
            if kunci not in cur or cur[kunci] is None:
                cur[kunci] = [] if self._is_index(segs[i + 1]) else {}
            cur = cur[kunci]
        terakhir = segs[-1]
        return cur, int(terakhir) if self._is_index(terakhir) else terakhir

    def _set_path(self, path: str, value: Any) -> "ImagingStudyBuilder":
        induk, kunci = self._titik(path)
        induk[kunci] = value
        return self

    def _push_path(self, path: str, value: Any) -> "ImagingStudyBuilder":
        induk, kunci = self._titik(path)
        if not isinstance(induk.get(kunci), list):
            induk[kunci] = []
        induk[kunci].append(value)
        return self

    def _push(self, key: str, value: Any) -> "ImagingStudyBuilder":  # type: ignore[override]
        self.data.setdefault(key, []).append(value)
        return self

    # --- setter ---------------------------------------------------------------

    def set_id(self, id: str) -> "ImagingStudyBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, system: str, value: str) -> "ImagingStudyBuilder":
        return self._push("identifier", {"system": system, "value": value})

    def set_status(self, status: str) -> "ImagingStudyBuilder":
        self.data["status"] = status
        return self

    def add_modality(self, system: str, code: str, display: str = "") -> "ImagingStudyBuilder":
        return self._push("modality", {"system": system, "code": code, "display": display})

    def set_subject(self, reference: str) -> "ImagingStudyBuilder":
        self.data["subject"] = {"reference": reference}
        return self

    def set_encounter(self, reference: str) -> "ImagingStudyBuilder":
        self.data["encounter"] = {"reference": reference}
        return self

    def set_started(self, date_time: str) -> "ImagingStudyBuilder":
        self.data["started"] = date_time
        return self

    def set_ended(self, date_time: str) -> "ImagingStudyBuilder":
        self.data["ended"] = date_time
        return self

    def set_location(self, reference: str) -> "ImagingStudyBuilder":
        self.data["location"] = {"reference": reference}
        return self

    def add_referrer(self, reference: str) -> "ImagingStudyBuilder":
        """Quirk kanon: dinamai "add" tetapi MENIMPA; R4 0..1 sehingga namanya keliru."""
        self.data["referrer"] = {"reference": reference}
        return self

    def add_part_of(self, reference: str) -> "ImagingStudyBuilder":
        return self._push("partOf", {"reference": reference})

    def add_series(
        self,
        uid: str,
        system: str,
        code: str,
        display: str,
        status: Optional[str] = None,
        description: Optional[str] = None,
        number: Optional[int] = None,
    ) -> "ImagingStudyBuilder":
        series: Dict[str, Any] = {"uid": uid, "modality": {"system": system, "code": code, "display": display}}
        if status is not None:
            series["status"] = status
        if description is not None:
            series["description"] = description
        if number is not None:
            series["number"] = number
        return self._push("series", series)

    def set_series_started(self, series_idx: int, date_time: str) -> "ImagingStudyBuilder":
        return self._set_path(f"series/{series_idx}/started", date_time)

    def set_series_body_site(self, series_idx: int, system: str, code: str, display: str = "") -> "ImagingStudyBuilder":
        """series.bodySite bertipe CodeableConcept: kode dibungkus di dalam `coding`."""
        coding: Dict[str, Any] = {"system": system, "code": code}
        if display:
            coding["display"] = display
        return self._set_path(f"series/{series_idx}/bodySite", {"coding": [coding]})

    def add_series_instance(
        self,
        series_idx: int,
        uid: str,
        dicom_class_system: str,
        dicom_class_code: str,
        dicom_class_display: str,
    ) -> "ImagingStudyBuilder":
        return self._push_path(
            f"series/{series_idx}/instance",
            {
                "uid": uid,
                "sopClass": {"system": dicom_class_system, "code": dicom_class_code, "display": dicom_class_display},
            },
        )

    def add_series_instance_number(self, series_idx: int, instance_idx: int, number: int) -> "ImagingStudyBuilder":
        return self._set_path(f"series/{series_idx}/instance/{instance_idx}/number", number)

    # --- tambahan yang sah R4, tidak ada di kanon -----------------------------

    def set_description(self, description: str) -> "ImagingStudyBuilder":
        self.data["description"] = description
        return self

    def add_endpoint(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        endpoint: Dict[str, Any] = {"reference": reference}
        if display:
            endpoint["display"] = display
        return self._push("endpoint", endpoint)

    def add_procedure_reference(self, reference: str) -> "ImagingStudyBuilder":
        return self._push("procedureReference", {"reference": reference})

    # --- alias nama lama ------------------------------------------------------

    def set_modality(self, system: str, code: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        return self.add_modality(system, code, display or "")

    def add_referencer(self, reference: str, display: Optional[str] = None) -> "ImagingStudyBuilder":
        """Alias lama: dulu hanya menulis bila belum ada — kini menimpa seperti kanon."""
        self.add_referrer(reference)
        if display:
            self.data["referrer"]["display"] = display
        return self

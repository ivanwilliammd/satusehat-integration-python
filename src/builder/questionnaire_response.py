"""QuestionnaireResponse resource builder for SATUSEHAT FHIR R4.

Setara PayloadBuilderQuestionnaireResponse.php. Versi sebelumnya enam method tanpa
awalan `set_`, dengan dua cacat:

- `questionnaire` ditulis sebagai Reference ({'reference': …}), padahal R4 dan kanon
  memakai canonical (string URL);
- `status` tidak divalidasi dan tidak memakai default `completed` seperti kanon
  (PHP juga menurunkan huruf jadi kecil sebelum memeriksa).

Ditambah: setId, source, addItem (linkId + teks opsional + satu jawaban).
Catatan quirk: `addItem` membungkus satu jawaban di dalam daftar `answer`, sehingga
satu item tidak bisa memuat lebih dari satu jawaban — R4 mengizinkan 0..*.
"""
from typing import Any, Dict, Optional

from src.builder.base_builder import BaseBuilder


def _konsep(nilai: Any, code: Optional[str] = None, display: Optional[str] = None) -> Dict[str, Any]:
    if isinstance(nilai, dict):
        return nilai
    coding: Dict[str, Any] = {"system": nilai, "code": code or ""}
    if display:
        coding["display"] = display
    return {"coding": [coding]}


def _rujukan(nilai: Any) -> Dict[str, Any]:
    return nilai if isinstance(nilai, dict) else {"reference": nilai}


class QuestionnaireResponseBuilder(BaseBuilder):
    """Builder for QuestionnaireResponse resource."""

    VALID_STATUSES = ["in-progress", "completed", "amended", "entered-in-error", "stopped"]

    def __init__(self) -> None:
        super().__init__("QuestionnaireResponse")

    def set_id(self, id: str) -> "QuestionnaireResponseBuilder":
        self.data["id"] = id
        return self

    def set_status(self, status: str = "completed") -> "QuestionnaireResponseBuilder":
        nilai = status.lower()
        if nilai not in self.VALID_STATUSES:
            raise ValueError("Invalid status: must be one of " + ", ".join(self.VALID_STATUSES))
        self.data["status"] = nilai
        return self

    def set_questionnaire(self, questionnaire: str) -> "QuestionnaireResponseBuilder":
        """R4: questionnaire bertipe canonical (string), bukan Reference."""
        self.data["questionnaire"] = questionnaire
        return self

    def set_subject(self, subject: Any) -> "QuestionnaireResponseBuilder":
        self.data["subject"] = _rujukan(subject)
        return self

    def set_encounter(self, encounter: Any) -> "QuestionnaireResponseBuilder":
        self.data["encounter"] = _rujukan(encounter)
        return self

    def set_authored(self, authored: str) -> "QuestionnaireResponseBuilder":
        self.data["authored"] = authored
        return self

    def set_author(self, author: Any) -> "QuestionnaireResponseBuilder":
        self.data["author"] = _rujukan(author)
        return self

    def set_source(self, source: Any) -> "QuestionnaireResponseBuilder":
        self.data["source"] = _rujukan(source)
        return self

    def add_item(self, link_id: str, text: Optional[str], answer: Any) -> "QuestionnaireResponseBuilder":
        item: Dict[str, Any] = {"linkId": link_id}
        if text is not None:
            item["text"] = text
        item["answer"] = [_konsep(answer)]
        return self._push("item", item)

    def build(self) -> Dict[str, Any]:
        """Kanon mengisi status default `completed` saat build."""
        if "status" not in self.data:
            self.data["status"] = "completed"
        return super().build()

    # --- alias nama lama ------------------------------------------------------

    def status(self, value: str) -> "QuestionnaireResponseBuilder":
        return self.set_status(value)

    def questionnaire(self, reference: str) -> "QuestionnaireResponseBuilder":
        """Alias lama: dulu menulis Reference; kini menulis canonical seperti kanon."""
        return self.set_questionnaire(reference)

    def subject(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self.set_subject(reference)

    def encounter(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self.set_encounter(reference)

    def authored(self, value: str) -> "QuestionnaireResponseBuilder":
        return self.set_authored(value)

    def author(self, reference: str) -> "QuestionnaireResponseBuilder":
        return self.set_author(reference)

"""SubstanceReferenceInformationParser — pembaca elemen tingkat atas resource FHIR R4 SubstanceReferenceInformation.

Dihasilkan dari SubstanceReferenceInformationBuilder oleh scripts/generate_parsers.py — jangan disunting tangan.
Setiap getter mengembalikan None bila elemen tidak ada, sehingga pemanggil tidak terhenti oleh
akses yang meleset.
"""
from __future__ import annotations

from typing import Any, Optional


class SubstanceReferenceInformationParser:
    def __init__(self, data: Optional[dict[str, Any]] = None) -> None:
        self._data: dict[str, Any] = data if isinstance(data, dict) else {}

    def get_raw(self) -> dict[str, Any]:
        return self._data

    getRaw = get_raw

    def get_id(self) -> Any:
        return self._data.get("id")

    getId = get_id

    def get_status(self) -> Any:
        return self._data.get("status")

    getStatus = get_status

    def get_comment(self) -> Any:
        return self._data.get("comment")

    getComment = get_comment

    def get_gene(self) -> Any:
        return self._data.get("gene")

    getGene = get_gene

    def get_gene_element(self) -> Any:
        return self._data.get("geneElement")

    getGeneElement = get_gene_element

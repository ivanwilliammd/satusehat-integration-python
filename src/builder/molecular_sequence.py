"""MolecularSequence resource builder for SATUSEHAT FHIR R4."""
from typing import List, Optional
from src.builder.base_builder import BaseBuilder


class MolecularSequenceBuilder(BaseBuilder):
    """Builder for MolecularSequence resource."""

    def __init__(self):
        super().__init__("MolecularSequenceBuilder")
        self.data = {"resourceType": "MolecularSequence"}

    def set_id(self, id: str) -> "MolecularSequenceBuilder":
        self.data["id"] = id
        return self

    def set_type(self, type: str) -> "MolecularSequenceBuilder":
        self.data["type"] = type
        return self

    def set_coordinate_system(self, coordinate_system: int) -> "MolecularSequenceBuilder":
        self.data["coordinateSystem"] = coordinate_system
        return self

    def set_patient(self, reference: str, display: Optional[str] = None) -> "MolecularSequenceBuilder":
        self.data["patient"] = {"reference": reference}
        if display:
            self.data["patient"]["display"] = display
        return self

    def set_specimen(self, reference: str) -> "MolecularSequenceBuilder":
        self.data["specimen"] = {"reference": reference}
        return self

    def set_device(self, reference: str) -> "MolecularSequenceBuilder":
        self.data["device"] = {"reference": reference}
        return self

    def set_observation(self, reference: str) -> "MolecularSequenceBuilder":
        self.data["observation"] = [{"reference": reference}]
        return self

    def set_reference_seq(
        self,
        chromosome: Optional[str] = None,
        genome_build: Optional[str] = None,
        reference_seq: Optional[str] = None
    ) -> "MolecularSequenceBuilder":
        ref: dict = {}
        if chromosome:
            ref["chromosome"] = {"coding": [{"code": chromosome}]}
        if genome_build:
            ref["genomeBuild"] = genome_build
        if reference_seq:
            ref["referenceSeqString"] = reference_seq
        self.data["referenceSeq"] = ref
        return self

    def add_variant(
        self,
        start: int,
        end: int,
        observed_allele: Optional[str] = None,
        reference_allele: Optional[str] = None
    ) -> "MolecularSequenceBuilder":
        self.data.setdefault("variant", [])
        variant: dict = {"start": start, "end": end}
        if observed_allele:
            variant["observedAllele"] = observed_allele
        if reference_allele:
            variant["referenceAllele"] = reference_allele
        self.data["variant"].append(variant)
        return self

    def add_quality(
        self,
        quality_type: str,
        start: Optional[int] = None,
        end: Optional[int] = None,
        score: Optional[float] = None,
        method_code: Optional[str] = None,
        method_system: Optional[str] = None
    ) -> "MolecularSequenceBuilder":
        self.data.setdefault("quality", [])
        qual: dict = {"type": quality_type}
        if start is not None:
            qual["start"] = start
        if end is not None:
            qual["end"] = end
        if score is not None:
            qual["score"] = {"value": score}
        if method_code:
            qual["method"] = {"coding": [{"code": method_code}]}
            if method_system:
                qual["method"]["coding"][0]["system"] = method_system
        self.data["quality"].append(qual)
        return self

    def set_pointer(self, reference: str) -> "MolecularSequenceBuilder":
        self.data["pointer"] = [{"reference": reference}]
        return self

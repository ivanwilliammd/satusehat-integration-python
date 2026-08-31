from src.builder.base_builder import BaseBuilder


class SubstanceReferenceInformationBuilder(BaseBuilder):
    def __init__(self) -> None:
        super().__init__("SubstanceReferenceInformation")

    def set_id(self, val: str) -> "SubstanceReferenceInformationBuilder":
        return self._set("id", val)

    def add_identifier(self, system: str, value: str, use: str = None, type_code: str = None, type_display: str = None) -> "SubstanceReferenceInformationBuilder":
        ident = {"system": system, "value": value}
        if use:
            ident["use"] = use
        if type_code:
            ident["type"] = {
                "coding": [{
                    "system": "http://terminology.hl7.org/CodeSystem/v2-0203",
                    "code": type_code,
                    "display": type_display if type_display else type_code,
                }]
            }
        return self._push("identifier", ident)

    def set_status(self, val: str) -> "SubstanceReferenceInformationBuilder":
        return self._set("status", val)

    def set_comment(self, val: str) -> "SubstanceReferenceInformationBuilder":
        return self._set("comment", val)

    def set_gene(self, system: str, code: str, display: str = "") -> "SubstanceReferenceInformationBuilder":
        return self._set("gene", {"coding": [{"system": system, "code": code, "display": display}]})

    def set_gene_element(self, system: str, code: str, display: str = "") -> "SubstanceReferenceInformationBuilder":
        return self._set("geneElement", {"coding": [{"system": system, "code": code, "display": display}]})

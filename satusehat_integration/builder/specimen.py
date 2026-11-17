from typing import Any, List, Optional
from satusehat_integration.builder.base_builder import BaseBuilder


class SpecimenBuilder(BaseBuilder):
    _resourceType = "Specimen"

    def __init__(self) -> None:
        super().__init__("Specimen")

    def identifier(self, system: str, value: str) -> "SpecimenBuilder":
        return self._append("identifier", {"system": system, "value": value})

    def accession_identifier(self, system: str, value: str) -> "SpecimenBuilder":
        return self._set("accessionIdentifier", {"system": system, "value": value})

    def status(self, value: str) -> "SpecimenBuilder":
        return self._set("status", value)

    def type(self, codeable_concept: dict) -> "SpecimenBuilder":
        return self._set("type", codeable_concept)

    def subject(self, reference: str, display: Optional[str] = None) -> "SpecimenBuilder":
        sub: dict = {"reference": reference}
        if display:
            sub["display"] = display
        return self._set("subject", sub)

    def received_time(self, value: str) -> "SpecimenBuilder":
        return self._set("receivedTime", value)

    def parent(self, reference: str) -> "SpecimenBuilder":
        return self._append("parent", {"reference": reference})

    def request(self, reference: str) -> "SpecimenBuilder":
        return self._append("request", {"reference": reference})

    def collection(self, collected_date_time: Optional[str] = None, collected_period: Optional[dict] = None, quantity: Optional[dict] = None, body_site: Optional[dict] = None, fasting_status: Optional[dict] = None) -> "SpecimenBuilder":
        col: dict = {}
        if collected_date_time:
            col["collectedDateTime"] = collected_date_time
        if collected_period:
            col["collectedPeriod"] = collected_period
        if quantity:
            col["quantity"] = quantity
        if body_site:
            col["bodySite"] = body_site
        if fasting_status:
            col["fastingStatus"] = fasting_status
        return self._set("collection", col) if col else self

    def processing(self, description: Optional[str] = None, procedure_codeable_concept: Optional[dict] = None, time_date_time: Optional[str] = None, time_period: Optional[dict] = None) -> "SpecimenBuilder":
        proc: dict = {}
        if description:
            proc["description"] = description
        if procedure_codeable_concept:
            proc["procedure"] = procedure_codeable_concept
        if time_date_time:
            proc["timeDateTime"] = time_date_time
        if time_period:
            proc["timePeriod"] = time_period
        return self._append("processing", proc) if proc else self

    def container(self, type_codeable_concept: Optional[dict] = None, identifier: Optional[dict] = None, specimen_quantity: Optional[dict] = None) -> "SpecimenBuilder":
        cnt: dict = {}
        if type_codeable_concept:
            cnt["type"] = type_codeable_concept
        if identifier:
            cnt["identifier"] = identifier
        if specimen_quantity:
            cnt["specimenQuantity"] = specimen_quantity
        return self._append("container", cnt) if cnt else self

    def note(self, text: str) -> "SpecimenBuilder":
        return self._append("note", {"text": text})

    # --- Nama kanon (cermin PayloadBuilderSpecimen) ---

    def _arr(self, value: Any) -> Any:
        return value.to_array() if hasattr(value, "to_array") else value

    def _path(self, path: str, value: Any) -> "SpecimenBuilder":
        """Menyetel elemen bersarang lewat path bertitik, seperti set('collection/quantity') di PHP."""
        node = self.data
        bagian = path.split("/")
        for kunci in bagian[:-1]:
            node = node.setdefault(kunci, {})
        node[bagian[-1]] = value
        return self

    def set_id(self, id: str) -> "SpecimenBuilder":
        self.data["id"] = id
        return self

    def add_identifier(self, identifier: Any, value: Optional[str] = None) -> "SpecimenBuilder":
        entry = {"system": identifier, "value": value} if value is not None else self._arr(identifier)
        self.data.setdefault("identifier", []).append(entry)
        return self

    def set_status(self, status: str) -> "SpecimenBuilder":
        self.data["status"] = status
        return self

    def set_type(self, specimen_type: Any) -> "SpecimenBuilder":
        self.data["type"] = self._arr(specimen_type)
        return self

    def set_subject(self, subject: Any) -> "SpecimenBuilder":
        if isinstance(subject, str):
            self.data["subject"] = {"reference": subject}
        else:
            self.data["subject"] = self._arr(subject)
        return self

    def set_received_time(self, date_time: str) -> "SpecimenBuilder":
        self.data["receivedTime"] = date_time
        return self

    def set_collected_date_time(self, date_time: str) -> "SpecimenBuilder":
        return self._path("collection/collectedDateTime", date_time)

    def set_collector(self, collector: Any) -> "SpecimenBuilder":
        return self._path("collection/collector", self._arr(collector))

    def set_fasting_status_codeable_concept(self, status: Any) -> "SpecimenBuilder":
        return self._path("collection/fastingStatusCodeableConcept", self._arr(status))

    def set_method(self, method: Any) -> "SpecimenBuilder":
        return self._path("collection/method", self._arr(method))

    def set_quantity(self, quantity: Any) -> "SpecimenBuilder":
        return self._path("collection/quantity", self._arr(quantity))

    def set_body_site(self, body_site: Any) -> "SpecimenBuilder":
        return self._path("collection/bodySite", self._arr(body_site))

    def add_request(self, request: Any) -> "SpecimenBuilder":
        entry = {"reference": request} if isinstance(request, str) else self._arr(request)
        self.data.setdefault("request", []).append(entry)
        return self

    def add_condition(self, text: str) -> "SpecimenBuilder":
        self.data.setdefault("condition", []).append({"text": text})
        return self

    def add_processing(self, time_date_time: str) -> "SpecimenBuilder":
        self.data.setdefault("processing", []).append({"timeDateTime": time_date_time})
        return self

    def add_extension(self, url: str, value: str) -> "SpecimenBuilder":
        self.data.setdefault("extension", []).append({"url": url, "valueString": value})
        return self

    def add_transported_time(self, date_time: str) -> "SpecimenBuilder":
        self.data.setdefault("extension", []).append({
            "url": "https://fhir.kemkes.go.id/r4/StructureDefinition/TransportedTime",
            "valueDateTime": date_time,
        })
        return self

    def add_transported_person(self, name: str, telecom: Optional[list] = None) -> "SpecimenBuilder":
        self.data.setdefault("extension", []).append({
            "url": "https://fhir.kemkes.go.id/r4/StructureDefinition/TransportedPerson",
            "valueContactDetail": {"name": name, "telecom": telecom or []},
        })
        return self

    def add_received_person(self, person: Any) -> "SpecimenBuilder":
        entry = {"reference": person} if isinstance(person, str) else self._arr(person)
        self.data.setdefault("extension", []).append({
            "url": "https://fhir.kemkes.go.id/r4/StructureDefinition/ReceivedPerson",
            "valueReference": entry,
        })
        return self

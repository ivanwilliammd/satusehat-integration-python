class BaseBuilder:
    def __init__(self, resource_type: str):
        self.data = {"resourceType": resource_type}

    def to_dict(self):
        return self.data

class PatientBuilder(BaseBuilder):
    def __init__(self): super().__init__("Patient")
    def set_nik(self, nik: str):
        self.data["identifier"] = [{"system": "https://fhir.kemkes.go.id/id/nik", "value": nik}]
        return self
    def set_name(self, name: str):
        self.data["name"] = [{"use": "official", "text": name}]
        return self
    def set_gender(self, gender: str):
        self.data["gender"] = gender
        return self
    def set_birth_date(self, birth_date: str):
        self.data["birthDate"] = birth_date
        return self

class PractitionerBuilder(BaseBuilder):
    def __init__(self): super().__init__("Practitioner")
    def set_nik(self, nik: str):
        self.data["identifier"] = [{"system": "https://fhir.kemkes.go.id/id/nik", "value": nik}]
        return self
    def set_name(self, name: str):
        self.data["name"] = [{"use": "official", "text": name}]
        return self

class OrganizationBuilder(BaseBuilder):
    def __init__(self): super().__init__("Organization")
    def set_id(self, org_id: str):
        self.data["id"] = org_id
        return self
    def set_name(self, name: str):
        self.data["name"] = name
        return self

class LocationBuilder(BaseBuilder):
    def __init__(self): super().__init__("Location")
    def set_name(self, name: str):
        self.data["name"] = name
        return self
    def set_managing_organization(self, org_ref: str):
        self.data["managingOrganization"] = {"reference": org_ref}
        return self

class EncounterBuilder(BaseBuilder):
    def __init__(self): super().__init__("Encounter")
    def set_status(self, status: str):
        self.data["status"] = status
        return self
    def set_subject(self, ref: str, display: str):
        self.data["subject"] = {"reference": ref, "display": display}
        return self

class ConditionBuilder(BaseBuilder):
    def __init__(self): super().__init__("Condition")
    def set_clinical_status(self, code: str):
        self.data["clinicalStatus"] = {
            "coding": [{"system": "http://terminology.hl7.org/CodeSystem/condition-clinical", "code": code}]
        }
        return self
    def set_subject(self, ref: str, display: str):
        self.data["subject"] = {"reference": ref, "display": display}
        return self

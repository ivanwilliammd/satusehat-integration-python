class BaseBuilder:
    def __init__(self, resource_type: str):
        self.data = {"resourceType": resource_type}

    def to_dict(self):
        return self.data

class PatientBuilder(BaseBuilder):
    def __init__(self): super().__init__("Patient")
    def set_name(self, name: str):
        self.data["name"] = [{"use": "official", "text": name}]
        return self

class PractitionerBuilder(BaseBuilder):
    def __init__(self): super().__init__("Practitioner")
    def set_name(self, name: str):
        self.data["name"] = [{"use": "official", "text": name}]
        return self

class OrganizationBuilder(BaseBuilder):
    def __init__(self): super().__init__("Organization")

class LocationBuilder(BaseBuilder):
    def __init__(self): super().__init__("Location")

class EncounterBuilder(BaseBuilder):
    def __init__(self): super().__init__("Encounter")

class ConditionBuilder(BaseBuilder):
    def __init__(self): super().__init__("Condition")

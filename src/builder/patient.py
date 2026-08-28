class PatientBuilder:
    def __init__(self):
        self.data = {"resourceType": "Patient"}

    def set_name(self, name: str):
        self.data["name"] = [{"use": "official", "text": name}]
        return self

    def to_dict(self):
        return self.data

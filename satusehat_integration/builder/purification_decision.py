class PurificationDecisionBuilder:
    def __init__(self):
        self.data: dict = {"resourceType": "PurificationDecision"}

    def set(self, key, value):
        self.data[key] = value

    def push(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def auto_prefix(self, ref, resource_type):
        if not ref.startswith(("urn:", "http://", "https://")) and "/" not in ref:
            return f"{resource_type}/{ref}"
        return ref

    def build(self):
        return {k: v for k, v in self.data.items() if v is not None and v != []}

    def set_id(self, val):
        self.set("id", val)
        return self

    def add_identifier(self, system, value):
        self.push("identifier", {"system": system, "value": value})
        return self

    def set_status(self, code, display=None, system=None):
        coding = {"code": code, "display": display if display else code}
        if system:
            coding["system"] = system
        self.set("status", {"coding": [coding]})
        return self

    def set_insurer(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Organization")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("insurer", res)
        return self

    def set_provider(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Organization")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("provider", res)
        return self

    def set_claim_response(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "ClaimResponse")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("claimResponse", res)
        return self

    def set_created(self, dt):
        self.set("created", dt)
        return self

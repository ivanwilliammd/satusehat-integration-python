class BillingStatusBuilder:
    def __init__(self):
        self.data: dict = {"resourceType": "BillingStatus"}

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

    def set_status(self, val):
        self.set("status", val)
        return self

    def set_insurer(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Organization")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("insurer", res)
        return self

    def set_recipient(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Organization")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("recipient", res)
        return self

    def set_subject(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Patient")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("subject", res)
        return self

    def set_request(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "CoverageEligibilityRequest")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("request", res)
        return self

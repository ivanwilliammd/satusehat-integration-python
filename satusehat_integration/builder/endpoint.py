class EndpointBuilder:
    def __init__(self):
        self.data: dict = {"resourceType": "Endpoint"}

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
        valid = ["active", "suspended", "error", "off", "entered-in-error", "test"]
        if val not in valid:
            raise ValueError(f"Invalid status: {val}")
        self.set("status", val)
        return self

    def set_connection_type(self, code, display, system="http://terminology.hl7.org/CodeSystem/endpoint-connection-type"):
        self.set("connectionType", {"coding": [{"code": code, "display": display, "system": system}]})
        return self

    def set_name(self, val):
        self.set("name", val)
        return self

    def set_managing_organization(self, ref, display=None):
        prefixed = self.auto_prefix(ref, "Organization")
        res = {"reference": prefixed}
        if display:
            res["display"] = display
        self.set("managingOrganization", res)
        return self

    def add_contact(self, system, value, use=None):
        res = {"system": system, "value": value}
        if use:
            res["use"] = use
        self.push("contact", res)
        return self

    def set_period(self, start, end=None):
        res = {"start": start}
        if end:
            res["end"] = end
        self.set("period", res)
        return self

    def add_payload_type(self, code, display, system="http://terminology.hl7.org/CodeSystem/endpoint-payload-type"):
        self.push("payloadType", {"coding": [{"code": code, "display": display, "system": system}]})
        return self

    def add_payload_mime_type(self, mime_type):
        self.push("payloadMimeType", mime_type)
        return self

    def set_address(self, addr):
        self.set("address", addr)
        return self

    def add_header(self, header):
        self.push("header", header)
        return self

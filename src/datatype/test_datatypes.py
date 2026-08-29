from src.datatype.datatypes import Identifier, Coding, CodeableConcept

def test_identifier():
    ident = Identifier(system="https://fhir.kemkes.go.id/id/nik", value="987654321")
    assert ident.value == "987654321"
    assert ident.to_array()["value"] == "987654321"

def test_coding():
    c = Coding(system="http://snomed.info/sct", code="123", display="Test")
    assert c.system == "http://snomed.info/sct"
    result = c.to_array()
    assert result["system"] == "http://snomed.info/sct"
    assert result["code"] == "123"

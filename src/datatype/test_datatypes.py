from src.datatype.datatypes import Identifier

def test_identifier():
    ident = Identifier(system="https://fhir.kemkes.go.id/id/nik", value="987654321")
    assert ident.value == "987654321"
    assert ident.to_array()["value"] == "987654321"

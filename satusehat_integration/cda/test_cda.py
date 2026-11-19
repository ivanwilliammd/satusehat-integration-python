"""Tests for CDA R2 parsing and building.

The fixture is byte-identical to the PHP and Node SDKs': parity is a test, not a claim in a README.
"""

from pathlib import Path

import pytest

from satusehat_integration.cda import CdaError, Document

FIXTURE = (Path(__file__).parent / "fixtures" / "clinical_document.xml").read_text(encoding="utf-8")


def doc() -> Document:
    return Document.parse(FIXTURE)


def test_reads_the_header():
    d = doc()
    assert d.title() == "Resume Medis Rawat Inap"
    assert d.type_code() == "34133-9"
    assert d.effective_time() == "20261118103000"
    assert d.custodian() == "RS Umum Contoh"
    assert d.document_id() == "2.16.840.1.113883.3.3157.1004.1|DOC-20261118-0001"


def test_keeps_identifier_roots_apart():
    patient = doc().patient()
    assert patient.name() == "Siti ANGGRAENI"
    assert patient.administrative_gender == "F"
    assert patient.birth_time == "19850312"
    assert len(patient.identifiers) == 2
    assert patient.identifier("2.16.840.1.113883.3.3157.1003.1") == "3171234567890001"
    assert patient.identifier("1.2.840.114350.1.13.1.1") == "MRN-0098123"
    assert patient.identifier("9.9.9") == ""


def test_reads_authors():
    assert doc().authors() == ["Ivan HARSONO"]


def test_finds_nested_sections_by_loinc():
    d = doc()
    assert len(d.sections()) == 2
    assert d.sections()[0].title == "Riwayat Penyakit Sekarang"
    diagnosis = d.section("29548-5")
    assert diagnosis is not None and len(diagnosis.children) == 1
    assert d.section("11450-4") is not None
    assert d.section("00000-0") is None


def test_section_text_is_plain_text_with_paragraph_breaks():
    text = doc().section_text("10164-2")
    assert "demam tiga hari" in text
    assert "demam tiga hari.\nRiwayat perjalanan" in text
    assert "<paragraph>" not in text


def test_validate_accepts_a_complete_document():
    assert doc().validate() == []


def test_validate_reports_what_is_missing():
    broken = '<ClinicalDocument xmlns="urn:hl7-org:v3"><title>Kosong</title></ClinicalDocument>'
    problems = Document.parse(broken).validate()
    assert "ClinicalDocument/id wajib ada." in problems
    assert "recordTarget wajib ada." in problems
    assert "custodian wajib ada." in problems
    assert "author wajib ada." in problems
    assert "structuredBody wajib berisi minimal satu section." in problems


def test_build_produces_a_document_that_validates():
    d = Document.build(
        {
            "id": "DOC-TEST-1",
            "title": "Resume Medis",
            "custodian": "RS Contoh",
            "author": "Dokter Contoh",
            "patientId": "3171234567890001",
            "patientName": "ANGGRAENI",
            "gender": "F",
            "birthTime": "19850312",
            "sections": [
                {"loinc": "10164-2", "title": "Riwayat", "text": "<paragraph>Demam.</paragraph>"}
            ],
        }
    )
    assert d.validate() == []
    assert d.title() == "Resume Medis"
    assert d.patient().name() == "ANGGRAENI"
    assert d.patient().identifier("2.16.840.1.113883.3.3157.1003.1") == "3171234567890001"
    assert d.section_text("10164-2") == "Demam."


def test_round_trip_preserves_structure_the_sdk_does_not_model():
    again = Document.parse(doc().to_xml())
    xml = again.to_xml()
    assert "encompassingEncounter" in xml
    assert "ENC-556677" in xml
    assert again.title() == "Resume Medis Rawat Inap"
    assert len(again.sections()) == 2


def test_refuses_xml_that_is_not_a_clinical_document():
    with pytest.raises(CdaError, match="bukan ClinicalDocument"):
        Document.parse('<Patient xmlns="http://hl7.org/fhir"><id value="1"/></Patient>')


def test_refuses_malformed_xml():
    with pytest.raises(CdaError, match="tidak sah"):
        Document.parse("<ClinicalDocument><unclosed>")

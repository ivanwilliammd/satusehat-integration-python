"""Unit tests for all 18 FHIR resource parsers."""
from __future__ import annotations

from src.parser import (
    DeviceParser,
    DiagnosticReportParser,
    DocumentReferenceParser,
    EncounterParser,
    GenomicStudyParser,
    GroupParser,
    LocationParser,
    MolecularSequenceParser,
    ObservationParser,
    OrganizationParser,
    PatientParser,
    PractitionerParser,
    ProcedureParser,
    RelatedPersonParser,
    RiskAssessmentParser,
    ServiceRequestParser,
    SpecimenParser,
    TaskParser,
)


def test_all_18_parsers():
    dev = DeviceParser({"status": "active", "manufacturer": "Acme", "deviceName": [{"name": "ECG"}]})
    assert dev.get_status() == "active"
    assert dev.getManufacturer() == "Acme"
    assert dev.get_device_names()[0]["name"] == "ECG"

    dr = DiagnosticReportParser({
        "status": "final",
        "subject": {"reference": "Patient/P123"},
        "encounter": {"reference": "Encounter/E123"},
        "performer": [{"reference": "Practitioner/PR1"}],
        "result": [{"reference": "Observation/OB1"}],
        "specimen": [{"reference": "Specimen/SP1"}],
    })
    assert dr.get_subject_reference() == "P123"
    assert dr.getEncounterReference() == "E123"
    assert dr.get_performer_references() == ["PR1"]
    assert dr.get_result_references() == ["OB1"]
    assert dr.get_specimen_references() == ["SP1"]

    doc = DocumentReferenceParser({
        "status": "current",
        "subject": {"reference": "Patient/P123"},
        "custodian": {"reference": "Organization/O1"},
    })
    assert doc.get_status() == "current"
    assert doc.get_subject_reference() == "Patient/P123"
    assert doc.get_custodian_reference() == "Organization/O1"

    enc = EncounterParser({
        "status": "arrived",
        "subject": {"reference": "Patient/P123", "display": "Budi"},
        "location": [{"location": {"reference": "Location/L1", "display": "Poli Umum"}}],
        "participant": [{"individual": {"reference": "Practitioner/PR1", "display": "dr. Andi"}}],
        "diagnosis": [{"condition": {"reference": "Condition/C1", "display": "Flu"}}],
        "identifier": [{"value": "REG-001"}],
        "period": {"start": "2026-01-01T08:00:00+00:00", "end": "2026-01-01T09:00:00+00:00"},
    })
    assert enc.get_subject_reference() == "P123"
    assert enc.get_location_references() == ["L1"]
    assert enc.get_participant_references() == ["PR1"]
    assert enc.get_diagnosis_references() == ["C1"]
    assert enc.get_registration_ids() == ["REG-001"]
    assert enc.get_period_start() == "2026-01-01T08:00:00+00:00"

    gs = GenomicStudyParser({
        "status": "registered",
        "subject": {"reference": "Patient/P123"},
        "encounter": {"reference": "Encounter/E123"},
        "referrer": {"reference": "Practitioner/PR1"},
    })
    assert gs.get_status() == "registered"
    assert gs.get_subject_reference() == "Patient/P123"
    assert gs.get_referrer_reference() == "Practitioner/PR1"

    grp = GroupParser({"active": True, "type": "person", "actual": True, "quantity": 5})
    assert grp.get_active() is True
    assert grp.get_quantity() == 5

    loc = LocationParser({
        "name": "Ruang 1",
        "managingOrganization": {"reference": "Organization/ORG1"},
        "partOf": {"reference": "Location/LOC0"},
    })
    assert loc.get_name() == "Ruang 1"
    assert loc.get_managing_organization_reference() == "ORG1"
    assert loc.get_part_of_reference() == "LOC0"

    ms = MolecularSequenceParser({
        "type": "dna",
        "coordinateSystem": 0,
        "patient": {"reference": "Patient/P1"},
        "specimen": {"reference": "Specimen/S1"},
        "device": {"reference": "Device/D1"},
        "performer": {"reference": "Organization/O1"},
    })
    assert ms.get_patient_reference() == "P1"
    assert ms.get_specimen_reference() == "S1"
    assert ms.get_device_reference() == "D1"
    assert ms.get_performer_reference() == "Organization/O1" or ms.get_performer_reference() == "O1"

    obs = ObservationParser({
        "status": "final",
        "subject": {"reference": "Patient/P1"},
        "encounter": {"reference": "Encounter/E1"},
        "performer": [{"reference": "Practitioner/PR1"}],
        "specimen": {"reference": "Specimen/S1"},
        "valueQuantity": {"value": 120, "unit": "mmHg"},
    })
    assert obs.get_subject_reference() == "P1"
    assert obs.get_encounter_reference() == "E1"
    assert obs.get_performer_references() == ["PR1"]
    assert obs.get_specimen_reference() == "S1"
    assert obs.get_value_quantity()["value"] == 120

    org = OrganizationParser({
        "name": "RS Sehat",
        "partOf": {"reference": "Organization/ORG-PARENT"},
    })
    assert org.get_name() == "RS Sehat"
    assert org.get_part_of_reference() == "ORG-PARENT"

    pat = PatientParser({
        "gender": "male",
        "birthDate": "1990-01-01",
        "multipleBirthInteger": 2,
    })
    assert pat.get_gender() == "male"
    assert pat.get_multiple_birth() == 2

    prac = PractitionerParser({
        "id": "PR-1",
        "gender": "female",
        "address": [
            {
                "line": ["Jl. Merdeka 1"],
                "extension": [
                    {
                        "extension": [
                            {"url": "province", "valueCode": "31"},
                            {"url": "city", "valueCode": "3171"},
                            {"url": "district", "valueCode": "317101"},
                            {"url": "village", "valueCode": "3171011001"},
                        ]
                    }
                ],
            }
        ],
        "qualification": [{"identifier": [{"value": "STR-12345"}]}],
    })
    assert prac.get_id() == "PR-1"
    assert prac.get_address_line() == "Jl. Merdeka 1"
    assert prac.get_city() == "3171"
    assert prac.get_village() == "3171011001"
    assert prac.get_qualifications() == "STR-12345"

    proc = ProcedureParser({
        "status": "completed",
        "subject": {"reference": "Patient/P1", "display": "Budi"},
        "encounter": {"reference": "Encounter/E1", "display": "Enc 1"},
        "performer": [{"actor": {"reference": "Practitioner/PR1", "display": "dr. A"}}],
        "location": {"reference": "Location/L1"},
    })
    assert proc.get_subject_reference() == "P1"
    assert proc.get_encounter_reference() == "E1"
    assert proc.get_performer_references() == ["PR1"]
    assert proc.get_location() == "L1"

    rp = RelatedPersonParser({
        "active": True,
        "patient": {"reference": "Patient/P1"},
        "gender": "female",
    })
    assert rp.get_active() is True
    assert rp.get_patient_reference() == "Patient/P1"

    ra = RiskAssessmentParser({
        "status": "final",
        "subject": {"reference": "Patient/P1"},
        "encounter": {"reference": "Encounter/E1"},
        "condition": {"reference": "Condition/C1"},
        "performer": {"reference": "Practitioner/PR1"},
    })
    assert ra.get_subject_reference() == "P1"
    assert ra.get_encounter_reference() == "E1"
    assert ra.get_condition_reference() == "C1"
    assert ra.get_performer_reference() == "PR1"

    sr = ServiceRequestParser({
        "status": "active",
        "intent": "order",
        "encounter": {"reference": "Encounter/E1", "display": "Enc 1"},
        "requester": {"reference": "Practitioner/PR1", "display": "dr. A"},
    })
    assert sr.get_encounter_reference() == "E1"
    assert sr.get_requester_reference() == "Practitioner/PR1"

    spec = SpecimenParser({
        "status": "available",
        "subject": {"reference": "Patient/P1", "display": "Budi"},
        "collection": {
            "collectedDateTime": "2026-01-01T10:00:00+00:00",
            "collector": {"reference": "Practitioner/PR1", "display": "Perawat B"},
        },
    })
    assert spec.get_subject_reference() == "P1"
    assert spec.get_collector_reference() == "PR1"
    assert spec.get_collected_date_time() == "2026-01-01T10:00:00+00:00"

    tsk = TaskParser({
        "status": "requested",
        "intent": "order",
        "for": {"reference": "Patient/P1"},
        "encounter": {"reference": "Encounter/E1"},
        "requester": {"reference": "Practitioner/PR1"},
    })
    assert tsk.get_for_reference() == "P1"
    assert tsk.get_encounter_reference() == "E1"
    assert tsk.get_requester_reference() == "PR1"

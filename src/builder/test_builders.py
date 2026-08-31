import pytest
from src.builder.billing_status import BillingStatusBuilder
from src.builder.endpoint import EndpointBuilder
from src.builder.purification_decision import PurificationDecisionBuilder
from src.builder.medication_statement import MedicationStatementBuilder
from src.builder.task import TaskBuilder


class TestBillingStatusBuilder:
    def test_resource_type(self):
        assert BillingStatusBuilder().build()["resourceType"] == "BillingStatus"

    def test_set_id(self):
        assert BillingStatusBuilder().set_id("bs-1").build()["id"] == "bs-1"

    def test_add_identifier(self):
        res = BillingStatusBuilder().add_identifier("http://sys", "VAL").build()
        assert res["identifier"][0]["system"] == "http://sys"
        assert res["identifier"][0]["value"] == "VAL"

    def test_auto_prefix_insurer(self):
        res = BillingStatusBuilder().set_insurer("org-001", "BPJS").build()
        assert res["insurer"]["reference"] == "Organization/org-001"

    def test_auto_prefix_subject(self):
        res = BillingStatusBuilder().set_subject("1001", "Budi").build()
        assert res["subject"]["reference"] == "Patient/1001"

    def test_auto_prefix_request(self):
        res = BillingStatusBuilder().set_request("cer-001").build()
        assert res["request"]["reference"] == "CoverageEligibilityRequest/cer-001"

    def test_full(self):
        res = (BillingStatusBuilder()
            .set_id("bs-full").set_status("active")
            .add_identifier("http://sys", "VAL")
            .set_insurer("org-001", "BPJS")
            .set_subject("1001", "Budi")
            .build())
        assert res["resourceType"] == "BillingStatus"
        assert res["status"] == "active"


class TestEndpointBuilder:
    def test_resource_type(self):
        assert EndpointBuilder().build()["resourceType"] == "Endpoint"

    def test_set_id(self):
        assert EndpointBuilder().set_id("ep-1").build()["id"] == "ep-1"

    def test_set_status_valid(self):
        assert EndpointBuilder().set_status("active").build()["status"] == "active"

    def test_set_status_invalid(self):
        with pytest.raises(Exception):
            EndpointBuilder().set_status("invalid")

    def test_connection_type(self):
        res = EndpointBuilder().set_connection_type("ihe-xcpd", "IHE XCPD").build()
        assert res["connectionType"]["coding"][0]["code"] == "ihe-xcpd"

    def test_auto_prefix_managing_org(self):
        res = EndpointBuilder().set_managing_organization("org-001").build()
        assert res["managingOrganization"]["reference"] == "Organization/org-001"

    def test_add_contact(self):
        res = EndpointBuilder().add_contact("phone", "+6221", "work").build()
        assert res["contact"][0]["system"] == "phone"

    def test_period(self):
        res = EndpointBuilder().set_period("2022-12-20", "2022-12-30").build()
        assert res["period"]["start"] == "2022-12-20"
        assert res["period"]["end"] == "2022-12-30"


class TestPurificationDecisionBuilder:
    def test_resource_type(self):
        assert PurificationDecisionBuilder().build()["resourceType"] == "PurificationDecision"

    def test_set_id(self):
        assert PurificationDecisionBuilder().set_id("pd-1").build()["id"] == "pd-1"

    def test_set_status(self):
        res = PurificationDecisionBuilder().set_status("approved", "Approved", "http://sys").build()
        assert res["status"]["coding"][0]["code"] == "approved"

    def test_auto_prefix_insurer(self):
        res = PurificationDecisionBuilder().set_insurer("org-001").build()
        assert res["insurer"]["reference"] == "Organization/org-001"

    def test_auto_prefix_provider(self):
        res = PurificationDecisionBuilder().set_provider("hos-001").build()
        assert res["provider"]["reference"] == "Organization/hos-001"

    def test_auto_prefix_claim_response(self):
        res = PurificationDecisionBuilder().set_claim_response("cr-001").build()
        assert res["claimResponse"]["reference"] == "ClaimResponse/cr-001"


class TestMedicationStatementBuilder:
    def test_resource_type(self):
        assert MedicationStatementBuilder().build()["resourceType"] == "MedicationStatement"

    def test_auto_prefix_subject(self):
        res = MedicationStatementBuilder().set_subject("100000030009", "Budi").build()
        assert res["subject"]["reference"] == "Patient/100000030009"

    def test_auto_prefix_medication(self):
        res = MedicationStatementBuilder().set_medication_reference("med-001", "Paracetamol").build()
        assert res["medicationReference"]["reference"] == "Medication/med-001"

    def test_auto_prefix_context(self):
        res = MedicationStatementBuilder().set_context("enc-001").build()
        assert res["context"]["reference"] == "Encounter/enc-001"

    def test_urn_preserved(self):
        res = MedicationStatementBuilder().set_subject("urn:uuid:550e8400-e29b-41d4-a716").build()
        assert res["subject"]["reference"] == "urn:uuid:550e8400-e29b-41d4-a716"

    def test_dosage_instruction(self):
        res = MedicationStatementBuilder().add_dosage_instruction("Paracetamol 500mg", 3, 1, "d").build()
        assert res["dosage"][0]["text"] == "Paracetamol 500mg"
        assert res["dosage"][0]["timing"]["repeat"]["frequency"] == 3


class TestTaskBuilder:
    def test_resource_type(self):
        assert TaskBuilder().build()["resourceType"] == "Task"

    def test_set_id(self):
        assert TaskBuilder().set_id("task-1").build()["id"] == "task-1"

    def test_set_status_valid(self):
        assert TaskBuilder().set_status("requested").build()["status"] == "requested"

    def test_set_status_invalid(self):
        with pytest.raises(Exception):
            TaskBuilder().set_status("invalid")

    def test_set_intent_valid(self):
        assert TaskBuilder().set_intent("order").build()["intent"] == "order"

    def test_set_intent_invalid(self):
        with pytest.raises(Exception):
            TaskBuilder().set_intent("invalid")

    def test_auto_prefix_for(self):
        res = TaskBuilder().set_for("100000030009", "Budi").build()
        assert res["for"]["reference"] == "Patient/100000030009"

    def test_auto_prefix_encounter(self):
        res = TaskBuilder().set_encounter("enc-001").build()
        assert res["encounter"]["reference"] == "Encounter/enc-001"

    def test_auto_prefix_requester(self):
        res = TaskBuilder().set_requester("N10000001").build()
        assert res["requester"]["reference"] == "Practitioner/N10000001"

    def test_auto_prefix_owner(self):
        res = TaskBuilder().set_owner("N20000001").build()
        assert res["owner"]["reference"] == "Practitioner/N20000001"

    def test_auto_prefix_location(self):
        res = TaskBuilder().set_location("loc-001").build()
        assert res["location"]["reference"] == "Location/loc-001"

    def test_add_input(self):
        res = TaskBuilder().add_input("Darah", "120/80").build()
        assert res["input"][0]["type"]["text"] == "Darah"
        assert res["input"][0]["valueString"] == "120/80"

    def test_add_output(self):
        res = TaskBuilder().add_output("Hasil", "Normal").build()
        assert res["output"][0]["type"]["text"] == "Hasil"

    def test_add_identifier(self):
        res = TaskBuilder().add_identifier("http://sys", "TASK-001").build()
        assert res["identifier"][0]["system"] == "http://sys"

    def test_full(self):
        res = (TaskBuilder()
            .set_id("task-full").set_status("requested").set_intent("order")
            .set_for("100000030009").set_encounter("enc-001")
            .set_requester("N10000001")
            .add_input("Catatan", "Pasien stabil")
            .build())
        assert res["resourceType"] == "Task"
        assert res["status"] == "requested"
        assert res["for"]["reference"] == "Patient/100000030009"

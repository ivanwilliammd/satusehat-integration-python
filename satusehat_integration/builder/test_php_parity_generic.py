"""53 builder yang permukaannya sama persis di PHP, Go, Node dan Python.

Golden-nya keluaran builder PHP. Perbandingan yang dipakai kesamaan payload penuh,
bukan pemeriksaan beberapa field: uji field sendiri lolos meski salah port.
"""
import json
from pathlib import Path

import pytest

from satusehat_integration.builder.audit_event import AuditEventBuilder
from satusehat_integration.builder.basic import BasicBuilder
from satusehat_integration.builder.binary import BinaryBuilder
from satusehat_integration.builder.biologically_derived_product import BiologicallyDerivedProductBuilder
from satusehat_integration.builder.body_structure import BodyStructureBuilder
from satusehat_integration.builder.contract import ContractBuilder
from satusehat_integration.builder.device_definition import DeviceDefinitionBuilder
from satusehat_integration.builder.device_request import DeviceRequestBuilder
from satusehat_integration.builder.device_use_statement import DeviceUseStatementBuilder
from satusehat_integration.builder.effect_evidence_synthesis import EffectEvidenceSynthesisBuilder
from satusehat_integration.builder.enrollment_request import EnrollmentRequestBuilder
from satusehat_integration.builder.event_definition import EventDefinitionBuilder
from satusehat_integration.builder.evidence import EvidenceBuilder
from satusehat_integration.builder.evidence_variable import EvidenceVariableBuilder
from satusehat_integration.builder.example_scenario import ExampleScenarioBuilder
from satusehat_integration.builder.flag import FlagBuilder
from satusehat_integration.builder.guidance_response import GuidanceResponseBuilder
from satusehat_integration.builder.imaging_manifest import ImagingManifestBuilder
from satusehat_integration.builder.imaging_selection import ImagingSelectionBuilder
from satusehat_integration.builder.immunization_evaluation import ImmunizationEvaluationBuilder
from satusehat_integration.builder.immunization_recommendation import ImmunizationRecommendationBuilder
from satusehat_integration.builder.library import LibraryBuilder
from satusehat_integration.builder.linkage import LinkageBuilder
from satusehat_integration.builder.measure import MeasureBuilder
from satusehat_integration.builder.measure_report import MeasureReportBuilder
from satusehat_integration.builder.media import MediaBuilder
from satusehat_integration.builder.message_definition import MessageDefinitionBuilder
from satusehat_integration.builder.message_header import MessageHeaderBuilder
from satusehat_integration.builder.operation_outcome import OperationOutcomeBuilder
from satusehat_integration.builder.person import PersonBuilder
from satusehat_integration.builder.plan_definition import PlanDefinitionBuilder
from satusehat_integration.builder.provenance import ProvenanceBuilder
from satusehat_integration.builder.questionnaire import QuestionnaireBuilder
from satusehat_integration.builder.request_group import RequestGroupBuilder
from satusehat_integration.builder.research_definition import ResearchDefinitionBuilder
from satusehat_integration.builder.research_element_definition import ResearchElementDefinitionBuilder
from satusehat_integration.builder.research_subject import ResearchSubjectBuilder
from satusehat_integration.builder.risk_evidence_synthesis import RiskEvidenceSynthesisBuilder
from satusehat_integration.builder.schedule import ScheduleBuilder
from satusehat_integration.builder.search_parameter import SearchParameterBuilder
from satusehat_integration.builder.slot import SlotBuilder
from satusehat_integration.builder.subscription import SubscriptionBuilder
from satusehat_integration.builder.substance_nucleic_acid import SubstanceNucleicAcidBuilder
from satusehat_integration.builder.substance_polymer import SubstancePolymerBuilder
from satusehat_integration.builder.substance_protein import SubstanceProteinBuilder
from satusehat_integration.builder.substance_source_material import SubstanceSourceMaterialBuilder
from satusehat_integration.builder.substance_specification import SubstanceSpecificationBuilder
from satusehat_integration.builder.supply_delivery import SupplyDeliveryBuilder
from satusehat_integration.builder.supply_request import SupplyRequestBuilder
from satusehat_integration.builder.test_report import TestReportBuilder
from satusehat_integration.builder.test_script import TestScriptBuilder
from satusehat_integration.builder.verification_result import VerificationResultBuilder
from satusehat_integration.builder.vision_prescription import VisionPrescriptionBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_php_golden.json").read_text())


KASUS = [
    (
        "audit_event",
        lambda: AuditEventBuilder()
        .set_id("audit-event-1")
        .add_identifier("http://sys.id/ni", "NI-100")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "basic",
        lambda: BasicBuilder()
        .set_id("basic-1")
        .add_identifier("http://sys.id/ni", "NI-101")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "binary",
        lambda: BinaryBuilder()
        .set_id("binary-1")
        .add_identifier("http://sys.id/ni", "NI-102")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "biologically_derived_product",
        lambda: BiologicallyDerivedProductBuilder()
        .set_id("biologically-derived-product-1")
        .add_identifier("http://sys.id/ni", "NI-103")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "body_structure",
        lambda: BodyStructureBuilder()
        .set_id("body-structure-1")
        .add_identifier("http://sys.id/ni", "NI-104")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "contract",
        lambda: ContractBuilder()
        .set_id("contract-1")
        .add_identifier("http://sys.id/ni", "NI-105")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "device_definition",
        lambda: DeviceDefinitionBuilder()
        .set_id("device-definition-1")
        .add_identifier("http://sys.id/ni", "NI-106")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "device_request",
        lambda: DeviceRequestBuilder()
        .set_id("device-request-1")
        .add_identifier("http://sys.id/ni", "NI-107")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "device_use_statement",
        lambda: DeviceUseStatementBuilder()
        .set_id("device-use-statement-1")
        .add_identifier("http://sys.id/ni", "NI-108")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "effect_evidence_synthesis",
        lambda: EffectEvidenceSynthesisBuilder()
        .set_id("effect-evidence-synthesis-1")
        .add_identifier("http://sys.id/ni", "NI-109")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "enrollment_request",
        lambda: EnrollmentRequestBuilder()
        .set_id("enrollment-request-1")
        .add_identifier("http://sys.id/ni", "NI-110")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "event_definition",
        lambda: EventDefinitionBuilder()
        .set_id("event-definition-1")
        .add_identifier("http://sys.id/ni", "NI-111")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "evidence",
        lambda: EvidenceBuilder()
        .set_id("evidence-1")
        .add_identifier("http://sys.id/ni", "NI-112")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "evidence_variable",
        lambda: EvidenceVariableBuilder()
        .set_id("evidence-variable-1")
        .add_identifier("http://sys.id/ni", "NI-113")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "example_scenario",
        lambda: ExampleScenarioBuilder()
        .set_id("example-scenario-1")
        .add_identifier("http://sys.id/ni", "NI-114")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "flag",
        lambda: FlagBuilder()
        .set_id("flag-1")
        .add_identifier("http://sys.id/ni", "NI-115")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "guidance_response",
        lambda: GuidanceResponseBuilder()
        .set_id("guidance-response-1")
        .add_identifier("http://sys.id/ni", "NI-116")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "imaging_manifest",
        lambda: ImagingManifestBuilder()
        .set_id("imaging-manifest-1")
        .add_identifier("http://sys.id/ni", "NI-117")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "imaging_selection",
        lambda: ImagingSelectionBuilder()
        .set_id("imaging-selection-1")
        .add_identifier("http://sys.id/ni", "NI-118")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "immunization_evaluation",
        lambda: ImmunizationEvaluationBuilder()
        .set_id("immunization-evaluation-1")
        .add_identifier("http://sys.id/ni", "NI-119")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "immunization_recommendation",
        lambda: ImmunizationRecommendationBuilder()
        .set_id("immunization-recommendation-1")
        .add_identifier("http://sys.id/ni", "NI-120")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "library",
        lambda: LibraryBuilder()
        .set_id("library-1")
        .add_identifier("http://sys.id/ni", "NI-121")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "linkage",
        lambda: LinkageBuilder()
        .set_id("linkage-1")
        .add_identifier("http://sys.id/ni", "NI-122")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "measure",
        lambda: MeasureBuilder()
        .set_id("measure-1")
        .add_identifier("http://sys.id/ni", "NI-123")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "measure_report",
        lambda: MeasureReportBuilder()
        .set_id("measure-report-1")
        .add_identifier("http://sys.id/ni", "NI-124")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "media",
        lambda: MediaBuilder()
        .set_id("media-1")
        .add_identifier("http://sys.id/ni", "NI-125")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "message_definition",
        lambda: MessageDefinitionBuilder()
        .set_id("message-definition-1")
        .add_identifier("http://sys.id/ni", "NI-126")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "message_header",
        lambda: MessageHeaderBuilder()
        .set_id("message-header-1")
        .add_identifier("http://sys.id/ni", "NI-127")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "operation_outcome",
        lambda: OperationOutcomeBuilder()
        .set_id("operation-outcome-1")
        .add_identifier("http://sys.id/ni", "NI-128")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "person",
        lambda: PersonBuilder()
        .set_id("person-1")
        .add_identifier("http://sys.id/ni", "NI-129")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "plan_definition",
        lambda: PlanDefinitionBuilder()
        .set_id("plan-definition-1")
        .add_identifier("http://sys.id/ni", "NI-130")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "provenance",
        lambda: ProvenanceBuilder()
        .set_id("provenance-1")
        .add_identifier("http://sys.id/ni", "NI-131")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "questionnaire",
        lambda: QuestionnaireBuilder()
        .set_id("questionnaire-1")
        .add_identifier("http://sys.id/ni", "NI-132")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "request_group",
        lambda: RequestGroupBuilder()
        .set_id("request-group-1")
        .add_identifier("http://sys.id/ni", "NI-133")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "research_definition",
        lambda: ResearchDefinitionBuilder()
        .set_id("research-definition-1")
        .add_identifier("http://sys.id/ni", "NI-134")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "research_element_definition",
        lambda: ResearchElementDefinitionBuilder()
        .set_id("research-element-definition-1")
        .add_identifier("http://sys.id/ni", "NI-135")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "research_subject",
        lambda: ResearchSubjectBuilder()
        .set_id("research-subject-1")
        .add_identifier("http://sys.id/ni", "NI-136")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "risk_evidence_synthesis",
        lambda: RiskEvidenceSynthesisBuilder()
        .set_id("risk-evidence-synthesis-1")
        .add_identifier("http://sys.id/ni", "NI-137")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "schedule",
        lambda: ScheduleBuilder()
        .set_id("schedule-1")
        .add_identifier("http://sys.id/ni", "NI-138")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "search_parameter",
        lambda: SearchParameterBuilder()
        .set_id("search-parameter-1")
        .add_identifier("http://sys.id/ni", "NI-139")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "slot",
        lambda: SlotBuilder()
        .set_id("slot-1")
        .add_identifier("http://sys.id/ni", "NI-140")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "subscription",
        lambda: SubscriptionBuilder()
        .set_id("subscription-1")
        .add_identifier("http://sys.id/ni", "NI-141")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "substance_nucleic_acid",
        lambda: SubstanceNucleicAcidBuilder()
        .set_id("substance-nucleic-acid-1")
        .add_identifier("http://sys.id/ni", "NI-142")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "substance_polymer",
        lambda: SubstancePolymerBuilder()
        .set_id("substance-polymer-1")
        .add_identifier("http://sys.id/ni", "NI-143")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "substance_protein",
        lambda: SubstanceProteinBuilder()
        .set_id("substance-protein-1")
        .add_identifier("http://sys.id/ni", "NI-144")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "substance_source_material",
        lambda: SubstanceSourceMaterialBuilder()
        .set_id("substance-source-material-1")
        .add_identifier("http://sys.id/ni", "NI-145")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "substance_specification",
        lambda: SubstanceSpecificationBuilder()
        .set_id("substance-specification-1")
        .add_identifier("http://sys.id/ni", "NI-146")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "supply_delivery",
        lambda: SupplyDeliveryBuilder()
        .set_id("supply-delivery-1")
        .add_identifier("http://sys.id/ni", "NI-147")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "supply_request",
        lambda: SupplyRequestBuilder()
        .set_id("supply-request-1")
        .add_identifier("http://sys.id/ni", "NI-148")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "test_report",
        lambda: TestReportBuilder()
        .set_id("test-report-1")
        .add_identifier("http://sys.id/ni", "NI-149")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "test_script",
        lambda: TestScriptBuilder()
        .set_id("test-script-1")
        .add_identifier("http://sys.id/ni", "NI-150")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "verification_result",
        lambda: VerificationResultBuilder()
        .set_id("verification-result-1")
        .add_identifier("http://sys.id/ni", "NI-151")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
    (
        "vision_prescription",
        lambda: VisionPrescriptionBuilder()
        .set_id("vision-prescription-1")
        .add_identifier("http://sys.id/ni", "NI-152")
        .set_status("active")
        .set_subject("Patient/1000000001", "Budi Santoso")
        .set_code({"coding": [{"system": "http://terminology.kemkes.go.id/CodeSystem/activity", "code": "ACT-1", "display": "Konsultasi"}]})
        .set_encounter("Encounter/enc-1")
        .build(),
    ),
]


@pytest.mark.parametrize("nama,buat", KASUS, ids=[n for n, _ in KASUS])
def test_sama_dengan_golden_php(nama, buat):
    assert buat() == golden(nama)

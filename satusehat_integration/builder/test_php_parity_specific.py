"""Golden PHP untuk builder yang permukaannya khas per resource.

Pemanggilan setter dijalankan lewat `jalankan()` dan bukan rantai langsung: tanda
tangan `set_code` tidak seragam di repo ini — sebagian menerima dict coding,
sebagian tiga argumen. Perbedaan itu nyata dan tidak boleh disembunyikan, jadi
diterjemahkan di satu tempat.
"""
import json
from pathlib import Path

import pytest

from satusehat_integration.builder.activity_definition import ActivityDefinitionBuilder
from satusehat_integration.builder.billing_status import BillingStatusBuilder
from satusehat_integration.builder.capability_statement import CapabilityStatementBuilder
from satusehat_integration.builder.catalog_entry import CatalogEntryBuilder
from satusehat_integration.builder.communication import CommunicationBuilder
from satusehat_integration.builder.communication_request import CommunicationRequestBuilder
from satusehat_integration.builder.consent import ConsentBuilder
from satusehat_integration.builder.coverage_eligibility_request import CoverageEligibilityRequestBuilder
from satusehat_integration.builder.coverage_eligibility_response import CoverageEligibilityResponseBuilder
from satusehat_integration.builder.detected_issue import DetectedIssueBuilder
from satusehat_integration.builder.device_metric import DeviceMetricBuilder
from satusehat_integration.builder.document_manifest import DocumentManifestBuilder
from satusehat_integration.builder.enrollment_response import EnrollmentResponseBuilder
from satusehat_integration.builder.explanation_of_benefit import ExplanationOfBenefitBuilder
from satusehat_integration.builder.insurance_plan import InsurancePlanBuilder
from satusehat_integration.builder.medication_knowledge import MedicationKnowledgeBuilder
from satusehat_integration.builder.medicinal_product import MedicinalProductBuilder
from satusehat_integration.builder.medicinal_product_authorization import MedicinalProductAuthorizationBuilder
from satusehat_integration.builder.medicinal_product_contraindication import MedicinalProductContraindicationBuilder
from satusehat_integration.builder.medicinal_product_indication import MedicinalProductIndicationBuilder
from satusehat_integration.builder.medicinal_product_ingredient import MedicinalProductIngredientBuilder
from satusehat_integration.builder.medicinal_product_interaction import MedicinalProductInteractionBuilder
from satusehat_integration.builder.medicinal_product_manufactured import MedicinalProductManufacturedBuilder
from satusehat_integration.builder.medicinal_product_packaged import MedicinalProductPackagedBuilder
from satusehat_integration.builder.medicinal_product_pharmaceutical import MedicinalProductPharmaceuticalBuilder
from satusehat_integration.builder.medicinal_product_undesirable_effect import MedicinalProductUndesirableEffectBuilder
from satusehat_integration.builder.observation_definition import ObservationDefinitionBuilder
from satusehat_integration.builder.organization_affiliation import OrganizationAffiliationBuilder
from satusehat_integration.builder.purification_decision import PurificationDecisionBuilder
from satusehat_integration.builder.research_study import ResearchStudyBuilder
from satusehat_integration.builder.resource_guide import ResourceGuideBuilder
from satusehat_integration.builder.specimen_definition import SpecimenDefinitionBuilder
from satusehat_integration.builder.substance_reference_information import SubstanceReferenceInformationBuilder

GOLDEN = Path(__file__).resolve().parent / "testdata"


def golden(nama: str):
    return json.loads((GOLDEN / f"{nama}_php_golden.json").read_text())


def jalankan(builder_cls, langkah):
    b = builder_cls()
    for method, args in langkah:
        try:
            getattr(b, method)(*args)
        except TypeError:
            if method != "set_code" or len(args) != 3:
                raise
            b.set_code({"coding": [{"system": args[0], "code": args[1], "display": args[2]}]})
    return b.build()


KASUS = {
    "activity_definition": (ActivityDefinitionBuilder, [("set_id", ("ad-1",)), ("add_identifier", ("http://sys.id/ni", "NI-1",)), ("set_status", ("active",)), ("set_description", ("Edukasi gizi",)), ("set_kind", ("http://terminology.hl7.org/CodeSystem/activity-definition-kind", "ServiceRequest", "Service Request",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/activity", "EDU-1", "Edukasi",)), ("set_author", ("Practitioner/1000000002", "dr. Budi",)), ("set_timing", ("2026-01-05",))]),
    "billing_status": (BillingStatusBuilder, [("set_id", ("bs-1",)), ("add_identifier", ("http://sys.id/ni", "NI-90",)), ("set_status", ("active",)), ("set_insurer", ("Organization/1000000001", "BPJS",)), ("set_recipient", ("Organization/1000000002", "RS Sehat",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_request", ("CoverageEligibilityRequest/cer-1", "Klaim",))]),
    "capability_statement": (CapabilityStatementBuilder, [("set_id", ("cs-1",)), ("add_identifier", ("http://sys.id/ni", "NI-2",)), ("set_status", ("active",)), ("set_date", ("2026-01-05",)), ("set_kind", ("http://hl7.org/fhir/capability-statement-kind", "instance", "Instance",)), ("set_fhir_version", ("http://hl7.org/fhir/FHIR-version", "4.0.1", "4.0.1",)), ("set_format", ("http://hl7.org/fhir/restful-format", "json", "JSON",)), ("set_rest", ("http://hl7.org/fhir/restful-mode", "server", "Server",))]),
    "catalog_entry": (CatalogEntryBuilder, [("set_id", ("ce-1",)), ("add_identifier", ("http://sys.id/ni", "NI-3",)), ("set_status", ("active",)), ("set_type", ("http://terminology.hl7.org/CodeSystem/catalogType", "medication", "Medication",)), ("set_reference", ("Medication/med-1", "Amoksisilin",)), ("set_validity_period", ("2026-01-05/2026-12-31",))]),
    "communication": (CommunicationBuilder, [("set_id", ("communication-1",)), ("add_identifier", ("http://sys.id/ni", "NI-32",)), ("set_status", ("active",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/activity", "ACT-1", "Konsultasi",)), ("set_encounter", ("Encounter/enc-1",))]),
    "communication_request": (CommunicationRequestBuilder, [("set_id", ("communicationrequest-1",)), ("add_identifier", ("http://sys.id/ni", "NI-33",)), ("set_status", ("active",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/activity", "ACT-1", "Konsultasi",)), ("set_encounter", ("Encounter/enc-1",))]),
    "consent": (ConsentBuilder, [("set_id", ("consent-1",)), ("add_identifier", ("http://sys.id/ni", "NI-35",)), ("set_status", ("active",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/activity", "ACT-1", "Konsultasi",)), ("set_encounter", ("Encounter/enc-1",))]),
    "coverage_eligibility_request": (CoverageEligibilityRequestBuilder, [("set_id", ("cer-2",)), ("add_identifier", ("http://sys.id/ni", "NI-60",)), ("set_status", ("active",)), ("set_patient", ("Patient/1000000001", "Budi Santoso",)), ("set_insurer", ("Organization/1000000001",)), ("set_created", ("2026-01-05",)), ("add_coverage", ("Coverage/cov-1", "PRE-1",)), ("set_enterer", ("Practitioner/1000000002",)), ("set_provider", ("Organization/1000000001",)), ("add_item", ("http://terminology.kemkes.go.id/CodeSystem/lab", "LAB-1", "Darah Lengkap", "http://terminology.hl7.org/CodeSystem/ex-benefitcategory", "1",)), ("set_priority", ("http://terminology.hl7.org/CodeSystem/processpriority", "normal", "Normal",)), ("set_purpose", (["validation", "benefits"],)), ("set_serviced_date", ("2026-01-05",))]),
    "coverage_eligibility_response": (CoverageEligibilityResponseBuilder, [("set_id", ("cer-1",)), ("set_status", ("active",)), ("set_purpose", (["benefits"],)), ("set_serviced_date", ("2026-01-05",)), ("set_request_provider", ("Organization/1000000001",)), ("set_patient", ("Patient/1000000001",)), ("add_insurance", ("Coverage/cov-1", "Rawat inap", "http://terminology.hl7.org/CodeSystem/benefit-category", "1", "Medical Care",))]),
    "detected_issue": (DetectedIssueBuilder, [("set_id", ("detectedissue-1",)), ("add_identifier", ("http://sys.id/ni", "NI-34",)), ("set_status", ("active",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/activity", "ACT-1", "Konsultasi",)), ("set_encounter", ("Encounter/enc-1",))]),
    "device_metric": (DeviceMetricBuilder, [("set_id", ("dm-1",)), ("add_identifier", ("http://sys.id/ni", "NI-4",)), ("set_status", ("active",)), ("set_type", ("http://terminology.hl7.org/CodeSystem/device-metric-type", "heart-rate", "Heart rate",)), ("set_category", ("http://terminology.hl7.org/CodeSystem/metric-category", "measurement", "Measurement",)), ("set_measurement_period", ("2026-01-05",))]),
    "document_manifest": (DocumentManifestBuilder, [("set_id", ("dmf-1",)), ("add_identifier", ("http://sys.id/ni", "NI-5",)), ("set_status", ("current",)), ("set_type", ("http://loinc.org", "34133-9", "Summary of episode note",)), ("set_subject", ("Patient/1000000001", "Budi Santoso",)), ("set_created", ("2026-01-05",)), ("set_source", ("Practitioner/1000000002", "dr. Budi",))]),
    "enrollment_response": (EnrollmentResponseBuilder, [("set_id", ("er-1",)), ("add_identifier", ("http://sys.id/ni", "NI-6",)), ("set_status", ("active",)), ("set_request", ("EnrollmentRequest/erq-1", "Pendaftaran",)), ("set_outcome", ("http://terminology.hl7.org/CodeSystem/remittance-outcome", "complete", "Complete",)), ("set_disposition", ("Disetujui",)), ("set_created", ("2026-01-05",))]),
    "explanation_of_benefit": (ExplanationOfBenefitBuilder, [("set_id", ("eob-1",)), ("add_identifier", ("http://sys.id/ni", "NI-7",)), ("set_status", ("active",)), ("set_type", ("http://terminology.hl7.org/CodeSystem/claim-type", "institutional", "Institutional",)), ("set_use", ("http://terminology.hl7.org/CodeSystem/claim-use", "claim", "Claim",)), ("set_patient", ("Patient/1000000001", "Budi Santoso",)), ("set_created", ("2026-01-05",)), ("set_provider", ("Organization/1000000001", "RS Sehat",))]),
    "insurance_plan": (InsurancePlanBuilder, [("set_id", ("ip-1",)), ("add_identifier", ("http://sys.id/ni", "NI-8",)), ("set_status", ("active",)), ("set_name", ("BPJS Kesehatan",)), ("set_type", ("http://terminology.hl7.org/CodeSystem/insurance-plan-type", "medical", "Medical",)), ("set_administered_by", ("Organization/1000000001", "BPJS",)), ("set_coverage", ("http://terminology.hl7.org/CodeSystem/coverage-type", "institutional", "Institutional",))]),
    "medication_knowledge": (MedicationKnowledgeBuilder, [("set_id", ("mk-1",)), ("add_identifier", ("http://sys.id/ni", "NI-9",)), ("set_status", ("active",)), ("set_code", ("http://terminology.kemkes.go.id/CodeSystem/medication", "MED-1", "Amoksisilin",)), ("set_manufacturer", ("Organization/1000000001", "Kimia Farma",)), ("set_dose_form", ("http://snomed.info/sct", "385055001", "Tablet",))]),
    "medicinal_product": (MedicinalProductBuilder, [("set_id", ("mp-1",)), ("add_identifier", ("http://sys.id/ni", "NI-20",)), ("set_status", ("active",)), ("set_name", ("Amoksisilin",)), ("set_manufacturer", ("Organization/1000000001", "Kimia Farma",)), ("set_product_class", ("http://terminology.hl7.org/CodeSystem/medicinal-product-class", "antibiotic", "Antibiotic",))]),
    "medicinal_product_authorization": (MedicinalProductAuthorizationBuilder, [("set_id", ("mpa-1",)), ("add_identifier", ("http://sys.id/ni", "NI-21",)), ("set_status", ("active",)), ("set_country", ("urn:iso:std:iso:3166", "ID", "Indonesia",)), ("set_regulator", ("Organization/1000000002", "BPOM",)), ("set_validity_period", ("2026-01-05/2031-01-05",))]),
    "medicinal_product_contraindication": (MedicinalProductContraindicationBuilder, [("set_id", ("mpc-1",)), ("add_identifier", ("http://sys.id/ni", "NI-22",)), ("set_status", ("active",)), ("set_subject", ("MedicinalProduct/mp-1", "Amoksisilin",)), ("set_disease", ("http://snomed.info/sct", "91936005", "Alergi penisilin",)), ("set_comorbidity", ("Condition/cond-9", "Gagal ginjal",))]),
    "medicinal_product_indication": (MedicinalProductIndicationBuilder, [("set_id", ("mpi-1",)), ("add_identifier", ("http://sys.id/ni", "NI-23",)), ("set_status", ("active",)), ("set_subject", ("MedicinalProduct/mp-1", "Amoksisilin",)), ("set_disease", ("http://snomed.info/sct", "233604007", "Pneumonia",)), ("set_comorbidity", ("Condition/cond-10", "Diabetes",))]),
    "medicinal_product_ingredient": (MedicinalProductIngredientBuilder, [("set_id", ("mpg-1",)), ("add_identifier", ("http://sys.id/ni", "NI-24",)), ("set_status", ("active",)), ("set_role", ("http://terminology.hl7.org/CodeSystem/medicinal-product-ingredient-role", "active", "Active",)), ("set_substance", ("Amoksisilin trihidrat",)), ("set_quantity", ("500 mg",))]),
    "medicinal_product_interaction": (MedicinalProductInteractionBuilder, [("set_id", ("mpn-1",)), ("add_identifier", ("http://sys.id/ni", "NI-25",)), ("set_status", ("active",)), ("set_subject", ("MedicinalProduct/mp-1", "Amoksisilin",)), ("set_description", ("Interaksi dengan warfarin",)), ("set_interactant", ("http://snomed.info/sct", "372756006", "Warfarin",))]),
    "medicinal_product_manufactured": (MedicinalProductManufacturedBuilder, [("set_id", ("mpm-1",)), ("add_identifier", ("http://sys.id/ni", "NI-26",)), ("set_status", ("active",)), ("set_quantity", ("500 mg",)), ("set_manufacturer", ("Organization/1000000001", "Kimia Farma",)), ("set_ingredient", ("http://snomed.info/sct", "387517004", "Amoksisilin",))]),
    "medicinal_product_packaged": (MedicinalProductPackagedBuilder, [("set_id", ("mpp-1",)), ("add_identifier", ("http://sys.id/ni", "NI-27",)), ("set_status", ("active",)), ("set_package_item", ("http://terminology.hl7.org/CodeSystem/package-type", "box", "Box",)), ("set_description", ("Dus 10 tablet",)), ("set_manufacturer", ("Organization/1000000001", "Kimia Farma",))]),
    "medicinal_product_pharmaceutical": (MedicinalProductPharmaceuticalBuilder, [("set_id", ("mph-1",)), ("add_identifier", ("http://sys.id/ni", "NI-28",)), ("set_status", ("active",)), ("set_route", ("http://snomed.info/sct", "26643006", "Oral",)), ("set_dose_form", ("http://snomed.info/sct", "385055001", "Tablet",)), ("set_ingredient", ("http://snomed.info/sct", "387517004", "Amoksisilin",))]),
    "medicinal_product_undesirable_effect": (MedicinalProductUndesirableEffectBuilder, [("set_id", ("mpu-1",)), ("add_identifier", ("http://sys.id/ni", "NI-29",)), ("set_status", ("active",)), ("set_subject", ("MedicinalProduct/mp-1", "Amoksisilin",)), ("set_symptom_condition_effect", ("http://snomed.info/sct", "422587007", "Nausea",)), ("set_classification", ("http://terminology.hl7.org/CodeSystem/undesirable-effect-frequency", "common", "Common",))]),
    "observation_definition": (ObservationDefinitionBuilder, [("set_id", ("od-1",)), ("add_identifier", ("http://sys.id/ni", "NI-10",)), ("set_status", ("active",)), ("set_code", ("http://loinc.org", "8867-4", "Heart rate",)), ("set_category", ("http://terminology.hl7.org/CodeSystem/observation-category", "vital-signs", "Vital Signs",)), ("set_method", ("http://snomed.info/sct", "37931006", "Auscultation",))]),
    "organization_affiliation": (OrganizationAffiliationBuilder, [("set_id", ("oa-1",)), ("add_identifier", ("http://sys.id/ni", "NI-11",)), ("set_status", ("active",)), ("set_organization", ("Organization/1000000001", "RS Sehat",)), ("set_participating_organization", ("Organization/1000000002", "Klinik Sehat",)), ("set_network", ("http://terminology.hl7.org/CodeSystem/network-type", "nt1", "Network 1",)), ("set_code", ("http://terminology.hl7.org/CodeSystem/organization-role", "provider", "Provider",))]),
    "purification_decision": (PurificationDecisionBuilder, [("set_id", ("pd-1",)), ("add_identifier", ("http://sys.id/ni", "NI-91",)), ("set_status", ("approved", "Approved", "http://terminology.hl7.org/CodeSystem/decision",)), ("set_insurer", ("Organization/1000000001", "BPJS",)), ("set_provider", ("Organization/1000000002", "RS Sehat",)), ("set_claim_response", ("ClaimResponse/cr-1", "Respons",)), ("set_created", ("2026-01-05",))]),
    "research_study": (ResearchStudyBuilder, [("set_id", ("rs-1",)), ("add_identifier", ("http://sys.id/ni", "NI-12",)), ("set_status", ("active",)), ("set_title", ("Studi Hipertensi",)), ("set_protocol", ("PlanDefinition/pd-1", "Protokol",)), ("set_sponsor", ("Organization/1000000001", "FKUI",)), ("set_phase", ("http://terminology.hl7.org/CodeSystem/research-study-phase", "phase-2", "Phase 2",))]),
    "resource_guide": (ResourceGuideBuilder, [("set_id", ("rg-1",)), ("add_identifier", ("http://sys.id/ni", "NI-92", "official", "MC", "Medical Record Number",)), ("set_status", ("active",)), ("set_name", ("Panduan",)), ("set_description", ("Panduan implementasi",)), ("set_version", ("1.0.0",)), ("set_publisher", ("Kemenkes",))]),
    "specimen_definition": (SpecimenDefinitionBuilder, [("set_id", ("sd-1",)), ("add_identifier", ("http://sys.id/ni", "NI-81",)), ("set_status", ("active",)), ("set_type", ("http://snomed.info/sct", "122555007", "Venous blood specimen",)), ("set_collection", ("Darah vena",)), ("set_preparation", ("http://terminology.hl7.org/CodeSystem/preparation", "spun", "Spun",))]),
    "substance_reference_information": (SubstanceReferenceInformationBuilder, [("set_id", ("sri-1",)), ("set_status", ("active",)), ("set_comment", ("Informasi referensi",)), ("set_gene", ("http://www.genenames.org", "HGNC:5", "A1BG",)), ("set_gene_element", ("http://snomed.info/sct", "123", "Elemen",))]),
}


@pytest.mark.parametrize("nama", list(KASUS), ids=list(KASUS))
def test_sama_dengan_golden_php(nama):
    builder_cls, langkah = KASUS[nama]
    assert jalankan(builder_cls, langkah) == golden(nama)

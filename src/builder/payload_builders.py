class BaseBuilder:

    def __init__(self, resource_type: str):

        self.resource_type = resource_type

        self.data: dict = {}


    def get_resource_type(self) -> str:

        return self.resource_type


    def to_json(self) -> dict:

        return self.data


    def set_id(self, id_val: str) -> "BaseBuilder":

        self.data["id"] = id_val

        return self


    def add_meta(self, meta: dict) -> "BaseBuilder":

        self.data["meta"] = meta

        return self


    def add_extension(self, ext: str, val) -> "BaseBuilder":

        self.data[ext] = val

        return self



class AccountBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Account')


class AllergyIntoleranceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('AllergyIntolerance')


class BundleBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Bundle')


class CarePlanBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('CarePlan')


class ChargeItemBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ChargeItem')


class ChargeItemDefinitionBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ChargeItemDefinition')


class ChargeItemResponseBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ChargeItemResponse')


class ClaimBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Claim')


class ClaimResponseBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ClaimResponse')


class ClinicalImpressionBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ClinicalImpression')


class CompositionBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Composition')


class ConditionBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Condition')


class CoverageBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Coverage')


class CoverageEligibilityRequestBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('CoverageEligibilityRequest')


class CoverageEligibilityResponseBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('CoverageEligibilityResponse')


class DeviceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Device')


class DiagnosticReportBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('DiagnosticReport')


class DocumentReferenceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('DocumentReference')


class EncounterBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Encounter')


class EpisodeOfCareBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('EpisodeOfCare')


class FamilyMemberHistoryBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('FamilyMemberHistory')


class GenomicStudyBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('GenomicStudy')


class GoalBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Goal')


class GroupBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Group')


class ImagingStudyBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ImagingStudy')


class ImmunizationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Immunization')


class InvoiceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Invoice')


class LocationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Location')


class MedicationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Medication')


class MedicationAdministrationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('MedicationAdministration')


class MedicationDispenseBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('MedicationDispense')


class MedicationRequestBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('MedicationRequest')


class MedicationStatementBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('MedicationStatement')


class MolecularSequenceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('MolecularSequence')


class NutritionOrderBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('NutritionOrder')


class ObservationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Observation')


class OrganizationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Organization')


class PatientBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Patient')


class PaymentNoticeBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('PaymentNotice')


class PaymentReconciliationBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('PaymentReconciliation')


class PractitionerBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Practitioner')


class PractitionerRoleBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('PractitionerRole')


class ProcedureBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Procedure')


class QuestionnaireResponseBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('QuestionnaireResponse')


class RelatedPersonBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('RelatedPerson')


class RiskAssessmentBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('RiskAssessment')


class ServiceRequestBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('ServiceRequest')


class SpecimenBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Specimen')


class SubstanceBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Substance')


class TaskBuilder(BaseBuilder):

    def __init__(self):

        super().__init__('Task')

# satusehat-integration

> **Open-source Python SDK for integrating with SATUSEHAT** — Indonesia's national health data platform powered by FHIR R4. Pure Python, no framework dependency.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4-orange)](https://hl7.org/fhir/R4/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://github.com/ivanwilliammd/satusehat-integration-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanwilliammd/satusehat-integration-python/actions)
[![PyPI](https://img.shields.io/pypi/v/satusehat-integration)](https://pypi.org/project/satusehat-integration)
[![PyPI](https://img.shields.io/pypi/dm/satusehat-integration)](https://pypi.org/project/satusehat-integration)

---

## Overview

`satusehat-integration` is an **open-source** Python SDK for integrating with **SATUSEHAT** — Indonesia's national health data platform powered by FHIR R4.

Built on the official [SATUSEHAT Platform Guidelines](https://satusehat.kemkes.go.id/platform/docs). Ships with:
- **115+ PayloadBuilder** classes — fluent builders for all FHIR R4 resources (Patient, Practitioner, Organization, Encounter, Observation, Procedure, etc.)
- **50 DataType** classes — composable FHIR R4 value objects with `to_json()` serialization
- **TerminologyResolver** — castable terminology strings (`"ICD10:A00"`, `"LOINC:2951-2"`, `"SNOMED:38341003"`) directly to CodeableConcept
- **3 SATUSEHAT-specific** resources: BillingStatus (NON-FHIR JSON), PurificationDecision (NON-FHIR JSON), Endpoint (FHIR R4)
- **Queue + Rate Limiter** — in-memory queue with configurable RPM rate limiting
- **pytest** test suite — all builders have comprehensive unit tests

Zero dependencies beyond standard library. Works standalone or with Django/FastAPI/Flask.

---

## Requirements

- Python 3.10 or later

---

## Quick Install

```bash
pip install satusehat-integration
# or
git clone https://github.com/ivanwilliammd/satusehat-integration.git
cd satusehat-integration && pip install -e .
```

```env
# .env
SATUSEHAT_ENV=DEV          # DEV | STG | PROD
SATUSEHAT_BASE_URL_DEV=https://api-satusehat-dev.dto.kemkes.go.id
CLIENTID_DEV=your_client_id
CLIENTSECRET_DEV=your_client_secret
ORGID_DEV=your_org_id
```

---

## Architecture

### DataType Classes (`src/datatype/`)

Atomic FHIR R4 value objects. All provide a `to_json()` method — nested types serialize to clean FHIR JSON automatically.

| Category | Classes |
|----------|---------|
| Core | `Coding`, `CodeableConcept`, `Identifier`, `ContactPoint`, `Address`, `HumanName`, `Reference` |
| Quantity | `Age`, `Quantity` |
| Utility | `Period`, `ParameterComponent` |

Example — `HumanName`:

```python
from src.datatype.datatypes import HumanName

name = HumanName(
    family='Doe',
    given=['John', 'Michael'],
    use='official'
)
# name.to_json() → {'family': 'Doe', 'given': ['John', 'Michael'], 'use': 'official'}
```

### PayloadBuilder Pattern (`src/builder/`)

Fluent builder for each FHIR resource. Each builder exposes chainable methods and returns the resource payload via `to_json()`.

```python
from src.builder.payload_builders import PatientBuilder, HumanName

patient = PatientBuilder()
patient.add_name(HumanName(family='Doe', given=['John'], use='official').to_json())
patient.set_gender('male')
patient.set_birth_date('1990-01-15')

payload = patient.to_json()
```

---

## Supported FHIR Resources

**115+ PayloadBuilder classes** covering all FHIR R4 resources used in SATUSEHAT interoperability, plus 3 SATUSEHAT-specific resources.

### SATUSEHAT Interoperability Resources (47)

| # | Resource | Builder |
|---|----------|---------|
| 1 | Account | `AccountBuilder` |
| 2 | AllergyIntolerance | `AllergyIntoleranceBuilder` |
| 3 | BillingStatus ⚡NON-FHIR | `BillingStatusBuilder` |
| 4–37 | CarePlan, Condition, Encounter, Goal, Immunization, Location, Medication*, Observation, Organization, Patient, Practitioner, Procedure, ServiceRequest, Specimen, Substance, Task, and more | see `src/builder/` |
| 38 | **Endpoint** | `EndpointBuilder` |
| 39 | **MedicationStatement** | `MedicationStatementBuilder` |
| 40 | **Task** | `TaskBuilder` |
| 41 | **PurificationDecision** ⚡NON-FHIR | `PurificationDecisionBuilder` |
| 42–47 | Claim, ClaimResponse, CoverageEligibilityRequest/Response, DocumentReference, QuestionnaireResponse | see `src/builder/` |

⚡ = NON-FHIR JSON (SATUSEHAT-specific extension)

### BillingStatus (NON-FHIR JSON)
```python
from src.builder.billing_status import BillingStatusBuilder

billing = (BillingStatusBuilder()
    .set_id('bs-001')
    .add_identifier('http://sys-ids.kemkes.go.id/billing/org-001', 'BILL-12345')
    .set_status('active')
    .set_insurer('Organization/org-bpjs', 'BPJS Kesehatan')
    .set_subject('100000030009', 'Budi Santoso')
    .set_request('cer-001')
    .build())
```

### Endpoint (FHIR R4)
```python
from src.builder.endpoint import EndpointBuilder

endpoint = (EndpointBuilder()
    .set_id('ep-001')
    .set_status('active')
    .set_connection_type('ihe-xcpd', 'IHE XCPD')
    .set_name('SATUSEHAT FHIR Endpoint')
    .set_managing_organization('Organization/org-ihs')
    .set_address('https://satusehat-api.example.com/fhir/r4')
    .build())
```

### PurificationDecision (NON-FHIR JSON)
```python
from src.builder.purification_decision import PurificationDecisionBuilder

pd = (PurificationDecisionBuilder()
    .set_id('pd-001')
    .add_identifier('http://sys-ids.kemkes.go.id/purification/org-001', 'PD-12345')
    .set_status('approved', 'Approved')
    .set_insurer('Organization/org-bpjs', 'BPJS Kesehatan')
    .set_provider('Organization/hos-001', 'Rumah Sakit Sehat')
    .set_claim_response('cr-001')
    .set_created('2024-01-15T10:35:00+00:00')
    .build())
```

### TerminologyResolver — castable codes
```python
from src.terminology.resolver import resolve, expand_array

# Cast terminology strings directly to CodeableConcept
resolve('ICD10:A00')
# → {'coding': [{'system': 'http://hl7.org/fhir/sid/icd-10', 'code': 'A00', 'display': 'A00'}], 'text': 'A00'}

resolve('LOINC:2951-2')
# → {'coding': [{'system': 'http://loinc.org', 'code': '2951-2', 'display': '2951-2'}], 'text': '2951-2'}

# Batch expand
expand_array(['ICD10:A00', 'ICD10:J18.9'])
# → [resolved_A00, resolved_J18.9]
```

---

## Usage Examples

### Patient

```python
from src.builder.payload_builders import PatientBuilder

patient = PatientBuilder()
patient.add_name({
    'family': 'Doe',
    'given': ['John'],
    'use': 'official'
})
patient.set_gender('male')
patient.set_birth_date('1990-01-15')
patient.add_telecom({'system': 'phone', 'value': '081234567890', 'use': 'mobile'})

payload = patient.to_json()
print(payload)
```

### Claim (BPJS Klaim)

```python
from src.builder.payload_builders import ClaimBuilder

claim = ClaimBuilder()
claim.set_status('active')
claim.set_use('claim')
claim.set_type('institutional')
claim.set_patient('pat-123', 'enc-456')
claim.add_item(1, 'PROCID001', 150000, 'IDR')
claim.set_total(150000, 'IDR')

payload = claim.to_json()
```

---

## Documentation

| Page | Description |
|------|-------------|
| [Wiki Home](https://github.com/ivanwilliammd/satusehat-integration.wiki.git) | Full documentation |
| [Getting Started](https://github.com/ivanwilliammd/satusehat-integration/wiki/Getting-Started) | Installation, configuration |
| [DataTypes](https://github.com/ivanwilliammd/satusehat-integration/wiki/DataTypes) | Complete type reference |
| [Builders](https://github.com/ivanwilliammd/satusehat-integration/wiki/Builders) | Builder usage guide |
| [Resources](https://github.com/ivanwilliammd/satusehat-integration/wiki/Resources) | All FHIR resources |
| [Claim Module](https://github.com/ivanwilliammd/satusehat-integration/wiki/Claim-Module) | BPJS Klaim integration |

---

## External Resources

- [HL7 FHIR R4 Specification](https://hl7.org/fhir/R4/)
- [SATUSEHAT Platform Docs](https://satusehat.kemkes.go.id/platform/docs)
- [Main PHP SDK](https://github.com/ivanwilliammd/satusehat-integration)
- [SATUSEHAT Sandbox API](https://api-satusehat-dev.dto.kemkes.go.id)

---

## Contributing

Contributions are welcome. Please ensure tests pass and follow existing code conventions.

---

## License

MIT — see [LICENSE](LICENSE).

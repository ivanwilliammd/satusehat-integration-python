# satusehat-integration

> **Open-source Python SDK for integrating with SATUSEHAT** — Indonesia's national health data platform powered by FHIR R4. Pure Python, no framework dependency.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4-orange)](https://hl7.org/fhir/R4/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![CI](https://github.com/ivanwilliammd/satusehat-integration-python/actions/workflows/ci.yml/badge.svg)](https://github.com/ivanwilliammd/satusehat-integration-python/actions)

---

## Overview

`satusehat-integration` is an **open-source** Python SDK for integrating with **SATUSEHAT** — Indonesia's national health data platform powered by FHIR R4.

Built on the official [SATUSEHAT Platform Guidelines](https://satusehat.kemkes.go.id/platform/docs). Ships with:
- **50 DataType** classes — composable FHIR R4 value objects with `to_json()` serialization
- **50 PayloadBuilder** classes — fluent builders for all FHIR resources (Patient, Practitioner, Organization, etc.)
- **Queue + Rate Limiter** — in-memory queue with configurable RPM rate limiting

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

All 51 resources fully implemented via PayloadBuilder classes. Core (✅) + Non-Core (💼):

| # | Resource | Notes |
|---|----------|-------|
| 1 | Patient | ✅ MPI |
| 2 | Practitioner | ✅ SDMK |
| 3 | PractitionerRole | ✅ |
| 4 | Organization | ✅ MSI |
| 5 | Location | ✅ |
| 6 | Encounter | ✅ |
| 7 | Condition | ✅ |
| 8 | Observation | ✅ |
| 9 | Procedure | ✅ |
| 10 | MedicationRequest | ✅ |
| 11 | Bundle | ✅ batch/transaction |
| 12–37 | CarePlan through Task | ✅ |
| 38–50 | Account through Invoice | 💼 Billing/Claim resources |

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

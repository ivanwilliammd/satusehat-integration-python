# satusehat-integration

> **Open-source Python SDK for integrating with SATUSEHAT** — Indonesia's national health data platform powered by FHIR R4. Pure Python, no framework dependency.

[![PyPI](https://img.shields.io/pypi/v/satusehat-integration?label=pypi)](https://pypi.org/project/satusehat-integration/)
[![downloads](https://img.shields.io/pypi/dm/satusehat-integration)](https://pypi.org/project/satusehat-integration/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://pypi.org/project/satusehat-integration/)
[![FHIR R4](https://img.shields.io/badge/FHIR-R4-orange)](https://hl7.org/fhir/R4/)

## Status and coverage (measured, not claimed)

| Area | Count | Evidence |
| --- | --- | --- |
| Builder | 141 resources | `satusehat_integration/builder` |
| Builder methods | 1,405 | `satusehat_integration/builder/test_method_name_parity.py` (contract `contracts/php_method_surface.json`) |
| Parser | 141 resources (one per builder) | `satusehat_integration/parser`, `satusehat_integration/parser/test_parser_surface.py` |
| R5 namespace | 144 builder modules | `satusehat_integration/r5/builder`, `satusehat_integration/r5/test_r5_namespace.py` |
| Tests | 2,080 | `python -m pytest` |

R4 stays the reference; R5 means changing one import:

```python
from satusehat_integration.builder.basic import BasicBuilder      # R4
from satusehat_integration.r5.builder.basic import BasicBuilder   # R5 — this line only
```

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
- **140 PayloadBuilder** classes — fluent builders for all FHIR R4 resources (Patient, Practitioner, Organization, Encounter, Observation, Procedure, etc.)
- **50 DataType** classes — composable FHIR R4 value objects with `to_json()` serialization
- **`OAuth2Client` & `SSRequest`** — full SATUSEHAT OAuth2 authentication (`DEV`, `STG`, `PROD`), FHIR R4 HTTP client (`GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `patch_fhir_path`, `post_bundle`) with automatic 401 token refresh and 429/5xx exponential backoff
- **`SSResponse`, `BundleResponse` & `SSValidationError`** — response wrappers and complete 558-rule SATUSEHAT validation error dictionary (`RuleNumber` 10003–20021)
- **142 FHIR Resource Parsers** — `PatientParser`, `EncounterParser`, `ObservationParser`, `DiagnosticReportParser`, `PractitionerParser`, `ProcedureParser`, `ServiceRequestParser`, `SpecimenParser`, `TaskParser`, and more
- **SQLite Queue + Worker + Monitor** — full 8-module persistent SQLite queue (`SqliteQueue`, `Worker`, `QueueMonitor`, `RateLimiter`, `ErrorClassifier`, `QueueResult`, `QueueException`, `QueueInterface`) with DLQ and retry scheduling
- **`TerminologyClient` & `TerminologyResolver`** — SmarTerm HTTP client + castable terminology strings (`"ICD10:A00"`, `"LOINC:2951-2"`, `"SNOMED:38341003"`) directly to CodeableConcept
- **3 SATUSEHAT-specific** resources: BillingStatus (NON-FHIR JSON), PurificationDecision (NON-FHIR JSON), Endpoint (FHIR R4)
- **pytest** test suite — 92 unit tests covering builders, datatypes, HTTP transport, validation rules, parsers, queue, and terminology

Works standalone or with Django/FastAPI/Flask.

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

### DataType Classes (`satusehat_integration/datatype/`)

Atomic FHIR R4 value objects. All provide a `to_json()` method — nested types serialize to clean FHIR JSON automatically.

| Category | Classes |
|----------|---------|
| Core | `Coding`, `CodeableConcept`, `Identifier`, `ContactPoint`, `Address`, `HumanName`, `Reference` |
| Quantity | `Age`, `Quantity` |
| Utility | `Period`, `ParameterComponent` |

Example — `HumanName`:

```python
from satusehat_integration.datatype.datatypes import HumanName

name = HumanName(
    family='Doe',
    given=['John', 'Michael'],
    use='official'
)
# name.to_json() → {'family': 'Doe', 'given': ['John', 'Michael'], 'use': 'official'}
```

### PayloadBuilder Pattern (`satusehat_integration/builder/`)

Fluent builder for each FHIR resource. Each builder exposes chainable methods and returns the resource payload via `to_json()`.

```python
from satusehat_integration.builder.payload_builders import PatientBuilder, HumanName

patient = PatientBuilder()
patient.add_name(HumanName(family='Doe', given=['John'], use='official').to_json())
patient.set_gender('male')
patient.set_birth_date('1990-01-15')

payload = patient.to_json()
```

### HTTP Client & Response Handling (`satusehat_integration/ssrequest/`, `satusehat_integration/ssresponse/`)

```python
from satusehat_integration.ssrequest import OAuth2Client, SSRequest
from satusehat_integration.ssresponse import BundleResponse, SSValidationError

oauth = OAuth2Client(satusehat_env="DEV")
req = SSRequest(oauth2=oauth)

res = req.post("Observation", observation_payload)
if res.is_success():
    print("Created resource ID:", res.get_resource_id())
else:
    validator = SSValidationError.from_response(res)
    print(validator.get_summary())
```

### Resource Parsers (`satusehat_integration/parser/`)

```python
from satusehat_integration.parser import EncounterParser, ObservationParser

enc = EncounterParser(encounter_json)
print(enc.get_subject_reference(), enc.get_location_references())
```

### SQLite Queue & Worker (`satusehat_integration/queue/`)

```python
from satusehat_integration.queue import SqliteQueue, Worker, QueueMonitor

queue = SqliteQueue("satusehat_queue.db")
queue.enqueue("POST", "Encounter", "Encounter", encounter_payload)

worker = Worker(queue, {
    "base_url": oauth.base_url,
    "fhir_url": oauth.fhir_url,
    "client_id": oauth.client_id,
    "client_secret": oauth.client_secret,
})
stats = worker.process(limit=50)
monitor = QueueMonitor(queue)
print(monitor.health_check())
```

---

## Supported FHIR Resources

**140 PayloadBuilder classes** covering all FHIR R4 resources used in SATUSEHAT interoperability, plus 3 SATUSEHAT-specific resources.

### SATUSEHAT Interoperability Resources (47)

| # | Resource | Builder |
|---|----------|---------|
| 1 | Account | `AccountBuilder` |
| 2 | AllergyIntolerance | `AllergyIntoleranceBuilder` |
| 3 | BillingStatus ⚡NON-FHIR | `BillingStatusBuilder` |
| 4–37 | CarePlan, Condition, Encounter, Goal, Immunization, Location, Medication*, Observation, Organization, Patient, Practitioner, Procedure, ServiceRequest, Specimen, Substance, Task, and more | see `satusehat_integration/builder/` |
| 38 | **Endpoint** | `EndpointBuilder` |
| 39 | **MedicationStatement** | `MedicationStatementBuilder` |
| 40 | **Task** | `TaskBuilder` |
| 41 | **PurificationDecision** ⚡NON-FHIR | `PurificationDecisionBuilder` |
| 42–47 | Claim, ClaimResponse, CoverageEligibilityRequest/Response, DocumentReference, QuestionnaireResponse | see `satusehat_integration/builder/` |

⚡ = NON-FHIR JSON (SATUSEHAT-specific extension)

### BillingStatus (NON-FHIR JSON)
```python
from satusehat_integration.builder.billing_status import BillingStatusBuilder

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
from satusehat_integration.builder.endpoint import EndpointBuilder

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
from satusehat_integration.builder.purification_decision import PurificationDecisionBuilder

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
from satusehat_integration.terminology.resolver import resolve, expand_array

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

### TerminologyClient — HTTP client SmarTerm (terminology.ivanmd.id)

`TerminologyClient` is a standalone HTTP client for **SmarTerm**, separate from the SATUSEHAT
ecosystem — do not reuse the Kemkes SATUSEHAT OAuth. SmarTerm has its own authentication, in two
modes:

1. **Sanctum PAT** (static token) sent as a `Bearer` header. Environment: `TERMINOLOGY_API_TOKEN`.
2. **OIDC client_credentials** against `auth.ivanmd.id` (Passport) — the JWT is fetched lazily, cached
   until expiry, and refreshed once on a `401`. Environment: `TERMINOLOGY_CLIENT_ID`,
   `TERMINOLOGY_CLIENT_SECRET`, `TERMINOLOGY_TOKEN_URL`
   (default `https://auth.ivanmd.id/oauth/token`).

When both are supplied, PAT wins. Other environment variables: `TERMINOLOGY_BASE_URL`
(default `https://terminology.ivanmd.id`).

```python
from satusehat_integration.terminology import TerminologyClient

term = TerminologyClient()  # baca env, atau: TerminologyClient(token='pat-xxx')

# Fluent chaining
term.query('pemasangan kateter').on('kptl').limit(10).get()
term.query('demam').category('diagnosis').first()
term.query('paracetamol').on('kfa').all()

# as_code() → POST validate; the system is inferred from the shape of the code
term.query('93004944').as_code().get()   # 93xxxx → system 'kfa'
term.query('J18.9').as_code().get()      # ICD-10

# Pencarian & mapping
term.search('demam', category='all', limit=20)          # unified search
term.search_system('icd10', 'demam', limit=20)          # per-sistem
term.kptl_combine('9.10.1', ['9.11.1', '9.11.2'])       # modifier join koma
term.map('icd10', 'snomed', 'J18.9')                    # cross-mapping
term.validate('icd10', 'J18.9')
term.auto_map('icd10', 'J18.9')                         # → SNOMED

# Context-aware FHIR resolution (body otomatis buang field None)
term.resolve_condition('J18.9')
term.resolve_chief_complaint('demam')
term.resolve_observation('2951-2', system_hint='loinc')
term.resolve_medication('93004944')
term.resolve_service_request('LAB001', category='lab')

# Value sets
term.value_sets()
term.value_set('kfa')
```

HTTP status `>= 400` melempar `RuntimeError("TerminologyClient HTTP {status}: …")`;
network error melempar `RuntimeError("TerminologyClient network error: …")`.

---

## Usage Examples

### Patient

```python
from satusehat_integration.builder.payload_builders import PatientBuilder

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
from satusehat_integration.builder.payload_builders import ClaimBuilder

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

## HL7 v2 and MLLP

SATUSEHAT speaks FHIR R4; analyzers and LIS speak HL7 v2 over MLLP. Both ship in this package, so one
install covers the whole path from instrument to national platform.

```python
from satusehat_integration.hl7v2 import Ack, Client, Message, Profiles

msg = Message.parse(er7)          # CR, LF or CRLF; encoding characters read from MSH-2
msg.message_type()                # "ADT"
msg.get("PID.5.1")                # family name, escapes decoded
msg.set("PID.8", "F")             # re-escaped on write
str(msg)                          # ER7, CR-terminated, byte-for-byte round trip
```

```python
result = Client("10.0.0.21:2575").send(msg)
result.accepted      # MSA-1 == "AA"
result.control_id    # MSA-2, verified against MSH-10

results = Client("10.0.0.21:2575").session(messages)   # one socket, one result each
```

Rules that are enforced rather than documented:

- **Transport failures retry, verdicts do not.** `AE`/`AR` is returned to the caller; retrying an
  application rejection turns one bad message into a thousand.
- **MSA-2 must echo MSH-10.** A reply with a different control id is stale or misrouted and raises.
- **Frames carry over.** `MllpReader` keeps bytes that arrive after a complete frame, because one
  `recv()` often returns two or three ACKs — a stateless reader would return the first and lose the rest.

Validation is data:

```python
from satusehat_integration.hl7v2 import PROFILES, Message

issues = PROFILES["oruR01"]().validate(Message.parse(er7))   # also adtA01, adtA08
errors = [i for i in issues if i.severity == "error"]        # warnings do not block
```

The test corpus lives in `satusehat_integration/hl7v2/fixtures/` and is **copied byte-for-byte from the
PHP SDK**: ten messages a hospital actually sends and ten that must be refused. Porting the corpus
rather than rewriting the tests is what makes "same behaviour in five languages" measurable.

Not implemented yet, and not claimed: batches (FHS/BHS), vendor-specific profiles beyond the three
built in, HL7 v2 table validation, and a supervised MLLP server daemon.

## CDA R2 documents

HL7 CDA R2 is the document format that travels alongside HL7 v2 messages: v2 carries the
transaction, CDA carries the signed document. This SDK reads and writes the part that is actually
used — the header and the sections with narrative text — and leaves everything else alone.

```python
from satusehat_integration.cda import Document

doc = Document.parse(xml)                  # refuses anything whose root is not ClinicalDocument
doc.title()                                # "Resume Medis Rawat Inap"
doc.patient().identifier("2.16.840.1.113883.3.3157.1003.1")   # NIK
doc.patient().name()
doc.authors()                              # ["Ivan HARSONO"]
doc.section("10164-2").title               # section by LOINC, searched depth-first
doc.section_text("10164-2")                # narrative flattened to text, paragraphs kept
doc.validate()                             # [] means exchangeable, not clinically correct
```

```python
from satusehat_integration.cda import Document

doc = Document.build({
    "id": "DOC-1",
    "title": "Resume Medis",
    "custodian": "RS Contoh",
    "author": "Dokter Contoh",
    "patientId": "3171234567890001",
    "patientName": "ANGGRAENI",
    "gender": "F",
    "birthTime": "19850312",
    "sections": [{"loinc": "10164-2", "title": "Riwayat", "text": "<paragraph>Demam.</paragraph>"}],
})
print(doc.to_xml())
```

Two decisions worth stating:

- **Unknown structure survives a round trip.** Parsing keeps the `ElementTree` and `to_xml()` writes
  it back, so `componentOf/encompassingEncounter`, `participant`, `legalAuthenticator` and vendor
  extensions are preserved even though the SDK does not model them. A parser that rebuilds the
  document from its own model quietly deletes everything it did not understand.
- **Identifiers keep their `root`.** A NIK without its assigning-authority root cannot be matched
  against anything, and dropping the root is how a local MRN silently becomes a national NIK.

No new dependency: `xml.etree.ElementTree` is the standard library. It does not resolve external
entities, so a hostile document cannot pull in a local file through the parser. The HL7 CDA R2
schemas are licensed; the classes implement the structural rules from the specification and do not
redistribute them.

Not implemented: signature verification (`ds:Signature`), templates beyond the generic
`POCD_MT000040` header, `nonXMLBody` attachments, CDA → FHIR mapping.

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

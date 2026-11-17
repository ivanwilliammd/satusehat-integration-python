# SRD — satusehat-integration (SATUSEHAT FHIR R4 SDK · Python)

Status: v2.1 · 2026-11-17 · Companions: `docs/PRD-SDK-ECOSYSTEM.md` (PHP repository) + `README.md`
Installed package version: **4.19.0** (`pyproject.toml`).

Every number here is **measured** from this checkout; canonical counts come from
`scripts/parity-manifest.sh` in the PHP repository, which applies the same de-duplication rule to all
five ports. When code changes, update this document in the same commit.

## 1. Scope

How the SDK works internally: layers, public contract, capability parity with the PHP SDK, error
mapping, compatibility rules, and test state. SATUSEHAT usage belongs in `README.md`.

## 2. Architecture principles

1. **Parity from construction to delivery.**
   - `src/builder` and `src/datatype` build FHIR R4 payloads purely, with no network access.
   - `src/ssrequest` (`OAuth2Client`, `SSRequest`) handles SATUSEHAT OAuth2 (`DEV`/`STG`/`PROD`), HTTP
     transport, automatic token refresh on `401`, and exponential backoff with `Retry-After` on
     `429`/`5xx`.
   - `src/ssresponse` (`SSResponse`, `BundleResponse`, `SSValidationError`) wraps HTTP responses and
     maps all **558 SATUSEHAT validation rules** (`RuleNumber`) plus 14 response categories.
   - `src/parser` provides one parser per FHIR resource.
   - `src/queue` provides SQLite-backed asynchronous delivery: `SqliteQueue`, `Worker`, `QueueMonitor`,
     `RateLimiter`, `ErrorClassifier`, `QueueInterface`, `QueueResult`, `QueueException`.
   - `src/terminology` provides `TerminologyClient` and `TerminologyResolver` for SmarTerm.
   - `src/conformance` provides `unknown_elements` / `assert_r4_elements` (opt-in strict R4 guard).
2. **A pip package, not a script.** `src/` is installed through `pyproject.toml`; tests run with
   `python -m pytest src`.
3. **Secrets come from the environment or arguments only.** SATUSEHAT and SmarTerm credentials are read
   from environment variables or constructor arguments.
4. **Pythonic names, cross-SDK aliases.** Methods expose `snake_case` and also accept `camelCase`
   aliases so a reader coming from the PHP/Node SDKs can keep their habits.
5. **Rules are data.** `required-rules.json` is compiled into `_rules_generated.py` and pinned by
   `RULES_SHA`, because setuptools does not ship JSON data files reliably.

## 3. Measured inventory

| Item | Count | Measurement |
|---|---|---|
| Payload builders | 141 | `scripts/parity-manifest.sh` |
| Datatypes | 33 | `scripts/parity-manifest.sh` |
| FHIR parsers | 141 | `scripts/parity-manifest.sh` |
| R5 builder modules | 144 | `ls src/r5/builder/*.py \| wc -l` |
| Queue modules | 8 | `ls src/queue/*.py \| grep -v test_ \| wc -l` |
| Terminology modules | 23 | `scripts/parity-manifest.sh` |
| Test files | 218 | `find src -name "test_*.py" \| wc -l` |
| Test cases | 2.219 passing, 1 skipped | `python -m pytest -q` |

## 4. Capability parity with the PHP SDK

| Capability | PHP | Python | Evidence |
|---|---|---|---|
| Payload builders | 141 | 141 | `src/builder` |
| Datatypes | 33 | 33 | `src/datatype` |
| FHIR parsers | 142 | 141 | `src/parser` |
| R5 namespace | 142 | 144 | `src/r5/builder` |
| Queue modules | 8 | 8 | `src/queue` |
| Terminology modules | 23 | 23 | `src/terminology` |
| SATUSEHAT required rules | yes | yes | `_rules_generated.py` + `RULES_SHA` |
| Non-standard SATUSEHAT objects | yes | yes | `src/terminology/satusehat_nonstandard.py` |
| R4 element guard (opt-in) | yes | yes | `src/conformance/r4_element_guard.py` |

The one-parser difference is naming: PHP calls the `List` resource parser `ListParser`, Python calls it
`ListResourceParser`. Resource coverage is identical.

## 5. Public contract

- Package entry point: `src/__init__.py` re-exports builder, datatype, terminology, transport, parser,
  queue, and conformance modules.
- `pyproject.toml` declares `satusehat-integration` with `requires-python = ">=3.10"` and two runtime
  dependencies (`requests`, `pydantic`).
- Tests: `python -m pytest src`.

## 6. Error mapping

- **`SSRequest`**
  - **401** → when `oauth2.is_token_auto_refresh()` is enabled, call `refresh_token()` and retry with
    exponential backoff (`2^n` seconds, capped at 60) up to `max_retries` (default 5).
  - **429** → honour `Retry-After`, otherwise `2^n` seconds, up to `max_retries`.
  - **5xx** → exponential backoff up to `max_retries`.
  - Network failures return `SSResponse(0, OperationOutcome, message)` instead of raising into the
    caller.
- **`TerminologyClient`**
  - Default `timeout` is **30 seconds**.
  - `requests.RequestException` → `RuntimeError("TerminologyClient network error: …")`.
  - **401** → when no PAT is set and OIDC credentials exist, retry once with a fresh token.
  - **>= 400** → `RuntimeError("TerminologyClient HTTP <status>: …")`.

## 7. Compatibility rules

- Python 3.10+; no framework dependency.
- `snake_case` is canonical; `camelCase` aliases are kept for compatibility and may be removed only in a
  major release.
- Adding a builder, parser, or queue module is a minor change; changing an exported signature is not.

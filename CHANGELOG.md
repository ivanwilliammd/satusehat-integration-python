# Changelog

## Unreleased

### Added

- **HL7 v2 + MLLP**: `satusehat_integration.hl7v2` — `Message`/`Segment` (ER7 parse, path access,
  escape decode/encode, byte-for-byte round trip), `Mllp` framing with a stateful `MllpReader`, `Ack`
  (AA/AE/AR with MSA-2 echo), `Client` with `send()` and `session()` (one socket, one result per
  message), and declarative `Profile`s (`adt_a01()`, `adt_a08()`, `oru_r01()`).
- **Shared corpus**: the 20 fixtures are copied byte-for-byte from the PHP SDK, so behaviour parity is
  tested with the same messages instead of being re-described in prose.

## v4.19.1 — 2026-11-17

### Fixed

- **The published wheel could not be imported.** `pip install satusehat-integration` installed top-level
  modules named `builder`, `parser`, `ssrequest`, … because `src/` was treated as the package root, so
  `import satusehat_integration` raised `ModuleNotFoundError`. The directory is now
  `satusehat_integration/`, the imports inside the package follow, and a clean virtualenv can import and
  build a Patient from the wheel.
- Test and generator scripts that resolved `src/…` paths follow the new directory name.

### Changed

- Test count corrected in `docs/SRD.md`: 2,080 passing + 2 skipped (previously stated as 2,219 + 1).

## v4.19.0 - 2026-11-17

### Added

- `terminology.satusehat_rules`: SATUSEHAT required rules are executed from data
  (8 resources / 26 rules). The rules file is compiled into `_rules_generated.py` by
  `scripts/generate_rules.py` and pinned by `RULES_SHA`, because setuptools does not ship JSON
  data files reliably.
- Rules fingerprint test: byte count plus per-resource rule counts, computed after CRLF
  normalisation so Windows and Linux agree.

### Fixed

- `test_script.py` is a builder, not a test file; the test marker is the content (`def test_`),
  not the file name.

### Tests

- 2.207 passed, 1 skipped.

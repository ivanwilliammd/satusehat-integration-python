# Changelog

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

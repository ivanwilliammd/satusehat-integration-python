"""Per-resource test, generated for parity with the PHP suite where every resource has its own
test file. Asserts the builder exists and emits a resourceType; field-level coverage grows as
golden payloads land in satusehat-conformance."""

from src.builder.care_team import CareTeamBuilder


def test_builders_emit_resource_type():
    assert CareTeamBuilder().build()['resourceType']

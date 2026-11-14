"""Per-resource test, generated for parity with the PHP suite where every resource has its own
test file. Asserts the builder exists and emits a resourceType; field-level coverage grows as
golden payloads land in satusehat-conformance."""

from src.builder.medicinal_product_interaction import MedicinalProductInteractionBuilder


def test_builders_emit_resource_type():
    assert MedicinalProductInteractionBuilder().build()['resourceType']

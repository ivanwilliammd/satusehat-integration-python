"""Uji penjaga elemen R4."""
import pytest

from satusehat_integration.conformance.r4_element_guard import (
    assert_r4_elements,
    strict_r4_enabled,
    unknown_elements,
)


def test_payload_sah_tidak_menghasilkan_temuan():
    assert unknown_elements({"resourceType": "Patient", "identifier": [], "gender": "male"}) == []


def test_elemen_bukan_r4_ditangkap():
    # onsetDateTime milik Condition/Observation, bukan Goal.
    assert unknown_elements({"resourceType": "Goal", "onsetDateTime": "2026-01-01"}) == [
        "onsetDateTime"
    ]


def test_alias_list_resource():
    assert unknown_elements({"resourceType": "ListResource", "entry": []}) == []


def test_resource_di_luar_r4_tidak_diperiksa():
    assert unknown_elements({"resourceType": "BillingStatus", "apa": 1}) == []


def test_assert_melempar_dengan_nama_resource():
    with pytest.raises(ValueError, match="Goal menulis elemen yang tidak ada di FHIR R4: onsetDateTime"):
        assert_r4_elements({"resourceType": "Goal", "onsetDateTime": "x"})


def test_tanpa_resource_type_ditolak():
    assert unknown_elements({"nama": "x"}) == ["resourceType"]


def test_strict_bisa_dimatikan(monkeypatch):
    monkeypatch.setenv("SATUSEHAT_STRICT_R4", "0")
    assert strict_r4_enabled() is False
    monkeypatch.setenv("SATUSEHAT_STRICT_R4", "1")
    assert strict_r4_enabled() is True

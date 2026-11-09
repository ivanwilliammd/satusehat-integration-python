"""Unit tests for SSResponse, BundleResponse, and SSValidationError."""
from __future__ import annotations

from src.ssresponse import BundleResponse, SSResponse, SSValidationError


def test_ss_response_success_and_error():
    res = SSResponse(201, {"resourceType": "Patient", "id": "P-999"}, '{"resourceType":"Patient","id":"P-999"}')
    assert res.get_http_code() == 201
    assert res.getHttpCode() == 201
    assert res.is_success() is True
    assert res.isError() is False
    assert res.get_resource_id() == "P-999"
    assert res.get("Patient") == "P-999"

    err_body = {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "error",
                "code": "invalid",
                "details": {"text": "RuleNumber: 10003 - Invalid Condition.code"},
                "expression": ["Condition.code"],
            }
        ],
    }
    err_res = SSResponse(422, err_body, "{}")
    assert err_res.is_error() is True
    assert err_res.get_error_messages() == ["RuleNumber: 10003 - Invalid Condition.code"]


def test_bundle_response_methods():
    request_entries = [
        {"fullUrl": "urn:uuid:enc-1", "method": "POST", "url": "Encounter"},
        {"fullUrl": "urn:uuid:obs-1", "method": "PUT", "url": "Observation/obs-123"},
        {"fullUrl": "urn:uuid:pat-1", "method": "GET", "url": "Patient/P001"},
    ]
    bundle_body = {
        "resourceType": "Bundle",
        "type": "transaction-response",
        "total": 3,
        "entry": [
            {
                "fullUrl": "urn:uuid:enc-1",
                "response": {
                    "status": "201 Created",
                    "location": "https://api-satusehat.kemkes.go.id/fhir-r4/v1/Encounter/enc-server-1/_history/1",
                    "etag": 'W/"1"',
                },
            },
            {
                "fullUrl": "urn:uuid:obs-1",
                "response": {
                    "status": "422 Unprocessable Entity",
                    "outcome": {
                        "resourceType": "OperationOutcome",
                        "issue": [{"diagnostics": "Invalid valueQuantity"}],
                    },
                },
            },
            {
                "fullUrl": "urn:uuid:pat-1",
                "resource": {"resourceType": "Patient", "id": "P001"},
                "response": {"status": "200 OK", "location": "Patient/P001"},
            },
        ],
    }

    br = BundleResponse(200, bundle_body, request_entries)
    assert br.is_success() is True
    assert br.get_total() == 3
    assert len(br.get_entries()) == 3
    assert len(br.get_success_entries()) == 2
    assert len(br.get_failed_entries()) == 1
    assert br.is_all_success() is False
    assert br.get_entry_errors(1) == ["Invalid valueQuantity"]

    created = br.created()
    assert len(created) == 1
    assert created[0]["resourceId"] == "1" or created[0]["location"].endswith("_history/1")

    read_items = br.read()
    assert len(read_items) == 1
    assert read_items[0]["resource"]["id"] == "P001"

    found = br.find("Observation", "obs-123")
    assert found is not None
    assert found["statusCode"] == 422


def test_ss_validation_error_full_558_rules():
    rule_nums = SSValidationError.get_available_rule_numbers()
    assert len(rule_nums) == 558
    assert 10003 in rule_nums
    assert 20021 in rule_nums

    cond_rules = SSValidationError.get_rules_for_resource("Condition")
    assert 10003 in cond_rules

    loinc_rules = SSValidationError.search_rules("loinc")
    assert len(loinc_rules) > 0

    dup_type = SSValidationError.get_response_type("duplicate")
    assert dup_type is not None
    assert dup_type["title"] == "Found duplicate resource"

    outcome = {
        "resourceType": "OperationOutcome",
        "issue": [
            {
                "severity": "error",
                "code": "invalid",
                "details": {"text": "RuleNumber: 10003 Invalid date time format Duplicate"},
                "expression": ["Condition.code"],
            }
        ],
    }
    val = SSValidationError.from_response(outcome)
    assert val.get_rule_numbers() == [10003]
    assert val.get_rule_info(10003)["path"] == "Condition.code"
    assert val.is_duplicate() is True
    assert val.is_date_time_error() is True
    assert val.get_affected_paths() == ["Condition.code"]
    parsed = val.get_parsed_issues()
    assert len(parsed) == 1
    assert parsed[0]["rule_number"] == 10003
    assert "[10003] Condition.code =>" in val.get_summary()

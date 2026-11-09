"""Unit tests for OAuth2Client and SSRequest."""
from __future__ import annotations

import json
import pytest

from src.ssrequest import OAuth2Client, OAuth2ClientException, SSRequest


class MockResponse:
    def __init__(self, status_code: int, body: dict | None = None, headers: dict | None = None, text: str | None = None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}
        if text is not None:
            self.text = text
        elif body is not None:
            self.text = json.dumps(body)
        else:
            self.text = ""

    def json(self):
        if self._body is None:
            raise ValueError("No JSON")
        return self._body


class SequenceSession:
    def __init__(self, responses: list[MockResponse]):
        self.responses = list(responses)
        self.calls: list[dict] = []

    def request(self, method, url, headers=None, data=None, timeout=None, verify=None):
        self.calls.append({"method": method, "url": url, "headers": headers or {}, "data": data})
        return self.responses.pop(0)

    def post(self, url, data=None, headers=None, timeout=None):
        self.calls.append({"method": "POST", "url": url, "headers": headers or {}, "data": data})
        return self.responses.pop(0)

    def get(self, url, headers=None, timeout=None):
        self.calls.append({"method": "GET", "url": url, "headers": headers or {}})
        return self.responses.pop(0)

    def put(self, url, data=None, headers=None, timeout=None):
        self.calls.append({"method": "PUT", "url": url, "headers": headers or {}, "data": data})
        return self.responses.pop(0)


def test_oauth2_client_env_validation(monkeypatch):
    monkeypatch.delenv("SATUSEHAT_ENV", raising=False)
    with pytest.raises(OAuth2ClientException, match="SATUSEHAT environment is missing"):
        OAuth2Client()

    with pytest.raises(OAuth2ClientException, match="SATUSEHAT environment invalid"):
        OAuth2Client(satusehat_env="INVALID")

    with pytest.raises(OAuth2ClientException, match="CLIENTID_DEV"):
        OAuth2Client(satusehat_env="DEV")


def test_oauth2_client_token_and_methods():
    sess = SequenceSession([
        MockResponse(200, {"access_token": "tok-123"}),
        MockResponse(200, {"resourceType": "Patient", "id": "P001"}),
        MockResponse(200, {"resourceType": "Bundle", "total": 1, "entry": [{"resource": {"id": "PR001"}}]}),
        MockResponse(200, {"total": 2, "items": []}),
        MockResponse(201, {"resourceType": "Observation", "id": "OBS-1"}),
        MockResponse(200, {"resourceType": "Observation", "id": "OBS-1"}),
        MockResponse(200, {"access_token": "tok-456"}),
    ])
    client = OAuth2Client(
        satusehat_env="DEV",
        client_id="cid",
        client_secret="csec",
        organization_id="org-1",
        session=sess,
    )
    assert client.fhir_url == "https://api-satusehat-dev.dto.kemkes.go.id/fhir-r4/v1"
    assert client.token() == "tok-123"
    # Second call uses cached token
    assert client.token() == "tok-123"

    code, pat = client.get_by_id("Patient", "P001")
    assert code == 200
    assert pat["id"] == "P001"

    code, prac = client.get_by_nik("Practitioner", "1234567890123456")
    assert code == 200
    assert prac["entry"][0]["resource"]["id"] == "PR001"

    code, kfa = client.ss_kfa_get("products/all?", "page=1&size=10")
    assert code == 200
    assert kfa["total"] == 2

    code, obs = client.ss_post("Observation", {"resourceType": "Observation"})
    assert code == 201
    assert obs["id"] == "OBS-1"

    code, obs_put = client.ss_put("Observation", "OBS-1", {"resourceType": "Observation", "id": "OBS-1"})
    assert code == 200

    # Refresh token forces a new POST
    assert client.refreshToken() == "tok-456"


def test_ssrequest_crud_and_patch():
    sess = SequenceSession([
        MockResponse(200, {"resourceType": "Bundle", "total": 1, "entry": [{"resource": {"id": "P100"}}]}),
        MockResponse(201, {"resourceType": "Encounter", "id": "ENC-1"}),
        MockResponse(200, {"resourceType": "Encounter", "id": "ENC-1"}),
        MockResponse(200, {"resourceType": "Encounter", "id": "ENC-1"}),
        MockResponse(200, {"resourceType": "Parameters"}),
        MockResponse(204, {}),
    ])
    req = SSRequest(token="static-token", base_url="https://fhir.test/fhir-r4/v1", session=sess)

    r_get = req.get("Patient", {"identifier": "nik|123"})
    assert r_get.is_success()
    assert r_get.get_resource_id() == "P100"
    assert "identifier=nik%7C123" in sess.calls[0]["url"]

    r_post = req.post("Encounter", {"resourceType": "Encounter"})
    assert r_post.getHttpCode() == 201
    assert r_post.getResourceId() == "ENC-1"

    r_put = req.put("Encounter/ENC-1", {"resourceType": "Encounter", "id": "ENC-1"})
    assert r_put.isSuccess()

    r_patch = req.patch("Encounter/ENC-1", [{"op": "replace", "path": "/status", "value": "finished"}])
    assert r_patch.is_success()
    assert sess.calls[3]["headers"]["Content-Type"] == "application/json-patch+json"

    r_fhir_patch = req.patchFhirPath("Encounter/ENC-1", {"resourceType": "Parameters"})
    assert r_fhir_patch.is_success()
    assert sess.calls[4]["headers"]["Content-Type"] == "application/fhir+json"

    r_del = req.delete("Encounter/ENC-1")
    assert r_del.get_http_code() == 204


def test_ssrequest_retry_429_500_and_401_refresh():
    sleeps: list[float] = []
    oauth_sess = SequenceSession([
        MockResponse(200, {"access_token": "tok-initial"}),
        MockResponse(200, {"access_token": "tok-refreshed"}),
    ])
    oauth = OAuth2Client(
        satusehat_env="DEV",
        client_id="cid",
        client_secret="csec",
        organization_id="org-1",
        session=oauth_sess,
    )

    api_sess = SequenceSession([
        MockResponse(429, {"resourceType": "OperationOutcome"}, headers={"Retry-After": "3"}),
        MockResponse(503, {"resourceType": "OperationOutcome"}),
        MockResponse(401, {"resourceType": "OperationOutcome"}),
        MockResponse(200, {"resourceType": "Patient", "id": "P-OK"}),
    ])
    req = SSRequest(oauth2=oauth, session=api_sess, sleep_fn=lambda s: sleeps.append(s))
    res = req.get("Patient/P-OK")
    assert res.is_success()
    assert res.get_resource_id() == "P-OK"
    assert sleeps == [3, 4, 8]
    assert api_sess.calls[-1]["headers"]["Authorization"] == "Bearer tok-refreshed"

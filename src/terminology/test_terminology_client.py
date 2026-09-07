"""Tests untuk TerminologyClient + TerminologyQueryBuilder (mock requests)."""
import pytest

from src.terminology.terminology_client import TerminologyClient


class FakeResponse:
    def __init__(self, status_code, payload, json_ok=True):
        self.status_code = status_code
        self._payload = payload
        self._json_ok = json_ok
        self.text = "mock"

    def json(self):
        if not self._json_ok:
            raise ValueError("no json")
        return self._payload


class RecordingSession:
    """Mirror requests.Session surface; record calls."""

    def __init__(self, status=200, payload=None):
        self.status = status
        self.payload = payload
        self.calls = []
        self.headers = {}

    def request(self, method, url, params=None, json=None, headers=None, timeout=None):
        self.calls.append({"method": method, "url": url, "params": params, "json": json, "headers": headers})
        return FakeResponse(self.status, self.payload)

    def post(self, url, data=None, timeout=None):
        self.calls.append({"method": "POST", "url": url, "data": data})
        return FakeResponse(200, {"access_token": "jwt"})


@pytest.fixture
def client(monkeypatch):
    c = TerminologyClient(base_url="https://term.test", token="pat-1")
    session = RecordingSession(200, {"data": []})
    monkeypatch.setattr(c, "session", session)
    return c, session


def test_search_system_path_and_params(client):
    c, session = client
    c.search_system("kfa", "paracetamol", limit=5)
    call = session.calls[-1]
    assert call["method"] == "GET"
    assert call["url"] == "https://term.test/api/v1/terminology/kfa/search"
    assert call["params"] == {"q": "paracetamol", "limit": 5}
    assert call["headers"]["Authorization"] == "Bearer pat-1"


def test_chaining_on_kptl(client):
    c, session = client
    c.query("pemasangan kateter").on("kptl").limit(10).get()
    call = session.calls[-1]
    assert call["method"] == "GET"
    assert call["url"] == "https://term.test/api/v1/terminology/kptl/search"
    assert call["params"] == {"q": "pemasangan kateter", "limit": 10}


def test_as_code_93004944_validates_kfa(client):
    c, session = client
    c.query("93004944").as_code().get()
    call = session.calls[-1]
    assert call["method"] == "POST"
    assert call["url"] == "https://term.test/api/v1/terminology/validate"
    assert call["json"] == {"system": "kfa", "code": "93004944"}


def test_http_401_raises_runtime_error(monkeypatch):
    c = TerminologyClient(base_url="https://term.test", token="pat-1")
    monkeypatch.setattr(c, "session", RecordingSession(401, {"message": "Unauthenticated."}))
    with pytest.raises(RuntimeError, match="TerminologyClient HTTP 401"):
        c.search("demam")

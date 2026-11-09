"""Unit tests for the full 8-file SATUSEHAT Queue package."""
from __future__ import annotations

import json

from src.queue import (
    ErrorClassifier,
    QueueException,
    QueueInterface,
    QueueMonitor,
    QueueResult,
    RateLimiter,
    SqliteQueue,
    Worker,
)


class FakeHttpResponse:
    def __init__(self, status_code: int, body: dict | None = None, headers: dict | None = None):
        self.status_code = status_code
        self._body = body
        self.headers = headers or {}
        self.text = json.dumps(body) if body is not None else ""

    def json(self):
        if self._body is None:
            raise ValueError("No JSON")
        return self._body


class FakeWorkerSession:
    def __init__(self, responses: list[FakeHttpResponse]):
        self.responses = list(responses)
        self.calls: list[dict] = []

    def post(self, url, data=None, headers=None, timeout=None):
        self.calls.append({"method": "POST", "url": url, "data": data, "headers": headers})
        return self.responses.pop(0)

    def request(self, method, url, headers=None, data=None, timeout=None):
        self.calls.append({"method": method, "url": url, "data": data, "headers": headers})
        return self.responses.pop(0)


def test_error_classifier():
    c200 = ErrorClassifier.classify(200)
    assert c200["category"] == ErrorClassifier.CAT_SUCCESS
    assert c200["retryable"] is False

    c401 = ErrorClassifier.classify(401, {"message": "Token expired"})
    assert c401["category"] == ErrorClassifier.CAT_UNAUTHORIZED
    assert c401["retryable"] is True

    c422 = ErrorClassifier.classify(
        422,
        {"issue": [{"severity": "error", "diagnostics": "Invalid Condition.code"}]},
    )
    assert c422["category"] == ErrorClassifier.CAT_VALIDATION_ERROR
    assert c422["retryable"] is False
    assert "[ERROR] Invalid Condition.code" in c422["detail"]

    c429 = ErrorClassifier.classify(429)
    assert c429["category"] == ErrorClassifier.CAT_RATE_LIMITED
    assert c429["retryable"] is True

    c502 = ErrorClassifier.classify(502)
    assert c502["category"] == ErrorClassifier.CAT_SERVER_ERROR
    assert c502["retryable"] is True


def test_rate_limiter():
    slept: list[float] = []
    rl = RateLimiter(rpm=60.0, sleep_fn=lambda s: slept.append(s))
    rl.wait()
    rl.wait()
    assert len(slept) == 1
    assert RateLimiter.parse_retry_after("15") == 15.0
    assert RateLimiter.parse_retry_after("") is None


def test_sqlite_queue_and_monitor():
    q = SqliteQueue(":memory:")
    j1 = q.enqueue("POST", "Patient", "Patient", {"resourceType": "Patient"}, idempotency_key="uuid-1")
    j2 = q.enqueue_bundle({"resourceType": "Bundle", "type": "transaction"})

    assert q.pending_count() == 2
    assert len(q.pending_jobs()) == 2

    claimed = q.dequeue()
    assert claimed is not None
    assert claimed["id"] == j1["id"]

    q.mark_success(j1["id"], {"http_code": 201}, "Patient/P001")
    assert q.get(j1["id"])["status"] == QueueInterface.STATUS_SUCCESS

    claimed2 = q.dequeue()
    assert claimed2 is not None
    assert claimed2["id"] == j2["id"]
    q.mark_dlq(j2["id"], "Validation failed", {"http_code": 422})
    assert q.dlq_count() == 1
    assert len(q.dlq_jobs()) == 1

    mon = QueueMonitor(q)
    summary = mon.summary()
    assert summary["total"] == 2
    assert summary["success"] == 1
    assert summary["dlq"] == 1

    hc = mon.health_check()
    assert hc["status"] == "critical"
    assert mon.top_errors()[0]["last_error"] == "Validation failed"

    reset_cnt = q.reset_all()
    assert reset_cnt == 1
    assert q.dlq_count() == 0


def test_worker_process():
    q = SqliteQueue(":memory:")
    q.enqueue("POST", "Observation", "Observation", {"resourceType": "Observation"})
    q.enqueue("POST", "Condition", "Condition", {"resourceType": "Condition"})

    sess = FakeWorkerSession([
        FakeHttpResponse(200, {"access_token": "tok-worker-1", "expires_in": 3600}),
        FakeHttpResponse(201, {"fullUrl": "Observation/OBS-100"}),
        FakeHttpResponse(422, {"issue": [{"severity": "error", "diagnostics": "Missing subject"}]}),
    ])

    rl = RateLimiter(rpm=60000.0, sleep_fn=lambda _: None)
    worker = Worker(
        queue=q,
        oauth2_config={
            "base_url": "https://api-satusehat-dev.dto.kemkes.go.id",
            "fhir_url": "https://api-satusehat-dev.dto.kemkes.go.id/fhir-r4/v1",
            "client_id": "cid",
            "client_secret": "csec",
        },
        rate_limiter=rl,
        session=sess,
    )

    stats = worker.process(10)
    assert stats == {"processed": 2, "succeeded": 1, "failed": 0, "dlq": 1}


def test_queue_exception_and_result():
    ex = QueueException.enqueue("bad payload")
    assert ex.code == QueueException.E_ENQUEUE

    r_ok = QueueResult.success(1, {"ok": True}, 1)
    assert r_ok.is_success() is True
    assert r_ok.is_retriable() is False

    r_fail = QueueResult.failed(2, "timeout", {}, 2)
    assert r_fail.is_failed() is True
    assert r_fail.is_retriable() is True

class ErrorClassifier:
    @staticmethod
    def classify(http_code: int) -> dict:
        if 200 <= http_code < 300:
            return {"category": "success", "retryable": False, "status": "success", "detail": "OK"}
        if http_code == 401:
            return {"category": "unauthorized", "retryable": True, "status": "pending", "detail": "Unauthorized (401)"}
        if http_code == 429 or (500 <= http_code < 600):
            return {"category": "server_error", "retryable": True, "status": "pending", "detail": "Retryable error"}
        return {"category": "client_error", "retryable": False, "status": "dlq", "detail": "DLQ / Client error"}

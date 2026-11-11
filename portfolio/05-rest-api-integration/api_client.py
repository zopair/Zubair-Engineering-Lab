"""Small, defensive REST API client for repeatable integration work."""
from __future__ import annotations

import time
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Mapping
from urllib.parse import urlsplit

import httpx


RETRYABLE_STATUSES = {408, 425, 429, 500, 502, 503, 504}
RETRYABLE_METHODS = {"GET", "HEAD", "OPTIONS"}


class ApiError(RuntimeError):
    """Safe, concise API failure with optional HTTP status metadata."""

    def __init__(self, message: str, *, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class ApiClient:
    """Context-managed JSON API client with bounded retries for safe methods.

    POST requests are deliberately not retried automatically because a server
    may have committed the operation before a network failure was observed.
    """

    def __init__(
        self,
        base_url: str,
        *,
        token: str | None = None,
        timeout: float = 10.0,
        max_retries: int = 2,
        backoff_factor: float = 0.25,
        max_backoff: float = 4.0,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        parsed = urlsplit(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if parsed.username or parsed.password:
            raise ValueError("base_url must not contain embedded credentials")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        if max_retries < 0:
            raise ValueError("max_retries cannot be negative")
        if backoff_factor < 0 or max_backoff < 0:
            raise ValueError("backoff values cannot be negative")

        headers = {"Accept": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_backoff = max_backoff
        self._client = httpx.Client(
            base_url=base_url.rstrip("/") + "/",
            headers=headers,
            timeout=httpx.Timeout(timeout),
            transport=transport,
            follow_redirects=False,
        )

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def close(self) -> None:
        self._client.close()

    @staticmethod
    def _retry_after(response: httpx.Response) -> float | None:
        value = response.headers.get("Retry-After")
        if not value:
            return None
        try:
            return max(0.0, float(value))
        except ValueError:
            try:
                retry_at = parsedate_to_datetime(value)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=timezone.utc)
                return max(0.0, (retry_at - datetime.now(timezone.utc)).total_seconds())
            except (TypeError, ValueError, OverflowError):
                return None

    def _delay(self, attempt: int, response: httpx.Response | None = None) -> float:
        if response is not None:
            retry_after = self._retry_after(response)
            if retry_after is not None:
                return min(retry_after, self.max_backoff)
        return min(self.backoff_factor * (2 ** attempt), self.max_backoff)

    def request_json(
        self,
        method: str,
        path: str,
        *,
        json_body: Any = None,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
    ) -> Any:
        parsed_path = urlsplit(path)
        if parsed_path.scheme or parsed_path.netloc:
            raise ValueError("API request path must be relative to the configured base URL")

        method = method.upper()
        retryable = method in RETRYABLE_METHODS
        attempts = self.max_retries + 1 if retryable else 1

        for attempt in range(attempts):
            try:
                response = self._client.request(
                    method, path.lstrip("/"), json=json_body,
                    headers=dict(headers or {}), params=params,
                )
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if retryable and attempt < attempts - 1:
                    time.sleep(self._delay(attempt))
                    continue
                raise ApiError(
                    f"Network failure during {method} {path}: {type(exc).__name__}"
                ) from exc

            if response.status_code in RETRYABLE_STATUSES and retryable and attempt < attempts - 1:
                time.sleep(self._delay(attempt, response))
                continue

            if not response.is_success:
                raise ApiError(
                    f"HTTP {response.status_code} for {method} {path}",
                    status_code=response.status_code,
                )

            try:
                return response.json()
            except ValueError as exc:
                raise ApiError(
                    f"Expected a valid JSON response from {method} {path}",
                    status_code=response.status_code,
                ) from exc

        raise ApiError(f"Request attempts exhausted for {method} {path}")

    def get_json(self, path: str, *, params: Mapping[str, Any] | None = None) -> Any:
        return self.request_json("GET", path, params=params)

    def post_json(
        self,
        path: str,
        payload: Any,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        return self.request_json("POST", path, json_body=payload, headers=headers)

import json
import unittest
from unittest.mock import patch

import httpx

from api_client import ApiClient, ApiError


class ApiClientTests(unittest.TestCase):
    def client_for(self, handler, *, retries=2):
        transport = httpx.MockTransport(handler)
        return ApiClient("https://api.example.test/v1", token="test-token",
                         timeout=1.5, max_retries=retries,
                         transport=transport)

    def test_get_returns_decoded_json_and_sends_bearer_token(self):
        def handler(request):
            self.assertEqual(request.url.path, "/v1/status")
            self.assertEqual(request.headers["Authorization"], "Bearer test-token")
            return httpx.Response(200, json={"ok": True})

        with self.client_for(handler) as client:
            self.assertEqual(client.get_json("/status"), {"ok": True})

    def test_get_retries_transient_server_error_then_succeeds(self):
        calls = []

        def handler(request):
            calls.append(request)
            if len(calls) == 1:
                return httpx.Response(503, json={"error": "temporarily unavailable"})
            return httpx.Response(200, json={"items": [1, 2]})

        with patch("api_client.time.sleep") as sleep:
            with self.client_for(handler) as client:
                result = client.get_json("/items")
        self.assertEqual(result, {"items": [1, 2]})
        self.assertEqual(len(calls), 2)
        sleep.assert_called_once()

    def test_get_honors_retry_after_for_rate_limit(self):
        calls = []

        def handler(request):
            calls.append(request)
            if len(calls) == 1:
                return httpx.Response(429, headers={"Retry-After": "3"}, json={"error": "slow down"})
            return httpx.Response(200, json={"ok": True})

        with patch("api_client.time.sleep") as sleep:
            with self.client_for(handler) as client:
                self.assertEqual(client.get_json("/limited"), {"ok": True})
        sleep.assert_called_once_with(3.0)

    def test_post_is_not_retried_automatically(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(503, json={"error": "unavailable"})

        with self.client_for(handler) as client:
            with self.assertRaises(ApiError):
                client.post_json("/records", {"name": "sample"})
        self.assertEqual(len(calls), 1)

    def test_invalid_json_raises_clear_api_error(self):
        with self.client_for(lambda request: httpx.Response(200, text="not-json")) as client:
            with self.assertRaisesRegex(ApiError, "valid JSON"):
                client.get_json("/broken")

    def test_non_success_response_exposes_status_without_echoing_auth(self):
        with self.client_for(lambda request: httpx.Response(401, text="token rejected")) as client:
            with self.assertRaises(ApiError) as caught:
                client.get_json("/private")
        self.assertEqual(caught.exception.status_code, 401)
        self.assertNotIn("test-token", str(caught.exception))

    def test_get_stops_after_configured_retry_budget(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(503, json={"error": "still unavailable"})

        with patch("api_client.time.sleep"):
            with self.client_for(handler, retries=2) as client:
                with self.assertRaises(ApiError):
                    client.get_json("/outage")
        self.assertEqual(len(calls), 3)

    def test_redirect_is_not_followed_implicitly(self):
        calls = []

        def handler(request):
            calls.append(request)
            return httpx.Response(302, headers={"Location": "https://other.example.test/"})

        with self.client_for(handler) as client:
            with self.assertRaises(ApiError) as caught:
                client.get_json("/redirect")
        self.assertEqual(caught.exception.status_code, 302)
        self.assertEqual(len(calls), 1)

    def test_timeout_is_configurable_and_invalid_base_url_is_rejected(self):
        with self.assertRaises(ValueError):
            ApiClient("ftp://api.example.test")
        with self.client_for(lambda request: httpx.Response(200, json={})) as client:
            self.assertEqual(client.timeout, 1.5)


if __name__ == "__main__":
    unittest.main()

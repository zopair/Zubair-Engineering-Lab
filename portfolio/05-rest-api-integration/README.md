# Sample 05 — REST API Integration & Smoke Tests

A reusable, bounded-retry JSON API client with deterministic tests at the HTTP boundary.

## Business problem

Small integrations often fail at the edges: temporary upstream outages, rate limits, malformed responses, hidden credential leakage, and unsafe retries that can duplicate writes.

## What this delivers

- Reusable HTTP client with configurable base URL and timeout.
- Optional Bearer authentication; credentials are never printed in error messages.
- JSON GET and POST helpers with clear, typed API errors.
- Bounded exponential backoff for safe methods (GET, HEAD, OPTIONS).
- Retry support for transient HTTP responses: 408, 425, 429, 500, 502, 503, and 504.
- Numeric or HTTP-date `Retry-After` support, bounded by the configured maximum delay.
- No automatic retries for POST, preventing accidental duplicate writes.
- No implicit redirect following.
- Deterministic HTTP-boundary tests using httpx MockTransport; no external API account or live endpoint required.

## Quick start

Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```python
import os
from api_client import ApiClient

with ApiClient(
    "https://api.example.com/v1",
    token=os.getenv("API_TOKEN"),
    timeout=8.0,
    max_retries=2,
) as api:
    health = api.get_json("/health")
    print(health)
```

POST requests are explicit and are not automatically retried:

```python
with ApiClient("https://api.example.com/v1") as api:
    created = api.post_json(
        "/records",
        {"name": "Example"},
        headers={"Idempotency-Key": "client-generated-operation-id"},
    )
```

Use an idempotency key only when the upstream API documents and supports it. The client passes the header through; it does not assume server-side idempotency.

## Reliability and security boundaries

- Retry attempts are bounded and configurable.
- Automatic retries are restricted to safe HTTP methods.
- A failed POST is reported rather than repeated. The caller must reconcile ambiguous outcomes with the upstream API before retrying manually.
- Authentication is passed as an Authorization header and is not included in exception text.
- Redirects are not followed automatically, reducing the risk of forwarding credentials to an unintended host.
- This sample does not implement OAuth refresh, pagination, webhook verification, or API-specific schemas; those require the target provider's contract.
- Tests use a deterministic in-memory transport. They prove client behavior, not the uptime or correctness of any third-party API.

## Acceptance evidence

Run:

```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
```

Nine tests cover Bearer authentication, JSON decoding, transient 5xx retry, rate-limit Retry-After, bounded retry exhaustion, no automatic POST retry, malformed JSON, safe HTTP error metadata, redirect handling, timeout configuration, and invalid base URLs.

The dedicated GitHub Actions workflow installs the pinned dependency range and runs the suite on Python 3.12.

## Deliverables

- `api_client.py` — reusable JSON API client.
- `tests/test_api_client.py` — isolated HTTP-boundary tests.
- `requirements.txt` — runtime dependency declaration.
- `.github/workflows/portfolio-sample-05.yml` — automated acceptance workflow.

**Work-sample status:** implementation committed; CI verification pending.

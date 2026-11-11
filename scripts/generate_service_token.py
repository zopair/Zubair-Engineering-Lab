#!/usr/bin/env python3
"""Generate high-entropy credentials for services owned by this portfolio.

The token is printed once to stdout. Do not commit it, log it, or pass it to
third-party APIs as if it were a provider-issued credential.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import secrets


def generate_token(entropy_bytes: int = 32) -> str:
    """Generate a URL-safe random token with a bounded entropy size."""
    if not 32 <= entropy_bytes <= 128:
        raise ValueError("entropy_bytes must be between 32 and 128")
    return secrets.token_urlsafe(entropy_bytes)


def token_digest(token: str) -> str:
    """Return the SHA-256 digest suitable for server-side token lookup."""
    if not isinstance(token, str) or not token:
        raise ValueError("token must be a non-empty string")
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bytes", type=int, default=32, dest="entropy_bytes")
    args = parser.parse_args()
    token = generate_token(args.entropy_bytes)
    print(json.dumps({
        "token": token,
        "sha256": token_digest(token),
        "entropy_bytes": args.entropy_bytes,
        "warning": "Store the token in a secret manager. Never commit or log it.",
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

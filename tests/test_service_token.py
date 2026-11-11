import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "generate_service_token", ROOT / "scripts" / "generate_service_token.py"
)
tokens = importlib.util.module_from_spec(SPEC)


class ServiceTokenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        SPEC.loader.exec_module(tokens)

    def test_token_is_high_entropy_and_url_safe(self):
        token = tokens.generate_token(32)
        self.assertGreaterEqual(len(token), 40)
        self.assertRegex(token, r"^[A-Za-z0-9_-]+$")

    def test_tokens_are_not_reused(self):
        self.assertNotEqual(tokens.generate_token(32), tokens.generate_token(32))

    def test_digest_is_stable_and_does_not_expose_token(self):
        token = tokens.generate_token(32)
        digest = tokens.token_digest(token)
        self.assertEqual(digest, tokens.token_digest(token))
        self.assertEqual(len(digest), 64)
        self.assertNotEqual(digest, token)

    def test_entropy_size_is_bounded(self):
        for size in (0, 16, 129):
            with self.assertRaises(ValueError):
                tokens.generate_token(size)

    def test_empty_tokens_are_rejected_for_hashing(self):
        with self.assertRaises(ValueError):
            tokens.token_digest("")


if __name__ == "__main__":
    unittest.main()

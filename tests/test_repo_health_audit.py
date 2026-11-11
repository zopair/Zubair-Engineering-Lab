import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "repo_health_audit", ROOT / "scripts" / "repo_health_audit.py"
)
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


class RepositoryHealthAuditTests(unittest.TestCase):
    def test_scope_is_explicit_and_rejects_unknown_repositories(self):
        self.assertTrue(audit.is_in_scope("SINC-OS"))
        self.assertFalse(audit.is_in_scope("activepieces"))
        self.assertFalse(audit.is_in_scope("../SINC-OS"))

    def test_forks_and_other_owners_are_excluded(self):
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": True, "owner": {"login": "zopair"}},
            [],
            {},
            None,
        )
        self.assertEqual(result["status"], "excluded")
        self.assertIn("fork", result["reason"])

        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "someone-else"}},
            [],
            {},
            None,
        )
        self.assertEqual(result["status"], "excluded")

    def test_tracked_environment_files_are_high_severity(self):
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "zopair"}},
            [".env", ".env.example", "backend/.env.local.example"],
            {},
            None,
        )
        findings = [item for item in result["findings"] if item["id"] == "tracked_env_file"]
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["severity"], "high")
        self.assertNotIn("content", findings[0])

    def test_workflow_permissions_and_deprecated_artifacts_are_flagged(self):
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "zopair"}},
            [".github/workflows/ci.yml"],
            {".github/workflows/ci.yml": "permissions:\n  contents: write\n  actions: write\n uses: actions/upload-artifact@v3"},
            {"status": "completed", "conclusion": "failure"},
        )
        ids = {item["id"] for item in result["findings"]}
        self.assertIn("broad_write_permissions", ids)
        self.assertIn("deprecated_artifact_action", ids)
        self.assertEqual(result["latest_ci"]["conclusion"], "failure")

    def test_no_workflow_is_reported_without_claiming_runtime_failure(self):
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "zopair"}},
            ["README.md"],
            {},
            None,
        )
        self.assertIn("missing_ci", {item["id"] for item in result["findings"]})
        self.assertEqual(result["status"], "needs_review")


if __name__ == "__main__":
    unittest.main()

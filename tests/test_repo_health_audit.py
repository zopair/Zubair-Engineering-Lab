import importlib.util
import unittest
import urllib.error
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

    def test_job_scoped_write_permission_is_not_a_workflow_wide_red_flag(self):
        workflow = """permissions:
  contents: read
jobs:
  release:
    permissions:
      contents: write
"""
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "zopair"}},
            [".github/workflows/release.yml", "pyproject.toml"],
            {".github/workflows/release.yml": workflow},
            None,
        )
        self.assertNotIn("broad_write_permissions", {item["id"] for item in result["findings"]})

    def test_missing_ci_is_reported_for_code_repositories(self):
        result = audit.classify_repository(
            "SINC-OS",
            {"name": "SINC-OS", "fork": False, "owner": {"login": "zopair"}},
            ["requirements.txt", "src/main.py"],
            {},
            None,
        )
        self.assertIn("missing_ci", {item["id"] for item in result["findings"]})
        self.assertEqual(result["status"], "needs_review")


    def test_empty_default_branch_tree_is_classified_as_uninitialized(self):
        class EmptyRepositoryClient:
            def get_json(self, path):
                if path == "/repos/zopair/CLT-Core-Monorepo":
                    return {
                        "name": "CLT-Core-Monorepo",
                        "fork": False,
                        "owner": {"login": "zopair"},
                        "default_branch": "main",
                        "size": 200,
                    }
                raise urllib.error.HTTPError(path, 404, "Not Found", {}, None)

            def get_text(self, url):
                raise AssertionError("No raw workflow files should be fetched for an empty repository")

        result = audit.audit_one(EmptyRepositoryClient(), "CLT-Core-Monorepo")
        self.assertEqual(result["status"], "needs_review")
        self.assertIn("empty_repository", {item["id"] for item in result["findings"]})

    def test_empty_repository_is_reported_as_uninitialized_not_api_error(self):
        result = audit.classify_repository(
            "CLT-Core-Monorepo",
            {"name": "CLT-Core-Monorepo", "fork": False, "owner": {"login": "zopair"}, "size": 0},
            [],
            {},
            None,
        )
        self.assertIn("empty_repository", {item["id"] for item in result["findings"]})


if __name__ == "__main__":
    unittest.main()

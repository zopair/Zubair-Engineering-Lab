import json
import tempfile
import unittest
from pathlib import Path

from batch_organizer import build_plan, execute_plan


class BatchOrganizerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "report.txt").write_text("report", encoding="utf-8")
        (self.root / "image.png").write_bytes(b"image")
        (self.root / "notes.md").write_text("notes", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_plan_is_dry_run_and_filters_extensions(self):
        plan = build_plan(self.root, prefix="client_", extensions={".txt", ".png"})
        self.assertEqual(len(plan), 2)
        self.assertTrue(all(item["status"] == "planned" for item in plan))
        self.assertTrue((self.root / "report.txt").exists())
        self.assertEqual({Path(item["destination"]).name for item in plan},
                         {"client_report.txt", "client_image.png"})

    def test_existing_destination_is_skipped_without_overwrite(self):
        (self.root / "client_report.txt").write_text("keep", encoding="utf-8")
        plan = build_plan(self.root, prefix="client_", extensions={".txt"})
        report_item = next(item for item in plan if Path(item["source"]).name == "report.txt")
        self.assertEqual(report_item["status"], "skipped")
        result = execute_plan(plan, apply=True)
        self.assertEqual(result["applied"], 0)
        self.assertEqual((self.root / "client_report.txt").read_text(encoding="utf-8"), "keep")
        self.assertTrue((self.root / "report.txt").exists())

    def test_apply_renames_and_writes_audit_log(self):
        plan = build_plan(self.root, prefix="archived_", extensions={".txt"})
        audit = self.root / "audit.json"
        result = execute_plan(plan, apply=True, audit_path=audit)
        self.assertEqual(result["applied"], 1)
        self.assertFalse((self.root / "report.txt").exists())
        self.assertTrue((self.root / "archived_report.txt").exists())
        payload = json.loads(audit.read_text(encoding="utf-8"))
        self.assertEqual(payload["applied"], 1)
        self.assertEqual(len(payload["items"]), 1)

    def test_dry_run_never_mutates_files(self):
        plan = build_plan(self.root, prefix="new_", extensions={".txt"})
        result = execute_plan(plan, apply=False)
        self.assertEqual(result["applied"], 0)
        self.assertTrue((self.root / "report.txt").exists())
        self.assertFalse((self.root / "new_report.txt").exists())

    def test_rejects_non_directory(self):
        with self.assertRaises(NotADirectoryError):
            build_plan(self.root / "missing")

    def test_ignores_directories_and_symlinks(self):
        (self.root / "folder").mkdir()
        (self.root / "link.txt").symlink_to(self.root / "report.txt")
        plan = build_plan(self.root, prefix="x_")
        names = {item["source"] for item in plan}
        self.assertNotIn("folder", names)
        self.assertNotIn("link.txt", names)


if __name__ == "__main__":
    unittest.main()

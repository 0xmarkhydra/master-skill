#!/usr/bin/env python3
"""Regression tests for CodeLocal Skills kit verification; operate only on temporary copies."""
from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class SkillVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="master-skill-test-")
        self.root = Path(self.tmp.name)
        for folder in ("skills", ".agents", ".claude", "archive", "templates", "docs", "third_party"):
            shutil.copytree(ROOT / folder, self.root / folder)
        (self.root / "tools").mkdir()
        shutil.copy2(ROOT / "tools" / "verify_kit.py", self.root / "tools" / "verify_kit.py")
        for name in ("AGENTS.md", "CLAUDE.md", "README.md"):
            shutil.copy2(ROOT / name, self.root / name)

    def tearDown(self):
        self.tmp.cleanup()

    def verify(self):
        return subprocess.run(
            [sys.executable, str(self.root / "tools" / "verify_kit.py")],
            cwd=self.root, text=True, capture_output=True, check=False, timeout=30
        )

    def test_valid_package(self):
        r = self.verify()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("9 skills", r.stdout)

    def test_changed_mirror_detected(self):
        path = self.root / ".agents/skills/react-frontend-engineering/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\ncorrupted\n", encoding="utf-8")
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MIRROR MISMATCH", r.stdout)

    def test_policy_divergence_detected(self):
        with (self.root / "CLAUDE.md").open("a", encoding="utf-8") as f:
            f.write("\nDifference\n")
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("POLICY MISMATCH", r.stdout)

    def test_deleted_reference_detected(self):
        (self.root / "skills/ios-inspired-ui-design/references/VISUAL-QA.md").unlink()
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("CANONICAL FILE SET", r.stdout)

    def test_ponytail_missing_detected(self):
        (self.root / "skills/ponytail-review/SKILL.md").unlink()
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MISSING or non-regular file: skills/ponytail-review/SKILL.md", r.stdout)

    def test_ponytail_vendor_tampering_detected(self):
        path = self.root / "skills/ponytail/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\\nmodified\\n", encoding="utf-8")
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("VENDOR SOURCE MODIFIED", r.stdout)

    def test_ponytail_license_detected(self):
        (self.root / "third_party/ponytail/LICENSE").unlink()
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("MISSING", r.stdout)

    def test_active_legacy_detected(self):
        shutil.copytree(
            self.root / "archive/legacy-v0-two-skills/skills/code-logic",
            self.root / "skills/code-logic"
        )
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("LEGACY STILL ACTIVE", r.stdout)

    def test_archive_tampering_detected(self):
        path = self.root / "archive/legacy-v0-two-skills/.claude/skills/code-logic/SKILL.md"
        path.write_text(path.read_text(encoding="utf-8") + "\nmodified\n", encoding="utf-8")
        r = self.verify()
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("LEGACY ARCHIVE MISMATCH", r.stdout)


if __name__ == "__main__":
    unittest.main()
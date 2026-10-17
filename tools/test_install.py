#!/usr/bin/env python3
"""Unit tests for the safe downstream CodeLocal Skills installer."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from install import BEGIN, END, InstallError, SKILLS, install, ROOT  # noqa: E402


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="codelocal-install-test-")
        self.target = Path(self.tmp.name) / "client-project"
        self.target.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_both_agents_and_license_installed(self):
        (self.target / "AGENTS.md").write_text("# Pre-existing safety policy\n", encoding="utf-8")
        events = install(self.target, "both")
        self.assertTrue(events)
        for root in (".agents/skills", ".claude/skills"):
            for name in SKILLS:
                self.assertEqual(
                    (self.target / root / name / "SKILL.md").read_bytes(),
                    (ROOT / "skills" / name / "SKILL.md").read_bytes(),
                )
        agent_text = (self.target / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(agent_text.startswith("# Pre-existing safety policy\n"))
        self.assertIn(BEGIN, agent_text)
        self.assertIn("Ultra", agent_text)
        self.assertIn("P0", agent_text)
        self.assertIn(END, (self.target / "CLAUDE.md").read_text(encoding="utf-8"))
        self.assertEqual(
            (self.target / ".codelocal-skills/ponytail/LICENSE").read_bytes(),
            (ROOT / "third_party/ponytail/LICENSE").read_bytes(),
        )

    def test_rerun_skips_identical_files_and_block(self):
        install(self.target, "both")
        before = (self.target / "AGENTS.md").read_bytes()
        log = install(self.target, "both")
        self.assertTrue(all(line.startswith("SKIP") for line in log))
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), before)

    def test_conflict_aborts_without_partial_install(self):
        conflict = self.target / ".agents/skills/ponytail"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("custom version\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallError, "Conflicting existing skill"):
            install(self.target, "both")
        self.assertFalse((self.target / ".claude").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".codelocal-skills").exists())

    def test_dry_run_has_no_writes(self):
        events = install(self.target, "both", dry_run=True)
        self.assertIn("INSTALL .agents/skills/ponytail", events)
        self.assertEqual(list(self.target.iterdir()), [])

    def test_claude_only_does_not_change_agents(self):
        (self.target / "AGENTS.md").write_text("# Leave me alone\n", encoding="utf-8")
        install(self.target, "claude")
        self.assertEqual((self.target / "AGENTS.md").read_text(encoding="utf-8"), "# Leave me alone\n")
        self.assertFalse((self.target / ".agents").exists())
        self.assertTrue((self.target / ".claude/skills/ponytail/SKILL.md").is_file())

    def test_custom_modified_block_not_overwritten(self):
        (self.target / "AGENTS.md").write_text(f"{BEGIN}\nuser-edited rule\n{END}\n", encoding="utf-8")
        with self.assertRaisesRegex(InstallError, "modified"):
            install(self.target, "codex")
        self.assertFalse((self.target / ".agents").exists())


if __name__ == "__main__":
    unittest.main()

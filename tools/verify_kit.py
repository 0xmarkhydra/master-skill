#!/usr/bin/env python3
"""Read-only structural, mirror, metadata, link and approved-rule validation."""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = {
    "backend-engineering": {
        "SKILL.md",
        "references/RULEBOOK.md",
        "references/API-SECURITY.md",
        "references/STACK-ADAPTERS.md",
        "references/OPERATIONS-QUALITY.md",
    },
    "react-frontend-engineering": {
        "SKILL.md",
        "references/RULEBOOK.md",
        "references/API-STATE-FORMS.md",
        "references/FEATURE-PARITY.md",
    },
    "ios-inspired-ui-design": {
        "SKILL.md",
        "references/RULEBOOK.md",
        "references/DESIGN-SYSTEM.md",
        "references/VISUAL-QA.md",
    },
    "ponytail": {"SKILL.md"},
    "ponytail-review": {"SKILL.md"},
    "ponytail-audit": {"SKILL.md"},
    "ponytail-debt": {"SKILL.md"},
    "ponytail-gain": {"SKILL.md"},
    "ponytail-help": {"SKILL.md"},
}
# Pristine MIT upstream files pinned at the imported Git revision.
VENDOR_HASHES = {
    "ponytail": "9badd22a32e19cb884e46dfa8d3aae82bb81dfa5484105b8b4f0262df823a509",
    "ponytail-review": "33fe4ebe22a460924e5d4a261e223df22e409cc94ab76182bee9fb91a3ef022e",
    "ponytail-audit": "2b3223a02c386d1263e1b08343cb8eb3a53e444cdafb1d79e26c8ec2a8fcad28",
    "ponytail-debt": "b5ec2762f6ba8c4af9ea7173aa6c9f91b88655a25e43f9de0264f6ce8722b25f",
    "ponytail-gain": "231034a896d6762e4b5c8468287083422c56b499119976ec9f76821f7d083090",
    "ponytail-help": "7fb330460bd0efe935dcae72ff2c0e14e5366542b5f04ff2f2a05c7b58366386",
}
UPSTREAM_REVISION = "6f1c2bfff0c837d268929a7c4e490918eb4fab29"
LEGACY = {"code-logic", "ui-v3-design"}
EXPECTED_RULE_COUNTS = {"backend-engineering": 19, "react-frontend-engineering": 12, "ios-inspired-ui-design": 10}
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def load(path: Path) -> bytes | None:
    if not path.is_file() or path.is_symlink():
        fail(f"MISSING or non-regular file: {path.relative_to(ROOT)}")
        return None
    return path.read_bytes()


def md_links(md: str) -> list[str]:
    # Markdown-style local links; remote and anchor-only links not checked here.
    return re.findall(r"\]\(([^)]+)\)", md)


def validate_references(file: Path) -> None:
    text = file.read_text(encoding="utf-8")
    for target in md_links(text):
        target = target.split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            continue
        candidate = file.parent / target
        if not candidate.is_file():
            fail(f"BROKEN LINK: {file.relative_to(ROOT)} -> {target}")


def validate_skill(name: str, relative_paths: set[str]) -> None:
    base = ROOT / "skills" / name
    skill_file = base / "SKILL.md"
    raw = load(skill_file)
    if raw is None:
        return
    text = raw.decode("utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
    if not frontmatter or not re.search(rf"(?m)^name: {re.escape(name)}$", frontmatter.group(1)):
        fail(f"INVALID FRONTMATTER: {name}")
    if not frontmatter or not re.search(r"(?m)^description:\s+\S", frontmatter.group(1)):
        fail(f"MISSING DESCRIPTION: {name}")

    actual = {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
    if actual != relative_paths:
        fail(f"CANONICAL FILE SET: {name}: missing={sorted(relative_paths - actual)}, extra={sorted(actual - relative_paths)}")
    for subpath in sorted(relative_paths):
        original = load(base / subpath)
        if original is None:
            continue
        validate_references(base / subpath)
        for mirror_root in (".agents/skills", ".claude/skills"):
            mirrored = load(ROOT / mirror_root / name / subpath)
            if mirrored is not None and original != mirrored:
                fail(f"MIRROR MISMATCH: {mirror_root}/{name}/{subpath}")

    for mirror_root in (".agents/skills", ".claude/skills"):
        mbase = ROOT / mirror_root / name
        actual_mirror = {p.relative_to(mbase).as_posix() for p in mbase.rglob("*") if p.is_file()} if mbase.is_dir() else set()
        if actual_mirror != relative_paths:
            fail(f"MIRROR FILE SET: {mirror_root}/{name}: missing={sorted(relative_paths - actual_mirror)}, extra={sorted(actual_mirror - relative_paths)}")

    rules = (base / "references" / "RULEBOOK.md")
    if rules.is_file():
        doc = rules.read_text(encoding="utf-8")
        # #06.1, #06.2, #06.3 are facets of the single top-level #06.
        numbered = {int(n) for n in re.findall(r"(?m)^#{2,3}\s+#(\d{2})(?:\.|\s)", doc)}
        expected = set(range(1, EXPECTED_RULE_COUNTS[name] + 1))
        if numbered != expected:
            fail(f"RULE IDS: {name}: missing={sorted(expected - numbered)}, extra={sorted(numbered - expected)}")
        if name == "backend-engineering" and not all(f"#06.{n}" in doc for n in (1, 2, 3)):
            fail("MISSING BACKEND SECURITY FACETS: #06.1/#06.2/#06.3")


def main() -> int:
    for relative in ("AGENTS.md", "CLAUDE.md", "README.md", "templates/PROJECT-PROFILE.md", "docs/PONYTAIL-INTEGRATION.md", "third_party/ponytail/SOURCE.md", "third_party/ponytail/LICENSE"):
        load(ROOT / relative)
    if (ROOT / "AGENTS.md").is_file() and (ROOT / "CLAUDE.md").is_file():
        if (ROOT / "AGENTS.md").read_bytes() != (ROOT / "CLAUDE.md").read_bytes():
            fail("POLICY MISMATCH: AGENTS.md != CLAUDE.md")

    # Verify active orchestrator mentions all nine skills and the safety boundary.
    policy_file = ROOT / "AGENTS.md"
    if policy_file.is_file():
        policy = policy_file.read_text(encoding="utf-8")
        if not all(name in policy for name in SKILLS):
            fail("ORCHESTRATION DOES NOT REFERENCE ALL NINE SKILLS")
        if "Ultra mode" not in policy or "P0" not in policy:
            fail("ORCHESTRATION MISSING ULTRA/SAFETY PRECEDENCE")
    # This distribution intentionally vendors skills, not plugin hooks or MCP binaries.
    for plugin_dir in (".codex-plugin", ".claude-plugin", "hooks", "ponytail-mcp"):
        if (ROOT / plugin_dir).exists():
            fail(f"PLUGIN RUNTIME UNEXPECTED IN SKILLS-ONLY KIT: {plugin_dir}")
    readme = ROOT / "README.md"
    if readme.is_file():
        validate_references(readme)

    for directory in ("skills", ".agents/skills", ".claude/skills"):
        basedir = ROOT / directory
        actual = {d.name for d in basedir.iterdir() if d.is_dir()} if basedir.is_dir() else set()
        expected = set(SKILLS)
        if actual != expected:
            fail(f"ACTIVE SKILLS {directory}: expected={sorted(expected)}, actual={sorted(actual)}")
        if actual & LEGACY:
            fail(f"LEGACY STILL ACTIVE: {directory}: {sorted(actual & LEGACY)}")

    for name, paths in SKILLS.items():
        validate_skill(name, paths)

    archive = ROOT / "archive/legacy-v0-two-skills"
    for name in LEGACY:
        canonical = archive / "skills" / name
        originals = {
            p.relative_to(canonical).as_posix(): p.read_bytes()
            for p in canonical.rglob("*") if p.is_file()
        } if canonical.is_dir() else {}
        if "SKILL.md" not in originals:
            fail(f"MISSING LEGACY ARCHIVE: {name}")
        for mirror in (".agents/skills", ".claude/skills"):
            mirror_dir = archive / mirror / name
            mirrored = {
                p.relative_to(mirror_dir).as_posix(): p.read_bytes()
                for p in mirror_dir.rglob("*") if p.is_file()
            } if mirror_dir.is_dir() else {}
            if mirrored != originals:
                fail(f"LEGACY ARCHIVE MISMATCH: {mirror}/{name}")

    # Ponytail is an independent MIT work; don't lose attribution or silently alter upstream.
    license_file = ROOT / "third_party/ponytail/LICENSE"
    if license_file.is_file():
        license_text = license_file.read_text(encoding="utf-8")
        if "MIT License" not in license_text or "Copyright (c) 2026 DietrichGebert" not in license_text:
            fail("PONYTAIL LICENSE INVALID OR ATTRIBUTION MISSING")
    source_file = ROOT / "third_party/ponytail/SOURCE.md"
    if source_file.is_file():
        source_text = source_file.read_text(encoding="utf-8")
        if UPSTREAM_REVISION not in source_text or "DietrichGebert/ponytail" not in source_text:
            fail("PONYTAIL REVISION/UPSTREAM CREDIT MISSING")
    for name, expected_hash in VENDOR_HASHES.items():
        source = ROOT / "skills" / name / "SKILL.md"
        if source.is_file() and hashlib.sha256(source.read_bytes()).hexdigest() != expected_hash:
            fail(f"VENDOR SOURCE MODIFIED: {name}; review and update source revision/license deliberately")
    integration = ROOT / "docs/PONYTAIL-INTEGRATION.md"
    if integration.is_file():
        text = integration.read_text(encoding="utf-8")
        if not all(word in text for word in ("Ultra", "P0", "skill-only")):
            fail("PONYTAIL INTEGRATION CONTRACT MISSING")
        validate_references(integration)
    if source_file.is_file():
        validate_references(source_file)

    if ERRORS:
        for error in ERRORS:
            print("FAIL:", error)
        print(f"FAIL: {len(ERRORS)} issue(s)")
        return 1
    total = sum(map(len, SKILLS.values()))
    print(f"PASS: 9 skills (3 approved domain skills: 19/12/10 rules + 6 Ponytail), {total} canonical files and both exact mirrors")
    print("PASS: policies identical, metadata/links, MIT provenance and vendor source hashes, legacy kit archived")
    return 0


if __name__ == "__main__":
    sys.exit(main())
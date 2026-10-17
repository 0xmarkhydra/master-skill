#!/usr/bin/env python3
"""Install CodeLocal Skills and append safe agent instructions to an existing project."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "backend-engineering",
    "react-frontend-engineering",
    "ios-inspired-ui-design",
    "ponytail",
    "ponytail-review",
    "ponytail-audit",
    "ponytail-debt",
    "ponytail-gain",
    "ponytail-help",
)
AGENTS = {
    "codex": (".agents/skills", "AGENTS.md"),
    "claude": (".claude/skills", "CLAUDE.md"),
}
BEGIN = "<!-- CODELOCAL-SKILLS:BEGIN -->"
END = "<!-- CODELOCAL-SKILLS:END -->"


class InstallError(Exception):
    pass


def managed_instructions(skill_dir: str) -> str:
    def path(skill: str) -> str:
        return f"{skill_dir}/{skill}/SKILL.md"

    return f"""\
{BEGIN}
## CodeLocal Skills — coding agent instructions

Before a coding task, inspect the repository, existing instructions, project stack,
Git state, affected workflows and contracts. Read the applicable skill(s), not all
nine indiscriminately:

- Server/API/DB/auth/security/migrations: {path("backend-engineering")} and relevant references.
- React/Vite/Next.js frontend behavior, state/forms/API/routing/feature parity:
  {path("react-frontend-engineering")} and relevant references.
- Design system, iOS-inspired UI, responsive, visual quality:
  {path("ios-inspired-ui-design")} and relevant references.
- Any code creation/fix/refactor: additionally read {path("ponytail")}.
  Apply Ponytail **Ultra** as a simplicity *decision policy*, not a plugin mode.
  Challenge unneeded complexity; reuse existing code/platform/dependencies first.
- On explicit review/audit/debt/benchmark/help requests, use
  {path("ponytail-review")}, {path("ponytail-audit")},
  {path("ponytail-debt")}, {path("ponytail-gain")}, or
  {path("ponytail-help")} as appropriate.

Precedence: project/user-approved scope, correctness, backend authorization, data
and API compatibility, feature parity, accessibility, tests and release safety
always beat code brevity (P0/P1 quality gates). Ponytail Ultra must NOT silently remove requirements,
validation, security checks, error handling or tests. Follow project branch/CI
policies. Report PASS/FAIL/NOT RUN/BLOCKED from evidence; do not invent success,
commit, push, merge, deployment or live testing.

This block was installed by CodeLocal Skills. Existing project instructions remain
in effect. Ponytail is third-party MIT-licensed; provenance is under
`.codelocal-skills/ponytail/`. No marketplace plugin or hooks are installed.
{END}"""


def contents_match(source: Path, destination: Path) -> bool:
    if not destination.is_dir() or destination.is_symlink():
        return False
    src_files = {
        p.relative_to(source): p.read_bytes()
        for p in source.rglob("*") if p.is_file() and not p.is_symlink()
    }
    dst_files = {
        p.relative_to(destination): p.read_bytes()
        for p in destination.rglob("*") if p.is_file() and not p.is_symlink()
    }
    return src_files == dst_files and not any(p.is_symlink() for p in destination.rglob("*"))


def check_path_is_safe(target: Path, relative: Path) -> None:
    current = target
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise InstallError(f"Symlink destination not supported: {current}")


def new_policy(existing: str, block: str, path: Path) -> str | None:
    has_begin, has_end = BEGIN in existing, END in existing
    if has_begin != has_end:
        raise InstallError(f"Broken CodeLocal managed block in {path}; please review manually.")
    if has_begin:
        start = existing.index(BEGIN)
        end = existing.index(END, start) + len(END)
        if existing[start:end] != block:
            raise InstallError(f"CodeLocal block modified in {path}; merge manually instead of overwriting.")
        return None
    separator = ("\n" if not existing.endswith("\n") else "") + "\n" if existing else ""
    return existing + separator + block + "\n"


def install(target: Path, agent: str = "both", dry_run: bool = False) -> list[str]:
    target = target.expanduser().resolve()
    if not target.is_dir():
        raise InstallError(f"Target is not an existing directory: {target}")
    if target == ROOT:
        raise InstallError("Target must be a downstream project, not the CodeLocal Skills source.")
    choices = tuple(AGENTS) if agent == "both" else (agent,)
    operations: list[tuple[str, Path, Path | str]] = []
    log: list[str] = []

    # Preflight ALL files first: conflicts abort without touching a destination.
    for choice in choices:
        skill_dir, policy_name = AGENTS[choice]
        for name in SKILLS:
            source = ROOT / "skills" / name
            if not (source / "SKILL.md").is_file():
                raise InstallError(f"Missing source skill: {source}")
            relative = Path(skill_dir) / name
            check_path_is_safe(target, relative)
            destination = target / relative
            if destination.exists():
                if not contents_match(source, destination):
                    raise InstallError(f"Conflicting existing skill: {destination}. Resolve manually; no overwrite.")
                log.append(f"SKIP identical {relative}")
            else:
                operations.append(("directory", destination, source))
                log.append(f"INSTALL {relative}")

        relative = Path(policy_name)
        check_path_is_safe(target, relative)
        path = target / relative
        if path.exists() and not path.is_file():
            raise InstallError(f"Existing policy is not a regular file: {path}")
        existing = path.read_text(encoding="utf-8") if path.exists() else ""
        update = new_policy(existing, managed_instructions(skill_dir), path)
        if update is None:
            log.append(f"SKIP managed block in {policy_name}")
        else:
            operations.append(("text", path, update))
            log.append(f"APPEND managed instructions to {policy_name}")

    license_dir = Path(".codelocal-skills/ponytail")
    for name, source in (
        ("LICENSE", ROOT / "third_party/ponytail/LICENSE"),
        ("SOURCE.md", ROOT / "third_party/ponytail/SOURCE.md"),
    ):
        relative = license_dir / name
        check_path_is_safe(target, relative)
        destination = target / relative
        if not source.is_file():
            raise InstallError(f"Missing third-party attribution: {source}")
        if destination.exists():
            if not destination.is_file() or destination.read_bytes() != source.read_bytes():
                raise InstallError(f"Conflicting attribution file: {destination}. No overwrite.")
            log.append(f"SKIP identical {relative}")
        else:
            operations.append(("file", destination, source))
            log.append(f"INSTALL attribution {relative}")

    if not dry_run:
        for kind, path, content in operations:
            path.parent.mkdir(parents=True, exist_ok=True)
            if kind == "directory":
                shutil.copytree(content, path)
            elif kind == "file":
                shutil.copy2(content, path)
            else:
                path.write_text(content, encoding="utf-8")
    return log


def main() -> int:
    parser = argparse.ArgumentParser(description="Install 9 CodeLocal Skills without overwriting project policies.")
    parser.add_argument("--target", type=Path, required=True, help="Existing target project root")
    parser.add_argument("--agent", choices=(*AGENTS, "both"), default="both")
    parser.add_argument("--dry-run", action="store_true", help="Show planned steps only; do not write files")
    args = parser.parse_args()

    check = subprocess.run(
        [sys.executable, str(ROOT / "tools/verify_kit.py")],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if check.returncode != 0:
        print("BLOCKED: CodeLocal Skills source verification failed.", file=sys.stderr)
        print(check.stdout + check.stderr, file=sys.stderr)
        return 1
    try:
        operations = install(args.target, args.agent, args.dry_run)
    except (InstallError, OSError, UnicodeError) as exc:
        print(f"BLOCKED: {exc}", file=sys.stderr)
        return 1
    for operation in operations:
        print(operation)
    print(f"PASS: {'dry-run plan' if args.dry_run else 'installation'} for {args.agent}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

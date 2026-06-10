#!/usr/bin/env python3
"""Episteme plugin-check.

Deterministic install-readiness check for the Episteme Claude Code plugin. Validates
the same things the harness needs at load time, so a green run is strong evidence the
plugin will install and its skills will be discoverable:

  - .claude-plugin/plugin.json  : valid JSON, has `name`
  - .claude-plugin/marketplace.json : valid JSON, lists the plugin
  - hooks/hooks.json            : valid JSON, declares a SessionStart hook
  - hooks/session-start.py      : runs and emits valid SessionStart JSON
  - skills/<name>/SKILL.md       : each has frontmatter with `name` + `description`,
                                   and `name` matches the folder

Usage: python3 tools/plugin-check.py
Exit 0 = install-ready; 1 = problems found; 2 = setup error.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load_json(path: Path, errors: list[str]) -> dict | None:
    if not path.is_file():
        errors.append(f"missing {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc.msg} at line {exc.lineno})")
        return None


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm: dict[str, str] = {}
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip()
    return fm


def main() -> int:
    errors: list[str] = []

    plugin = _load_json(ROOT / ".claude-plugin" / "plugin.json", errors)
    if plugin is not None and not plugin.get("name"):
        errors.append(".claude-plugin/plugin.json: missing `name`")

    market = _load_json(ROOT / ".claude-plugin" / "marketplace.json", errors)
    if market is not None:
        names = [p.get("name") for p in market.get("plugins", []) if isinstance(p, dict)]
        if plugin and plugin.get("name") and plugin["name"] not in names:
            errors.append(f"marketplace.json does not list plugin '{plugin['name']}'")

    hooks = _load_json(ROOT / "hooks" / "hooks.json", errors)
    if hooks is not None and "SessionStart" not in (hooks.get("hooks") or {}):
        errors.append("hooks/hooks.json: no SessionStart hook declared")

    # Skills: every skills/<name>/SKILL.md has name+description, name == folder.
    skills_dir = ROOT / "skills"
    skill_count = 0
    if not skills_dir.is_dir():
        errors.append("missing skills/ directory")
    else:
        for sub in sorted(skills_dir.iterdir()):
            skill_md = sub / "SKILL.md"
            if not skill_md.is_file():
                continue
            skill_count += 1
            fm = _frontmatter(skill_md.read_text(encoding="utf-8"))
            if not fm.get("name"):
                errors.append(f"skills/{sub.name}/SKILL.md: frontmatter missing `name`")
            elif fm["name"] != sub.name:
                errors.append(f"skills/{sub.name}/SKILL.md: name '{fm['name']}' != folder '{sub.name}'")
            if not fm.get("description"):
                errors.append(f"skills/{sub.name}/SKILL.md: frontmatter missing `description`")

    # Hook actually runs and emits valid SessionStart JSON.
    hook = ROOT / "hooks" / "session-start.py"
    if not hook.is_file():
        errors.append("missing hooks/session-start.py")
    else:
        try:
            out = subprocess.run([sys.executable, str(hook)], capture_output=True, text=True,
                                 env={"CLAUDE_PLUGIN_ROOT": str(ROOT), "PATH": "/usr/bin:/bin"})
            payload = json.loads(out.stdout)
            if "additionalContext" not in payload.get("hookSpecificOutput", {}):
                errors.append("session-start.py: output missing hookSpecificOutput.additionalContext")
        except Exception as exc:
            errors.append(f"session-start.py did not emit valid JSON: {exc}")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) ({skill_count} skills scanned)")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: plugin install-ready - {skill_count} skills, manifest + marketplace + SessionStart hook valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Episteme SessionStart hook.

Injects the `using-episteme` bootstrap skill into the session context so the
agent knows it has Episteme and when to reach for the loop vs a single voice.
Uses Python for safe JSON escaping of the markdown body.

Outputs the Claude Code SessionStart contract:
    {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "..."}}
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PLUGIN_ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT", Path(__file__).resolve().parent.parent))
BOOTSTRAP = PLUGIN_ROOT / "skills" / "using-episteme" / "SKILL.md"


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            nl = text.find("\n", end + 1)
            return text[nl + 1:].lstrip() if nl != -1 else ""
    return text


def main() -> int:
    try:
        body = _strip_frontmatter(BOOTSTRAP.read_text(encoding="utf-8"))
    except OSError:
        # Never break the session if the bootstrap is missing; emit nothing.
        return 0
    context = "You have Episteme - an epistemic control layer of skills for contract-driven development.\n\n" + body
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())

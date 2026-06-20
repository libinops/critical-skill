#!/usr/bin/env python3
"""Regenerate platform-specific skill/rule files from body.md.

Source of truth: body.md
Generates:
  - skills/critical/SKILL.md             (Claude)
  - .trae/skills/critical-skill/SKILL.md (Trae IDE)
  - .cursor/rules/critical.md            (Cursor)
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESCRIPTION = (
    "Behavioral guidelines to reduce common LLM coding mistakes. "
    "Use when writing, reviewing, or refactoring code to avoid overcomplication, "
    "make surgical changes, surface assumptions, and define verifiable success criteria."
)

TARGETS = [
    (ROOT / "skills/critical/SKILL.md",
     f"---\nname: critical-skill\ndescription: {DESCRIPTION}\nlicense: MIT\n---"),
    (ROOT / ".trae/skills/critical-skill/SKILL.md",
     f"---\nname: critical-skill\ndescription: {DESCRIPTION}\n---"),
    (ROOT / ".cursor/rules/critical.md",
     f"---\ndescription: {DESCRIPTION}\nalwaysApply: true\n---"),
]


def main() -> None:
    body = (ROOT / "body.md").read_text(encoding="utf-8").rstrip() + "\n"
    for path, frontmatter in TARGETS:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{frontmatter}\n\n{body}", encoding="utf-8")
        print(f"wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

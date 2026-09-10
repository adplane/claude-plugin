#!/usr/bin/env python3
"""Lint the Adplane plugin's skills and commands.

Checks, per skill (skills/<dir>/SKILL.md):
  - frontmatter present with `name` equal to the directory and a
    `description` of 50 to 1000 characters that contains "Use when",
    "Use for", or "Load for" (the model reads only the description when
    deciding whether to load a skill)
  - SKILL.md under the size ceiling
Checks, per command (commands/*.md):
  - frontmatter with a `description`
Checks, across skills, commands, and references:
  - no em-dashes (house style)
  - every http(s) URL is on the allowlist
  - no plan names or currency-prefixed prices (directory policy: skill text
    may not sell)
  - every backticked google_* / meta_* / ping tool name exists in
    scripts/tool-names.txt (a renamed tool must not leave a dead reference)

Exit 1 on any finding.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_MAX_BYTES = 8_000
ALLOWED_URLS = {
    "https://adplane.ai",
    "https://adplane.ai/accounts",
    "https://adplane.ai/docs",
}
TRIGGER_WORDS = ("Use when", "Use for", "Load for")
FORBIDDEN_PATTERNS = [
    (re.compile(r"—"), "em-dash"),
    (re.compile(r"\$\s?\d"), "currency-prefixed price"),
    (re.compile(r"\b(Pro|Plus|Max|Team|Enterprise|Starter|Free)\s+plan\b"), "plan name"),
    (re.compile(r"\b(upgrade|pricing|/billing)\b", re.I), "upsell wording"),
]
TOOL_REF = re.compile(r"`((?:google|meta)_[a-z_]+|ping)`")
URL = re.compile(r"https?://[^\s)\]>`\"']+")


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    block = text[4:end]
    out: dict[str, str] = {}
    key = None
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if m:
            key = m.group(1)
            out[key] = m.group(2).strip()
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def main() -> int:
    findings: list[str] = []
    tool_names = set((ROOT / "scripts" / "tool-names.txt").read_text().split())

    skill_files = sorted((ROOT / "skills").glob("*/SKILL.md"))
    command_files = sorted((ROOT / "commands").glob("*.md"))
    reference_files = sorted((ROOT / "skills").glob("*/references/*.md"))

    for path in skill_files:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        fm = frontmatter(text)
        if fm is None:
            findings.append(f"{rel}: missing frontmatter")
            continue
        if fm.get("name") != path.parent.name:
            findings.append(f"{rel}: frontmatter name {fm.get('name')!r} != directory {path.parent.name!r}")
        desc = fm.get("description", "")
        if not 50 <= len(desc) <= 1000:
            findings.append(f"{rel}: description length {len(desc)} outside 50..1000")
        if not any(w in desc for w in TRIGGER_WORDS):
            findings.append(f"{rel}: description lacks a trigger phrase ({', '.join(TRIGGER_WORDS)})")
        size = len(text.encode())
        if size > SKILL_MAX_BYTES:
            findings.append(f"{rel}: {size} bytes exceeds {SKILL_MAX_BYTES}")

    for path in command_files:
        fm = frontmatter(path.read_text())
        rel = path.relative_to(ROOT)
        if fm is None or not fm.get("description"):
            findings.append(f"{rel}: missing frontmatter description")

    for path in skill_files + command_files + reference_files:
        text = path.read_text()
        rel = path.relative_to(ROOT)
        for pattern, label in FORBIDDEN_PATTERNS:
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"{rel}:{line}: {label}: {m.group(0)!r}")
        for m in URL.finditer(text):
            url = m.group(0).rstrip(".,;:")
            if url not in ALLOWED_URLS:
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"{rel}:{line}: URL not on allowlist: {url}")
        for m in TOOL_REF.finditer(text):
            if m.group(1) not in tool_names:
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"{rel}:{line}: unknown tool name {m.group(1)}")

    if findings:
        print("\n".join(findings))
        print(f"\n{len(findings)} finding(s)")
        return 1
    print(f"ok: {len(skill_files)} skills, {len(command_files)} commands, {len(reference_files)} references")
    return 0


if __name__ == "__main__":
    sys.exit(main())

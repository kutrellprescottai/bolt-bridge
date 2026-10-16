#!/usr/bin/env python3
"""Validate Bolt skill files against Bolt's import rules.

Bolt's importer rejects a skill whose frontmatter is malformed, so run this
before every commit to the skills/ directory.

Usage:  python3 scripts/validate-skills.py [skills_dir]

Exit code 0 = every skill valid. 1 = at least one invalid.
"""
import os
import re
import sys
from typing import Optional

RESERVED = ("anthropic", "claude")
NAME_RE = re.compile(r"^[a-z0-9-]+$")
XML_RE = re.compile(r"</?[A-Za-z][^>]*>")
MAX_NAME = 64
MAX_DESC = 1024
MAX_FILE = 256 * 1024


def parse_frontmatter(text: str) -> tuple[Optional[dict], str, Optional[str]]:
    """Return (frontmatter, body, error). On failure frontmatter is None."""
    if not text.startswith("---"):
        return None, "", "file does not start with '---'"
    lines = text.split("\n")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, "", "frontmatter block is never closed with '---'"
    fm: dict = {}
    for raw in lines[1:end]:
        if not raw.strip():
            continue
        if ":" not in raw:
            return None, "", f"frontmatter line is not key: value -> {raw!r}"
        key, _, val = raw.partition(":")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            val = val[1:-1]
        fm[key] = val
    return fm, "\n".join(lines[end + 1:]), None


def check(path: str) -> list[str]:
    problems: list[str] = []
    size = os.path.getsize(path)
    if size > MAX_FILE:
        problems.append(f"file is {size} bytes, over the {MAX_FILE} byte limit")

    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    fm, body, err = parse_frontmatter(text)
    if err:
        return [err]
    assert fm is not None  # guaranteed when err is None

    keys = set(fm)
    if keys != {"name", "description"}:
        problems.append(
            f"frontmatter keys are {sorted(keys)}; must be exactly name + description"
        )

    name = fm.get("name", "")
    if not name:
        problems.append("missing 'name'")
    else:
        if not NAME_RE.match(name):
            problems.append(f"name {name!r} has chars outside [a-z0-9-]")
        if len(name) > MAX_NAME:
            problems.append(f"name is {len(name)} chars, over {MAX_NAME}")
        lowered = name.lower()
        for word in RESERVED:
            if word in lowered:
                problems.append(f"name contains reserved word {word!r}")

    desc = fm.get("description", "")
    if not desc:
        problems.append("missing 'description'")
    else:
        if len(desc) > MAX_DESC:
            problems.append(f"description is {len(desc)} chars, over {MAX_DESC}")
        if not desc.startswith("Use when"):
            problems.append("description must open with 'Use when'")
        if XML_RE.search(desc):
            problems.append("description contains XML tags")

    if not body.strip():
        problems.append("body is empty (no instructions)")

    folder = os.path.basename(os.path.dirname(path))
    if name and folder != name:
        problems.append(f"folder {folder!r} does not match name {name!r}")

    return problems


def main() -> int:
    root = sys.argv[1] if len(sys.argv) > 1 else "skills"
    found: list[str] = []
    for dirpath, _dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn in ("SKILL.md", "SKILL.mdx"):
                found.append(os.path.join(dirpath, fn))

    if not found:
        print(f"no SKILL.md files found under {root!r}")
        return 1

    bad = 0
    for path in sorted(found):
        problems = check(path)
        if problems:
            bad += 1
            print(f"FAIL  {path}")
            for p in problems:
                print(f"        - {p}")
        else:
            print(f"ok    {path}")

    print(f"\n{len(found) - bad}/{len(found)} valid")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

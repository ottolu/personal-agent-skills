#!/usr/bin/env python3
"""
Apply a candidate_description from an improvement report back into SKILL.md.
"""

import argparse
import json
import re
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description="Apply candidate description to SKILL.md")
    parser.add_argument("skill_path")
    parser.add_argument("report_json")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    skill_md = skill_path / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    report = load_json(Path(args.report_json))
    candidate = report.get("candidate_description", "").strip()
    if not candidate:
        raise SystemExit("No candidate_description found in report.")

    pattern = r"(^description:\s*)(.*?)(\n---)"
    new_text, count = re.subn(pattern, lambda m: m.group(1) + candidate + m.group(3), text, count=1, flags=re.DOTALL | re.MULTILINE)
    if count != 1:
        raise SystemExit("Could not replace description in SKILL.md frontmatter.")

    skill_md.write_text(new_text, encoding="utf-8")
    print(f"Applied candidate description to: {skill_md}")


if __name__ == "__main__":
    main()

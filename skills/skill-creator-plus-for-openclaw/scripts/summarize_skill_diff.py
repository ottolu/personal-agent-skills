#!/usr/bin/env python3
"""
Summarize differences between two skill directories.

This is a lightweight comparison helper for OpenClaw skill iteration. It does
not attempt semantic evaluation; it highlights file-level changes and flags
areas likely to affect triggering, workflow, or bundled resources.
"""

import argparse
import difflib
import json
from pathlib import Path

TEXT_EXTS = {".md", ".py", ".txt", ".json", ".yaml", ".yml"}


def list_files(root: Path):
    return {
        str(p.relative_to(root))
        for p in root.rglob("*")
        if p.is_file() and not p.name.endswith(".skill") and ".git" not in p.parts
    }


def classify_path(rel: str) -> list[str]:
    tags = []
    if rel == "SKILL.md":
        tags.extend(["front-door", "workflow-or-trigger"])
    if rel.startswith("references/"):
        tags.append("reference-layer")
    if rel.startswith("scripts/"):
        tags.append("script-layer")
    if rel.startswith("assets/"):
        tags.append("asset-layer")
    if "eval" in rel:
        tags.append("eval-related")
    return tags


def unified_preview(old_file: Path, new_file: Path, max_lines: int = 40) -> list[str]:
    try:
        old_text = old_file.read_text(encoding="utf-8").splitlines()
        new_text = new_file.read_text(encoding="utf-8").splitlines()
    except Exception:
        return ["<binary-or-unreadable>"]
    diff = list(difflib.unified_diff(old_text, new_text, fromfile=str(old_file), tofile=str(new_file), lineterm=""))
    return diff[:max_lines]


def main():
    parser = argparse.ArgumentParser(description="Summarize differences between two skill directories")
    parser.add_argument("old_skill", help="Path to old skill directory")
    parser.add_argument("new_skill", help="Path to new skill directory")
    parser.add_argument("--output", help="Optional path to write JSON summary")
    args = parser.parse_args()

    old_root = Path(args.old_skill).resolve()
    new_root = Path(args.new_skill).resolve()

    old_files = list_files(old_root)
    new_files = list_files(new_root)

    added = sorted(new_files - old_files)
    removed = sorted(old_files - new_files)
    common = sorted(old_files & new_files)

    changed = []
    for rel in common:
        old_file = old_root / rel
        new_file = new_root / rel
        if old_file.suffix.lower() in TEXT_EXTS and new_file.suffix.lower() in TEXT_EXTS:
            try:
                if old_file.read_text(encoding="utf-8") != new_file.read_text(encoding="utf-8"):
                    changed.append(rel)
            except Exception:
                changed.append(rel)
        else:
            if old_file.stat().st_size != new_file.stat().st_size:
                changed.append(rel)

    summary = {
        "old_skill": str(old_root),
        "new_skill": str(new_root),
        "counts": {
            "added": len(added),
            "removed": len(removed),
            "changed": len(changed),
        },
        "added": [{"path": rel, "tags": classify_path(rel)} for rel in added],
        "removed": [{"path": rel, "tags": classify_path(rel)} for rel in removed],
        "changed": [
            {
                "path": rel,
                "tags": classify_path(rel),
                "preview": unified_preview(old_root / rel, new_root / rel),
            }
            for rel in changed
        ],
    }

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote diff summary to: {output_path}")
    else:
        print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate a starter evals.json for OpenClaw skill iteration.

This script is intentionally simple: it creates a structured skeleton that
matches references/eval-schemas.md, without pretending to fully automate eval
design.
"""

import argparse
import json
from pathlib import Path

DEFAULT_EVALS = {
    "draft-only": [
        {
            "name": "core-draft",
            "goal": "Checks that the first draft has a coherent SKILL.md, usable description, and sensible file split.",
            "expectations": [
                "Produces a valid SKILL.md structure",
                "Description includes concrete trigger contexts",
                "Avoids obvious placeholder or TODO leakage"
            ],
            "tags": ["core", "draft"],
            "priority": "high"
        },
        {
            "name": "near-miss-trigger",
            "goal": "Checks that the skill description does not overclaim adjacent tasks.",
            "expectations": [
                "The draft implies a clear scope boundary",
                "Description does not read as universally applicable"
            ],
            "tags": ["trigger", "boundary"],
            "priority": "medium"
        }
    ],
    "structured-build": [
        {
            "name": "core-happy-path",
            "goal": "Checks that the skill draft covers routing, structure, and user-relevant workflow guidance.",
            "expectations": [
                "Produces a valid SKILL.md structure",
                "Uses references for heavy details instead of bloating SKILL.md",
                "Description includes concrete trigger contexts"
            ],
            "tags": ["core", "build"],
            "priority": "high"
        },
        {
            "name": "resource-justification",
            "goal": "Checks that scripts and references exist for a reason, not for show.",
            "expectations": [
                "Bundled resources provide clear leverage",
                "No obvious dead-weight resource files"
            ],
            "tags": ["resources"],
            "priority": "medium"
        }
    ],
    "eval-first": [
        {
            "name": "eval-quality-check",
            "goal": "Checks that the eval set is realistic and discriminating.",
            "expectations": [
                "Includes realistic prompts",
                "Includes at least one nontrivial expectation",
                "Includes at least one failure-mode or near-miss eval"
            ],
            "tags": ["evals"],
            "priority": "high"
        }
    ],
    "refactor-and-upgrade": [
        {
            "name": "upgrade-retains-purpose",
            "goal": "Checks that the revised skill remains faithful to the original intent while improving structure or clarity.",
            "expectations": [
                "Core purpose of the skill is preserved",
                "Workflow coherence improves or stays strong",
                "Description becomes clearer or more discriminating"
            ],
            "tags": ["upgrade", "comparison"],
            "priority": "high"
        }
    ],
    "package-and-polish": [
        {
            "name": "release-readiness",
            "goal": "Checks that the skill is coherent, validated, and ready for packaging.",
            "expectations": [
                "No placeholder TODO text remains",
                "Description clearly states what the skill does and when to use it",
                "References and scripts are justified"
            ],
            "tags": ["release"],
            "priority": "high"
        }
    ]
}


def build_skeleton(skill_name: str, mode: str) -> dict:
    templates = DEFAULT_EVALS.get(mode, DEFAULT_EVALS["structured-build"])
    evals = []
    for idx, item in enumerate(templates, start=1):
        evals.append(
            {
                "id": idx,
                "name": item["name"],
                "prompt": f"<replace with a realistic user prompt for {skill_name}>",
                "goal": item["goal"],
                "files": [],
                "expectations": item["expectations"],
                "tags": item["tags"],
                "priority": item["priority"],
            }
        )
    return {"skill_name": skill_name, "mode": mode, "evals": evals}


def main():
    parser = argparse.ArgumentParser(description="Generate a starter evals.json skeleton")
    parser.add_argument("skill_name", help="Skill name under evaluation")
    parser.add_argument("--mode", default="structured-build", help="draft-only|structured-build|eval-first|refactor-and-upgrade|package-and-polish")
    parser.add_argument("--output", required=True, help="Path to output evals.json")
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_skeleton(args.skill_name, args.mode)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote eval skeleton to: {output_path}")


if __name__ == "__main__":
    main()

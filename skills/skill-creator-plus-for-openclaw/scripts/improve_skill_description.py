#!/usr/bin/env python3
"""
Lightweight OpenClaw-compatible description improver.

Input: a skill path plus a JSON file of should-trigger / should-not-trigger cases.
Output: a structured recommendation for rewriting the SKILL.md description.

This is not Anthropic's exact trigger-eval harness. It is a practical substitute
that helps teams reason about trigger coverage and boundary quality.
"""

import argparse
import json
import re
from pathlib import Path


def read_skill_md(skill_path: Path) -> str:
    return (skill_path / "SKILL.md").read_text(encoding="utf-8")


def extract_frontmatter_description(skill_md: str) -> str:
    m = re.search(r"^---\n.*?^description:\s*(.*?)\n---", skill_md, re.DOTALL | re.MULTILINE)
    return m.group(1).strip() if m else ""


def load_cases(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return data
    return data.get("cases", [])


def summarize_cases(cases):
    should = [c for c in cases if c.get("should_trigger") is True]
    should_not = [c for c in cases if c.get("should_trigger") is False]
    return should, should_not


def infer_patterns(cases):
    phrases = []
    for c in cases:
        q = c.get("query", "")
        q = q.replace("\n", " ").strip()
        if q:
            phrases.append(q[:140])
    return phrases[:8]


def build_recommendation(current_description: str, should, should_not):
    should_examples = infer_patterns(should)
    should_not_examples = infer_patterns(should_not)

    missing_signals = []
    if "Use when" not in current_description and "use when" not in current_description.lower():
        missing_signals.append("description does not explicitly state when to use the skill")
    if len(current_description) < 120:
        missing_signals.append("description is likely too short to encode trigger boundaries well")
    if not any(word in current_description.lower() for word in ["create", "improve", "evaluate", "package", "refactor", "optimize"]):
        missing_signals.append("description may not enumerate the major actions this skill supports")

    recommendation = {
        "current_description": current_description,
        "analysis": {
            "should_trigger_count": len(should),
            "should_not_trigger_count": len(should_not),
            "should_trigger_examples": should_examples,
            "should_not_trigger_examples": should_not_examples,
            "likely_gaps": missing_signals,
        },
        "rewrite_guidance": [
            "State what the skill does in action terms, not just domain terms.",
            "Include explicit 'use when' trigger contexts.",
            "Mention adjacent user phrasings that should still trigger the skill.",
            "Avoid sounding universally applicable; preserve boundaries against near-miss tasks.",
        ],
        "candidate_description": "[Rewrite this using the guidance and the should-trigger / should-not-trigger cases above.]"
    }

    verbs = []
    for word in ["create", "improve", "evaluate", "benchmark", "package", "refactor", "optimize"]:
        if any(word in ex.lower() for ex in should_examples):
            verbs.append(word)
    if not verbs:
        verbs = ["create", "improve", "evaluate"]

    scope = ", ".join(verbs[:5])
    recommendation["candidate_description"] = (
        f"{scope.capitalize()} OpenClaw-compatible skills with structured iteration loops, eval design, review artifacts, and packaging guidance. "
        f"Use when building a new skill, improving an existing skill, designing evals, comparing skill revisions, or tightening trigger descriptions and release readiness."
    )
    return recommendation


def main():
    parser = argparse.ArgumentParser(description="Improve a skill description using trigger case analysis")
    parser.add_argument("skill_path")
    parser.add_argument("cases_json")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    current = extract_frontmatter_description(read_skill_md(skill_path))
    cases = load_cases(Path(args.cases_json))
    should, should_not = summarize_cases(cases)
    recommendation = build_recommendation(current, should, should_not)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(recommendation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote description improvement report to: {output_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate iteration-review.json from one or more grading.json files.

This is a lightweight OpenClaw-compatible helper: it aggregates grading outputs,
turns them into rubric-oriented scores, and produces a starter iteration review
that humans can further refine.
"""

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def clamp_score(x: float) -> int:
    return max(1, min(5, round(x)))


def pass_rate_to_score(rate: float) -> int:
    return clamp_score(1 + 4 * rate)


def summarize_gradings(grading_files):
    total_passed = total_failed = total_total = 0
    strengths = []
    weaknesses = []
    uncertainties = []
    eval_feedback = []

    for gf in grading_files:
        data = load_json(gf)
        summary = data.get("summary", {})
        total_passed += int(summary.get("passed", 0))
        total_failed += int(summary.get("failed", 0))
        total_total += int(summary.get("total", 0))

        qn = data.get("quality_notes", {})
        strengths.extend(qn.get("strengths", []))
        weaknesses.extend(qn.get("weaknesses", []))
        uncertainties.extend(qn.get("uncertainties", []))

        ef = data.get("eval_feedback", {})
        for item in ef.get("suggestions", []):
            reason = item.get("reason")
            if reason:
                eval_feedback.append(reason)

    pass_rate = (total_passed / total_total) if total_total else 0.0
    return {
        "passed": total_passed,
        "failed": total_failed,
        "total": total_total,
        "pass_rate": pass_rate,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "uncertainties": uncertainties,
        "eval_feedback": eval_feedback,
    }


def build_review(skill_name: str, iteration: str, agg: dict) -> dict:
    pass_score = pass_rate_to_score(agg["pass_rate"])
    weak_count = len(agg["weaknesses"])
    uncertainty_count = len(agg["uncertainties"])
    feedback_count = len(agg["eval_feedback"])

    review = {
        "iteration": iteration,
        "skill_name": skill_name,
        "summary": {
            "what_improved": agg["strengths"][:5],
            "what_regressed": agg["weaknesses"][:5],
            "open_issues": agg["uncertainties"][:5] or agg["eval_feedback"][:5],
        },
        "scores": {
            "trigger_clarity": pass_score,
            "workflow_coherence": pass_score if weak_count < 3 else max(1, pass_score - 1),
            "output_usefulness": pass_score,
            "evidence_of_real_leverage": pass_score if agg["strengths"] else 2,
            "overfitting_risk": 3 if feedback_count == 0 else 2,
            "evaluation_quality": max(1, min(5, 5 - feedback_count)) if feedback_count else 4,
        },
        "benchmark_notes": [
            f"Aggregated pass rate: {agg['passed']}/{agg['total']} ({agg['pass_rate']:.0%})",
            f"Observed weaknesses: {weak_count}",
            f"Observed uncertainties: {uncertainty_count}",
        ],
        "next_actions": [],
    }

    if agg["eval_feedback"]:
        review["next_actions"].append("Improve non-discriminating or weak eval expectations")
    if agg["weaknesses"]:
        review["next_actions"].append("Revise workflow/description based on recorded weaknesses")
    if not review["next_actions"]:
        review["next_actions"].append("Run another iteration with harder near-miss evals")

    return review


def main():
    parser = argparse.ArgumentParser(description="Generate iteration-review.json from grading files")
    parser.add_argument("skill_name")
    parser.add_argument("iteration")
    parser.add_argument("grading_files", nargs="+", help="One or more grading.json files")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    grading_paths = [Path(p) for p in args.grading_files]
    agg = summarize_gradings(grading_paths)
    review = build_review(args.skill_name, args.iteration, agg)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote iteration review to: {output_path}")


if __name__ == "__main__":
    main()

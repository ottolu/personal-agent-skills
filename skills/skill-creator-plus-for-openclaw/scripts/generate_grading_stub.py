#!/usr/bin/env python3
"""
Generate grading stub files from evals.json.

Useful when the actual run/evaluation will be done manually or by a separate
agent, but you still want the grading artifacts to conform to the OpenClaw
skill-iteration schema.
"""

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def make_stub(expectations):
    return {
        "expectations": [
            {"text": exp, "passed": False, "evidence": "<fill with evidence after review>"}
            for exp in expectations
        ],
        "summary": {"passed": 0, "failed": len(expectations), "total": len(expectations), "pass_rate": 0.0},
        "quality_notes": {"strengths": [], "weaknesses": [], "uncertainties": []},
        "eval_feedback": {"suggestions": [], "overall": "<fill after review>"},
    }


def main():
    parser = argparse.ArgumentParser(description="Generate grading stubs from evals.json")
    parser.add_argument("evals_json")
    parser.add_argument("--workspace", required=True, help="Iteration workspace root")
    args = parser.parse_args()

    evals = load_json(Path(args.evals_json)).get("evals", [])
    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    for item in evals:
        eval_name = item.get("name", f"eval-{item.get('id', 'unknown')}")
        eval_dir = workspace / eval_name
        eval_dir.mkdir(parents=True, exist_ok=True)
        grading_path = eval_dir / "grading.stub.json"
        grading_path.write_text(json.dumps(make_stub(item.get("expectations", [])), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote grading stub: {grading_path}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Set up a lightweight OpenClaw skill-eval workspace from evals.json.

This is not a full Anthropic-style automated harness. It creates a clean
iteration directory, per-eval folders, run-record.json files, and grading
stubs so execution/review can happen in a disciplined way.
"""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def safe_name(name: str) -> str:
    return "-".join(name.strip().lower().split()) if name.strip() else "unnamed-eval"


def main():
    parser = argparse.ArgumentParser(description="Create an OpenClaw skill-eval iteration workspace")
    parser.add_argument("evals_json")
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--workspace", required=True, help="Workspace root for all iterations")
    parser.add_argument("--iteration", default=None, help="Explicit iteration name, e.g. iteration-1")
    parser.add_argument("--configuration", default="with_skill", help="with_skill|without_skill|old_skill|candidate_skill")
    args = parser.parse_args()

    eval_data = load_json(Path(args.evals_json))
    skill_name = eval_data.get("skill_name", Path(args.skill_path).name)
    evals = eval_data.get("evals", [])

    workspace_root = Path(args.workspace)
    workspace_root.mkdir(parents=True, exist_ok=True)

    iteration = args.iteration
    if not iteration:
        existing = [p.name for p in workspace_root.iterdir() if p.is_dir() and p.name.startswith("iteration-")]
        nums = []
        for name in existing:
            try:
                nums.append(int(name.split("-")[-1]))
            except Exception:
                pass
        iteration = f"iteration-{(max(nums) + 1) if nums else 1}"

    iteration_dir = workspace_root / iteration
    iteration_dir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "skill_name": skill_name,
        "skill_path": str(Path(args.skill_path).resolve()),
        "evals_json": str(Path(args.evals_json).resolve()),
        "configuration": args.configuration,
        "created_at": utc_now(),
        "iteration": iteration,
        "eval_count": len(evals),
    }
    (iteration_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for item in evals:
        eval_name = safe_name(item.get("name") or f"eval-{item.get('id', 'unknown')}")
        eval_dir = iteration_dir / eval_name
        outputs_dir = eval_dir / "outputs"
        outputs_dir.mkdir(parents=True, exist_ok=True)

        run_record = {
            "eval_id": item.get("id"),
            "eval_name": item.get("name", eval_name),
            "iteration": iteration,
            "configuration": args.configuration,
            "prompt": item.get("prompt", ""),
            "artifacts": {
                "skill_path": str(Path(args.skill_path).resolve()),
                "outputs_dir": str(outputs_dir.resolve()),
            },
            "notes": [
                f"Goal: {item.get('goal', '')}",
                f"Priority: {item.get('priority', 'unknown')}",
            ],
            "status": "prepared",
        }
        (eval_dir / "run-record.json").write_text(json.dumps(run_record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        grading_stub = {
            "expectations": [
                {"text": exp, "passed": False, "evidence": "<fill with evidence after review>"}
                for exp in item.get("expectations", [])
            ],
            "summary": {
                "passed": 0,
                "failed": len(item.get("expectations", [])),
                "total": len(item.get("expectations", [])),
                "pass_rate": 0.0,
            },
            "quality_notes": {"strengths": [], "weaknesses": [], "uncertainties": []},
            "eval_feedback": {"suggestions": [], "overall": "<fill after review>"},
        }
        (eval_dir / "grading.stub.json").write_text(json.dumps(grading_stub, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        prompt_note = {
            "eval_id": item.get("id"),
            "name": item.get("name", eval_name),
            "goal": item.get("goal", ""),
            "prompt": item.get("prompt", ""),
            "expectations": item.get("expectations", []),
            "files": item.get("files", []),
            "tags": item.get("tags", []),
        }
        (eval_dir / "eval-input.json").write_text(json.dumps(prompt_note, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    history_path = workspace_root / "history.json"
    if history_path.exists():
        history = load_json(history_path)
    else:
        history = {
            "started_at": utc_now(),
            "skill_name": skill_name,
            "current_best": iteration,
            "iterations": [],
        }
    history["iterations"].append({
        "version": iteration,
        "parent": history["iterations"][-1]["version"] if history.get("iterations") else None,
        "pass_rate": 0.0,
        "result": "prepared",
        "is_current_best": len(history["iterations"]) == 0,
    })
    if not history.get("current_best"):
        history["current_best"] = iteration
    history_path.write_text(json.dumps(history, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Prepared iteration workspace: {iteration_dir}")
    print(f"Manifest: {iteration_dir / 'manifest.json'}")
    print(f"History: {history_path}")


if __name__ == "__main__":
    main()

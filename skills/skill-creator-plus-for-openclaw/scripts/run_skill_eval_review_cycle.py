#!/usr/bin/env python3
"""
Run a lightweight OpenClaw skill eval + review cycle.

This orchestrates existing helper scripts:
- generate iteration workspace
- generate grading stubs
- optionally ingest completed grading.json files
- generate iteration review
- aggregate benchmark summary

It does not execute the model task itself. It prepares and closes the loop around
artifacts so OpenClaw users can run disciplined iterations without Anthropic's
full proprietary harness.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def find_iteration_dir(workspace: Path, iteration: str | None):
    if iteration:
        return workspace / iteration
    candidates = [p for p in workspace.iterdir() if p.is_dir() and p.name.startswith("iteration-")]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name)[-1]


def main():
    parser = argparse.ArgumentParser(description="Run an OpenClaw skill eval/review cycle")
    parser.add_argument("skill_name")
    parser.add_argument("evals_json")
    parser.add_argument("--skill-path", required=True)
    parser.add_argument("--workspace", required=True)
    parser.add_argument("--configuration", default="with_skill")
    parser.add_argument("--iteration", default=None)
    parser.add_argument("--finalize", action="store_true", help="Generate iteration review + benchmark summary from completed grading.json files")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    workspace = Path(args.workspace)
    workspace.mkdir(parents=True, exist_ok=True)

    if not args.finalize:
        run([
            sys.executable,
            str(script_dir / "run_openclaw_skill_eval.py"),
            args.evals_json,
            "--skill-path", args.skill_path,
            "--workspace", args.workspace,
            "--configuration", args.configuration,
            *( ["--iteration", args.iteration] if args.iteration else [] ),
        ])
        print("Prepared eval/review cycle workspace. Next: run the evals, fill grading.json files, then rerun with --finalize.")
        return

    iteration_dir = find_iteration_dir(workspace, args.iteration)
    if iteration_dir is None:
        raise SystemExit("No iteration directory found to finalize.")

    grading_files = sorted(iteration_dir.rglob("grading.json"))
    if not grading_files:
        raise SystemExit("No grading.json files found under iteration directory. Finalization requires completed grading files.")

    review_path = iteration_dir / "iteration-review.json"
    run([
        sys.executable,
        str(script_dir / "generate_iteration_review.py"),
        args.skill_name,
        iteration_dir.name,
        *[str(p) for p in grading_files],
        "--output", str(review_path),
    ])

    bench_path = iteration_dir / "benchmark-summary.json"
    bench_inputs = [f"{args.configuration}={p}" for p in grading_files] + [f"candidate={review_path}"]
    run([
        sys.executable,
        str(script_dir / "aggregate_benchmark_summary.py"),
        args.skill_name,
        *bench_inputs,
        "--output", str(bench_path),
    ])

    print(f"Finalized cycle for {iteration_dir}")
    print(f"Iteration review: {review_path}")
    print(f"Benchmark summary: {bench_path}")


if __name__ == "__main__":
    main()

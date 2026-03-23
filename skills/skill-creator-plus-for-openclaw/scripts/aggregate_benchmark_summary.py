#!/usr/bin/env python3
"""
Aggregate multiple grading or iteration-review files into benchmark-summary.json.

This intentionally avoids Anthropic viewer lock-in. It produces a lightweight
summary suitable for OpenClaw skill iteration and comparison.
"""

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def mean(values):
    return sum(values) / len(values) if values else 0.0


def stddev(values):
    if len(values) <= 1:
        return 0.0
    m = mean(values)
    return math.sqrt(sum((v - m) ** 2 for v in values) / len(values))


def parse_input(path: Path):
    data = load_json(path)
    if "summary" in data and "expectations" in data:
        pass_rate = float(data.get("summary", {}).get("pass_rate", 0.0))
        review_score = 0.0
        return pass_rate, review_score
    if "scores" in data:
        scores = data.get("scores", {})
        vals = [float(v) for v in scores.values()] if scores else [0.0]
        review_score = mean(vals)
        return 0.0, review_score
    return 0.0, 0.0


def main():
    parser = argparse.ArgumentParser(description="Aggregate benchmark summary from files")
    parser.add_argument("skill_name")
    parser.add_argument("inputs", nargs="+", help="Format: configuration=path")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    buckets = defaultdict(lambda: {"pass_rate": [], "review_score": []})
    for item in args.inputs:
        if "=" not in item:
            raise SystemExit(f"Invalid input '{item}', expected configuration=path")
        config, path_str = item.split("=", 1)
        path = Path(path_str)
        pass_rate, review_score = parse_input(path)
        if pass_rate:
            buckets[config]["pass_rate"].append(pass_rate)
        if review_score:
            buckets[config]["review_score"].append(review_score)

    run_summary = {}
    for config, data in buckets.items():
        run_summary[config] = {
            "pass_rate": {
                "mean": round(mean(data["pass_rate"]), 4),
                "stddev": round(stddev(data["pass_rate"]), 4),
            },
            "review_score": {
                "mean": round(mean(data["review_score"]), 4),
                "stddev": round(stddev(data["review_score"]), 4),
            },
        }

    configs = list(run_summary.keys())
    delta = {}
    if len(configs) >= 2:
        a, b = configs[0], configs[1]
        delta = {
            "pass_rate": f"{run_summary[a]['pass_rate']['mean'] - run_summary[b]['pass_rate']['mean']:+.4f}",
            "review_score": f"{run_summary[a]['review_score']['mean'] - run_summary[b]['review_score']['mean']:+.4f}",
            "basis": f"{a} minus {b}",
        }

    payload = {
        "metadata": {
            "skill_name": args.skill_name,
            "configurations": configs,
        },
        "run_summary": run_summary,
        "delta": delta,
        "notes": [],
    }

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote benchmark summary to: {output_path}")


if __name__ == "__main__":
    main()

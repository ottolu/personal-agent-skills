#!/usr/bin/env python3
"""
Grade a prepared/executed OpenClaw eval directory into grading.json.

This is a lightweight grader. It uses simple textual heuristics over:
- eval-input.json
- transcript.md
- files in outputs/

It is intentionally conservative and evidence-oriented, inspired by Anthropic
Skill Creator 2.0's grader philosophy, but without pretending to solve fully
general semantic evaluation.
"""

import argparse
import json
from pathlib import Path


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_if_exists(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def gather_outputs_text(outputs_dir: Path) -> tuple[str, list[str]]:
    texts = []
    files = []
    if outputs_dir.exists():
        for p in sorted(outputs_dir.rglob("*")):
            if p.is_file():
                files.append(str(p.name))
                try:
                    texts.append(f"\n--- FILE: {p.name} ---\n" + p.read_text(encoding="utf-8", errors="replace"))
                except Exception:
                    texts.append(f"\n--- FILE: {p.name} ---\n<unreadable>")
    return "\n".join(texts), files


def judge_expectation(expectation: str, corpus: str, output_files: list[str], transcript: str):
    exp = expectation.strip()
    exp_lower = exp.lower()
    evidence = "No direct evidence found."
    passed = False

    if "valid skill.md structure" in exp_lower or "valid skill" in exp_lower:
        passed = "skill.md" in corpus.lower() or "skill.md" in transcript.lower()
        evidence = "Found mention of SKILL.md in outputs/transcript." if passed else evidence
    elif "description" in exp_lower and "trigger" in exp_lower:
        passed = ("description" in corpus.lower() or "description" in transcript.lower()) and ("trigger" in corpus.lower() or "use when" in corpus.lower() or "trigger" in transcript.lower())
        evidence = "Found description/trigger-related text in outputs/transcript." if passed else evidence
    elif "references" in exp_lower:
        passed = any("references" in f.lower() for f in output_files) or "references/" in corpus or "references/" in transcript
        evidence = "Found references-layer evidence in files or transcript." if passed else evidence
    elif "todo" in exp_lower or "placeholder" in exp_lower:
        passed = "todo" not in corpus.lower() and "todo" not in transcript.lower()
        evidence = "No TODO leakage found in outputs/transcript." if passed else "Found TODO-like text or insufficient evidence."
    elif "scripts" in exp_lower:
        passed = any("script" in f.lower() or f.endswith(".py") for f in output_files) or "scripts/" in corpus or "scripts/" in transcript
        evidence = "Found script-related evidence in outputs/transcript." if passed else evidence
    else:
        # fallback heuristic: require at least one substantial keyword hit
        keywords = [w for w in exp_lower.replace("/", " ").replace("-", " ").split() if len(w) >= 5]
        hits = [kw for kw in keywords if kw in corpus.lower() or kw in transcript.lower()]
        passed = len(hits) >= 1
        if hits:
            evidence = f"Matched keywords in corpus/transcript: {', '.join(hits[:5])}"

    return {"text": exp, "passed": passed, "evidence": evidence}


def main():
    parser = argparse.ArgumentParser(description="Grade one OpenClaw eval directory")
    parser.add_argument("eval_dir", help="Path to one eval directory containing eval-input.json")
    parser.add_argument("--output", default=None, help="Path to grading.json (default: eval_dir/grading.json)")
    args = parser.parse_args()

    eval_dir = Path(args.eval_dir)
    eval_input = load_json(eval_dir / "eval-input.json")
    transcript = read_text_if_exists(eval_dir / "transcript.md")
    outputs_text, output_files = gather_outputs_text(eval_dir / "outputs")
    corpus = outputs_text

    expectations = eval_input.get("expectations", [])
    graded = [judge_expectation(exp, corpus, output_files, transcript) for exp in expectations]

    passed = sum(1 for item in graded if item["passed"])
    total = len(graded)
    failed = total - passed

    quality_notes = {
        "strengths": [],
        "weaknesses": [],
        "uncertainties": [],
    }
    if passed:
        quality_notes["strengths"].append(f"Passed {passed} expectation(s).")
    if failed:
        quality_notes["weaknesses"].append(f"Failed {failed} expectation(s).")
    if not output_files:
        quality_notes["uncertainties"].append("No output files were found; grading relied mainly on transcript evidence.")

    weak_assertions = []
    for item in graded:
        if item["passed"] and item["evidence"].startswith("Matched keywords"):
            weak_assertions.append({
                "assertion": item["text"],
                "reason": "This pass relied on weak keyword evidence; consider a more discriminating expectation."
            })

    payload = {
        "expectations": graded,
        "summary": {
            "passed": passed,
            "failed": failed,
            "total": total,
            "pass_rate": (passed / total) if total else 0.0,
        },
        "quality_notes": quality_notes,
        "eval_feedback": {
            "suggestions": weak_assertions,
            "overall": "Auto-graded with heuristic evidence. Human review is still recommended for high-stakes skill changes."
        }
    }

    output_path = Path(args.output) if args.output else (eval_dir / "grading.json")
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote grading file: {output_path}")


if __name__ == "__main__":
    main()

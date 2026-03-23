#!/usr/bin/env python3
"""
Execute a lightweight OpenClaw skill eval run from a prepared iteration workspace.

This script does not replicate Anthropic's proprietary harness. Instead, it:
- reads prepared eval directories
- writes execution manifests and transcripts placeholders
- optionally runs a user-provided command template per eval
- captures stdout/stderr and marks run status

The goal is to make the middle of the eval loop real and inspectable.
"""

import argparse
import json
import shlex
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def render_command(template: str, eval_input: dict, outputs_dir: Path) -> str:
    values = {
        "prompt": eval_input.get("prompt", ""),
        "goal": eval_input.get("goal", ""),
        "name": eval_input.get("name", ""),
        "outputs_dir": str(outputs_dir.resolve()),
        "files": " ".join(eval_input.get("files", [])),
    }
    return template.format(**values)


def execute_eval(eval_dir: Path, command_template: str | None):
    eval_input = load_json(eval_dir / "eval-input.json")
    run_record_path = eval_dir / "run-record.json"
    run_record = load_json(run_record_path)
    outputs_dir = eval_dir / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    transcript_path = eval_dir / "transcript.md"
    execution_manifest = {
        "started_at": utc_now(),
        "eval_name": eval_input.get("name"),
        "prompt": eval_input.get("prompt"),
        "goal": eval_input.get("goal"),
        "command_template": command_template,
        "status": "running",
    }
    write_json(eval_dir / "execution.json", execution_manifest)

    transcript_lines = [
        f"# Eval Transcript: {eval_input.get('name', eval_dir.name)}",
        "",
        f"- started_at: {execution_manifest['started_at']}",
        f"- goal: {eval_input.get('goal', '')}",
        f"- prompt: {eval_input.get('prompt', '')}",
        "",
    ]

    if not command_template:
        transcript_lines.append("## Status")
        transcript_lines.append("No executor command template was supplied. Workspace prepared for manual execution.")
        execution_manifest["status"] = "manual"
        execution_manifest["finished_at"] = utc_now()
        run_record["status"] = "manual-execution-required"
        write_json(eval_dir / "execution.json", execution_manifest)
        write_json(run_record_path, run_record)
        transcript_path.write_text("\n".join(transcript_lines) + "\n", encoding="utf-8")
        return

    cmd = render_command(command_template, eval_input, outputs_dir)
    transcript_lines.append("## Command")
    transcript_lines.append("```bash")
    transcript_lines.append(cmd)
    transcript_lines.append("```")
    transcript_lines.append("")

    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    transcript_lines.append("## STDOUT")
    transcript_lines.append("```")
    transcript_lines.append(proc.stdout or "")
    transcript_lines.append("```")
    transcript_lines.append("")
    transcript_lines.append("## STDERR")
    transcript_lines.append("```")
    transcript_lines.append(proc.stderr or "")
    transcript_lines.append("```")
    transcript_lines.append("")
    transcript_lines.append(f"## Exit Code\n{proc.returncode}")

    execution_manifest["finished_at"] = utc_now()
    execution_manifest["status"] = "completed" if proc.returncode == 0 else "failed"
    execution_manifest["exit_code"] = proc.returncode
    execution_manifest["stdout_path"] = str((eval_dir / "stdout.txt").resolve())
    execution_manifest["stderr_path"] = str((eval_dir / "stderr.txt").resolve())

    (eval_dir / "stdout.txt").write_text(proc.stdout or "", encoding="utf-8")
    (eval_dir / "stderr.txt").write_text(proc.stderr or "", encoding="utf-8")
    transcript_path.write_text("\n".join(transcript_lines) + "\n", encoding="utf-8")
    write_json(eval_dir / "execution.json", execution_manifest)

    run_record["status"] = "completed" if proc.returncode == 0 else "execution-failed"
    run_record.setdefault("notes", []).append(f"Execution status: {execution_manifest['status']}")
    write_json(run_record_path, run_record)


def main():
    parser = argparse.ArgumentParser(description="Execute prepared evals in an iteration workspace")
    parser.add_argument("workspace", help="Iteration directory, e.g. /tmp/foo/iteration-1")
    parser.add_argument("--command-template", default=None,
                        help="Shell template with placeholders: {prompt} {goal} {name} {outputs_dir} {files}")
    parser.add_argument("--eval", default=None, help="Only execute one eval directory name")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        raise SystemExit(f"Workspace not found: {workspace}")

    eval_dirs = [p for p in workspace.iterdir() if p.is_dir() and (p / "eval-input.json").exists()]
    if args.eval:
        eval_dirs = [p for p in eval_dirs if p.name == args.eval]
    if not eval_dirs:
        raise SystemExit("No prepared eval directories found.")

    for eval_dir in sorted(eval_dirs):
        execute_eval(eval_dir, args.command_template)
        print(f"Executed eval dir: {eval_dir}")


if __name__ == "__main__":
    main()

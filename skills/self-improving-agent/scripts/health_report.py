#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None  # type: ignore


TZ = ZoneInfo("Asia/Shanghai") if ZoneInfo else None
ENTRY_HEADER_RE = re.compile(r"^## \[(?P<id>[A-Z]+-\d{8}-[A-Z0-9]+)\] (?P<slug>.+)$")
FIELD_RE = re.compile(r"^\*\*(?P<key>[^*]+)\*\*:\s*(?P<value>.*)$")
REVIEW_FILE_RE = re.compile(r"^(Weekly Review|Promotion Log) - (?P<date>\d{4}-\d{2}-\d{2})\.md$")


@dataclass
class Entry:
    entry_id: str
    slug: str
    logged_at: datetime | None
    status: str
    priority: str
    area: str
    summary: str
    source_file: str


@dataclass
class FileStats:
    name: str
    path: Path
    total: int
    new_7d: int
    new_14d: int
    last_logged_at: datetime | None
    statuses: dict[str, int]
    entries: list[Entry]


@dataclass
class CronJobSummary:
    name: str
    enabled: bool
    next_run_at: datetime | None
    last_run_at: datetime | None
    last_status: str
    consecutive_errors: int


@dataclass
class ReviewArtifact:
    kind: str
    path: Path
    artifact_date: datetime


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a lightweight self-improving-agent health report for an OpenClaw workspace."
    )
    parser.add_argument(
        "--workspace",
        default=os.path.expanduser("~/.openclaw/workspace"),
        help="OpenClaw workspace path (default: ~/.openclaw/workspace)",
    )
    parser.add_argument(
        "--output",
        help="Write the markdown report to this path. Defaults to reports/self-improvement/Health Report - YYYY-MM-DD.md inside the workspace.",
    )
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Print the markdown report to stdout as well.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON summary to stdout instead of markdown.",
    )
    parser.add_argument(
        "--skip-cron",
        action="store_true",
        help="Do not query `openclaw cron list --json`.",
    )
    return parser.parse_args()


def now_local() -> datetime:
    if TZ:
        return datetime.now(TZ)
    return datetime.now().astimezone()


def ensure_tz(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=TZ) if TZ else dt.astimezone()
    return dt.astimezone(TZ) if TZ else dt.astimezone()


def parse_iso_datetime(value: str) -> datetime | None:
    value = value.strip()
    if not value or value.lower() in {"none", "n/a", "unknown"}:
        return None
    try:
        return ensure_tz(datetime.fromisoformat(value))
    except ValueError:
        return None


def format_dt(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return ensure_tz(dt).strftime("%Y-%m-%d %H:%M %Z")


def format_date(dt: datetime | None) -> str:
    if dt is None:
        return "—"
    return ensure_tz(dt).strftime("%Y-%m-%d")


def format_age(dt: datetime | None, now: datetime) -> str:
    if dt is None:
        return "—"
    delta = now - ensure_tz(dt)
    days = delta.days
    hours = delta.seconds // 3600
    if days > 0:
        return f"{days}d {hours}h ago"
    minutes = (delta.seconds % 3600) // 60
    if hours > 0:
        return f"{hours}h {minutes}m ago"
    return f"{minutes}m ago"


def bucket_status(delta_days: float, green_days: float, yellow_days: float) -> str:
    if delta_days <= green_days:
        return "healthy"
    if delta_days <= yellow_days:
        return "watch"
    return "stale"


def parse_entries(path: Path) -> list[Entry]:
    if not path.exists():
        return []

    lines = path.read_text(encoding="utf-8").splitlines()
    entries: list[Entry] = []
    i = 0
    while i < len(lines):
        match = ENTRY_HEADER_RE.match(lines[i])
        if not match:
            i += 1
            continue

        start = i
        i += 1
        section: list[str] = []
        while i < len(lines) and not ENTRY_HEADER_RE.match(lines[i]):
            section.append(lines[i])
            i += 1

        fields: dict[str, str] = {}
        summary = ""
        in_summary = False
        for line in section:
            field_match = FIELD_RE.match(line)
            if field_match:
                fields[field_match.group("key").strip().lower()] = field_match.group("value").strip()
            if line.strip() == "### Summary":
                in_summary = True
                continue
            if in_summary:
                if line.startswith("### "):
                    in_summary = False
                    continue
                if line.strip() and not summary:
                    summary = line.strip()

        entries.append(
            Entry(
                entry_id=match.group("id"),
                slug=match.group("slug").strip(),
                logged_at=parse_iso_datetime(fields.get("logged", "")),
                status=fields.get("status", "unknown"),
                priority=fields.get("priority", "unknown"),
                area=fields.get("area", "unknown"),
                summary=summary or "(no summary)",
                source_file=str(path),
            )
        )
    return entries


def collect_file_stats(path: Path, now: datetime) -> FileStats:
    entries = parse_entries(path)
    window_7 = now - timedelta(days=7)
    window_14 = now - timedelta(days=14)
    statuses: dict[str, int] = {}
    last_logged_at: datetime | None = None
    new_7d = 0
    new_14d = 0

    for entry in entries:
        statuses[entry.status] = statuses.get(entry.status, 0) + 1
        if entry.logged_at and (last_logged_at is None or entry.logged_at > last_logged_at):
            last_logged_at = entry.logged_at
        if entry.logged_at and entry.logged_at >= window_7:
            new_7d += 1
        if entry.logged_at and entry.logged_at >= window_14:
            new_14d += 1

    return FileStats(
        name=path.stem,
        path=path,
        total=len(entries),
        new_7d=new_7d,
        new_14d=new_14d,
        last_logged_at=last_logged_at,
        statuses=statuses,
        entries=entries,
    )


def collect_review_artifacts(report_dir: Path) -> list[ReviewArtifact]:
    artifacts: list[ReviewArtifact] = []
    if not report_dir.exists():
        return artifacts

    for child in report_dir.iterdir():
        if not child.is_file():
            continue
        match = REVIEW_FILE_RE.match(child.name)
        if not match:
            continue
        try:
            artifact_date = datetime.fromisoformat(match.group("date"))
        except ValueError:
            continue
        artifact_date = ensure_tz(artifact_date)
        kind = "weekly_review" if child.name.startswith("Weekly Review") else "promotion_log"
        artifacts.append(ReviewArtifact(kind=kind, path=child, artifact_date=artifact_date))

    artifacts.sort(key=lambda item: item.artifact_date)
    return artifacts


def latest_artifact(artifacts: Iterable[ReviewArtifact], kind: str) -> ReviewArtifact | None:
    candidates = [item for item in artifacts if item.kind == kind]
    return candidates[-1] if candidates else None


def ms_to_dt(value: int | float | None) -> datetime | None:
    if value is None:
        return None
    try:
        return ensure_tz(datetime.fromtimestamp(float(value) / 1000.0, tz=TZ))
    except Exception:
        return None


def load_cron_jobs(skip: bool) -> list[CronJobSummary]:
    if skip:
        return []

    try:
        result = subprocess.run(
            "openclaw cron list --json",
            shell=True,
            executable="/bin/zsh",
            capture_output=True,
            text=True,
            timeout=40,
            check=True,
        )
    except Exception:
        return []

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    jobs = payload.get("jobs", []) if isinstance(payload, dict) else []
    summaries: list[CronJobSummary] = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        name = str(job.get("name", ""))
        payload_message = ""
        payload_obj = job.get("payload")
        if isinstance(payload_obj, dict):
            payload_message = str(payload_obj.get("message", ""))
        combined = f"{name}\n{payload_message}".lower()
        if "self-improving-agent" not in combined and "self-improvement" not in combined:
            continue
        state = job.get("state") if isinstance(job.get("state"), dict) else {}
        summaries.append(
            CronJobSummary(
                name=name or "(unnamed cron)",
                enabled=bool(job.get("enabled", False)),
                next_run_at=ms_to_dt(state.get("nextRunAtMs")),
                last_run_at=ms_to_dt(state.get("lastRunAtMs")),
                last_status=str(state.get("lastStatus") or state.get("lastRunStatus") or "unknown"),
                consecutive_errors=int(state.get("consecutiveErrors") or 0),
            )
        )
    summaries.sort(key=lambda item: (item.next_run_at or datetime.max.replace(tzinfo=TZ if TZ else None), item.name))
    return summaries


def find_skill_link_status(workspace: Path, skill_root: Path) -> tuple[str, str]:
    live_link = workspace / "skills" / "self-improving-agent"
    if not live_link.exists():
        return "missing", f"missing: {live_link}"
    try:
        resolved = live_link.resolve()
    except Exception:
        return "broken", f"broken: {live_link}"
    if resolved == skill_root.resolve():
        return "healthy", f"ok: {live_link} -> {resolved}"
    return "watch", f"points elsewhere: {live_link} -> {resolved}"


def status_counts_repr(statuses: dict[str, int]) -> str:
    if not statuses:
        return "—"
    return ", ".join(f"{key}={value}" for key, value in sorted(statuses.items()))


def build_markdown(
    *,
    workspace: Path,
    now: datetime,
    file_stats: list[FileStats],
    artifacts: list[ReviewArtifact],
    cron_jobs: list[CronJobSummary],
    skill_link_status: tuple[str, str],
) -> str:
    stats_by_name = {item.name.upper(): item for item in file_stats}
    all_entries = sorted(
        [entry for stats in file_stats for entry in stats.entries if entry.logged_at],
        key=lambda item: item.logged_at or datetime.min.replace(tzinfo=TZ if TZ else None),
        reverse=True,
    )
    total_new_7d = sum(item.new_7d for item in file_stats)
    total_new_14d = sum(item.new_14d for item in file_stats)
    latest_activity = max((item.last_logged_at for item in file_stats if item.last_logged_at), default=None)
    latest_review = latest_artifact(artifacts, "weekly_review")
    latest_promotion = latest_artifact(artifacts, "promotion_log")

    activity_status = bucket_status((now - latest_activity).total_seconds() / 86400.0, 7, 14) if latest_activity else "stale"
    review_status = bucket_status((now - latest_review.artifact_date).total_seconds() / 86400.0, 8, 14) if latest_review else "stale"
    promotion_status = bucket_status((now - latest_promotion.artifact_date).total_seconds() / 86400.0, 16, 28) if latest_promotion else "stale"
    wiring_status, wiring_detail = skill_link_status

    status_rank = {"healthy": 0, "watch": 1, "stale": 2, "missing": 2, "broken": 2}
    worst = max([wiring_status, activity_status, review_status, promotion_status], key=lambda item: status_rank.get(item, 1))
    overall = {
        "healthy": "healthy",
        "watch": "watch",
        "stale": "needs-attention",
        "missing": "needs-attention",
        "broken": "needs-attention",
    }.get(worst, "watch")

    flags: list[str] = []
    feature_stats = stats_by_name.get("FEATURE_REQUESTS")
    if feature_stats and feature_stats.total == 0:
        flags.append("`FEATURE_REQUESTS.md` 仍为空。")
    if feature_stats and feature_stats.last_logged_at and (now - feature_stats.last_logged_at).days > 21:
        flags.append("`FEATURE_REQUESTS.md` 超过 21 天无新增，能力缺口分支可能重新休眠。")
    if latest_review is None:
        flags.append("未发现 `reports/self-improvement/Weekly Review - YYYY-MM-DD.md`。")
    if latest_promotion is None:
        flags.append("未发现 `reports/self-improvement/Promotion Log - YYYY-MM-DD.md`。")
    if not cron_jobs:
        flags.append("未读到 self-improving-agent 相关 cron；若这是预期，可忽略。")
    for job in cron_jobs:
        if job.consecutive_errors > 0:
            flags.append(f"cron `{job.name}` 连续错误 {job.consecutive_errors} 次。")

    recent_entries = all_entries[:6]

    lines: list[str] = []
    lines.append(f"# Self-Improving Agent Health Report — {format_date(now)}")
    lines.append("")
    lines.append("## 1. Snapshot")
    lines.append(f"- **Generated At:** {format_dt(now)}")
    lines.append(f"- **Workspace:** `{workspace}`")
    lines.append(f"- **Overall Health:** **{overall}**")
    lines.append(f"- **Live Wiring:** `{wiring_status}` — {wiring_detail}")
    lines.append(f"- **Recent Activity:** 7d = **{total_new_7d}** entries, 14d = **{total_new_14d}** entries")
    lines.append(f"- **Latest Learning Activity:** {format_dt(latest_activity)} ({format_age(latest_activity, now)})")
    lines.append(f"- **Latest Weekly Review:** {format_date(latest_review.artifact_date) if latest_review else '—'}")
    lines.append(f"- **Latest Promotion Log:** {format_date(latest_promotion.artifact_date) if latest_promotion else '—'}")
    if cron_jobs:
        lines.append(f"- **Tracked Cron Jobs:** {len(cron_jobs)}")
    lines.append("")

    lines.append("## 2. Activity by Branch")
    lines.append("| Branch | Total | New 7d | New 14d | Last Logged | Status Mix |")
    lines.append("| --- | ---: | ---: | ---: | --- | --- |")
    for stats in file_stats:
        lines.append(
            f"| `{stats.name}` | {stats.total} | {stats.new_7d} | {stats.new_14d} | {format_dt(stats.last_logged_at)} | {status_counts_repr(stats.statuses)} |"
        )
    lines.append("")

    lines.append("## 3. Cadence Evidence")
    lines.append(f"- **Weekly Review Status:** `{review_status}`")
    if latest_review:
        lines.append(
            f"  - Latest file: `{latest_review.path.relative_to(workspace)}` ({format_age(latest_review.artifact_date, now)})"
        )
    else:
        lines.append("  - Latest file: —")
    lines.append(f"- **Promotion Status:** `{promotion_status}`")
    if latest_promotion:
        lines.append(
            f"  - Latest file: `{latest_promotion.path.relative_to(workspace)}` ({format_age(latest_promotion.artifact_date, now)})"
        )
    else:
        lines.append("  - Latest file: —")
    lines.append(f"- **Activity Status:** `{activity_status}`")
    lines.append("  - Heuristic: green <= 7d, watch <= 14d, otherwise stale")
    lines.append("")

    lines.append("## 4. Cron Watch")
    if cron_jobs:
        lines.append("| Cron | Enabled | Next Run | Last Run | Last Status | Errors |")
        lines.append("| --- | --- | --- | --- | --- | ---: |")
        for job in cron_jobs:
            lines.append(
                f"| `{job.name}` | {'yes' if job.enabled else 'no'} | {format_dt(job.next_run_at)} | {format_dt(job.last_run_at)} | {job.last_status} | {job.consecutive_errors} |"
            )
    else:
        lines.append("- No self-improving-agent-specific cron job detected (or cron query skipped/unavailable).")
    lines.append("")

    lines.append("## 5. Recent Entries")
    if recent_entries:
        for entry in recent_entries:
            lines.append(
                f"- `{entry.entry_id}` ({Path(entry.source_file).stem}, {entry.status}, {format_dt(entry.logged_at)}) — {entry.summary}"
            )
    else:
        lines.append("- No parsed entries found.")
    lines.append("")

    lines.append("## 6. Flags")
    if flags:
        for flag in flags:
            lines.append(f"- {flag}")
    else:
        lines.append("- No immediate red flags in this lightweight pass.")
    lines.append("")

    lines.append("## 7. One-Line Verdict")
    if overall == "healthy":
        lines.append("`self-improving-agent` 在这个 workspace 里处于可见、可验证、仍在工作的状态；后续重点是保持 cadence，而不是再做大修。")
    elif overall == "watch":
        lines.append("`self-improving-agent` 基本在运作，但节奏和可见性还不够稳，建议继续盯 activity / weekly review / promotion 三条证据链。")
    else:
        lines.append("`self-improving-agent` 目前不是“坏了”，但至少有一条关键证据链已经发黄或变红，应该尽快补 cadence / cron / review 证据。")
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_json_summary(
    *,
    workspace: Path,
    now: datetime,
    file_stats: list[FileStats],
    artifacts: list[ReviewArtifact],
    cron_jobs: list[CronJobSummary],
    skill_link_status: tuple[str, str],
) -> dict:
    latest_review = latest_artifact(artifacts, "weekly_review")
    latest_promotion = latest_artifact(artifacts, "promotion_log")
    return {
        "generatedAt": ensure_tz(now).isoformat(),
        "workspace": str(workspace),
        "wiring": {"status": skill_link_status[0], "detail": skill_link_status[1]},
        "branches": [
            {
                "name": stats.name,
                "path": str(stats.path),
                "total": stats.total,
                "new7d": stats.new_7d,
                "new14d": stats.new_14d,
                "lastLoggedAt": ensure_tz(stats.last_logged_at).isoformat() if stats.last_logged_at else None,
                "statuses": stats.statuses,
            }
            for stats in file_stats
        ],
        "latestWeeklyReview": {
            "path": str(latest_review.path) if latest_review else None,
            "date": ensure_tz(latest_review.artifact_date).isoformat() if latest_review else None,
        },
        "latestPromotionLog": {
            "path": str(latest_promotion.path) if latest_promotion else None,
            "date": ensure_tz(latest_promotion.artifact_date).isoformat() if latest_promotion else None,
        },
        "cron": [
            {
                "name": job.name,
                "enabled": job.enabled,
                "nextRunAt": ensure_tz(job.next_run_at).isoformat() if job.next_run_at else None,
                "lastRunAt": ensure_tz(job.last_run_at).isoformat() if job.last_run_at else None,
                "lastStatus": job.last_status,
                "consecutiveErrors": job.consecutive_errors,
            }
            for job in cron_jobs
        ],
    }


def main() -> int:
    args = parse_args()
    workspace = Path(args.workspace).expanduser().resolve()
    now = now_local()
    skill_root = Path(__file__).resolve().parent.parent

    learning_dir = workspace / ".learnings"
    file_paths = [
        learning_dir / "LEARNINGS.md",
        learning_dir / "ERRORS.md",
        learning_dir / "FEATURE_REQUESTS.md",
    ]
    file_stats = [collect_file_stats(path, now) for path in file_paths]
    artifacts = collect_review_artifacts(workspace / "reports" / "self-improvement")
    cron_jobs = load_cron_jobs(skip=args.skip_cron)
    skill_link_status = find_skill_link_status(workspace, skill_root)

    if args.json:
        payload = build_json_summary(
            workspace=workspace,
            now=now,
            file_stats=file_stats,
            artifacts=artifacts,
            cron_jobs=cron_jobs,
            skill_link_status=skill_link_status,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    markdown = build_markdown(
        workspace=workspace,
        now=now,
        file_stats=file_stats,
        artifacts=artifacts,
        cron_jobs=cron_jobs,
        skill_link_status=skill_link_status,
    )

    default_output = workspace / "reports" / "self-improvement" / f"Health Report - {format_date(now)}.md"
    output_path = Path(args.output).expanduser() if args.output else default_output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    if args.stdout or not args.output:
        print(markdown)
        print(f"[written] {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

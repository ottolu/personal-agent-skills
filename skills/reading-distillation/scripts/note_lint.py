#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

REQUIRED_KEYS = [
    "type",
    "source_type",
    "title",
    "publisher",
    "author",
    "url",
    "date_published",
    "date_ingested",
    "status",
    "review_week",
    "tags",
    "topics",
    "signal_level",
]

REQUIRED_HEADINGS = [
    "# ",
    "## Source",
    "## TL;DR",
    "## Summary",
    "## Key Points",
    "## Original Text (Cleaned Archive)",
    "## Key Quotes / Excerpts",
    "## First-Principles Analysis",
    "## My Observation",
    "## Why It Matters for Lewei",
    "## Follow-ups",
]

TAG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://")
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:\s+\d{2}:\d{2})?$")


def parse_frontmatter(text: str):
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    body = text[end + 5 :]
    data = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data, body


def parse_list(value: str):
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [item.strip().strip('"\'') for item in inner.split(",") if item.strip()]


def section_content(body: str, heading: str):
    start = body.find(heading)
    if start == -1:
        return ""
    start = body.find("\n", start)
    if start == -1:
        return ""
    start += 1
    next_positions = []
    for marker in ["\n## ", "\n# "]:
        pos = body.find(marker, start)
        if pos != -1:
            next_positions.append(pos)
    end = min(next_positions) if next_positions else len(body)
    return body[start:end].strip()


def fail(errors):
    for error in errors:
        print(f"FAIL: {error}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Lint a reading note for stable structure.")
    parser.add_argument("--file", required=True)
    parser.add_argument("--source-type", choices=["wechat-oa", "web-article"])
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        fail([f"file not found: {path}"])

    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    errors = []

    if fm is None:
        fail(["missing YAML frontmatter"])

    for key in REQUIRED_KEYS:
        if key not in fm:
            errors.append(f"missing frontmatter key: {key}")

    if fm.get("type") != "reading-note":
        errors.append("type must be reading-note")

    source_type = fm.get("source_type")
    if source_type not in {"wechat-oa", "web-article"}:
        errors.append("source_type must be wechat-oa or web-article")
    if args.source_type and source_type != args.source_type:
        errors.append(f"source_type mismatch: expected {args.source_type}, got {source_type}")

    if not fm.get("title"):
        errors.append("title cannot be empty")
    if not fm.get("publisher"):
        errors.append("publisher cannot be empty")
    if not URL_RE.match(fm.get("url", "")):
        errors.append("url must start with http:// or https://")
    if fm.get("date_published") and not DATE_RE.match(fm.get("date_published")):
        errors.append("date_published must be YYYY-MM-DD or YYYY-MM-DD HH:MM")
    if fm.get("date_ingested") and not DATE_RE.match(fm.get("date_ingested")):
        errors.append("date_ingested must be YYYY-MM-DD or YYYY-MM-DD HH:MM")
    if fm.get("status") not in {"distilled", "partial"}:
        errors.append("status must be distilled or partial")
    if fm.get("review_week") and not WEEK_RE.match(fm.get("review_week")):
        errors.append("review_week must be YYYY-Wnn")
    if fm.get("signal_level") not in {"high", "medium", "low"}:
        errors.append("signal_level must be high, medium, or low")

    tags = parse_list(fm.get("tags", ""))
    if tags is None:
        errors.append("tags must be a bracketed list")
        tags = []
    topics = parse_list(fm.get("topics", ""))
    if topics is None:
        errors.append("topics must be a bracketed list")
        topics = []

    if "reading" not in tags:
        errors.append("tags must include reading")
    if source_type and source_type not in tags:
        errors.append(f"tags must include {source_type}")
    if len(tags) < 2:
        errors.append("use at least 2 tags")
    if len(tags) > 8:
        errors.append("keep tags to 8 or fewer")
    for tag in tags:
        if not TAG_RE.match(tag):
            errors.append(f"invalid tag format: {tag}")

    positions = []
    for heading in REQUIRED_HEADINGS:
        pos = body.find(heading)
        if pos == -1:
            errors.append(f"missing heading: {heading}")
        positions.append(pos)
    present_positions = [p for p in positions if p != -1]
    if present_positions != sorted(present_positions):
        errors.append("required headings are out of order")

    original_text = section_content(body, "## Original Text (Cleaned Archive)")
    if len(original_text) < 200:
        errors.append("original text archive is too short; preserve cleaned body text")

    followups = section_content(body, "## Follow-ups")
    for expected in ["纳入本周 review", "升级为长期知识", "继续跟踪作者 / 主题"]:
        if expected not in followups:
            errors.append(f"follow-ups missing canonical item: {expected}")

    if errors:
        fail(errors)

    print(f"PASS: {path}")
    print(f"source_type={source_type} tags={len(tags)} topics={len(topics)}")


if __name__ == "__main__":
    main()

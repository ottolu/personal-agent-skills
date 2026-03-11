#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import time
from typing import Any


def run_xurl_search(query: str, limit: int, timeout: int, retries: int) -> dict[str, Any]:
    cmd = ["xurl", "search", query, "-n", str(limit)]
    last_error: str | None = None

    for attempt in range(1, retries + 2):
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            last_error = f"xurl search timeout after {timeout}s (attempt {attempt}/{retries + 1})"
        else:
            if p.returncode != 0:
                last_error = p.stderr.strip() or p.stdout.strip() or "xurl search failed"
            else:
                try:
                    return json.loads(p.stdout)
                except json.JSONDecodeError as e:
                    preview = (p.stdout or "")[:400].replace("\n", "\\n")
                    raise RuntimeError(
                        f"xurl returned non-JSON output for query={query!r}: {e}; stdout={preview}"
                    ) from e

        if attempt <= retries:
            time.sleep(min(2 ** (attempt - 1), 4))

    raise RuntimeError(last_error or "xurl search failed")


def score(item: dict[str, Any]) -> float:
    pm = item.get("public_metrics") or {}
    likes = pm.get("like_count", 0)
    reposts = pm.get("retweet_count", 0)
    replies = pm.get("reply_count", 0)
    return likes + 2 * reposts + 1.5 * replies


def classify_reply(text: str) -> str:
    s = (text or "").strip().lower()
    if not s:
        return "low_signal"
    if any(k in s for k in ["?", "为什么", "why", "how", "怎么", "能不能", "how to"]):
        return "question_or_blocker"
    if any(k in s for k in ["bug", "broken", "fail", "issue", "problem", "not work", "不行", "有问题", "报错", "踩坑"]):
        return "negative_or_blocker"
    if any(k in s for k in ["great", "nice", "love", "amazing", "好用", "牛", "赞", "强", "wow"]):
        return "positive"
    if any(k in s for k in ["integrat", "deploy", "workflow", "tool", "mcp", "cron", "gateway", "memory", "接入", "部署", "工作流", "集成"]):
        return "practical_signal"
    return "general"


def main() -> None:
    ap = argparse.ArgumentParser(description="Sample top replies for a tweet conversation")
    ap.add_argument("tweet_id", help="target tweet id")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--timeout", type=int, default=30)
    ap.add_argument("--retries", type=int, default=2)
    args = ap.parse_args()

    if args.limit < 1:
        raise ValueError("--limit must be >= 1")
    if args.top < 1:
        raise ValueError("--top must be >= 1")
    if args.top > args.limit:
        raise ValueError("--top must be <= --limit")
    if args.timeout < 1:
        raise ValueError("--timeout must be >= 1")
    if args.retries < 0:
        raise ValueError("--retries must be >= 0")

    query = f"conversation_id:{args.tweet_id}"
    data = run_xurl_search(query, args.limit, args.timeout, args.retries)

    tweets = data.get("data") or []
    users = {u.get("id"): u for u in (data.get("includes", {}).get("users") or [])}

    root_removed = 0
    filtered: list[dict[str, Any]] = []
    for t in tweets:
        if str(t.get("id")) == str(args.tweet_id):
            root_removed += 1
            continue
        filtered.append(t)

    filtered.sort(key=score, reverse=True)

    out = []
    for t in filtered[: args.top]:
        uid = t.get("author_id")
        u = users.get(uid, {})
        pm = t.get("public_metrics") or {}
        text = (t.get("text") or "").replace("\n", " ").strip()
        out.append(
            {
                "id": t.get("id"),
                "author": u.get("username", "unknown"),
                "likes": pm.get("like_count", 0),
                "reposts": pm.get("retweet_count", 0),
                "replies": pm.get("reply_count", 0),
                "score": score(t),
                "stance_hint": classify_reply(text),
                "text": text,
            }
        )

    status = "ok"
    error_message = None
    if not tweets:
        status = "empty"
        error_message = "conversation search returned no tweets"
    elif not filtered:
        status = "root_only"
        error_message = "conversation only contained the root tweet"
    elif len(out) < args.top:
        status = "partial"
        error_message = f"requested top={args.top}, sampled={len(out)}"

    print(
        json.dumps(
            {
                "tweet_id": args.tweet_id,
                "query": query,
                "status": status,
                "fetched_count": len(tweets),
                "root_removed": root_removed,
                "sampled_count": len(out),
                "error_message": error_message,
                "sampling_note": "High-engagement reply sample only; not a full stance or consensus analysis.",
                "top_replies": out,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

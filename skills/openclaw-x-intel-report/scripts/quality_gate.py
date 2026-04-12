#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import Iterable


SECTION_PATTERNS = {
    "top": r"(?m)^##\s*1\)\s*Top Priority Signals",
    "kol": r"(?m)^##\s*2\)\s*大V名单",
    "cn": r"(?m)^##\s*3\)\s*中文圈热帖",
    "en": r"(?m)^##\s*4\)\s*英文圈热帖",
    "watchlist": r"(?m)^##\s*5\)\s*Watchlist",
    "actions": r"(?m)^##\s*6\)\s*今日动作",
    "checklist": r"(?m)^##\s*7\)\s*质量自检",
}

URL_RE = re.compile(r"https?://(?:x|twitter)\.com/\S+", re.I)
WINDOW_RE = re.compile(r"\b(?:24h|72h)\b", re.I)
PLACEHOLDER_SET = {"...", "…", "{{url}}", "{{time}}", "{{score}}", "{{confidence}}"}


def extract_section(text: str, start_pattern: str, next_patterns: Iterable[str]) -> str:
    m = re.search(start_pattern, text, flags=re.M)
    if not m:
        return ""
    start = m.end()
    end = len(text)
    tail = text[start:]
    for pat in next_patterns:
        n = re.search(pat, tail, flags=re.M)
        if n:
            end = min(end, start + n.start())
    return text[start:end]


def split_top_items(section_text: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^###\s*\d+\.", section_text))
    if not matches:
        return []
    blocks: list[str] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        blocks.append(section_text[start:end].strip())
    return blocks


def split_numbered_items(section_text: str) -> list[str]:
    matches = list(re.finditer(r"(?m)^\d+\)\s+", section_text))
    if not matches:
        return []
    blocks: list[str] = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(section_text)
        blocks.append(section_text[start:end].strip())
    return blocks


def extract_field(block: str, label: str) -> str:
    pattern = re.compile(rf"(?m)^\s*-\s*{re.escape(label)}[^:：]*[:：]\s*(.*)$")
    m = pattern.search(block)
    if not m:
        return ""
    tail = m.group(1).strip()
    if tail:
        return tail
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if re.match(rf"^\s*-\s*{re.escape(label)}[^:：]*[:：]\s*$", line):
            for nxt in lines[i + 1 :]:
                candidate = nxt.strip()
                if not candidate:
                    continue
                if re.match(r"^(?:###\s*\d+\.|\d+\)\s+|-\s*[^:：]+[:：])", candidate):
                    return ""
                return candidate
    return ""


def non_empty(value: str) -> bool:
    return bool(value and value.strip() and value.strip() not in PLACEHOLDER_SET)


def summary_length_ok(summary: str) -> tuple[bool, int]:
    n = len(re.sub(r"\s+", "", summary or ""))
    return 100 <= n <= 200, n


def parse_score(raw: str):
    if not raw:
        return None
    m = re.search(r"(\d+(?:\.\d+)?)", raw)
    return float(m.group(1)) if m else None


def parse_interactions(raw: str):
    if not raw:
        return None, None, None

    def grab(patterns: list[str]):
        for pat in patterns:
            m = re.search(pat, raw, flags=re.I)
            if m:
                try:
                    return int(m.group(1))
                except ValueError:
                    return None
        return None

    likes = grab([r"赞\s*(\d+)", r"likes?\s*(\d+)"])
    reposts = grab([r"转推\s*(\d+)", r"(?:reposts?|retweets?)\s*(\d+)"])
    replies = grab([r"回复\s*(\d+)", r"replies?\s*(\d+)"])
    return likes, reposts, replies


def is_zero_engagement(raw: str) -> bool:
    likes, reposts, replies = parse_interactions(raw)
    return (likes, reposts, replies) == (0, 0, 0)


def count_low_confidence(text: str) -> int:
    return len(re.findall(r"低置信补位", text))


def require(condition: bool, failed: list[str], message: str) -> None:
    if not condition:
        failed.append(message)


def validate_item_common(block: str, section: str, idx: int, failed: list[str], require_summary: bool = True) -> dict:
    url = extract_field(block, "原帖")
    interaction = extract_field(block, "互动")
    query = extract_field(block, "命中查询")
    source = extract_field(block, "采集方式")
    score = extract_field(block, "分数")
    confidence = extract_field(block, "置信级别")
    narrative = extract_field(block, "叙事标签")
    window = extract_field(block, "信号窗口")

    require(non_empty(url) and bool(URL_RE.search(url)), failed, f"{section}[{idx}] 缺少合法原帖链接")
    require(non_empty(interaction), failed, f"{section}[{idx}] 缺少互动数据")
    if non_empty(interaction):
        likes, reposts, replies = parse_interactions(interaction)
        require(None not in (likes, reposts, replies), failed, f"{section}[{idx}] 互动数据不可解析")
    require(non_empty(query), failed, f"{section}[{idx}] 缺少命中查询")
    require(non_empty(source), failed, f"{section}[{idx}] 缺少采集方式")
    require(non_empty(window) and bool(WINDOW_RE.search(window)), failed, f"{section}[{idx}] 缺少 24h/72h 信号窗口标记")
    require(non_empty(score) and parse_score(score) is not None, failed, f"{section}[{idx}] 缺少可解析分数")
    require(non_empty(confidence), failed, f"{section}[{idx}] 缺少置信级别")
    require(non_empty(narrative), failed, f"{section}[{idx}] 缺少叙事标签")

    if require_summary:
        summary = extract_field(block, "摘要") or extract_field(block, "核心观点")
        ok, n = summary_length_ok(summary)
        require(ok, failed, f"{section}[{idx}] 摘要/核心观点长度不在 100-200 字（当前 {n}）")

    return {
        "url": url,
        "interaction": interaction,
        "score": parse_score(score),
        "zero": is_zero_engagement(interaction),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    args = ap.parse_args()

    p = Path(args.file)
    if not p.exists():
        print(f"FAIL: file not found: {p}")
        sys.exit(2)
    if not p.is_file():
        print(f"FAIL: not a regular file: {p}")
        sys.exit(2)

    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError as e:
        print(f"FAIL: cannot read file {p}: {e}")
        sys.exit(2)

    failed: list[str] = []

    sec_top = extract_section(text, SECTION_PATTERNS["top"], [SECTION_PATTERNS["kol"], SECTION_PATTERNS["cn"], SECTION_PATTERNS["en"], SECTION_PATTERNS["watchlist"], SECTION_PATTERNS["actions"], SECTION_PATTERNS["checklist"]])
    sec_kol = extract_section(text, SECTION_PATTERNS["kol"], [SECTION_PATTERNS["cn"], SECTION_PATTERNS["en"], SECTION_PATTERNS["watchlist"], SECTION_PATTERNS["actions"], SECTION_PATTERNS["checklist"]])
    sec_cn = extract_section(text, SECTION_PATTERNS["cn"], [SECTION_PATTERNS["en"], SECTION_PATTERNS["watchlist"], SECTION_PATTERNS["actions"], SECTION_PATTERNS["checklist"]])
    sec_en = extract_section(text, SECTION_PATTERNS["en"], [SECTION_PATTERNS["watchlist"], SECTION_PATTERNS["actions"], SECTION_PATTERNS["checklist"]])
    sec_watch = extract_section(text, SECTION_PATTERNS["watchlist"], [SECTION_PATTERNS["actions"], SECTION_PATTERNS["checklist"]])
    sec_actions = extract_section(text, SECTION_PATTERNS["actions"], [SECTION_PATTERNS["checklist"]])

    top_items = split_top_items(sec_top)
    kol_items = split_numbered_items(sec_kol)
    cn_items = split_numbered_items(sec_cn)
    en_items = split_numbered_items(sec_en)
    watch_items = split_numbered_items(sec_watch)
    action_items = split_numbered_items(sec_actions)

    require(len(top_items) == 5, failed, f"Top Priority Signals 数量应为 5，当前 {len(top_items)}")
    require(15 <= len(kol_items) <= 20, failed, f"A failed: KOL count {len(kol_items)} not in [15,20]")
    require(5 <= len(cn_items) <= 8, failed, f"B failed: CN hot posts {len(cn_items)} not in [5,8]")
    require(5 <= len(en_items) <= 8, failed, f"C failed: EN hot posts {len(en_items)} not in [5,8]")
    require(len(watch_items) <= 3, failed, f"D failed: watchlist count {len(watch_items)} > 3")
    require(len(action_items) >= 3, failed, f"今日动作数量应 >= 3，当前 {len(action_items)}")

    top_meta = []
    kol_meta = []
    cn_meta = []
    en_meta = []

    for idx, block in enumerate(top_items, start=1):
        meta = validate_item_common(block, "Top", idx, failed, require_summary=True)
        reply = extract_field(block, "回复区观察")
        impact = extract_field(block, "为什么重要") or extract_field(block, "影响判断")
        action = extract_field(block, "今日动作")
        require(non_empty(reply), failed, f"Top[{idx}] 缺少回复区观察")
        require(non_empty(impact), failed, f"Top[{idx}] 缺少为什么重要/影响判断")
        require(non_empty(action), failed, f"Top[{idx}] 缺少今日动作")
        require((meta["score"] or 0) >= 78, failed, f"Top[{idx}] 分数低于 78")
        require(not meta["zero"], failed, f"Top[{idx}] 不允许 0互动条目")
        top_meta.append(meta)

    for idx, block in enumerate(kol_items, start=1):
        meta = validate_item_common(block, "KOL", idx, failed, require_summary=True)
        profile = extract_field(block, "账号")
        followers = extract_field(block, "粉丝量级") or extract_field(block, "粉丝")
        follow = extract_field(block, "跟进")
        require(non_empty(profile) and bool(URL_RE.search(profile)), failed, f"KOL[{idx}] 缺少账号链接")
        require(non_empty(followers), failed, f"KOL[{idx}] 缺少粉丝量级")
        require(non_empty(follow), failed, f"KOL[{idx}] 缺少跟进判断")
        require((meta["score"] or 0) >= 64, failed, f"KOL[{idx}] 分数低于 64")
        kol_meta.append(meta)

    for idx, block in enumerate(cn_items, start=1):
        meta = validate_item_common(block, "CN", idx, failed, require_summary=True)
        why = extract_field(block, "为什么重要") or extract_field(block, "热度理由")
        action = extract_field(block, "跟进动作") or extract_field(block, "建议动作")
        require(non_empty(why), failed, f"CN[{idx}] 缺少为什么重要/热度理由")
        require(non_empty(action), failed, f"CN[{idx}] 缺少跟进动作/建议动作")
        require((meta["score"] or 0) >= 64, failed, f"CN[{idx}] 分数低于 64")
        require(not meta["zero"], failed, f"CN[{idx}] 不允许 0互动条目")
        cn_meta.append(meta)

    for idx, block in enumerate(en_items, start=1):
        meta = validate_item_common(block, "EN", idx, failed, require_summary=True)
        why = extract_field(block, "为什么重要") or extract_field(block, "热度理由")
        action = extract_field(block, "跟进动作") or extract_field(block, "建议动作")
        require(non_empty(why), failed, f"EN[{idx}] 缺少为什么重要/热度理由")
        require(non_empty(action), failed, f"EN[{idx}] 缺少跟进动作/建议动作")
        require((meta["score"] or 0) >= 64, failed, f"EN[{idx}] 分数低于 64")
        require(not meta["zero"], failed, f"EN[{idx}] 不允许 0互动条目")
        en_meta.append(meta)

    for idx, block in enumerate(watch_items, start=1):
        meta = validate_item_common(block, "Watchlist", idx, failed, require_summary=False)
        reason = extract_field(block, "观察理由")
        not_main = extract_field(block, "为什么今天不进主报告")
        trigger = extract_field(block, "明日触发条件")
        require(non_empty(reason), failed, f"Watchlist[{idx}] 缺少观察理由")
        require(non_empty(not_main), failed, f"Watchlist[{idx}] 缺少为什么今天不进主报告")
        require(non_empty(trigger), failed, f"Watchlist[{idx}] 缺少明日触发条件")

    # bucket-level thresholds
    kol_high = sum(1 for m in kol_meta if (m["score"] or 0) >= 72)
    kol_medium = sum(1 for m in kol_meta if 64 <= (m["score"] or 0) < 72)
    kol_zero = sum(1 for m in kol_meta if m["zero"])
    require(kol_high >= 8, failed, f"KOL 高置信条目不足：当前 {kol_high} < 8")
    require(kol_medium <= 7, failed, f"KOL 中等置信补位过多：当前 {kol_medium} > 7")
    require(kol_zero <= 2, failed, f"KOL 中 0互动例外过多：当前 {kol_zero} > 2")

    def bucket_check(name: str, metas: list[dict], strong_floor: float) -> None:
        if not metas:
            return
        strong = sum(1 for m in metas if (m["score"] or 0) >= strong_floor)
        fallback = sum(1 for m in metas if 64 <= (m["score"] or 0) < strong_floor)
        require(strong / len(metas) >= 0.8, failed, f"{name} bucket 中 >= {int(strong_floor)} 的条目比例不足 80%")
        require(fallback <= 1, failed, f"{name} bucket fallback 条目过多：当前 {fallback} > 1")

    bucket_check("CN", cn_meta, 68)
    bucket_check("EN", en_meta, 68)

    low_conf = count_low_confidence(text)
    if low_conf > 2:
        failed.append(f"低置信补位 {low_conf} > 2")

    warnings: list[str] = []
    if re.search(r"编造|虚构", text):
        warnings.append("warning: 报告中出现‘编造/虚构’字样，请人工复核‘无编造数据’声明")

    if failed:
        print("QUALITY_GATE: FAILED")
        for f in failed:
            print("-", f)
        for w in warnings:
            print("-", w)
        sys.exit(1)

    print("QUALITY_GATE: PASSED")
    print(
        f"Top={len(top_items)}, KOL={len(kol_items)}, CN={len(cn_items)}, EN={len(en_items)}, Watchlist={len(watch_items)}, Actions={len(action_items)}, low_conf={low_conf}, kol_zero={kol_zero}"
    )
    for w in warnings:
        print("-", w)


if __name__ == "__main__":
    main()

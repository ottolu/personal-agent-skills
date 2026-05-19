#!/usr/bin/env bash
# 应用保守过滤规则筛选 bot 账号
# 用法：
#   ./filter-bots.sh <profiles.jsonl> <output-block-list.txt> [output-keep-list.txt]
#
# 规则（保守，宁可漏不可错）：
# 1) 完全零产出（allRepos/issues/PRs/gists/commits/issueCommits/prCommits 全 0）→ block
# 2) bio 含 prs_[hex]+ → block（PR 农场任务 ID 铁证）
# 3) 其他 → keep（包括只有 1 个 fork 也保留）

set -euo pipefail

PROFILES="${1:?用法: $0 <profiles.jsonl> <output-block-list.txt> [output-keep-list.txt]}"
BLOCK_OUT="${2:?}"
KEEP_OUT="${3:-/dev/null}"

jq -c '
. + {
  should_block: (
    (.allRepos.totalCount == 0 and
     .issuesOpened.totalCount == 0 and
     .prsOpened.totalCount == 0 and
     .gists.totalCount == 0 and
     .contributionsCollection.totalCommitContributions == 0 and
     .contributionsCollection.totalIssueContributions == 0 and
     .contributionsCollection.totalPullRequestContributions == 0)
    or
    (.bio // "" | test("prs_[0-9a-f]+"; "i"))
  ),
  block_reason: (
    if (.bio // "" | test("prs_[0-9a-f]+"; "i")) then "prs_bio"
    elif (.allRepos.totalCount == 0 and .contributionsCollection.totalCommitContributions == 0) then "zero_activity"
    else "keep"
    end
  )
}
' "$PROFILES" > /tmp/scored.jsonl

# 分别输出
jq -r 'select(.should_block) | .login' /tmp/scored.jsonl | sort -u > "$BLOCK_OUT"
jq -r 'select(.should_block | not) | .login' /tmp/scored.jsonl | sort -u > "$KEEP_OUT"

echo "应 block: $(wc -l < "$BLOCK_OUT")"
echo "应 keep: $(wc -l < "$KEEP_OUT")"
echo ""
echo "=== Block 分原因统计 ==="
jq -r 'select(.should_block) | .block_reason' /tmp/scored.jsonl | sort | uniq -c
echo ""
echo "=== 含 prs_ bio 的（铁证 bot）==="
jq -r 'select(.block_reason == "prs_bio") | "  \(.login)\t(repos=\(.allRepos.totalCount))\tbio=\(.bio)"' /tmp/scored.jsonl

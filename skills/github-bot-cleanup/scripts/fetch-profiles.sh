#!/usr/bin/env bash
# 批量拉 GitHub 用户 profile + 活动数据
# 用法：
#   ./fetch-profiles.sh <username-list.txt> <output.jsonl>
#
# 输入：每行一个用户名
# 输出：JSONL，每行一个 user 对象（含 createdAt/bio/repos/issues/PRs/contributions）

set -euo pipefail

LIST="${1:?用法: $0 <username-list> <output.jsonl>}"
OUT="${2:?用法: $0 <username-list> <output.jsonl>}"

USERS=()
while IFS= read -r line; do USERS+=("$line"); done < "$LIST"
echo "拉取 profile: ${#USERS[@]} 个账号" >&2

> "$OUT"
BATCH=10  # GraphQL 复杂查询，每批 10 个稳定，更多容易丢
i=0
while [ $i -lt ${#USERS[@]} ]; do
  query="{"
  j=0
  while [ $j -lt $BATCH ] && [ $((i+j)) -lt ${#USERS[@]} ]; do
    user="${USERS[$((i+j))]}"
    query+="u${j}: user(login: \"$user\") { login createdAt bio "
    query+="allRepos: repositories { totalCount } "
    query+="originalRepos: repositories(isFork: false) { totalCount } "
    query+="forkedRepos: repositories(isFork: true) { totalCount } "
    query+="issuesOpened: issues { totalCount } "
    query+="prsOpened: pullRequests { totalCount } "
    query+="gists { totalCount } "
    query+="followers { totalCount } following { totalCount } "
    query+="contributionsCollection { totalCommitContributions totalIssueContributions totalPullRequestContributions } "
    query+="} "
    j=$((j+1))
  done
  query+="}"
  gh api graphql -f query="$query" 2>/dev/null | jq -c '.data | to_entries[] | .value | select(. != null)' >> "$OUT"
  i=$((i+BATCH))
  [ $((i % 50)) -eq 0 ] && echo "进度: $i/${#USERS[@]}" >&2
done

GOT=$(wc -l < "$OUT")
echo "完成: $GOT / ${#USERS[@]}" >&2

# 检查并补查丢失的（GraphQL 偶尔丢数据）
if [ "$GOT" -lt "${#USERS[@]}" ]; then
  echo "补查丢失的..." >&2
  jq -r '.login' "$OUT" | sort -u > /tmp/got.txt
  sort -u "$LIST" > /tmp/want.txt
  comm -23 /tmp/want.txt /tmp/got.txt > /tmp/missing.txt
  echo "补查 $(wc -l < /tmp/missing.txt) 个..." >&2
  while IFS= read -r u; do
    # REST 模式补查（构造与 GraphQL 输出兼容的结构）
    resp=$(gh api "/users/$u" 2>/dev/null || echo "")
    if [ -n "$resp" ]; then
      echo "$resp" | jq -c '{
        login: .login,
        createdAt: .created_at,
        bio: .bio,
        allRepos: {totalCount: .public_repos},
        originalRepos: {totalCount: 0},
        forkedRepos: {totalCount: 0},
        issuesOpened: {totalCount: 0},
        prsOpened: {totalCount: 0},
        gists: {totalCount: .public_gists},
        followers: {totalCount: .followers},
        following: {totalCount: .following},
        contributionsCollection: {totalCommitContributions: 0, totalIssueContributions: 0, totalPullRequestContributions: 0}
      }' >> "$OUT"
    fi
  done < /tmp/missing.txt
  echo "补查完成，总数: $(wc -l < "$OUT")" >&2
fi

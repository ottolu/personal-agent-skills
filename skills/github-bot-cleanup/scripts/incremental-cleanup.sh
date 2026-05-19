#!/usr/bin/env bash
# 增量监控 - 用于持续清理（攻击不断涌入的场景）
# 用法：
#   ./incremental-cleanup.sh <org/repo> [--auto-apply]
#
# 行为：
# 1. 拉最新 stargazers
# 2. 与上次 snapshot 对比，找出新增账号
# 3. 跑过滤规则
# 4. 默认 dry-run；加 --auto-apply 则自动 block
# 5. 把 snapshot 存到 ~/.cache/github-bot-cleanup/<org>_<repo>/

set -euo pipefail

REPO="${1:?用法: $0 <org/repo> [--auto-apply]}"
AUTO="${2:-}"

ORG="${REPO%/*}"
REPO_NAME="${REPO#*/}"
CACHE_DIR="$HOME/.cache/github-bot-cleanup/${ORG}_${REPO_NAME}"
mkdir -p "$CACHE_DIR"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SNAPSHOT="$CACHE_DIR/last_snapshot.txt"
FRESH="$CACHE_DIR/fresh.json"
NEW_USERS="$CACHE_DIR/new_users.txt"
PROFILES="$CACHE_DIR/new_profiles.jsonl"
BLOCK_LIST="$CACHE_DIR/block_$(date +%Y%m%d-%H%M%S).txt"
KEEP_LIST="$CACHE_DIR/keep_$(date +%Y%m%d-%H%M%S).txt"

echo "=== 增量清理 $REPO ==="
echo "缓存目录: $CACHE_DIR"
echo ""

# Step 1: 拉最新 stargazers
echo "[1/4] 拉取最新 stargazers..."
gh api -H "Accept: application/vnd.github.star+json" \
  "/repos/$REPO/stargazers?per_page=100" \
  --paginate > "$FRESH"
TOTAL=$(jq 'length' "$FRESH")
echo "      当前 $TOTAL 个 star"

# Step 2: 对比 snapshot
jq -r '.[].user.login' "$FRESH" | sort -u > "$CACHE_DIR/current.txt"

if [ -f "$SNAPSHOT" ]; then
  comm -23 "$CACHE_DIR/current.txt" "$SNAPSHOT" > "$NEW_USERS"
  NEW_COUNT=$(wc -l < "$NEW_USERS" | tr -d ' ')
  echo "[2/4] 与上次 snapshot 对比：新增 $NEW_COUNT 个 star"
else
  cp "$CACHE_DIR/current.txt" "$NEW_USERS"
  NEW_COUNT=$(wc -l < "$NEW_USERS" | tr -d ' ')
  echo "[2/4] 首次运行，全量当作 '新增'：$NEW_COUNT 个"
fi

if [ "$NEW_COUNT" -eq 0 ]; then
  echo "      没有新增 star，结束。"
  cp "$CACHE_DIR/current.txt" "$SNAPSHOT"
  exit 0
fi

# Step 3: 拉新增账号 profile + 过滤
echo "[3/4] 拉取新账号 profile + 过滤..."
bash "$SCRIPT_DIR/fetch-profiles.sh" "$NEW_USERS" "$PROFILES"
bash "$SCRIPT_DIR/filter-bots.sh" "$PROFILES" "$BLOCK_LIST" "$KEEP_LIST"

# Step 4: block（如果加了 --auto-apply）
echo ""
if [ "$AUTO" = "--auto-apply" ]; then
  echo "[4/4] 自动执行 block..."
  bash "$SCRIPT_DIR/batch-block.sh" "$ORG" "$BLOCK_LIST" --apply
else
  echo "[4/4] 跳过 block（要执行加 --auto-apply）"
  echo "      待 block 名单: $BLOCK_LIST"
  echo "      手动执行: bash $SCRIPT_DIR/batch-block.sh $ORG $BLOCK_LIST --apply"
fi

# 更新 snapshot
cp "$CACHE_DIR/current.txt" "$SNAPSHOT"
echo ""
echo "Snapshot 已更新到 $SNAPSHOT"

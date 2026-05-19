#!/usr/bin/env bash
# 批量 block GitHub org 的 bot 账号
# 用法：
#   ./batch-block.sh <org> <list-file>          # dry-run，只打印
#   ./batch-block.sh <org> <list-file> --apply  # 真正执行
#
# 效果：被 block 的账号在该 org 所有 repo 的 star/fork/watch 立刻被移除
# 前置：gh auth 需要 admin:org scope，且账号是 org admin/owner

set -euo pipefail

ORG="${1:?用法: $0 <org> <list-file> [--apply]}"
LIST="${2:?用法: $0 <org> <list-file> [--apply]}"
APPLY="${3:-}"

LOG="block-$(date +%Y%m%d-%H%M%S).log"
TOTAL=$(wc -l < "$LIST" | tr -d ' ')
SUCCESS=0
ALREADY=0
FAILED=0
i=0

echo "Org: $ORG"
echo "名单: $LIST ($TOTAL 个账号)"
echo "模式: $([ "$APPLY" = "--apply" ] && echo '真实执行' || echo 'DRY RUN（加 --apply 才真跑）')"
echo "日志: $LOG"
echo "---"

while IFS= read -r user; do
  [ -z "$user" ] && continue
  i=$((i+1))

  if [ "$APPLY" != "--apply" ]; then
    printf "[%3d/%d] DRY-RUN: would block %s\n" "$i" "$TOTAL" "$user"
    continue
  fi

  # 先检查是否已被 block
  if gh api "/orgs/$ORG/blocks/$user" --silent 2>/dev/null; then
    printf "[%3d/%d] %-40s already blocked\n" "$i" "$TOTAL" "$user" | tee -a "$LOG"
    ALREADY=$((ALREADY+1))
    continue
  fi

  # 执行 block
  if gh api -X PUT "/orgs/$ORG/blocks/$user" --silent 2>>"$LOG"; then
    printf "[%3d/%d] %-40s BLOCKED\n" "$i" "$TOTAL" "$user" | tee -a "$LOG"
    SUCCESS=$((SUCCESS+1))
  else
    printf "[%3d/%d] %-40s FAILED\n" "$i" "$TOTAL" "$user" | tee -a "$LOG"
    FAILED=$((FAILED+1))
  fi

  sleep 0.3  # 限流，避免 secondary rate limit
done < "$LIST"

echo "---"
echo "完成: 新 block=$SUCCESS  已 block=$ALREADY  失败=$FAILED  总数=$TOTAL"
echo "日志: $LOG"

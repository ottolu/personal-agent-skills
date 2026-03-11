#!/usr/bin/env bash
set -euo pipefail

# backup-live-state.sh
#
# 目标：
# - 对 live workspace 当前状态做只读友好的归档备份。
# - 默认 dry-run，仅展示将备份什么。
# - 备份内容侧重“回滚前置”：skills/、常见根文件，以及现有 symlink 映射清单。
# - 不修改 live 文件，不调用 gateway。
#
# 备份产物：
# - tar.gz 归档（尽量保留 live 状态）
# - symlinks.tsv（记录 live/skills 下每个 symlink 当前指向）
#
# 可选：
# - --apply            真正写入备份文件
# - --output-dir PATH  指定备份目录

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LIVE_ROOT="${LIVE_ROOT:-$HOME/.openclaw/workspace}"
OUTPUT_DIR="${BACKUP_ROOT:-$PROJECT_ROOT/backups}"
DRY_RUN=1

log() { printf '[backup-live-state] %s\n' "$*"; }
warn() { printf '[backup-live-state][warn] %s\n' "$*" >&2; }
die() { printf '[backup-live-state][error] %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage:
  bootstrap/backup-live-state.sh [--apply] [--output-dir PATH]

默认行为：dry-run，只打印备份计划。

备份内容：
  - live workspace 下的 skills/
  - 常见根文件（若存在）: AGENTS.md USER.md SOUL.md TOOLS.md IDENTITY.md MEMORY.md SESSION-STATE.md
  - live/skills 下一级 symlink 映射清单

说明：
  - 不会修改 live 文件
  - 不会调用 gateway
  - 建议在 relink / install 前先执行 --apply
EOF
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      DRY_RUN=0
      ;;
    --output-dir)
      shift
      [[ $# -gt 0 ]] || die "--output-dir 需要一个路径参数"
      OUTPUT_DIR="$1"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "未知参数: $1"
      ;;
  esac
  shift
done

[[ -d "$LIVE_ROOT" ]] || die "live workspace 不存在: $LIVE_ROOT"
command -v tar >/dev/null 2>&1 || die "tar 不可用"

STAMP="$(date +%Y%m%d-%H%M%S)"
BASENAME="live-state-${STAMP}"
TMP_LIST="${OUTPUT_DIR}/${BASENAME}.include.txt"
LINKS_TSV="${OUTPUT_DIR}/${BASENAME}.symlinks.tsv"
ARCHIVE="${OUTPUT_DIR}/${BASENAME}.tar.gz"

ROOT_FILES=(
  AGENTS.md
  USER.md
  SOUL.md
  TOOLS.md
  IDENTITY.md
  MEMORY.md
  SESSION-STATE.md
)

log "live root: $LIVE_ROOT"
log "backup output dir: $OUTPUT_DIR"
log "archive target: $ARCHIVE"
log "symlink manifest: $LINKS_TSV"

run "mkdir -p \"$OUTPUT_DIR\""

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "将纳入备份的候选内容："
  if [[ -d "$LIVE_ROOT/skills" ]]; then
    printf '  - %s\n' "$LIVE_ROOT/skills"
  else
    printf '  - [missing] %s\n' "$LIVE_ROOT/skills"
  fi
  for name in "${ROOT_FILES[@]}"; do
    if [[ -e "$LIVE_ROOT/$name" ]]; then
      printf '  - %s\n' "$LIVE_ROOT/$name"
    fi
  done
  if [[ -d "$LIVE_ROOT/skills" ]]; then
    log "当前 live/skills 一级 symlink 清单："
    find "$LIVE_ROOT/skills" -mindepth 1 -maxdepth 1 -type l -print | while IFS= read -r link; do
      printf '  - %s -> %s\n' "$link" "$(readlink "$link")"
    done
  fi
  log "dry-run 完成；未写入任何备份文件"
  exit 0
fi

mkdir -p "$OUTPUT_DIR"
: > "$TMP_LIST"
: > "$LINKS_TSV"
printf 'path\ttarget\n' >> "$LINKS_TSV"

if [[ -d "$LIVE_ROOT/skills" ]]; then
  printf 'skills\n' >> "$TMP_LIST"
  find "$LIVE_ROOT/skills" -mindepth 1 -maxdepth 1 -type l -print | while IFS= read -r link; do
    printf '%s\t%s\n' "${link#"$LIVE_ROOT"/}" "$(readlink "$link")" >> "$LINKS_TSV"
  done
fi

for name in "${ROOT_FILES[@]}"; do
  if [[ -e "$LIVE_ROOT/$name" ]]; then
    printf '%s\n' "$name" >> "$TMP_LIST"
  fi
done

if [[ ! -s "$TMP_LIST" ]]; then
  warn "没有找到可备份的目标；仅保留 symlink manifest"
fi

(
  cd "$LIVE_ROOT"
  tar -czf "$ARCHIVE" -T "$TMP_LIST"
)

rm -f "$TMP_LIST"
log "备份完成: $ARCHIVE"
log "symlink manifest 已写入: $LINKS_TSV"
log "提示：回滚时可先参考 symlink manifest，再手动恢复对应链接/文件"

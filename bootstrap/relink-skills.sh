#!/usr/bin/env bash
set -euo pipefail

# relink-skills.sh
#
# 目标：
# - 将 repo 中的 skills 逐目录软链到 live workspace 中。
# - 对模板类文件采用 copy_if_missing：仅当 live 中缺失时才复制。
# - 默认 dry-run，不覆盖 live 文件，不删除 live 文件。
# - 在执行任何写操作前要求已完成/确认备份。
#
# 默认约定：
#   repo 根目录:    <this-script>/..
#   repo skills:    <repo>/skills
#   repo templates: <repo>/templates/workspace
#   live root:      ~/.openclaw/workspace
#
# 注意：
# - 该脚本只会从 repo 级 templates/workspace 做 copy_if_missing。
# - skill 自带的 assets/ 不会被这里直接自动复制到 workspace 根目录。
#
# 你也可以通过环境变量覆盖：
#   LIVE_ROOT, REPO_SKILLS_DIR, TEMPLATE_DIR

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LIVE_ROOT="${LIVE_ROOT:-$HOME/.openclaw/workspace}"
REPO_SKILLS_DIR="${REPO_SKILLS_DIR:-$PROJECT_ROOT/skills}"
TEMPLATE_DIR="${TEMPLATE_DIR:-$PROJECT_ROOT/templates/workspace}"
BACKUP_SCRIPT="${SCRIPT_DIR}/backup-live-state.sh"

DRY_RUN=1
FORCE=0
ASSUME_BACKED_UP=0

log() { printf '[relink-skills] %s\n' "$*"; }
warn() { printf '[relink-skills][warn] %s\n' "$*" >&2; }
die() { printf '[relink-skills][error] %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage:
  bootstrap/relink-skills.sh [--apply] [--force] [--assume-backed-up]

默认行为：仅打印计划（dry-run）。

Options:
  --apply             真正创建 symlink / copy_if_missing
  --force             允许替换“指向本 repo 之外”的同名 symlink；仍不会覆盖普通文件/目录
  --assume-backed-up  跳过“先备份”的强提醒（仅在 --apply 时有意义）
  -h, --help          显示帮助

Safety:
  - skills 采用逐目录 symlink
  - templates 采用 copy_if_missing
  - 不会覆盖 live 普通文件
  - 不会删除 live 文件
EOF
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

ensure_backup_preflight() {
  if [[ "$DRY_RUN" -eq 1 || "$ASSUME_BACKED_UP" -eq 1 ]]; then
    return 0
  fi
  [[ -x "$BACKUP_SCRIPT" ]] || die "执行写操作前需要备份脚本，但未找到: $BACKUP_SCRIPT"
  log "写操作前先执行备份脚本"
  "$BACKUP_SCRIPT" --apply
}

link_skill_dir() {
  local src="$1"
  local name dest current
  name="$(basename -- "$src")"
  dest="$LIVE_ROOT/skills/$name"

  if [[ ! -d "$src" ]]; then
    warn "跳过非目录 skills 源: $src"
    return 0
  fi

  if [[ -e "$dest" || -L "$dest" ]]; then
    if [[ -L "$dest" ]]; then
      current="$(readlink "$dest")"
      if [[ "$current" == "$src" ]]; then
        log "已存在正确 symlink: $dest -> $src"
        return 0
      fi
      if [[ "$FORCE" -eq 1 ]]; then
        run "ln -sfn \"$src\" \"$dest\""
        log "已更新 symlink: $dest -> $src"
        return 0
      fi
      warn "目标已是其他 symlink，未修改（可加 --force）: $dest -> $current"
      return 0
    fi

    warn "目标已存在且不是 symlink，出于安全考虑跳过: $dest"
    return 0
  fi

  run "mkdir -p \"$(dirname -- "$dest")\""
  run "ln -s \"$src\" \"$dest\""
  log "将创建 symlink: $dest -> $src"
}

copy_if_missing() {
  local src="$1"
  local rel="$2"
  local dest="$LIVE_ROOT/$rel"

  if [[ ! -e "$src" ]]; then
    warn "模板源不存在，跳过: $src"
    return 0
  fi

  if [[ -e "$dest" || -L "$dest" ]]; then
    log "目标已存在，按 copy_if_missing 跳过: $dest"
    return 0
  fi

  run "mkdir -p \"$(dirname -- "$dest")\""
  if [[ -d "$src" ]]; then
    run "cp -R \"$src\" \"$dest\""
  else
    run "cp \"$src\" \"$dest\""
  fi
  log "将复制缺失模板: $src -> $dest"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      DRY_RUN=0
      ;;
    --force)
      FORCE=1
      ;;
    --assume-backed-up)
      ASSUME_BACKED_UP=1
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

log "repo root: $PROJECT_ROOT"
log "live root: $LIVE_ROOT"
log "skills source: $REPO_SKILLS_DIR"
log "template source: $TEMPLATE_DIR"

[[ "$LIVE_ROOT" == "$HOME/.openclaw/workspace" ]] || warn "当前 LIVE_ROOT 已被覆盖为自定义路径: $LIVE_ROOT"
[[ -d "$REPO_SKILLS_DIR" ]] || warn "skills 目录不存在（可先创建后再运行）: $REPO_SKILLS_DIR"
[[ -d "$TEMPLATE_DIR" ]] || warn "templates 目录不存在（可先创建后再运行）: $TEMPLATE_DIR"

ensure_backup_preflight

if [[ -d "$REPO_SKILLS_DIR" ]]; then
  while IFS= read -r -d '' dir; do
    link_skill_dir "$dir"
  done < <(find "$REPO_SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
fi

if [[ -d "$TEMPLATE_DIR" ]]; then
  while IFS= read -r -d '' path; do
    rel="${path#"$TEMPLATE_DIR"/}"
    copy_if_missing "$path" "$rel"
  done < <(find "$TEMPLATE_DIR" -mindepth 1 -maxdepth 1 -print0 | sort -z)
fi

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "dry-run 完成；未修改 live workspace"
else
  log "relink 完成；未覆盖 live 普通文件，未删除 live 文件"
fi

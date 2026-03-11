#!/usr/bin/env bash
set -euo pipefail

# install-openclaw.sh
#
# 目标：
# - 为 live workspace 准备“安全安装前检查”与“备份前置提示”骨架。
# - 默认不写入、不覆盖、不调用 gateway。
# - 仅在显式传入 --apply 后才执行安装命令；且仍然不会触碰 gateway。
#
# 设计原则：
# - 默认 DRY_RUN=1，先看计划再执行。
# - 不直接改 live workspace 内容。
# - 不覆盖已有文件。
# - 将“备份 live 状态”作为任何潜在变更前的前置步骤。

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
BACKUP_SCRIPT="${SCRIPT_DIR}/backup-live-state.sh"

DRY_RUN=1
ASSUME_YES=0
PREFIX="${OPENCLAW_PREFIX:-$HOME/.local}"
INSTALL_CMD="npm install -g openclaw"

log() { printf '[install-openclaw] %s\n' "$*"; }
warn() { printf '[install-openclaw][warn] %s\n' "$*" >&2; }
die() { printf '[install-openclaw][error] %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage:
  bootstrap/install-openclaw.sh [--apply] [--yes] [--prefix PATH]

默认行为：只做检查与打印计划（dry-run）。

Options:
  --apply         真正执行安装命令；默认仅 dry-run
  --yes           跳过交互确认（仅在 --apply 时有意义）
  --prefix PATH   指定安装前缀（默认: $OPENCLAW_PREFIX 或 ~/.local）
  -h, --help      显示帮助

Notes:
  - 本脚本不会调用 openclaw gateway。
  - 本脚本不会修改 live workspace 文件。
  - 真正安装前，建议先运行 bootstrap/backup-live-state.sh 做备份。
EOF
}

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] %s\n' "$*"
  else
    eval "$@"
  fi
}

confirm() {
  local prompt="$1"
  if [[ "$ASSUME_YES" -eq 1 ]]; then
    return 0
  fi
  read -r -p "$prompt [y/N] " answer
  [[ "$answer" =~ ^[Yy]$ ]]
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply)
      DRY_RUN=0
      ;;
    --yes)
      ASSUME_YES=1
      ;;
    --prefix)
      shift
      [[ $# -gt 0 ]] || die "--prefix 需要一个路径参数"
      PREFIX="$1"
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

log "project root: ${PROJECT_ROOT}"
log "install prefix: ${PREFIX}"

command -v bash >/dev/null 2>&1 || die "bash 不可用"
command -v npm >/dev/null 2>&1 || die "npm 不可用，无法安装 openclaw"

if command -v openclaw >/dev/null 2>&1; then
  log "检测到现有 openclaw: $(command -v openclaw)"
  run "openclaw --version || true"
else
  log "当前未检测到 openclaw，可执行全新安装"
fi

if [[ -x "$BACKUP_SCRIPT" ]]; then
  log "安装前建议先备份 live 状态"
  run "\"$BACKUP_SCRIPT\""
else
  warn "未找到可执行的备份脚本: $BACKUP_SCRIPT"
fi

log "计划执行的安装命令："
run "npm_config_prefix=\"$PREFIX\" $INSTALL_CMD"

if [[ "$DRY_RUN" -eq 1 ]]; then
  log "dry-run 完成；未执行任何安装写操作"
  exit 0
fi

confirm "确认执行 openclaw 安装？" || die "用户取消安装"

mkdir -p "$PREFIX"
npm_config_prefix="$PREFIX" npm install -g openclaw

log "安装完成。下一步建议："
log "1) 重新打开 shell，确保 PATH 包含 ${PREFIX}/bin"
log "2) 运行 bootstrap/doctor.sh 做环境检查"
log "3) 如需同步 skills，运行 bootstrap/relink-skills.sh --apply"

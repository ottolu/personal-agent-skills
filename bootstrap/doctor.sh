#!/usr/bin/env bash
set -euo pipefail

# doctor.sh
#
# 目标：
# - 只读检查 bootstrap 所需环境是否齐备。
# - 默认无副作用，不调用 gateway。
# - 输出可读的 PASS/WARN/FAIL，帮助正式 apply 前先体检。

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
LIVE_ROOT="${LIVE_ROOT:-$HOME/.openclaw/workspace}"
REPO_SKILLS_DIR="${REPO_SKILLS_DIR:-$PROJECT_ROOT/skills}"
TEMPLATE_DIR="${TEMPLATE_DIR:-$PROJECT_ROOT/templates/workspace}"
BACKUP_ROOT_DEFAULT="${BACKUP_ROOT:-$PROJECT_ROOT/backups}"

PASS_COUNT=0
WARN_COUNT=0
FAIL_COUNT=0

pass() { PASS_COUNT=$((PASS_COUNT + 1)); printf 'PASS  %s\n' "$*"; }
warn() { WARN_COUNT=$((WARN_COUNT + 1)); printf 'WARN  %s\n' "$*"; }
fail() { FAIL_COUNT=$((FAIL_COUNT + 1)); printf 'FAIL  %s\n' "$*"; }

check_cmd() {
  local cmd="$1"
  if command -v "$cmd" >/dev/null 2>&1; then
    pass "命令可用: $cmd ($(command -v "$cmd"))"
  else
    fail "命令缺失: $cmd"
  fi
}

printf '== bootstrap doctor ==\n'
printf 'project_root: %s\n' "$PROJECT_ROOT"
printf 'live_root:    %s\n' "$LIVE_ROOT"
printf 'skills_src:   %s\n' "$REPO_SKILLS_DIR"
printf 'templates(workspace): %s\n' "$TEMPLATE_DIR"
printf 'backup_root:  %s\n\n' "$BACKUP_ROOT_DEFAULT"

check_cmd bash
check_cmd find
check_cmd cp
check_cmd ln
check_cmd tar

if command -v npm >/dev/null 2>&1; then
  pass "npm 可用: $(npm --version 2>/dev/null || echo unknown)"
else
  warn "npm 不可用；若不安装 openclaw 可忽略，否则 install-openclaw.sh 将失败"
fi

if command -v openclaw >/dev/null 2>&1; then
  pass "openclaw 已安装: $(command -v openclaw)"
else
  warn "openclaw 未安装；可先运行 install-openclaw.sh（默认也是 dry-run）"
fi

if [[ -d "$PROJECT_ROOT" ]]; then
  pass "repo 根目录存在"
else
  fail "repo 根目录不存在"
fi

if [[ -d "$REPO_SKILLS_DIR" ]]; then
  SKILL_COUNT="$(find "$REPO_SKILLS_DIR" -mindepth 1 -maxdepth 1 -type d | wc -l | tr -d ' ')"
  pass "skills 目录存在，发现 ${SKILL_COUNT} 个一级目录"
else
  warn "skills 目录不存在；relink-skills.sh 仍可运行，但不会创建任何 skill symlink"
fi

if [[ -d "$TEMPLATE_DIR" ]]; then
  TEMPLATE_COUNT="$(find "$TEMPLATE_DIR" -mindepth 1 -maxdepth 1 | wc -l | tr -d ' ')"
  pass "templates 目录存在，发现 ${TEMPLATE_COUNT} 个一级条目"
else
  warn "templates 目录不存在；copy_if_missing 阶段将无事可做"
fi

if [[ -d "$LIVE_ROOT" ]]; then
  pass "live workspace 存在"
else
  warn "live workspace 不存在；若后续 apply，需要先创建或确认路径"
fi

if [[ -e "$LIVE_ROOT" && ! -d "$LIVE_ROOT" ]]; then
  fail "live root 存在但不是目录"
fi

if [[ -d "$LIVE_ROOT/skills" ]]; then
  pass "live skills 目录存在"
else
  warn "live skills 目录不存在；apply 时会按需 mkdir -p"
fi

if [[ -x "$SCRIPT_DIR/backup-live-state.sh" ]]; then
  pass "备份脚本存在且可执行"
else
  fail "备份脚本缺失或不可执行: $SCRIPT_DIR/backup-live-state.sh"
fi

if [[ -x "$SCRIPT_DIR/relink-skills.sh" ]]; then
  pass "relink 脚本存在且可执行"
else
  fail "relink 脚本缺失或不可执行: $SCRIPT_DIR/relink-skills.sh"
fi

if [[ -x "$SCRIPT_DIR/install-openclaw.sh" ]]; then
  pass "install 脚本存在且可执行"
else
  fail "install 脚本缺失或不可执行: $SCRIPT_DIR/install-openclaw.sh"
fi

printf '\n== summary ==\n'
printf 'pass=%s warn=%s fail=%s\n' "$PASS_COUNT" "$WARN_COUNT" "$FAIL_COUNT"

if [[ "$FAIL_COUNT" -gt 0 ]]; then
  exit 1
fi

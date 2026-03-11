# 安装与挂载说明

## 1. 安装目标

这里的“安装”不是重新部署 OpenClaw，也不是改 Gateway，而是：

- 准备 repo 目录
- 将某个已正式纳入 repo 的真实 skill 放入 repo
- 在 live workspace 中用**逐目录 symlink**挂载该 skill
- 对模板文件执行 **copy_if_missing**

整个过程：

- **不碰 Gateway**
- **不迁移运行态文件到 repo**
- **可回滚**

---

## 2. 前提

- live workspace：`/Users/luotto/.openclaw/workspace`
- repo staging：`/Users/luotto/.openclaw/workspace/repo-staging/personal-agent-skills`
- 当前 manifest 首批只处理 3 个正式纳入的 skill

### 2.1 当前 live workspace 中已识别到的真实候选 skills

- `blogwatcher`
- `find-skills`
- `github`
- `mcporter`
- `model-usage`
- `obsidian`
- `openclaw-x-intel-report`
- `oracle`
- `proactive-agent`
- `self-improving-agent`
- `tavily-search`

### 2.2 当前正式纳入 repo / manifest 的首批 3 个 skill

- `openclaw-x-intel-report`
- `proactive-agent`
- `self-improving-agent`

注意：候选集合不等于已纳入集合。当前安装文档默认以 manifest 中这 3 个 skill 为准。

---

## 3. 标准安装方式

### 步骤 A：把 skill 本体放入 repo

目标形态：

```text
repo-staging/personal-agent-skills/skills/<skill-name>/
```

说明：

- repo 中存放真实 skill 内容
- 只有真实内容已经进入 repo 时，才创建该子目录
- 不为尚未纳入的 skill 预留空目录
- live workspace 不再持有重复副本，而是通过 symlink 指向 repo

### 步骤 B：在 live workspace 创建逐目录 symlink

示例：

```text
workspace/skills/github -> repo-staging/personal-agent-skills/skills/github
```

要求：

- 以 skill 为单位单独挂载
- 不整体替换 `workspace/skills`
- 不影响未迁移目录

### 步骤 C：模板文件执行 copy_if_missing

当前 `bootstrap/relink-skills.sh` 的模板来源统一为：

```text
templates/workspace/
```

脚本会把该目录下一层内容按相对路径复制到 live workspace，仅在目标不存在时执行。

当前 staging 中实际可复制的 repo 级模板包括：

- `templates/workspace/HEARTBEAT.md`
- `templates/workspace/SESSION-STATE.md`
- `templates/workspace/memory/working-buffer.md`
- `templates/workspace/.learnings/ERRORS.md`
- `templates/workspace/.learnings/FEATURE_REQUESTS.md`
- `templates/workspace/.learnings/LEARNINGS.md`

执行规则：

- 目标不存在：复制
- 目标已存在：跳过

补充说明：

- 各 skill 自带的 `assets/` 仍属于 skill 包内容，会跟随 skill 目录一起进入 repo
- 但 relink 脚本**不会直接从 skill 的 `assets/` 自动注入 workspace 根目录**
- 若某个模板要成为统一初始化文件，应先整理到 `templates/workspace/`

**绝不覆盖本地已有文件。**

---

## 4. 不安装的内容

以下内容不属于 repo 安装范围：

- `memory/`
- `reports/`
- `.learnings/`
- session state
- 本地缓存
- Gateway 运行态

即：**运行态文件不入 repo。**

---

## 5. 当前推荐安装顺序

当前 manifest 首批已经收口到 3 个 skill，建议按风险从低到高处理：

### 第一组：流程型但相对边界清晰

- `openclaw-x-intel-report`

### 第二组：带模板或行为影响的 skill

- `self-improving-agent`
- `proactive-agent`

原因：

- `self-improving-agent` 含 `.learnings/` 相关内容，需要严格区分 repo 中的模板/示例与 live 运行态
- `proactive-agent` 含较多 `assets/`，但这些内容当前仍是 skill 包的一部分；只有被显式整理进 `templates/workspace/` 的文件才会按 copy_if_missing 触达 workspace 根目录

其余候选 skill 可在未来真实纳入 repo 后，再增补到 manifest 与安装顺序中。

---

## 6. 验收标准

完成单个 skill 安装后，应满足：

- live workspace 中该 skill 是指向 repo 的 symlink
- skill 可被正常读取
- 模板只做 copy_if_missing，没有覆盖现有本地文件
- `memory/`、`reports/`、`.learnings/` 未被纳入 repo
- 没有执行任何 Gateway 相关修改

---

## 7. 一句话安装原则

> skill 用逐目录 symlink，模板 copy_if_missing，运行态文件不入 repo，不碰 Gateway，可回滚。

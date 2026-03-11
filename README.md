# personal-agent-skills

这是一个**个人 Agent Skills 仓库骨架**，用于把当前已验证、可复用的 skill 以 **repo 管理 + workspace 挂载** 的方式整理出来。

## 目标

- 把“可版本化的 skill 内容”纳入 repo 管理
- 把“用户本地运行态文件”继续留在 live workspace
- 通过**逐目录 symlink**把 repo 中的 skill 挂到实际运行环境
- 对模板类文件采用 **copy_if_missing** 策略，避免覆盖现有本地配置
- **不碰 Gateway**，不改 daemon、不改服务状态、不改运行中配置
- 整个方案**可回滚**：移除 symlink / 删除新复制的模板即可恢复

## 设计原则

### 1. skill 用逐目录 symlink

repo 中的每个 skill 目录，按目录粒度单独挂载到 live workspace，例如：

- repo: `repo-staging/personal-agent-skills/skills/github`
- live: `workspace/skills/github -> <repo>/skills/github`

这样做的好处：

- skill 可以独立启用/回滚
- 不需要整体替换整个 `skills/`
- 不影响未纳入 repo 的其他本地内容
- 便于逐步迁移、逐步验证

### 2. 模板文件用 copy_if_missing

当前 bootstrap 脚本的 copy_if_missing 来源统一为：

- `templates/workspace/`

也就是说，只有被**明确整理进** `templates/workspace/` 的初始化文件，才会在目标不存在时复制到 live workspace。

当前 staging 中已存在的 repo 级模板包括：

- `templates/workspace/HEARTBEAT.md`
- `templates/workspace/SESSION-STATE.md`
- `templates/workspace/memory/working-buffer.md`
- `templates/workspace/.learnings/ERRORS.md`
- `templates/workspace/.learnings/FEATURE_REQUESTS.md`
- `templates/workspace/.learnings/LEARNINGS.md`

说明：

- skill 自带的 `assets/` 仍然保留在各自 skill 目录内，属于 skill 包内容
- 但 `bootstrap/relink-skills.sh` **不会直接从各 skill 的 `assets/` 自动复制到 workspace 根目录**
- 如需作为统一初始化模板生效，应先显式整理到 `templates/workspace/`

**原则：只补缺，不覆盖。**

也就是：

- 目标文件不存在：可复制
- 目标文件已存在：跳过，不修改

### 3. 运行态文件不入 repo

以下内容属于**运行态 / 本地态 / 高频变化内容**，**不进入本 repo**：

- `memory/`
- `reports/`
- `.learnings/`
- 任何用户私有运行日志
- session state / WAL / 本地缓存
- Gateway 运行配置与状态文件

本仓库只收：

- skill 本体
- skill 附带脚本
- references / assets / hooks
- 安装、迁移、回滚文档

### 4. 不碰 Gateway

本 repo 的职责仅限：

- 文档
- 目录结构约定
- skill 挂载方案
- 模板初始化说明

**不做：**

- `openclaw gateway start/stop/restart`
- 修改 Gateway 配置
- 改动 daemon 生命周期
- 改动在线运行态

### 5. 可回滚

迁移必须支持快速撤回：

- 删掉新增 symlink
- 恢复原目录/原文件
- 保留用户本地运行态不变
- 不依赖 Gateway 重启

## 当前文档

- `docs/architecture.md`：仓库架构与边界
- `docs/install.md`：安装/挂载方式
- `docs/migration.md`：从现有 workspace 迁移的步骤
- `docs/rollback.md`：回滚方案
- `docs/safety-checklist.md`：正式切换前后的人工审查清单

## 概念区分：当前 workspace 中的真实 skills vs 首批正式纳入 repo 的 skills

### A. 当前 live workspace 中已识别到的真实 skills（候选集合）

这些 skill 当前存在于 live workspace，可作为后续迁移候选；**这不等于它们都已经进入本 repo**：

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

### B. 第一批正式纳入 repo / manifest 的 3 个 skill（当前 staging 范围）

当前 `manifests/skills.yaml` 只声明首批正式纳入 repo 的 3 个 skill：

- `openclaw-x-intel-report`
- `proactive-agent`
- `self-improving-agent`

也就是说：

- **11 个 skill** 是“当前 workspace 中存在的真实候选集合”
- **3 个 skill** 是“当前 staging 已正式收口到 manifest 的首批纳入集合”

后续若要扩大纳入范围，应在 skill 内容实际落入 repo 后，再同步更新 manifests 与文档。

## 关于 `skills/` 目录的约束

- `skills/` 下**只有在某个 skill 已经有真实内容进入 repo 时**，才创建对应子目录。
- 如果某个子 skill 还没有真实迁移内容，**不要预留空目录**，避免让目录结构暗示“已纳入 repo”。
- 因此，文档中的目录树如果出现 skill 名称，应理解为**目标形态或已纳入清单**，不是要求一次性创建空壳。

## 建议的 repo 形态

```text
personal-agent-skills/
├─ README.md
├─ docs/
│  ├─ architecture.md
│  ├─ install.md
│  ├─ migration.md
│  ├─ rollback.md
│  └─ safety-checklist.md
├─ manifests/
│  ├─ skills.yaml
│  └─ compatibility.yaml
├─ bootstrap/
├─ templates/
│  └─ workspace/
└─ skills/
   └─ <仅在真正纳入某个 skill 时，放入真实目录>
```

注意：当前这一步先完成**文档骨架、manifest 边界与结构说明**。除已经真实纳入 repo 的 skill 外，不额外创建空的 skill 占位目录。

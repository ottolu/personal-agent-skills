# 迁移说明

## 1. 迁移目标

把 live workspace 中**已存在的真实 skill 候选**，按优先级逐个迁移到 repo 管理，同时保持运行环境稳定。

迁移的核心不是“搬空 workspace”，而是：

- repo 承载可版本化 skill 内容
- live workspace 保持运行入口
- skill 用**逐目录 symlink**接入 repo
- 模板按 **copy_if_missing** 初始化
- 运行态文件继续留在 live workspace

---

## 2. 明确不迁移的内容

以下内容**绝对不迁移进 repo**：

- `memory/`
- `reports/`
- `.learnings/`
- 各类运行日志、缓存、临时状态
- Gateway 相关状态与配置

也就是说：**运行态文件不入 repo。**

---

## 3. 盘点范围 vs 当前正式迁移范围

### 3.1 当前 live workspace 中已识别到的真实 skill 候选

当前确认存在的真实 skill 候选：

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

### 3.2 当前 staging 已正式纳入 manifest 的首批 3 个 skill

当前 `manifests/skills.yaml` 只声明以下 3 个 skill 为首批正式纳入对象：

- `openclaw-x-intel-report`
- `proactive-agent`
- `self-improving-agent`

因此：

- 本文会把 11 个真实 skill 当作**迁移候选池**来描述
- 但当前 staging 已正式收口到 manifest 的只有 **3 个 skill**
- 其余候选 skill 只有在真实内容进入 repo 后，才应补充到 manifests 与目录结构中

---

## 4. 推荐迁移流程

### 第 1 步：盘点 skill 内容

对单个 skill 识别以下内容：

- `SKILL.md`
- `_meta.json`
- `scripts/`
- `references/`
- `assets/`
- `hooks/`
- `.clawhub/`（若希望保留来源信息，可一并迁移）

### 第 2 步：识别模板 vs 运行态

迁移前先区分：

#### 可以进 repo 的

- skill 固定文档
- 脚本
- references
- assets 模板
- hooks

#### 不可以进 repo 的

- live `memory/`
- live `reports/`
- live `.learnings/`
- 用户实际运行中持续变化的数据

特别注意：

- `self-improving-agent` 自带 `.learnings/` 示例内容时，要区分“skill 内示例资产”与“live workspace 真正运行态 `.learnings/`”
- `proactive-agent` 的 `assets/*.md` 是模板资产，不等于 live 根目录正在使用的同名文件

### 第 3 步：复制 skill 到 repo

把 skill 本体复制到：

```text
repo-staging/personal-agent-skills/skills/<skill-name>
```

这里复制的是**版本化内容**，不是 live 运行态数据。

注意：

- 只有当某个 skill 的真实内容已经进入 repo，才创建该子目录
- 如果尚未迁移真实内容，**不要预留空目录**

### 第 4 步：live workspace 改为逐目录 symlink

把：

```text
workspace/skills/<skill-name>
```

变成指向 repo 的 symlink。

关键要求：

- 按 skill 单独处理
- 一次迁移一个或一小组
- 每一步都可撤销
- 不整体替换 `workspace/skills`

### 第 5 步：模板执行 copy_if_missing

如果 skill 需要向 live workspace 注入模板文件，规则必须是：

- 不存在才复制
- 已存在绝不覆盖

即：**模板 copy_if_missing**。

---

## 5. 当前首批 3 个 skill 的特殊注意事项

### `proactive-agent`

特点：

- 含 `assets/AGENTS.md`、`SOUL.md`、`USER.md`、`TOOLS.md`、`MEMORY.md`、`HEARTBEAT.md`
- 这些是初始化模板，不应覆盖 live 根目录现有文件

迁移要求：

- assets 可进 repo，作为 skill 包内容保留
- 若某份模板需要实际初始化到 live 根目录，应先整理进 `templates/workspace/`
- live 根目录模板只允许 copy_if_missing
- 已有文件必须保留原样

### `self-improving-agent`

特点：

- 含 `assets/LEARNINGS.md`、`assets/SKILL-TEMPLATE.md`
- skill 内还带 `.learnings/` 示例目录

迁移要求：

- skill 自带示例/参考内容可保留在 repo skill 内
- live workspace 下真实 `.learnings/` 不纳入 repo、不被覆盖
- 如需初始化，仅对 `templates/workspace/` 中已整理好的缺失模板执行 copy_if_missing

### `openclaw-x-intel-report`

特点：

- 包含 `scripts/`、`references/`、`assets/`
- 更像一个完整流程型 skill

迁移要求：

- repo 中完整保留版本化内容
- live 通过逐目录 symlink 引用
- 不把运行产出报告写回 repo

---

## 6. 对其余候选 skill 的规则

对于尚未进入当前首批 manifest 的候选 skill（如 `github`、`obsidian`、`oracle` 等），当前阶段只保留以下约束：

- 可以作为后续迁移候选继续评估
- 未完成真实迁移前，不应出现在 `skills/` 目录中作为空子目录
- 未正式纳入前，不应写入当前首批 manifest

---

## 7. 禁止事项

迁移过程中禁止：

- 为不存在真实内容的 skill 预创建空占位目录
- 修改 live `memory/`
- 修改 live `reports/`
- 修改 live `.learnings/`
- 顺手改 Gateway
- 用“大替换”方式整体改造 `workspace/skills`

---

## 8. 迁移完成的判定

单个 skill 迁移完成后，应满足：

- repo 中已有该 skill 的版本化内容
- live `skills/<name>` 已切换为指向 repo 的 symlink
- 模板文件仅做 copy_if_missing
- 运行态文件仍留在 live workspace
- 无 Gateway 变更
- 可以独立回滚

---

## 9. 迁移总原则

> skill 用逐目录 symlink，模板 copy_if_missing，运行态文件不入 repo，不碰 Gateway，可回滚。

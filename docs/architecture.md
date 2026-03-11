# 架构说明

## 1. 范围定义

这个 repo 只负责管理 **可版本化、可复用、适合代码审查** 的内容：

- skill 目录本体
- `SKILL.md`
- `_meta.json`
- `scripts/`
- `references/`
- `assets/`
- `hooks/`
- 相关文档
- manifests

这个 repo **不负责** 管理运行态内容，不承担 OpenClaw/Gateway 运维职责。

---

## 2. 核心边界

### 纳入 repo 的内容

适合进入版本控制的内容：

- 稳定的 skill 定义
- 可复用脚本
- 可复用模板 assets
- 参考资料 references
- hooks 实现
- 安装、迁移、回滚文档
- 描述已纳入 skill 的 manifests

### 不纳入 repo 的内容

以下内容保持在 live workspace，本 repo 不接管：

- `memory/`
- `reports/`
- `.learnings/`
- 本地日志、缓存、临时文件
- 用户私有运行数据
- Gateway 相关运行态与状态文件

一句话：**运行态文件不入 repo。**

---

## 3. 挂载模型

### 采用逐目录 symlink

每个 skill 按目录独立挂载，而不是把整个 `skills/` 一次性整体替换。

示意：

```text
repo-staging/personal-agent-skills/skills/github
        │
        └── symlink 到
                workspace/skills/github
```

即：

- repo 中保留真实内容
- live workspace 中保留入口目录名
- 入口通过 symlink 指向 repo 中对应 skill

### 为什么不用整体替换 `skills/`

因为整体替换会带来几个问题：

- 回滚粒度过粗
- 容易误伤未迁移 skill
- 难以灰度验证
- 与本地临时试验内容混杂

所以采用：**skill 用逐目录 symlink**。

---

## 4. 模板初始化策略

### copy_if_missing

对于模板类文件，统一采用 **copy_if_missing**：

- 目标不存在：复制
- 目标已存在：跳过
- 禁止覆盖用户已有文件

当前统一由 repo 级模板目录承载：

- `templates/workspace/HEARTBEAT.md`
- `templates/workspace/SESSION-STATE.md`
- `templates/workspace/memory/working-buffer.md`
- `templates/workspace/.learnings/ERRORS.md`
- `templates/workspace/.learnings/FEATURE_REQUESTS.md`
- `templates/workspace/.learnings/LEARNINGS.md`

补充说明：

- `proactive-agent`、`self-improving-agent` 等 skill 内部仍可保留各自 `assets/`
- 但 bootstrap 的 copy_if_missing 只认 `templates/workspace/`
- 若要把 skill 内某份模板作为统一初始化文件使用，应先显式整理进 `templates/workspace/`

这样可以保证：

- 第一次安装方便
- 后续升级不覆盖本地个性化内容
- 回滚时边界清晰

---

## 5. 概念区分：候选 skill 集合 vs 首批正式纳入集合

### 当前 live workspace 中已识别到的真实 skills（候选集合）

当前 live workspace 中，已确认存在以下真实 skill，可作为后续迁移候选：

1. `blogwatcher`
2. `find-skills`
3. `github`
4. `mcporter`
5. `model-usage`
6. `obsidian`
7. `openclaw-x-intel-report`
8. `oracle`
9. `proactive-agent`
10. `self-improving-agent`
11. `tavily-search`

### 第一批正式纳入 repo / manifest 的 3 个 skill

当前 staging 中，真正已经被 manifests 声明为“首批正式纳入”的只有：

1. `openclaw-x-intel-report`
2. `proactive-agent`
3. `self-improving-agent`

因此需要明确：

- 上面的 11 个 skill 是**现状盘点得到的候选集合**
- 当前正式纳入 repo 边界的是 **3 个 skill**
- 两者不能混写成“第一批已经全部纳入 repo”

---

## 6. `skills/` 目录策略

### 只为真实内容创建目录

`skills/` 目录遵循以下约束：

- 只有某个 skill 的真实内容已经进入 repo，才创建该子目录
- 如果某个 skill 尚未迁移真实内容，不预留空目录
- 文档可以列出候选 skill，但目录结构不能伪装成“已纳入”状态

这条规则的目的，是让目录结构与 manifest 边界保持一致，避免读者误判当前 repo 实际收录范围。

---

## 7. 推荐目录结构

当前推荐结构如下：

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
└─ skills/
   ├─ openclaw-x-intel-report/      # 已真实纳入时存在
   ├─ proactive-agent/              # 已真实纳入时存在
   └─ self-improving-agent/         # 已真实纳入时存在
```

如果未来扩大纳入范围，再按真实迁移进度新增其他 skill 子目录；**不要先建空壳目录**。

---

## 8. 风险控制

### 明确禁止

本仓库方案明确禁止以下动作：

- 修改 live workspace 的 `memory/`
- 修改 live workspace 的 `reports/`
- 修改 live workspace 的 `.learnings/`
- 修改 Gateway 运行方式
- 借迁移之名进行系统级重构
- 为未纳入的 skill 预创建空目录

### 允许动作

- 新建 repo 文档
- 维护 repo manifests
- 创建 repo 内 skill 内容副本（在正式迁移时）
- 创建指向 repo 的逐目录 symlink
- 按 copy_if_missing 复制模板
- 做可验证、可回滚的小步迁移

---

## 9. 回滚原则

架构从一开始就按“可回滚”设计：

- symlink 是可逆的
- 模板复制遵循 copy_if_missing，减少覆盖风险
- 运行态文件不入 repo，因此不需要从 repo 恢复运行态
- 不碰 Gateway，因此不需要依赖服务重启恢复

一句话总结：

> repo 管版本化内容，workspace 承载运行态；skill 用逐目录 symlink，模板 copy_if_missing，运行态文件不入 repo，不碰 Gateway，可回滚。

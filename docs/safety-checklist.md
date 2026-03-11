# Skills 仓库迁移安全与切换审查清单

> 适用范围：将 `repo-staging/personal-agent-skills` 中的内容迁移到 live workspace（`/Users/luotto/.openclaw/workspace/skills`）前后的人工操作检查。
>
> 目标：**先验证、再小步切换、随时可回滚**。本清单默认只处理 skill 仓库内容，**不修改 Gateway、不做全量覆盖**。

---

## 0. 操作原则（先看）

- [ ] **只在 staging 准备和审查**，不要直接在 live workspace 里边改边试。
- [ ] **一次只切一个 skill**，不要一次性全量替换整个 `skills/` 目录。
- [ ] **先备份，再切换**；没有备份就不执行切换。
- [ ] **优先按逐目录 symlink 切换 skill 入口**，不要把“单个 skill 切换”做成“整体目录替换”。
- [ ] **切换后立即做 smoke test**；测试不过，立刻回滚，不带病继续切下一个。
- [ ] **保留旧版本可恢复副本**，直到本轮全部 skill 验收通过。
- [ ] **只有 skill 真实内容进入 repo 时才创建对应子目录**，不要预留空目录冒充已纳入状态。

---

## 1. 迁移前检查项

### 1.1 路径与范围确认

- [ ] 确认 staging 路径正确：`/Users/luotto/.openclaw/workspace/repo-staging/personal-agent-skills`
- [ ] 确认 live skills 路径正确：`/Users/luotto/.openclaw/workspace/skills`
- [ ] 确认本次迁移对象仅限 **skills 仓库内容**，不是整个 workspace。
- [ ] 确认不会覆盖以下 live workspace 根目录文件：
  - `AGENTS.md`
  - `SOUL.md`
  - `USER.md`
  - `MEMORY.md`
  - `SESSION-STATE.md`
  - `TOOLS.md`
  - `HEARTBEAT.md`
  - `IDENTITY.md`
  - `memory/` 下所有文件
  - `.learnings/` 下所有文件
  - `.openclaw/` 下所有文件
  - `.git/` 下所有文件
  - `reports/` 下所有文件

### 1.2 内容审查

- [ ] 每个待迁移 skill 至少包含必要说明文件（通常是 `SKILL.md`，如有 `_meta.json` 也一并检查）。
- [ ] 检查 `SKILL.md` 中引用的相对路径是否在该 skill 目录内可解析。
- [ ] 检查是否误带本地临时文件，例如：
  - `*.tmp`
  - `*.log`
  - `.DS_Store`
  - 测试截图/录音/缓存文件
- [ ] 检查是否包含硬编码的私密信息：token、cookie、账号、绝对路径、个人邮箱、内部 URL。
- [ ] 检查是否出现会误导执行范围的文案，例如把 staging 路径写成 live 路径。
- [ ] 检查 manifest 与文档是否一致：候选 skill 集合可以更大，但当前正式纳入集合必须与 `manifests/skills.yaml` 一致。

### 1.3 切换准备

- [ ] 为 live `skills/` 目录做一次可恢复备份（推荐按 skill 目录单独备份）。
- [ ] 记录当前 live skills 列表，便于比对本次变更范围。
- [ ] 记录本次计划切换的 skill 名单，不临时夹带额外 skill。
- [ ] 确认当前没有正在依赖这些 skill 的关键长任务；若有，等任务结束再切换。
- [ ] 确认本次切换窗口允许快速验证和回滚，不在临睡前或无人值守时操作。

---

## 2. 当前建议切换顺序（以首批 3 个正式纳入 skill 为准）

原则：**先边界清晰，后高影响行为型。**

### 第一批首批 skill

- [ ] `openclaw-x-intel-report`

### 第二批首批 skill

- [ ] `self-improving-agent`
- [ ] `proactive-agent`

> 说明：
>
> - 当前 live workspace 中虽然还存在 `blogwatcher`、`github`、`obsidian` 等真实候选 skill，
>   但它们**当前不在首批正式 manifest 范围内**。
> - 如果未来把这些候选 skill 真实纳入 repo，再单独补充切换计划；当前不要因为文档里出现过候选清单，就把它们当成“已纳入”。

### 切换执行规则

每个 skill 都按下面顺序执行：

1. [ ] 备份 live 中该 skill 的当前目录
2. [ ] 确认 staging 中对应 skill 已有真实内容，且不是空目录
3. [ ] 先做目录 diff，确认只有预期变更
4. [ ] 将 live `skills/<skill-name>` 切换为指向 repo 对应目录的 symlink
5. [ ] 如需模板初始化，仅执行 copy_if_missing
6. [ ] 立刻执行该 skill 的 smoke test
7. [ ] 测试通过后，再继续下一个 skill
8. [ ] 测试失败则立即回滚，停止后续切换

> 不建议：
>
> - [ ] 不要整包 `skills/` 一次性覆盖
> - [ ] 不要把 `repo-staging/personal-agent-skills` 整体 rsync 到 workspace 根目录
> - [ ] 不要通过先创建空目录再“以后补内容”的方式制造假迁移状态

---

## 3. Smoke Test 清单（每切一个 skill 就做）

> 目标不是全量验收，而是确认：**能被发现、能被读取、关键说明不损坏、基本调用路径正常。**

### 3.1 通用 smoke test

对每个 skill，至少检查：

- [ ] live `skills/<skill-name>` 入口存在
- [ ] live `skills/<skill-name>` 为指向 repo 的正确 symlink
- [ ] `SKILL.md` 可正常读取
- [ ] 如存在 `_meta.json`，内容格式正常
- [ ] `SKILL.md` 中引用的本地文件路径存在
- [ ] skill 名称与目录名一致，没有大小写或拼写漂移
- [ ] 没有残留 staging 专用路径或无效绝对路径

### 3.2 行为 smoke test

- [ ] 用一句最小触发语确认该 skill 能被正常命中/使用
- [ ] 检查返回内容是否符合该 skill 的职责，而不是跑偏到别的 skill
- [ ] 检查是否出现明显报错、缺文件、缺路径、格式错误
- [ ] 检查是否引入新的高风险副作用（误写文件、误发消息、误触发外部动作）

### 3.3 针对高影响 skill 的额外检查

适用于：`proactive-agent`、`self-improving-agent`

- [ ] 检查是否会错误修改长期记忆、工作缓冲或学习文件
- [ ] 检查是否会在不该主动时过度主动
- [ ] 检查是否会放大 heartbeat / 记忆写入 / 错误记录频率
- [ ] 检查是否出现“默认自作主张”的行为漂移

### 3.4 本仓库当前首批 skill 的建议最小验证视角

- `openclaw-x-intel-report`：报告结构、质量门槛描述是否完整
- `self-improving-agent`：错误/修正/经验沉淀触发条件是否清晰
- `proactive-agent`：主动性边界、WAL/Working Buffer/Crons 等说明是否无歧义

---

## 4. 失败回滚步骤

> 原则：**回滚比排查更优先。** 先恢复服务质量，再慢慢分析原因。

### 4.1 触发回滚的条件

出现任一情况就回滚当前 skill：

- [ ] `SKILL.md` 缺失、损坏或无法读取
- [ ] skill 无法命中，或命中后明显跑偏
- [ ] 引用文件缺失
- [ ] 出现未预期的写操作 / 外部动作 / 高风险行为
- [ ] 主 agent 行为明显异常（尤其是高影响 skill 切换后）
- [ ] 你无法在几分钟内确认问题范围

### 4.2 单个 skill 回滚步骤

1. [ ] 停止继续切换后续 skill
2. [ ] 保留失败现场（不要覆盖日志/对比信息）
3. [ ] 删除或移开刚创建的 live `skills/<skill-name>` symlink
4. [ ] 将该 skill 的备份目录恢复回 live `skills/<skill-name>`
5. [ ] 如本次新建了模板文件，且确认未被人工修改，可按需删除这些新文件
6. [ ] 重新执行该 skill 的最小 smoke test
7. [ ] 确认恢复正常后，记录失败原因和观察现象
8. [ ] 本轮迁移暂停，除非问题已被明确修复并重新审查

### 4.3 如果多个 skill 连续出问题

- [ ] 不要继续逐个碰运气
- [ ] 回退到本轮开始前的整体备份点
- [ ] 重新审查 staging 仓库结构、命名和依赖文件
- [ ] 确认不是“路径基准变了 / 引用断了 / 说明写错目录”这类系统性问题

---

## 5. 哪些文件绝不能覆盖

> 这些文件/目录属于 **live workspace 的运行态、身份态、记忆态、环境态**，覆盖它们会把“skill 迁移”升级成“整机人格/上下文/运行状态变更”，风险完全不同。

### 5.1 workspace 根目录绝不能覆盖

- [ ] `AGENTS.md`
- [ ] `SOUL.md`
- [ ] `USER.md`
- [ ] `MEMORY.md`
- [ ] `SESSION-STATE.md`
- [ ] `TOOLS.md`
- [ ] `HEARTBEAT.md`
- [ ] `IDENTITY.md`

### 5.2 运行态/记忆态目录绝不能覆盖

- [ ] `memory/`
- [ ] `.learnings/`
- [ ] `.openclaw/`
- [ ] `.git/`
- [ ] `reports/`

### 5.3 为什么这些不能碰

- `AGENTS.md` / `SOUL.md` / `USER.md`：定义 agent 的行为边界、人格和用户上下文，覆盖后会导致行为突变。
- `MEMORY.md` / `memory/`：是长期/短期记忆，覆盖会造成记忆丢失或错乱。
- `SESSION-STATE.md`：是当前任务 RAM，覆盖会破坏在办事项。
- `.learnings/`：沉淀的是纠错与经验，覆盖会让同样错误反复发生。
- `.openclaw/`：通常包含运行相关状态，误覆盖容易引发不可预期故障。
- `.git/`：覆盖会破坏版本历史与当前仓库状态。
- `reports/`：可能含中间产物和审计信息，不应被 skill 仓库覆盖。

---

## 6. 为什么不碰 Gateway

> 这次是 **skills 内容迁移**，不是 **OpenClaw 基础设施变更**。Gateway 属于运行底座，和 skill 文档/逻辑切换不是一个层级的问题。

### 6.1 不碰 Gateway 的原因

- [ ] Gateway 变更会扩大故障半径：一旦出问题，不只是某个 skill 失效，而是整条工具链、连接链路都可能受影响。
- [ ] skills 问题与 Gateway 问题容易互相混淆：一边换 skill、一边动 Gateway，会让故障定位几乎失真。
- [ ] 本次目标是验证 skill 仓库迁移流程，而不是做运行环境升级。
- [ ] Gateway 重启/调整可能打断当前会话、后台任务、节点连接或浏览器/工具代理状态。
- [ ] 没有必要为了切 skill 去引入底层变量；这是典型的“本来是内容发布，结果顺手动了基础设施”的坏味道。

### 6.2 本次迁移的边界

- [ ] 不执行 `openclaw gateway restart`
- [ ] 不执行 `openclaw gateway stop`
- [ ] 不修改 Gateway 配置
- [ ] 不把 smoke test 失败归因到 Gateway，除非已有独立证据证明 Gateway 本身异常

---

## 7. 推荐执行模板（实际操作时照着走）

对每一个待切 skill，重复以下 checklist：

### Skill: `________________`

- [ ] 已确认 staging 版本内容完整
- [ ] 已确认该 skill 在当前 manifest 范围内
- [ ] 已备份 live 版本
- [ ] 已完成目录 diff
- [ ] live 入口切换仅限该 skill 的 symlink
- [ ] 已完成通用 smoke test
- [ ] 已完成该 skill 的最小行为验证
- [ ] 结果通过，可进入下一个 skill
- [ ] 如失败，已按回滚步骤恢复
- [ ] 已记录异常现象/原因

---

## 8. 最终放行条件

只有同时满足以下条件，才算本轮迁移通过：

- [ ] 所有计划中的 skill 都按顺序切换完成
- [ ] 每个 skill 都完成 smoke test
- [ ] 没有覆盖任何 live workspace 非 skill 文件
- [ ] 没有触碰 Gateway
- [ ] 没有残留未回滚的失败版本
- [ ] 已记录本轮变更列表、失败点（如有）、最终生效版本

---

## 9. 一句话原则

- **小步切、逐个验、出错就回、绝不顺手改底座。**

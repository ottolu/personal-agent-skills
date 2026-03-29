# Prompt patterns

## 1. Full Deep Research prompt

```text
帮我用 research-orchestrator 对“<主题>”做完整的 Deep Research。

要求：
1. 在正式调研前，先进行一轮轻量搜索，并基于初步结果给出一个研究计划。
2. 先不要直接写最终答案，先输出：
   - 你对任务的理解
   - 本次研究的 output orientation（exploration / decision-support / executive-brief / technical-due-diligence）及原因
   - 关键子问题拆解
   - 信息源类型与优先级
   - 计划使用哪些 subagent / research lanes，以及各自分工
   - red-team 会怎么做
   - 预期交付结构
   - 已知限制与可能的降级风险（如果有）
3. 调研必须采用 Full Deep Research 工作流，不要 silently downgrade 成 Lite 或单线程总结。
4. 至少采用以下多阶段结构：
   - 规划 / 拆题
   - 资料搜集 / Primary-source lane
   - 分维度研究（至少两个 domain lanes）
   - 独立 red-team / skeptic lane
   - 综合与结论
5. 信息源请分层处理：
   - Tier 1：官方资料、论文、文档、源码、发布会、filings、原始数据
   - Tier 2：可信媒体、研究博客、行业分析
   - Tier 3：社区讨论、社交媒体、论坛观点
6. 至少安排一个 lane 专门寻找：
   - 反例
   - 争议点
   - 失败案例
   - 相互矛盾的信息
   - 可能过时或带营销偏差的说法
7. 最终输出不要只是摘要，要包含：
   - 执行说明（用了哪些 lanes / red-team 是否完成 / source mix）
   - 全景综述
   - 关键事实
   - 主要分歧 / 争议点
   - 我的核心判断
   - 置信度分级
   - 尚未验证的问题
   - 如果继续深入，下一步该查什么
8. 结论中请区分：
   - 事实
   - 推断
   - 观点 / judgment
9. 如果因为工具或运行环境限制无法满足 Full Deep Research，要在计划阶段明确告诉我，不要静默降级。
```

## 2. Decision-support-oriented add-on

Use when the real goal is selection, recommendation, or strategic judgment.

Add:

```text
输出不要只追求信息覆盖，也要服务于后续决策、汇报或复用。
请优先形成可复用结构，如：
- 3~7 条关键判断
- 一页式结论摘要
- 关键证据表
- 对比矩阵
- 后续行动建议
```

## 3. Executive-brief-oriented add-on

Use when the final deliverable is for a leader, meeting, memo, or presentation.

Add:

```text
请采用结论先行的写法。
先给出 5 条最重要判断，再展开证据与分歧点。
控制结构清晰，避免信息堆砌。
```

## 4. Technical-due-diligence-oriented add-on

Use when the user wants serious technical scrutiny.

Add:

```text
请重点审查：
- 架构是否真实成立
- benchmark / eval 是否有缺口或不公平比较
- 是否存在 missing baseline
- 是否有 marketing inflation
- 哪些结论只是 demo 级证据，哪些结论有工程或 deployment 级证据
```

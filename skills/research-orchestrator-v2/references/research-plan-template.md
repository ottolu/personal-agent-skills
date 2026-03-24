# Research plan template

Use this shape after a light search and before a heavy run.

## 1. Task understanding
- what the user is really asking
- likely downstream use
- what is explicitly out of scope

## 2. Proposed mode
- exploration / decision-support / executive-brief / technical-due-diligence
- why this mode fits

## 3. Key subquestions
- 3-7 questions that determine whether the final answer will be useful
- phrase them so each one can drive a research lane

## 4. Source strategy
- Tier 1 targets
- Tier 2 context sources
- Tier 3 sentiment / operator signal sources
- obvious timeline or terminology traps to check

## 5. Research topology
- whether to stay single-threaded or use subagents
- if parallel: planner, primary-source scout, domain lanes, skeptic, synthesizer

## 6. Expected output structure
- executive summary
- key findings
- comparison matrix / taxonomy
- disagreements / uncertainty
- recommendation or next steps

## 7. Stop conditions
- what evidence would make the answer good enough
- what uncertainty will likely remain even after research

## Prompt-shaping fields

When rewriting or clarifying the task, try to make these explicit:
- subject
- objective
- audience
- output format
- constraints / scope boundaries
- source preferences
- whether subagents are warranted
- required skepticism level

## Example shorthand

```text
任务理解：
模式：
关键子问题：
信息源策略：
subagent 拆分：
预期交付结构：
主要风险 / 不确定性：
```

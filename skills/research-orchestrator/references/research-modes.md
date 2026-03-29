# Research orientations

`research-orchestrator` is **Full Deep Research only**.

The categories below are **output orientations / lenses**, not lighter execution modes.
They help shape the final deliverable while preserving the same deep-research contract:
- planning first
- light search before the full run
- subagents / role-based decomposition
- independent red-team lane
- source-tier handling
- facts / inferences / judgments separation

## 1. exploration-oriented

Use when the user wants breadth before judgment.

### Goal
- build a landscape map
- identify the main concepts, players, and fault lines
- surface what is worth deeper follow-up

### Typical outputs
- topic map / taxonomy
- key players or approaches
- major open questions
- first-pass comparisons
- suggested next-step research lanes

### Output emphasis
- favor breadth without losing structure
- do not overstate conclusions
- still maintain full-research verification discipline

## 2. decision-support-oriented

Use when the user ultimately needs a recommendation, choice, or strategic judgment.

### Goal
- support a decision with evidence, tradeoffs, and structured comparisons
- reduce ambiguity, not just summarize material

### Typical outputs
- recommendation
- comparison matrix
- pros / cons / risks
- evidence table
- action options and suggested path

### Output emphasis
- optimize for decision usefulness
- distinguish must-know facts from nice-to-know background
- bias toward comparisons, implications, and tradeoffs

## 3. executive-brief-oriented

Use when the output will feed a leader, meeting, memo, presentation, or high-level update.

### Goal
- compress complexity into a high-signal brief
- keep structure crisp and conclusion-first

### Typical outputs
- 3-7 key judgments
- one-page summary
- supporting evidence bullets
- major uncertainties
- recommended next actions

### Output emphasis
- lead with conclusions
- compress aggressively without losing nuance
- do not drown the brief in raw detail
- still preserve methodological rigor under the hood

## 4. technical-due-diligence-oriented

Use when the user needs a serious technical assessment of a model, system, product, framework, or architecture.

### Goal
- determine what is technically real, differentiated, scalable, or risky
- separate demos and claims from underlying substance

### Typical outputs
- architecture breakdown
- capability / benchmark assessment
- implementation or deployment considerations
- technical risks and unknowns
- strategic technical judgment

### Output emphasis
- prioritize Tier 1 and primary evidence
- explicitly flag benchmark quality, missing baselines, and evaluation gaps
- require stronger red-team scrutiny than most other orientations

## Orientation selection hints

Choose the orientation based on downstream use:
- user says “先帮我摸清楚/梳理全景/建立地图” -> exploration-oriented
- user says “帮我判断/比较/选型/给建议” -> decision-support-oriented
- user says “给老板看/汇报/一页纸/高层摘要” -> executive-brief-oriented
- user says “技术上到底怎么样/架构是否成立/benchmark 靠不靠谱” -> technical-due-diligence-oriented

If the user asks for both landscape and recommendation, keep the same Full Deep Research workflow but bias the final output toward decision-support-oriented synthesis.

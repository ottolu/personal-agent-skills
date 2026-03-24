---
name: research-orchestrator-v2
description: Plan and execute deep research with explicit scoping, light-search-first planning, source-tiering, role-based parallel decomposition, red-team verification, and decision-ready synthesis. Use when the user asks for deep research, broad investigation, multi-round search, landscape mapping, competitor analysis, technical diligence, executive briefs, recommendation support, plan-first research, or work that should benefit from subagents instead of a one-shot answer.
---

# Research Orchestrator V2

Run research as a staged system, not a single long answer. Optimize for decision usefulness, evidence quality, contradiction-finding, and reusable outputs.

## 1. Frame before searching hard

Before heavy research, lock five things:
- the real decision or downstream use
- target audience and output shape
- in-scope vs out-of-scope boundaries
- key unknowns / subquestions
- whether this is narrow enough for one thread or broad enough for parallel lanes

If the request is underspecified, ask a small number of high-leverage questions. If it is clear enough, proceed.

## 2. Do a light search before committing to a plan

Never produce a blind research plan.

Use a quick first pass to identify:
- canonical names, aliases, and keywords
- likely Tier 1 sources
- obvious comparison targets
- moving parts, controversies, or timeline issues
- whether the topic is broad enough to justify subagents

Then present a short plan unless the user clearly asked to skip straight to execution.

If you need mode guidance or a planning template, read `references/research-modes.md` and `references/research-plan-template.md`.

## 3. Choose the right research mode

Use one dominant mode:
- **exploration**: map the space before judging
- **decision-support**: help choose, compare, or recommend
- **executive-brief**: compress into a leader-ready brief
- **technical-due-diligence**: test technical substance, benchmarks, and risk

Infer the mode from downstream use, not surface wording.

## 4. Split by role, not by arbitrary parallelism

When the task is broad, high-stakes, or explicitly deep, use role-based decomposition.

Default lanes:
1. **planner** — frame, split, and define success criteria
2. **primary-source scout** — collect Tier 1 evidence and canonical artifacts
3. **domain lane(s)** — investigate distinct dimensions such as architecture, product, market, adoption, GTM, or ecosystem
4. **skeptic / red-team** — look for contradictions, missing baselines, adverse evidence, or stale claims
5. **synthesizer** — merge, judge, classify uncertainty, and produce the final deliverable

Do not spawn multiple agents that all search the same angle with slightly different wording.

If needed, read `references/multi-agent-topologies.md`.

## 5. Use source tiers deliberately

Classify evidence while researching and again while writing:
- **Tier 1**: official docs, papers, repos, benchmarks, filings, launch posts, source code, vendor docs
- **Tier 2**: credible technical blogs, industry analysis, strong media coverage, expert writeups
- **Tier 3**: community discussion, social posts, anecdotal operator reports

Rules:
- anchor factual claims in Tier 1 whenever possible
- use Tier 2 to contextualize and compare
- use Tier 3 for sentiment, practitioner signal, and hypothesis generation
- do not let Tier 3 dominate a serious memo unless the topic itself is community sentiment

If needed, read `references/evidence-and-output-rules.md`.

## 6. Require a red-team pass for serious work

For any nontrivial memo, explicitly search for:
- contradictory evidence
- benchmark or demo inflation
- outdated claims
- missing baselines
- deployment friction
- weak adoption evidence
- reasons the obvious conclusion might be wrong

If evidence conflicts, preserve the disagreement. Do not force fake certainty.

## 7. Separate facts, inferences, and judgments

In the final synthesis, distinguish:
- **facts** — directly supported by sources
- **inferences** — conclusions derived from evidence
- **judgments** — recommendations, bets, or strategic interpretation

Add confidence levels when useful.

## 8. Tailor the final output to the real use

Prefer decision-ready structure over raw notes.

Common sections:
- executive summary
- task framing and scope
- key findings
- comparison matrix or dimension table
- disagreements / uncertainty
- confidence levels
- implications / recommendations
- next-step research lanes

Mode emphasis:
- **exploration** -> taxonomy, landscape map, open questions, follow-up lanes
- **decision-support** -> recommendation, tradeoffs, risks, action options
- **executive-brief** -> 3-7 key judgments, concise evidence bullets, next actions
- **technical-due-diligence** -> architecture, evidence quality, benchmark scrutiny, technical risks, unknowns

If needed, read `references/output-shapes.md`.

## 9. When not to use this skill

Do not use this skill for:
- a narrow factual lookup answerable from 1-3 sources
- summarizing one article or one PDF without broader research intent
- lightweight brainstorming with no evidence requirement
- simple web search where no staged workflow is needed

## 10. Prompt shaping pattern

When reformulating the task, try to make these fields explicit:
- subject
- objective
- audience
- output format
- scope constraints
- source preferences
- whether subagents are warranted
- required skepticism / verification level

If useful, read `references/research-plan-template.md` for a reusable plan shape.

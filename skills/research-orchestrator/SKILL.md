---
name: research-orchestrator
description: Plan and execute deep research tasks with explicit scoping, phased search, source-tiering, multi-agent decomposition, red-team verification, and decision-ready synthesis. Use when the user asks for detailed research, broad/deep investigation, multi-round search, competitor/landscape analysis, technical deep dives, or wants a plan before execution and may benefit from subagents.
---

# Research Orchestrator

Run research as a **full deep-research workflow**, not a one-shot answer.

This skill is **Full Mode only**.
Do not silently downgrade it into a light search, a single-thread summary, or a quick memo.
If the user explicitly invokes `research-orchestrator`, the default expectation is:
- longer-horizon research
- broader source coverage
- explicit planning before execution
- multi-agent / multi-lane decomposition
- an independent red-team pass
- structured synthesis with evidence separation

If the task is too small for this workflow, say so explicitly and ask whether the user wants a lighter workflow or a different skill. Do **not** silently execute a Lite or Standard version inside this skill.

## Research orientation

This skill has only one execution mode: **Full Deep Research**.

You may still choose an **orientation** for the final output based on downstream use:
- **exploration-oriented**: map a space, build a taxonomy, identify open questions
- **decision-support-oriented**: support a recommendation or choice with tradeoffs and evidence
- **executive-brief-oriented**: produce conclusion-first, leader-friendly synthesis
- **technical-due-diligence-oriented**: stress-test technical claims, architecture, benchmarks, and risks

These are **output lenses**, not execution modes. They do not reduce the depth requirement.
If helpful, read `references/output-orientations.md`.

## Execution contract

If this skill is invoked, the minimum contract is:
1. **Light search first**
2. **Execution plan before full run**
3. **Subagents or equivalent role-based lanes are required**
4. **A dedicated red-team lane is required**
5. **Source tiers must be handled explicitly**
6. **Final output must separate facts, inferences, and judgments**
7. **Final output must include a short execution header**

If any part of this contract cannot be fulfilled because of tool/runtime constraints, tell the user during planning. Do not silently degrade.

## Planning step is mandatory

Before doing heavy research, always present a compact planning block that covers:
- task understanding
- research orientation and why it fits
- target output and audience
- key subquestions
- scope boundaries
- source-tier plan
- subagent / lane topology and responsibilities
- red-team plan
- expected deliverable structure
- any known constraints or downgrade risks

If the topic is ambiguous, ask a small number of high-value clarification questions.
If the topic is clear enough, proceed after the plan.

## Light search before full run

Before locking the plan, do a quick search pass to identify:
- official / primary sources
- canonical names, aliases, dates, and entities
- likely comparison targets
- obvious controversies or moving parts
- whether the problem should be split differently than the default topology

Use this pass to refine the plan. Do not jump straight to final synthesis.

## Subagents are mandatory in Full Mode

For this skill, subagents are not optional in normal operation.
At minimum, use role-based decomposition with clear differentiation.
Do not spawn multiple agents that search the same angle with no role distinction.

### Minimum required topology

Use this baseline unless there is a strong reason to adapt it:
1. **Planner**
   - define the frame
   - split the work into dimensions
   - set success criteria and unknowns
2. **Primary-source scout**
   - collect Tier 1 sources
   - normalize names, dates, objects, and primary evidence
3. **Domain lane A**
   - first major dimension
4. **Domain lane B**
   - second major dimension
5. **Red-team / skeptic**
   - search for contradictions, adverse evidence, weak evidence, outdated claims, and overreach
6. **Main synthesizer**
   - merge, deduplicate, classify evidence, and write the final view

You may add more lanes when the topic justifies it, but do not go below this topology without explicitly telling the user why.

### When to expand beyond the minimum topology

Add more lanes when:
- the topic naturally splits into 3+ distinct dimensions
- breadth matters as much as depth
- multiple expert angles are needed
- verification is especially important
- the user explicitly asks for very broad, deep, or multi-angle research

If helpful, read `references/multi-agent-topologies.md`.

## Red-team lane is mandatory

Every serious research memo produced via this skill must include an independent red-team lane.
This lane should actively look for:
- contradictory claims
- missing baselines
- outdated information
- marketing inflation / hype narratives
- adverse evidence
- weak or circular sourcing
- explanations that sound plausible but do not match the timing or evidence

Do not reduce the red-team pass to a token paragraph. It should materially pressure-test the main thesis.

### Minimum red-team deliverable standard

At minimum, the red-team output should cover:
1. **Evidence gaps**
   - which important claims are still weakly supported, indirectly supported, or not yet well evidenced
2. **Alternative explanations**
   - what competing interpretation could also explain the observed facts
3. **Boundary conditions**
   - where the main conclusion may fail, narrow, or stop generalizing

If no strong counterexample is found, do not just say "no issues found".
Explicitly state:
- which challenge directions were checked
- which strong rebuttals were not found
- which uncertainties still remain unresolved

## Source tiers are required

Distinguish source quality in both research and output:
- **Tier 1**: official docs, papers, repos, benchmarks, launch posts, filings, direct datasets, primary disclosures
- **Tier 2**: credible analysis, industry coverage, high-quality technical writeups, expert commentary
- **Tier 3**: community discussion, social posts, anecdotal operator feedback, forum sentiment

Prefer Tier 1 for factual claims.
Use Tier 3 mainly for hypothesis generation, sentiment, and edge-case signals.
Do not let Tier 3 drive major conclusions unless clearly labeled and corroborated.

## Evidence model is required

In the final synthesis, separate:
- **facts**: directly supported by sources
- **inferences**: reasoned conclusions built from facts
- **judgments**: strategic views, recommendations, or prioritization

Also include confidence levels where useful.
Do not collapse facts, inferences, and opinions into one bucket.

## Default split patterns

Use these as defaults when planning lane structure.

### Market / macro / investing topic
- market facts and timeline
- driver analysis and transmission mechanisms
- sector / style / asset-chain implications
- red-team

### Technical topic
- architecture / implementation
- benchmarks / eval quality
- ecosystem / tooling / adoption
- red-team

### Product / company topic
- product / capability map
- market / GTM / adoption
- competition / positioning
- red-team

### Landscape topic
- taxonomy / segmentation
- top players and positioning
- evidence by segment
- strategic implications
- red-team

## Output requirements

Prefer structured, decision-useful outputs over note dumps.
The final output should usually contain:
- short execution header
- executive summary
- key questions
- key findings
- source-tier-aware evidence
- disagreements / uncertainties
- facts vs inferences vs judgments
- implications / recommendations
- next-step research suggestions

### Required execution header

At the top of the final output, include a compact execution header covering:
- **Mode**: Full Deep Research
- **Orientation**: exploration / decision-support / executive-brief / technical-due-diligence
- **Topology**: planner + primary-source + domain lanes + red-team + synthesis
- **Subagents used**: yes/no and how many
- **Red-team pass**: completed / constrained
- **Source mix**: Tier 1 dominant / mixed / etc.
- **Evidence model**: facts / inferences / judgments separated

## Failure modes to avoid

Do not do any of the following:
- silently downgrade to a lighter workflow
- write a long report while skipping subagents and still treat it as full deep research
- skip the primary-source lane
- skip the red-team lane
- spawn multiple agents with no role distinction
- summarize material without making judgments where the task requires them
- mix facts, inferences, and opinions into a single undifferentiated narrative

## Prompt pattern

Use this shape when formulating or refining a deep-research request:
- subject
- objective
- audience
- output format
- constraints / scope boundaries
- source preferences
- required subagent topology
- required verification / skepticism level
- expected deliverable structure

If helpful, read `references/prompt-patterns.md` for reusable request templates.

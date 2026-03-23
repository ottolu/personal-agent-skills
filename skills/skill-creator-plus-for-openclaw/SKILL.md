---
name: skill-creator-plus-for-openclaw
description: Create, improve, evaluate OpenClaw-compatible skills with structured iteration loops, eval design, review artifacts, and packaging guidance. Use when building a new skill, improving an existing skill, designing evals, comparing skill revisions, or tightening trigger descriptions and release readiness.
---

# Skill Creator Plus for OpenClaw

Build skills as products, not just folders. Use a loop of draft -> test -> review -> improve -> package, but keep the workflow compatible with OpenClaw instead of assuming Anthropic-only runtime features.

## What this skill is for

Use this skill to do one or more of the following:
- create a new OpenClaw skill from scratch
- improve or refactor an existing skill
- design eval prompts and iteration loops for a skill
- compare two versions of a skill qualitatively or structurally
- improve a skill description so triggering is clearer
- package a finished skill into a distributable artifact

This skill is intentionally modeled after the stronger parts of Anthropic Skill Creator 2.0, but it should not assume Claude-only harnesses like `claude -p`, `.claude/commands`, or Anthropic-specific trigger-eval internals unless the user explicitly asks for that environment.

When execution automation is needed, prefer explicit OpenClaw-compatible command templates and persisted run artifacts over hidden runtime assumptions.

## Core operating principle

Separate skill work into five stages:
1. **Frame**: understand what the skill should do and when it should trigger
2. **Draft**: create or improve the skill structure and bundled resources
3. **Evaluate**: define realistic test prompts and compare outputs across iterations
4. **Improve**: revise based on observed failure modes, not just vague preference
5. **Package**: validate, package, and summarize next-step recommendations

Do not jump straight from “create a skill” to “done”. Prefer an explicit iteration loop when the skill matters.

## OpenClaw compatibility rule

When borrowing ideas from Anthropic Skill Creator 2.0:
- keep the methodology
- adapt the mechanics
- do not blindly copy Claude-specific runtime assumptions

Examples:
- OK to reuse the idea of eval sets, baselines, benchmark summaries, reviewer loops, and description optimization
- Not OK to assume OpenClaw can directly use `.claude/commands`, `claude -p`, or the exact Anthropic trigger-eval implementation

If the user wants direct compatibility with Anthropic tooling, say so explicitly and isolate that path as a separate workflow.

## Workflow

### 1. Capture intent
Before editing files, determine:
- what the skill should enable
- what phrases or contexts should trigger it
- what outputs matter
- whether the task is subjective or objectively testable
- whether this needs a minimal draft or a full eval-driven loop

If the user already has a draft skill, inspect it before proposing changes.

### 2. Choose the work mode
Use one of these modes:
- **draft-only**: create a practical v0 quickly
- **structured-build**: create skill + references/scripts + test prompts
- **eval-first**: focus on test cases, success criteria, and benchmark design
- **refactor-and-upgrade**: improve an existing skill without losing its purpose
- **package-and-polish**: validate, package, and tighten description/structure

If the user does not specify a mode, infer it from the stage of the work.

### 3. Draft the skill with progressive disclosure
Keep the main `SKILL.md` lean and procedural.
Move heavy details into `references/`.
Add `scripts/` only when deterministic repeated work is clearly useful.

Prefer this split:
- `SKILL.md`: workflow, triggers, routing, constraints
- `references/`: templates, rubrics, schemas, examples, evaluation guidance
- `scripts/`: repeatable helpers for validation, report generation, or packaging support

### 4. Design realistic evals
When a skill is important enough to test, create realistic prompts that a real user would plausibly say.

Good evals should:
- test trigger boundaries
- test representative usage patterns
- test likely failure modes
- include near-miss or ambiguity cases where helpful

Avoid toy evals unless the skill itself is toy-sized.

### 5. Compare iterations explicitly
When improving a skill, do not only rely on intuition. Compare:
- previous vs current structure
- previous vs current description clarity
- expected trigger scenarios
- output quality on representative prompts
- whether the skill overfits to narrow examples

If exact quantitative benchmarking is not available, do a structured qualitative comparison.

### 6. Improve the description deliberately
The description field is a trigger surface, not just documentation.

A good description should include:
- what the skill does
- when to use it
- specific trigger contexts
- adjacent phrases users may say without naming the skill directly

Avoid descriptions that are so narrow they undertrigger, or so broad they hijack unrelated tasks.

### 7. Package only after validation
Before packaging:
- validate frontmatter and structure
- remove dead placeholders
- check references are actually referenced when needed
- ensure scripts/resources are justified

Then package and summarize:
- what the skill now does
- what remains weak
- what should be tested next

## Recommended resource set

Read these references when needed:
- `references/openclaw-vs-anthropic.md` for design adaptation principles
- `references/eval-loop.md` for an OpenClaw-compatible eval workflow
- `references/eval-schemas.md` for Anthropic-inspired eval data structures adapted to OpenClaw
- `references/eval-rubric.md` for scoring and analyzer-style review dimensions
- `references/iteration-review-template.md` for per-iteration review output
- `references/openclaw-eval-adaptation-notes.md` for what to preserve vs adapt from Anthropic 2.0
- `references/description-optimization.md` for improving trigger descriptions
- `references/release-checklist.md` for final validation and packaging criteria

Use helper scripts only when they provide real leverage.
Current helpers:
- `scripts/generate_eval_skeleton.py`: generate a starter `evals.json` skeleton for a chosen mode
- `scripts/summarize_skill_diff.py`: compare two skill directories and flag changes likely to affect trigger/workflow/resource behavior
- `scripts/generate_iteration_review.py`: aggregate one or more `grading.json` files into a starter `iteration-review.json`
- `scripts/aggregate_benchmark_summary.py`: aggregate grading/review artifacts into a lightweight `benchmark-summary.json`
- `scripts/generate_grading_stub.py`: create per-eval grading stub files from an `evals.json`
- `scripts/run_openclaw_skill_eval.py`: prepare a structured iteration workspace with per-eval folders, run records, and grading stubs
- `scripts/run_skill_eval_review_cycle.py`: orchestrate the prepare/finalize parts of an eval-review cycle
- `scripts/run_openclaw_eval_executor.py`: execute prepared eval directories via an explicit command template and persist transcripts/stdout/stderr
- `scripts/grade_openclaw_eval.py`: grade one eval directory into a heuristic but schema-compliant `grading.json`
- `scripts/improve_skill_description.py`: analyze should-trigger / should-not-trigger cases and propose a stronger description rewrite
- `scripts/apply_description_rewrite.py`: apply a chosen candidate description back into `SKILL.md`

## Anti-patterns

Avoid these failure modes:
- creating a skill that is just a vague essay
- overfitting a skill to one conversation
- copying Anthropic runtime assumptions into OpenClaw without adaptation
- adding scripts because they feel impressive rather than necessary
- packaging a skill before checking whether it is actually coherent
- optimizing description keywords without thinking about real trigger intent

## Output expectations

When helping with a skill, prefer outputs like:
- a proposed skill architecture
- a diff plan for improvements
- a realistic eval set
- a benchmark / review plan
- a packaging readiness checklist

If the user asks to create the skill, produce a usable draft first, then propose the next iteration loop rather than trying to finish the whole maturity ladder in one shot.

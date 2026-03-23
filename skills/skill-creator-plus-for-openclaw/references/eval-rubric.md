# Eval rubric for OpenClaw skill iteration

This rubric is deeply inspired by the evaluator / analyzer mindset in Anthropic Skill Creator 2.0, but tuned for OpenClaw-compatible skill work.

## Principle

Do not ask only “does the skill look good?”
Ask:
- did it trigger for the right kinds of tasks?
- did it help produce better behavior?
- did it remain general enough to be reusable?
- did changes improve substance, not just appearance?

## Core dimensions

Score each dimension from 1 to 5.

### 1. Trigger clarity
Does the description make it clear when the skill should and should not be used?

Look for:
- concrete trigger contexts
- natural user phrasing
- healthy specificity without overclaiming
- clear relation between description and actual body

Bad signs:
- vague one-line description
- body contains trigger logic that should have been in frontmatter
- obvious undertrigger / overtrigger risk

### 2. Workflow coherence
Does the skill give a clear operating path once triggered?

Look for:
- good sequencing
- strong decision points
- explicit routing to references/scripts
- low ambiguity in fragile steps

Bad signs:
- skill reads like an essay, not a workflow
- missing transitions between steps
- references exist but are not meaningfully integrated

### 3. Output usefulness
Does the skill help the agent produce outputs that are actually more useful?

Look for:
- decision-useful structure
- realistic deliverables
- cleaner or more repeatable outcomes
- less reinvention of routine work

Bad signs:
- prettier wording without better outcomes
- lots of context but no actionability
- output format not aligned with user need

### 4. Evidence of real leverage
Does the skill create leverage beyond what a decent base model would already do?

Look for:
- domain-specific process knowledge
- reusable references
- deterministic helper scripts when justified
- non-obvious heuristics or constraints

Bad signs:
- generic advice any good model already knows
- scripts that exist for show, not leverage
- references that just restate common sense

### 5. Overfitting risk
Did the skill become too tailored to one conversation or one eval set?

Look for:
- instructions that generalize
- examples that guide instead of constrain
- abstractions that survive variant phrasing

Bad signs:
- brittle wording copied from one user example
- hard-coded assumptions with no reason
- over-specialized structure that will miss adjacent tasks

### 6. Evaluation quality
Are the evals themselves good enough to trust?

Look for:
- realistic prompts
- discriminating expectations
- near-miss cases when trigger quality matters
- at least some assertions that test meaningful outcomes

Bad signs:
- toy prompts
- assertions that pass for obviously wrong output
- no failure-mode coverage

## Suggested summary labels
- 4.5-5.0: excellent
- 3.5-4.4: strong
- 2.5-3.4: workable but needs iteration
- 1.5-2.4: weak
- 1.0-1.4: poor

## Review questions

After scoring, answer these:
1. What genuinely improved in this iteration?
2. What got worse or more brittle?
3. Which evals are non-discriminating and should be improved?
4. What should be changed before packaging?
5. What is the single highest-leverage next revision?

## Analyzer-style notes

Anthropic 2.0 gets one thing very right: aggregate scores hide patterns.
So when reviewing, also record freeform notes such as:
- expectations that always pass and therefore do not prove value
- evals with high variance or instability
- places where the skill adds quality but also obvious latency/verbosity cost
- regressions that summary scores alone might miss

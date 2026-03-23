# Eval schemas for OpenClaw skill iteration

This file is heavily inspired by Anthropic Skill Creator 2.0 `references/schemas.md`, but adapted for OpenClaw-compatible workflows.

## Design intent

Use schemas to make skill iteration repeatable.
A good eval system should answer:
- what prompt was tested
- what success meant
- what actually happened
- what regressed or improved
- what to change next

These schemas are intentionally lighter than Anthropic's full harness, but they preserve the same spirit: eval sets, per-run grading, iteration history, and benchmark summaries.

---

## 1. evals.json

Store realistic eval prompts and what each eval is trying to test.

Suggested location:
- inside a skill workspace: `evals/evals.json`
- or inside a review workspace for that skill

```json
{
  "skill_name": "example-skill",
  "mode": "structured-build",
  "evals": [
    {
      "id": 1,
      "name": "core-happy-path",
      "prompt": "Create a skill for summarizing customer interview notes into a decision memo.",
      "goal": "Checks that the skill draft covers routing, output structure, and realistic user needs.",
      "files": [],
      "expectations": [
        "Produces a valid SKILL.md structure",
        "Description includes concrete trigger contexts",
        "Uses references for heavy details instead of bloating SKILL.md"
      ],
      "tags": ["core", "draft"],
      "priority": "high"
    }
  ]
}
```

### Fields
- `skill_name`: skill name under evaluation
- `mode`: optional work mode such as `draft-only`, `structured-build`, `eval-first`, `refactor-and-upgrade`, `package-and-polish`
- `evals[].id`: stable numeric identifier
- `evals[].name`: short label for humans
- `evals[].prompt`: realistic user request
- `evals[].goal`: what this eval is testing
- `evals[].files`: optional input file list
- `evals[].expectations`: discriminating expectations, not fluff checks
- `evals[].tags`: optional grouping labels
- `evals[].priority`: `high`, `medium`, or `low`

### Guidance
- prefer real user phrasing over synthetic toy prompts
- include at least one near-miss or ambiguity eval when trigger boundaries matter
- include at least one failure-mode eval for nontrivial skills

---

## 2. run-record.json

Capture what happened in one execution of one eval.

Suggested location:
- `<workspace>/iteration-N/<eval-name>/run-record.json`

```json
{
  "eval_id": 1,
  "eval_name": "core-happy-path",
  "iteration": "iteration-1",
  "configuration": "with_skill",
  "prompt": "Create a skill for summarizing customer interview notes into a decision memo.",
  "artifacts": {
    "skill_path": "skills/example-skill",
    "outputs_dir": "iteration-1/core-happy-path/outputs"
  },
  "notes": [
    "Produced a clean skill structure",
    "Description is still too generic"
  ],
  "status": "completed"
}
```

### Fields
- `configuration`: usually `with_skill`, `without_skill`, `old_skill`, or `candidate_skill`
- `artifacts`: pointers to output locations
- `notes`: plain-language observations
- `status`: `completed`, `partial`, `failed`

---

## 3. grading.json

Record expectation grading for a run. Preserve Anthropic's good habit of storing evidence next to each verdict.

Suggested location:
- sibling to a run output directory

```json
{
  "expectations": [
    {
      "text": "Description includes concrete trigger contexts",
      "passed": true,
      "evidence": "The description explicitly mentions creating, improving, evaluating, benchmarking, and packaging OpenClaw-compatible skills."
    },
    {
      "text": "Uses references for heavy details instead of bloating SKILL.md",
      "passed": false,
      "evidence": "The main SKILL.md still contains detail that should be split into references/."
    }
  ],
  "summary": {
    "passed": 1,
    "failed": 1,
    "total": 2,
    "pass_rate": 0.5
  },
  "quality_notes": {
    "strengths": ["Clear workflow framing"],
    "weaknesses": ["Description under-specifies trigger boundaries"],
    "uncertainties": ["Need real trigger evals to know if over/undertriggering is fixed"]
  },
  "eval_feedback": {
    "suggestions": [
      {
        "assertion": "Uses references for heavy details instead of bloating SKILL.md",
        "reason": "Add a size or structure-oriented expectation so the eval is more discriminating."
      }
    ],
    "overall": "Good start, but expectations still lean structural rather than outcome-driven."
  }
}
```

### Important fields
- `expectations[].text`
- `expectations[].passed`
- `expectations[].evidence`

Keep these exact field names. Anthropic 2.0 does this for good reason: they are clear, stable, and easy to aggregate later.

---

## 4. iteration-review.json

Capture the conclusion of one iteration. This is the OpenClaw-friendly substitute for a heavier benchmark/reviewer stack when full automation is unavailable.

Suggested location:
- `<workspace>/iteration-N/iteration-review.json`

```json
{
  "iteration": "iteration-2",
  "skill_name": "example-skill",
  "summary": {
    "what_improved": [
      "Description now contains clearer trigger phrases",
      "References split reduced SKILL.md bloat"
    ],
    "what_regressed": [
      "The draft became more specific but slightly less general"
    ],
    "open_issues": [
      "Still no tested evidence for trigger precision"
    ]
  },
  "scores": {
    "trigger_clarity": 4,
    "workflow_coherence": 4,
    "output_usefulness": 4,
    "overfitting_risk": 3,
    "resource_leverage": 3
  },
  "next_actions": [
    "Add near-miss evals",
    "Test with one baseline comparison"
  ]
}
```

### Score scale
Use a 1-5 scale unless the user wants something else:
- 1 = poor
- 2 = weak
- 3 = acceptable
- 4 = strong
- 5 = excellent

---

## 5. history.json

Track the broader improvement arc across versions.

```json
{
  "started_at": "2026-03-22T14:00:00Z",
  "skill_name": "example-skill",
  "current_best": "iteration-2",
  "iterations": [
    {
      "version": "iteration-1",
      "parent": null,
      "pass_rate": 0.50,
      "result": "baseline",
      "is_current_best": false
    },
    {
      "version": "iteration-2",
      "parent": "iteration-1",
      "pass_rate": 0.75,
      "result": "won",
      "is_current_best": true
    }
  ]
}
```

### Why keep this
Anthropic 2.0 is right about one thing: once iterations start, memory gets fuzzy. Persist the progression.

---

## 6. benchmark-summary.json

Use this when you have enough repeated eval evidence to summarize a skill iteration more formally.

```json
{
  "metadata": {
    "skill_name": "example-skill",
    "timestamp": "2026-03-22T14:30:00Z",
    "evals_run": [1, 2, 3],
    "configurations": ["with_skill", "old_skill"]
  },
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.80, "stddev": 0.10},
      "review_score": {"mean": 4.2, "stddev": 0.4}
    },
    "old_skill": {
      "pass_rate": {"mean": 0.55, "stddev": 0.08},
      "review_score": {"mean": 3.4, "stddev": 0.3}
    }
  },
  "delta": {
    "pass_rate": "+0.25",
    "review_score": "+0.8"
  },
  "notes": [
    "New version improved trigger clarity but still shows moderate overfitting risk on narrow prompts"
  ]
}
```

### OpenClaw note
Unlike Anthropic's benchmark viewer schema, this version is intentionally lighter. It is for stable review and comparison, not viewer lock-in.

# OpenClaw eval adaptation notes

## Why this exists

Anthropic Skill Creator 2.0 has a richer built-in evaluation harness than OpenClaw currently exposes by default. That does not mean OpenClaw should skip eval discipline.

## Adaptation strategy

Adopt the same layers, but loosen the runtime coupling:
- eval set
- per-run grading
- iteration review
- history tracking
- benchmark summary when enough evidence exists

## What to preserve from Anthropic 2.0
- realistic eval prompts
- evidence-backed grading
- analyzer-style notes
- explicit comparison across iterations
- treating description quality as measurable work

## What to avoid copying blindly
- exact viewer schema lock-in unless needed
- Claude-specific trigger internals
- assuming browser-backed review flow always exists
- assuming all evals can be automated quantitatively

## OpenClaw-friendly fallback

If full automation is unavailable, do:
1. realistic eval prompts
2. structured grading with evidence
3. iteration-review.json
4. history.json
5. lightweight benchmark-summary.json when repeated comparisons exist

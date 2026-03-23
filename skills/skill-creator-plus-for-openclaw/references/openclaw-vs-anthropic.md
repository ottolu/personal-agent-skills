# OpenClaw vs Anthropic adaptation notes

## Design goal

Borrow the strongest ideas from Anthropic Skill Creator 2.0 without assuming Anthropic-specific runtime mechanics.

## Safe to borrow directly
- iterative skill-development loop
- test-prompt design
- reviewer / red-team thinking
- benchmark and comparison mindset
- description optimization as a first-class concern
- packaging only after validation

## Must be adapted for OpenClaw
- trigger evaluation implementation
- subagent orchestration mechanics
- browser/viewer assumptions
- CLI command assumptions such as `claude -p`
- directory/layout assumptions tied to `.claude/commands`

## Practical rule

Preserve the methodology. Re-implement the mechanics only where OpenClaw has an equivalent or where a lightweight substitute can be defined.

## Recommended OpenClaw stance

Treat Anthropic 2.0 as a design reference, not as a drop-in dependency.

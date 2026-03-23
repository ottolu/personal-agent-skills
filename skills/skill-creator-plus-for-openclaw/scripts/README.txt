Placeholder scripts directory.

For v0, this skill intentionally does not add helper Python scripts yet.
Reason: the workflow and references are defined, but the exact OpenClaw-compatible eval harness is not stable enough to justify hard-coding scripts.

Add scripts later only when a repeated deterministic need is proven, for example:
- generate eval skeletons
- compare skill metadata across iterations
- assemble benchmark summaries

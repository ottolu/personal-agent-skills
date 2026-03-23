# OpenClaw-compatible eval loop

## Purpose

Use this loop when a skill matters enough that drafting once is not sufficient.

## Loop

1. Draft or update the skill
2. Create a small eval set of realistic prompts
3. Define what success looks like for each eval
4. Run the skill on those prompts
5. Record observations:
   - what triggered correctly
   - what undertriggered or overtriggered
   - what outputs were weak or noisy
6. Compare current iteration against previous iteration or against a no-skill baseline when possible
7. Revise the skill
8. Repeat

## Eval categories
- core happy-path prompts
- near-miss prompts
- edge cases
- failure-mode prompts
- packaging/readiness checks

## Comparison dimensions
- trigger clarity
- workflow coherence
- output usefulness
- overfitting risk
- unnecessary verbosity
- missing reusable resources

## Output from an eval pass
- short summary of what improved
- list of regressions
- next changes to make

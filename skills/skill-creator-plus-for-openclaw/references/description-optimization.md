# Description optimization

## Why it matters

The `description` field determines whether a skill is considered at all. Treat it as part routing logic, part product positioning.

## What a strong description should contain
- what the skill does
- concrete trigger contexts
- phrases a user might naturally say
- nearby scenarios where the skill should still trigger even if not explicitly named

## Common failure modes
- too short and generic -> undertriggers
- too narrow -> misses adjacent but valid requests
- too broad -> causes false positives
- body contains trigger logic that should have been in the description

## Improvement process
1. List should-trigger scenarios
2. List should-not-trigger scenarios
3. Rewrite the description to better separate the two
4. Check whether the description matches the actual body of the skill
5. Prefer realistic user phrasing over taxonomy jargon

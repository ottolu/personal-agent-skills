# Reading Note Spec

This file defines the stable output contract for reading notes.

## Final paths

- WeChat OA: `20-Knowledge/Reading/WeChat-OA/`
- Web article: `20-Knowledge/Reading/Web/`
- `00-Inbox/Reading/` is temporary capture only, not a final destination once正文 is available.

## Filename rules

### WeChat OA
`YYYY-MM-DD - <Title>（<Publisher>）.md`

Example:
`2026-04-12 - Harness Engineering, Symphony 与 Frontier（51CTO技术栈）.md`

### Web article
`YYYY-MM-DD - <Title>（Web）.md`

If a better stable publisher/site label is available, prefer:
`YYYY-MM-DD - <Title>（<Site>）.md`

## Frontmatter schema

Required keys, in this order:

```yaml
---
type: reading-note
source_type: wechat-oa | web-article
title:
publisher:
author:
url:
date_published:
date_ingested:
status: distilled | partial
review_week:
tags: [reading, wechat-oa, ...]
topics: [...]
signal_level: high | medium | low
---
```

## Tag rules

- Keep tags in frontmatter only.
- Use lowercase kebab-case English tags only.
- Always include:
  - `reading`
  - source tag: `wechat-oa` or `web-article`
- Target range: 4-8 tags total.
- Prefer domain/topic tags like `agent`, `memory`, `retrieval`, `vision`, `workflow`, `openai`.
- Do not use body hashtags like `#AI #Agent #OpenAI`.
- Do not mix casing styles like `Agent`, `SelfImprovement`, `DevTools`.

## Topics rules

- `topics` is freer than `tags`.
- Allow Chinese or English phrases.
- Use it for human-readable themes, not retrieval hygiene.

## Required section order

Keep this order stable:

1. `# <title>`
2. `## Source`
3. `## TL;DR`
4. `## Summary`
5. `## Key Points`
6. `## Original Text (Cleaned Archive)`
7. `## Key Quotes / Excerpts`
8. `## First-Principles Analysis`
9. `## My Observation`
10. `## Why It Matters for Lewei`
11. `## Follow-ups`

## Completion criteria

A note counts as complete only when all are true:

1. written to the final Obsidian path
2. cleaned original text preserved in the note
3. required frontmatter present
4. required section order present
5. lint passes

## Partial-note policy

Use `status: partial` only when you cannot recover the full正文.
A partial note should still include:
- source metadata
- what was recovered
- why extraction was incomplete
- next-step suggestion if relevant

## Anti-drift rules

If the note starts drifting into free-form essay mode, pull it back to the template.
If older notes use a legacy structure, normalize them only when asked or when already editing them.

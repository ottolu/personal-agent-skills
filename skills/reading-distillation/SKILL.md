---
name: reading-distillation
description: Distill article links into stable Obsidian reading notes. Use when a user sends one or more article URLs, especially `mp.weixin.qq.com`, and expects summary, first-principles analysis, cleaned original text archiving, weekly-review candidate tracking, or durable reading-note ingestion. Also use when standardizing or repairing reading-note format, tags, filenames, or section structure.
---

# Reading Distillation

Produce a **stable reading note**, not an ad-hoc chat summary.

## Non-negotiable standards

1. Route by **content type**, not by channel.
2. A reading-intake task is complete only after the target note is written to the final Obsidian path.
3. Preserve the **cleaned original text** in the note. A link plus summary is not enough.
4. Keep note structure stable using `assets/reading-note-template.md` and `references/note-spec.md`.
5. Keep tags in frontmatter only. Do not drift into body hashtags like `#AI #Agent`.
6. Before delivery, run the lint check and fix failures.
7. If extraction is partial or blocked, mark the note as partial instead of pretending completion.

## Workflow

### Step 1) Classify the request

Check for explicit overrides first:
- `只讨论`
- `别入库`
- `仅总结`
- `先收一下`
- `仅测试`

If none are present, default article links to reading-intake.

### Step 2) Pick the route

- `mp.weixin.qq.com` -> treat as `wechat-oa`
- Other article/blog URLs -> treat as `web-article`

For WeChat articles, prefer a real browser when lightweight fetch cannot recover the正文.

### Step 3) Write the note in the final structure

Read before the first note of the session:
- `references/note-spec.md`
- `references/tagging-taxonomy.md`

Use:
- `assets/reading-note-template.md`

Write the note directly to the final path. Do not use inbox as the final destination once the正文 is available.

### Step 4) Lint the note

Run:

```bash
python3 skills/reading-distillation/scripts/note_lint.py --file "<note.md>" --source-type <wechat-oa|web-article>
```

If lint fails, normalize the note before replying.

### Step 5) Deliver the chat summary

The chat reply should include:
- one-line conclusion
- key points
- why it matters / how it connects to Lewei's main thread
- final note path when helpful

Do not reply with a thin receipt like `已处理完成`.

## Path rules

Use the path rules in `references/note-spec.md`.

Default final destinations:
- WeChat OA -> `20-Knowledge/Reading/WeChat-OA/`
- Web article -> `20-Knowledge/Reading/Web/`

## Repair mode for old notes

When asked to normalize old notes:
1. preserve substance first
2. add frontmatter if missing
3. normalize filename, tags, and section order
4. preserve or restore cleaned original text when possible
5. re-run lint after edits

Do not aggressively rewrite the analysis voice unless the user asks.

## Multi-link batches

For multiple links:
- create one compliant note per article
- then add a short cross-article synthesis in chat
- create a separate synthesis note only if the user asks or the batch is high-value enough to promote

## Failure handling

If正文 extraction fails:
- save a partial note only when useful
- state what is missing
- avoid pretending the note is complete

If metadata is uncertain:
- prefer conservative fields
- do not invent author/publisher/date

If tags are uncertain:
- keep them sparse and stable using `references/tagging-taxonomy.md`
- prefer fewer correct tags over many noisy ones

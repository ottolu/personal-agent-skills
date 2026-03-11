---
name: openclaw-x-intel-report
description: Generate a high-signal daily X intelligence report for OpenClaw. Use when producing recurring OpenClaw X monitoring briefs, KOL/watchlist updates, Chinese/English hot-post summaries, or action-oriented social intelligence outputs. Enforce strict quality gates (relevance, engagement, depth, structure) and reject low-quality filler posts.
---

# OpenClaw X Intel Report

Produce a **decision-oriented** daily report, not a feed dump.

## Required Inputs

- Date window (default: last 24h; fallback: last 72h if signal shortage)
- Topic scope: `OpenClaw`, `clawdbot`, `clawhub`, major releases, real deployments
- Output language: Chinese

## Non-Negotiable Standards

1. Prioritize **high-signal posts** (real insight, measurable engagement, practical value).
2. Exclude low-value noise (thin hype, zero-context reposts, low-engagement filler).
3. Explain **what happened + why it matters + what to do next**.
4. Keep structure stable and machine-checkable.
5. If quality gate fails, regenerate before delivery.
6. Never fabricate metrics, links, or inferred facts.

## Workflow

### Step 1) Collect candidates

Use `xurl` first. Build candidates with the query pack in:
- `references/query-pack.md`

Collect both:
- author-driven high-signal KOL posts
- topic-driven hot posts (Chinese + English)

For every candidate, keep an explicit record of:
- query source
- source method (`search` / `read` / `reply_sampler` / manual follow-up)
- signal window (`24h` / `72h`)

**Important:** do not treat the query pack as a fixed full-sweep checklist. Use it as:
- fixed core recall
- dynamic expansion recall
- targeted whitelist top-up
- narrow fallback recall only when needed

If 24h candidates are insufficient, expand to 72h and mark those entries as fallback-window items.

### Step 2) Enrich each candidate

For each post, collect:
- post URL, timestamp
- metrics: likes/reposts/replies (and views if available)
- author profile URL + followers
- full text
- reply-sample insights (for top-priority posts)

Use:
- `xurl read <post_id_or_url>`
- `xurl user @handle`
- `scripts/reply_sampler.py` for conversation sampling

**Important:** `scripts/reply_sampler.py` is a **reply sample extractor**, not a final stance-analysis engine. Use it to gather candidate replies, then summarize support / disagreement / practical blockers manually or with a second pass. Do not treat raw top replies as consensus.

### Step 3) Score and filter

Apply rubric from:
- `references/scoring-rubric.md`

Keep only posts above the minimum threshold. When signal is low, allow limited fallback entries and explicitly tag them as low-confidence placeholders.

**Important selection rule:** low-engagement items should normally be excluded from the main report body.
If an item has `0 likes / 0 reposts / 0 replies`, treat it as a watchlist candidate by default unless it satisfies a strong evidence-backed exception rule.

Each selected entry should carry:
- score
- confidence level
- narrative tag

### Step 4) Assemble report using template

Fill:
- `assets/report-template.md`

Mandatory sections:
1. Executive insights (3-5 bullets)
2. Top priority signals (5 deep dives, each with reply insight)
3. KOL list (10-12 entries, ranked)
4. Chinese hot posts (3-5)
5. English hot posts (3-5)
6. Watchlist / low-engagement high-signal observations (0-3)
7. Actions for today (3 items, with owner/action/metric)
8. Quality checklist

### Step 5) Run quality gate

Run:
```bash
python3 skills/openclaw-x-intel-report/scripts/quality_gate.py --file <report.md>
```

If failed, fix and re-run. Do not deliver failing reports.

## Ranking rules

- KOL ranking priority:
  1) relevance score
  2) engagement quality (not just likes)
  3) practical execution value
  4) account influence (tie-breaker, not primary signal)

- Hot-post selection:
  - must be directly related to OpenClaw ecosystem
  - must include clear insight or practical signal
  - avoid duplicate narratives
  - should not include zero-engagement items in the main hot-post buckets

- Watchlist selection:
  - use for low-spread but evidence-backed operator / security / deployment signals
  - do not let watchlist items occupy Top 5 or CN/EN hot-post main slots

## Writing rules (important)

For each key item, write:
- **Signal**: what exactly happened
- **Interpretation**: why it matters now
- **Actionability**: what we should do today

Avoid generic lines like “值得关注/互动较高” without mechanism-level explanation.

## Low-signal mode

If the last 24h does not contain enough credible items:
1. expand to the last 72h
2. explicitly mark fallback entries as `72h`
3. prefer **reducing quantity before reducing quality**
4. shrink KOL / CN / EN section sizes before relaxing thresholds
5. move weak-but-interesting items into watchlist instead of stuffing them into the main body
6. if quality still cannot be met, report the blockage instead of filling with weak content

## Minimum publishable evidence set

- **Top 5** must include: post URL, time, interaction data, query source, source method, score, confidence, narrative tag, reply sample, and today-action.
- **KOL entries** must include: profile URL, post URL, interaction data, query source, score, confidence, and follow-up judgment.
- **CN/EN hot posts** must include: post URL, interaction data, query source, score, confidence, narrative tag, why-it-matters, and follow-up action.

If key evidence is missing, downgrade the claim and mark `未查到` rather than inventing data.

## Failure handling

If API/browser extraction degrades:
1. downgrade gracefully with transparent missing-field tags (`未查到`)
2. keep quality gate strict for structure and traceability
3. reduce quantity before reducing quality
4. preserve intermediate artifacts when possible (candidate JSON / reply sample JSON / draft markdown)

## Output discipline

- Prefer fewer high-quality entries over many weak entries.
- Do not let low-engagement filler enter the main body just to satisfy quotas.
- Use watchlist for early / low-spread but still credible observations.
- If quality cannot be met, explicitly report the blockage and missing data source.
- Do not let template completeness masquerade as evidence completeness.

# Query Pack

Use these in order. Start with 24h window, expand only if needed.

## Query strategy overview

Do not rely on brand-keyword matching alone. Build the candidate pool from four layers:
1. fixed core recall
2. dynamic expansion recall
3. whitelist-author recall
4. evidence-heavy / fallback recall

For every candidate, keep:
- `query_source`
- `source_method`
- `signal_window` (`24h` / `72h`)
- keep / drop reason during filtering

**Important operating rule:** the query pack is no longer “run everything at full width.”
Use a **query budget** and prefer tighter, higher-signal recall over broad noisy sweeping.

Recommended daily budget:
- fixed core: 8-10 queries
- dynamic expansion: 6-10 queries
- whitelist top-up: 3-5 queries
- total: **18-24 queries**

If the signal is obviously abundant, you do **not** need to exhaust the full budget.

---

## A. Fixed core recall (always run)

These queries define the minimum stable spine of the report.

### Official / core
- `from:openclaw OpenClaw`
- `from:steipete OpenClaw`

### Release / safety / incidents
- `OpenClaw release OR v2026`
- `OpenClaw security OR vulnerability OR fix`
- `OpenClaw incident OR postmortem OR outage`
- `OpenClaw gateway OR config validate`

### Deployment / workflow / ops
- `OpenClaw deployment OR docker OR local`
- `OpenClaw cron OR heartbeat OR monitor`
- `OpenClaw MCP OR tool integration`
- `OpenClaw memory OR gateway OR relay OR workflow`

**Why this layer exists:**
It covers the highest-value daily signal classes: official updates, security/incident movement, deployment/ops practice, and durable workflow evolution.

---

## B. Dynamic expansion recall (generate each run)

After the fixed core, generate **6-10 dynamic queries** from the most recent high-signal artifacts.

### B1. Expansion sources
Use the last 2-3 days of:
- passed daily reports
- high-score shortlisted candidates
- top-priority signals
- recurring reply-zone questions

### B2. What to extract
Generate expansions from:
- recurring mechanism keywords
- recurring narrative clusters
- high-signal handles not already in fixed core
- release-specific nouns
- high-friction user questions

### B3. Good dynamic keyword examples
If recent reports repeatedly surface:
- `provenance`
- `backup`
- `verify`
- `context engine`
- `acpx`
- `telegram dupes`
- `doctor`
- `gateway restart`

then dynamic queries can look like:
- `OpenClaw provenance`
- `OpenClaw backup verify`
- `OpenClaw context engine`
- `OpenClaw acpx ACP`
- `OpenClaw Telegram dupes`
- `OpenClaw doctor OR install check`

### B4. Dynamic author expansion
If a handle produced a top signal in the past 72h, add at most 1-2 account-scoped recalls such as:
- `from:<handle> OpenClaw`
- `from:<handle> deployment OR workflow OR MCP OR memory OR gateway`

Do this only when the author has already produced at least one high-signal item recently.

### B5. What to avoid
Do **not** dynamically expand on:
- vague hype words
- meme phrases
- generic AI terms
- engagement bait keywords
- policy / investment framing unless directly tied to OpenClaw adoption evidence

---

## C. Whitelist-author recall (targeted, conditional)

Use account-scoped recall for known high-signal sources, even when the post body does not explicitly repeat the brand name.

Suggested buckets:
- official / core dev
- practitioner / deployer
- tool integrator
- media / curator

Examples:
- `from:<handle> OpenClaw`
- `from:<handle> deployment OR workflow OR MCP OR memory OR gateway`
- `from:<handle> benchmark OR incident OR postmortem`

**Rule:** only spend whitelist recall budget on accounts that have already proven signal quality.
Do not turn this into a vanity roster sweep.

---

## D. Evidence-heavy recall (conditional)

Use this layer when core recall is not enough or when you need stronger operator evidence.

Prefer posts that include:
- repo/docs/release links
- screenshots, logs, dashboards
- concrete setup steps
- before/after comparisons
- architecture diagrams or config snippets

Useful tightening directions:
- add `deployment`
- add `incident`
- add `benchmark`
- add `config`
- add concrete feature nouns from recent releases

---

## E. Broad / noisy recall (fallback only)

These are useful for finding edge signals, but they are noisy and should **not** be part of the default first wave.

Examples:
- `OpenClaw`
- `clawdbot`
- `clawhub`
- `OpenClaw lang:zh`
- `OpenClaw lang:en`
- `OpenClaw 教程`
- `OpenClaw 部署`
- `OpenClaw 复盘`
- `OpenClaw workflow`
- `OpenClaw production`
- `OpenClaw case study`
- `OpenClaw 接入 OR 踩坑 OR 稳定性 OR 工作流 OR 自动化`
- `OpenClaw deployment OR incident OR postmortem OR integration`
- `OpenClaw benchmark OR latency OR eval`

### When to use this layer
Only use these when:
1. fixed core + dynamic expansion still produce insufficient high-confidence items
2. you need to search for niche CN/EN cases deliberately
3. you are filling **watchlist**, not forcing the main report body

### Exit / downgrade rule
If a broad query produces mostly low-value or zero-engagement noise for 3 consecutive runs, downgrade it to:
- disabled by default, or
- watchlist-only recall

---

## F. Query hygiene

1. Prefer direct post evidence over profile hearsay.
2. Avoid query overfitting to hype words.
3. Wide queries must go through stricter second-pass filtering.
4. If results are noisy, add exclusion terms and tighten by source/account.
5. Keep an explicit record of which query produced each candidate.
6. Distinguish 24h primary hits from 72h fallback hits.
7. Do not treat “many candidates returned” as success; the metric is shortlist quality.

---

## G. Blacklist / noise-control strategy

Apply these controls during filtering.

### Account blacklist
- chronic low-signal promo accounts
- copy-paste aggregators
- engagement-bait accounts with little technical substance
- repost mills that rename official release notes without added insight

### Content blacklist
- pure repost with no added view
- pure hype / pure praise / pure attack without evidence
- link-only posts with no explanatory content
- generic “game changer” style claims without mechanism or proof
- thin tutorial spam with no proof of real use or discussion

### Low-engagement caution set
Treat `0 likes / 0 reposts / 0 replies` as suspicious by default.
Such posts should normally be:
- excluded, or
- moved to `watchlist`

Allow low-engagement exceptions only when **all** of the following are true:
1. direct OpenClaw relation is strong
2. evidence quality is strong (repo/docs/logs/config/release)
3. mechanism insight is strong
4. the post is genuinely useful despite low spread

Even then, keep them out of Top 5 and out of CN/EN hot-post main slots.

---

## H. Coverage targets

Before final selection, sanity-check distribution across:
- source role: official / core dev / practitioner / tool integrator / media
- language: CN / EN
- window: 24h / 72h
- narrative: release / deployment / operations / security / workflow / ecosystem

If one cluster dominates:
- rebalance the shortlist, or
- explicitly note the bias in the report

---

## I. Desired output shape

The point of the query pack is **not** to maximize raw recall.
The point is to produce a shortlist that is:
- easier to score
- harder to pollute with zero-engagement noise
- rich enough for Top 5
- selective enough that the report can shrink instead of getting watered down

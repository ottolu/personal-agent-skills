# Scoring Rubric (OpenClaw X Intel)

Use this rubric before selecting any entry.

The goal is not to reward generic relevance. The goal is to surface items that are:
- decision-relevant
- evidence-backed
- practically useful
- discussed enough to matter

If a post is perfectly “on topic” but nobody engaged with it and the evidence is thin, it usually belongs in `watchlist`, not in the main report.

---

## 1) Hard Filters (must pass)

Reject if any condition is true:
- No direct relation to OpenClaw / clawdbot / clawhub ecosystem
- Pure repost with no new commentary
- Pure promo with no concrete content
- No traceable post URL
- Metrics and core metadata both unavailable
- Link-only or slogan-only content with no mechanism / evidence / practical claim

### Low-engagement hard filter
Treat `0 likes / 0 reposts / 0 replies` as **fail by default** for the main report.

A zero-engagement item may survive only as a **low-engagement exception** when all of the following are true:
1. direct relevance is strong
2. evidence is strong (release/docs/repo/log/config/screenshot)
3. mechanism insight is strong
4. practical value is strong despite low spread

Even then:
- **Top 5**: zero-engagement items should not appear
- **CN/EN hot posts**: zero-engagement items should not appear
- **KOL list**: at most 2 such items total, clearly treated as exceptional observations
- **Watchlist**: allowed, if explicitly justified

---

## 2) Weighted Score (0-100)

```text
Total = Relevance(25)
      + InsightDepth(20)
      + Actionability(20)
      + EvidenceQuality(15)
      + EngagementQuality(15)
      + InfluenceOrReach(5)
```

### Relevance (0-25)
- 22-25: direct OpenClaw release / deployment / architecture / security / reliability signal
- 15-21: direct usage case, toolchain integration, credible workflow / benchmark
- 8-14: adjacent but useful ecosystem / infra / market context
- <8: weak / indirect mention

### InsightDepth (0-20)
- 16-20: specific mechanism, trade-offs, evidence, clear claim
- 10-15: meaningful point but partially shallow
- 0-9: generic commentary

### Actionability (0-20)
- 16-20: can convert into immediate action / workflow / policy
- 10-15: useful direction, but needs interpretation
- 0-9: mostly narrative, low practical value

### EvidenceQuality (0-15)
- 12-15: direct evidence, data, screenshots, logs, config snippets, repo / docs / release links, or a highly verifiable chain
- 8-11: some supporting facts/examples but limited evidence chain
- 4-7: weak but non-zero evidence
- 0-3: mostly opinion or unverifiable claim

### EngagementQuality (0-15)
Use a mix of absolute engagement and discussion density.

Suggested formula:
- `abs_engagement = min(10, log1p(likes)*0.40 + log1p(reposts)*0.35 + log1p(replies)*0.25)`
- `discussion_bonus = 0-5` based on reply density / discussion quality / follower normalization when available
- `EngagementQuality = min(15, abs_engagement + discussion_bonus)`

Scoring guidance:
- 12-15: clearly discussed / propagated / debated
- 8-11: respectable engagement, likely relevant beyond the author
- 4-7: weak but non-zero discussion
- 0-3: nearly no visible discussion

If follower baseline is unavailable, score conservatively.

### InfluenceOrReach (0-5)
Use only as weak context, not the main driver.
- 0-1: very small reach
- 2-3: moderate reach
- 4: large reach
- 5: very large reach

**Important:** influence should act as a tie-breaker when content quality is close, not override quality.

---

## 3) Selection Thresholds

- **High-confidence inclusion**: score >= 72
- **Medium-confidence inclusion**: 64-71
- **Watchlist / low-signal observation**: 58-63
- **<58**: exclude

### Additional rule
A score is not enough by itself.
Any item that fails slot-level hard floors should still be excluded from the main body even if the total score is numerically acceptable.

---

## 4) Required Structured Fields

Each selected entry should carry:
- `score`
- `confidence`
- `narrative_tag`
- `query_source`
- `source_method`
- `signal_window`

Recommended `narrative_tag` values:
- release
- deployment
- operations
- security
- workflow
- ecosystem
- community-reaction
- benchmark
- tutorial
- controversy

---

## 5) Top 5 rules

For top priority signals, include all of the following:
1. what happened
2. why it matters (mechanism)
3. reply-zone support / disagreement / blocker
4. what to do next (today)
5. evidence chain (URL + metrics + reason)

Top 5 should satisfy:
- total score >= 78
- InsightDepth >= 15
- Actionability >= 15
- EvidenceQuality >= 8
- **not zero-engagement**

Preferred source types:
- official release / incident / security
- core-dev workflow / architecture thread
- strong practitioner evidence with real deployment / ops detail

Avoid using Top 5 slots on:
- thin tutorials
- weakly discussed opinion posts
- early signals that belong in watchlist

---

## 6) KOL list rules

### Quantity
- **10-12 entries**, not 15 by default

### Quality
- All entries must be >= 64
- At least 8 entries should be high-confidence (>= 72)
- At most 2 entries may be medium-confidence fillers
- At most 2 entries may be low-engagement exceptions

### Diversity
Prioritize diversity across:
- official
- core dev
- practitioner
- tool integrator
- media / curator

Avoid single-cluster domination by one role type.

### Low-engagement exceptions
A low-engagement KOL item is only acceptable when:
- it is highly evidence-backed
- it represents a real engineering / ecosystem signal
- it would be genuinely useful to track even without social spread

Mark these as observation-style items, not as proof of broad market traction.

---

## 7) Hot posts rules (CN / EN)

### Quantity
- Chinese: **3-5 entries**
- English: **3-5 entries**

### Quality
- At least 80% of entries in each language bucket should be >= 68
- At most 1 entry in each bucket may be 64-67 as fallback
- **Zero-engagement items should not appear in hot-post buckets**
- Avoid repeating the same narrative more than 2 times
- Explicitly mark any 72h fallback entries

### What hot posts are for
These buckets are for posts that are:
- genuinely circulating
- clearly discussed
- good proxies for what the relevant audience is seeing

If an item is useful but not actually “hot”, move it to KOL or watchlist.

---

## 8) Watchlist rules

Use watchlist for items that are:
- early-stage but credible
- low-spread but high-evidence
- security / ops / deployment observations that deserve monitoring
- not yet strong enough for main-body slots

### Quantity
- 0-3 entries total

### Score band
- usually 58-67
- may be higher if interaction is still too weak for main-body placement

### Watchlist is not a dumping ground
Do not use watchlist to save obviously weak content.
Only keep items that are worth re-checking tomorrow.

---

## 9) Low-signal fallback rules

If 24h high-confidence candidates are insufficient:
1. expand to 72h
2. keep thresholds unchanged where possible
3. prefer reducing quantity before reducing quality
4. do not let low-confidence placeholders exceed 2 in the main body
5. explicitly mark fallback and blockage reasons
6. if still weak, shrink KOL / CN / EN counts instead of filling with noise

---

## 10) Decision heuristics

When in doubt:
- prefer one fewer item over one weak item
- prefer a strong operator / deployment post over a weak generic tutorial
- prefer a highly discussed official release over five low-engagement echoes of that release
- prefer watchlist over forced inclusion

A good report should feel selective, not exhaustive.

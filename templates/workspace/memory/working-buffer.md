# Working Buffer (Danger Zone Log)

**Status:** IDLE
**Started:**
**Reset Rule:** Clear and restart when a new danger-zone window begins.

> Use this only in long / dense sessions or when context is at risk.
> Append the user's message and a short agent summary for each exchange after the danger zone threshold is crossed.

---

## Usage Rules
1. When context gets dense, switch `Status` to `ACTIVE` and set `Started`.
2. Append both:
   - `## [timestamp] Human`
   - `## [timestamp] Agent (summary)`
3. Keep summaries short: 1-3 bullets, only what would matter after compaction.
4. When the session is safe again or reset starts, archive mentally and clear this file for the next danger zone.

---

## Example Skeleton

## [YYYY-MM-DD HH:MM] Human
- Main ask:
- New constraint:

## [YYYY-MM-DD HH:MM] Agent (summary)
- Decision made:
- Open loop:
- Next move:

# Runbook (OpenClaw X Intel Report)

## Scheduling

Current job:
- Job name: `openclaw-x-daily-brief`
- Schedule: `0 10 * * *`
- Time zone: `Asia/Shanghai`
- Delivery: Feishu DM

## Reliability baseline

### 1. Timeout
- Every external dependency should have a timeout.
- `reply_sampler.py` should be called with explicit timeout and retries.
- End-to-end report generation should have a watchdog timeout.

### 2. Retry
- Retry transient failures (timeout / rate limit / temporary upstream failure) up to 2-3 times.
- Do not blindly retry parsing or schema errors.

### 3. Degrade gracefully
- If reply sampling fails for a single post, mark it and continue report generation.
- If 24h signals are insufficient, expand to 72h and mark fallback entries.
- If evidence is incomplete, reduce quantity before reducing quality.

### 4. Alerting
At minimum, alert on:
- job start
- job success
- job failure
- quality gate failure
- fallback-to-72h activation
- degraded reply sampling

### 5. Recovery artifacts
Keep these artifacts when possible:
- candidate JSON
- reply-sample JSON
- scored candidate sheet
- draft markdown
- quality gate output

These artifacts make partial reruns and debugging possible.

## Minimum operational SLA

- By report deadline, there must be either:
  1. a passed formal report, or
  2. a clear failure / degraded-mode notification

Silent failure is not acceptable.

## Human handoff rules

When a report fails because of evidence quality, parser issues, or upstream limits:
- do not silently publish
- send a failure summary
- include whether the failure is retryable or needs manual intervention

## Notes

This runbook documents the minimum operating posture. It should stay aligned with:
- `SKILL.md`
- `assets/report-template.md`
- `scripts/quality_gate.py`
- cron payload in `~/.openclaw/cron/jobs.json`

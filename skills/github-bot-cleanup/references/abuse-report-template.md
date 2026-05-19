# GitHub Abuse Report 模板

Block 完成后建议向 GitHub 提交举报，让平台层封禁 bot 农场账号，避免他们继续攻击别的项目。

## 提交入口

<https://support.github.com/contact/report-abuse>

选择类型：
- "Reporting abusive content or contacts" → "I want to report"
- → "rank abuse" / "fake stars" / "inauthentic activity"

## 邮件正文模板（英文）

```
Subject: Coordinated Star-Farming Attack on <ORG>/<REPO>

Hi GitHub Trust & Safety team,

We are the maintainers of <ORG>/<REPO>. Our repository received a 
coordinated star-farming bot attack on <DATE>. We have already used 
org-level blocking to remove the visible stars, but the underlying 
bot farm accounts remain active on the platform and continue to 
attack other projects.

We are reporting these accounts so they can be reviewed and banned 
at the platform level.

## Attack Pattern

- Date of attack: <DATE>
- Number of fake stars detected: <N>
- Time window: <e.g., 286 stars in 5 hours>
- Baseline before attack: <e.g., 2-4 stars/day>

## Hard Evidence

### 1. Bio token "prs_<hex>" — internal task ID of star-farm operator

The following accounts have biographies matching `prs_[0-9a-f]+`, 
which appears to be an internal task tracking ID used by the bot 
operator. No legitimate user would have such a biography.

| Account | Bio | Repos |
|---------|-----|-------|
| <example> | prs_xxxxxx | <N> forks of crypto/agent repos |

### 2. Coordinated fork activity

These accounts forked the exact same set of repositories on overlapping 
dates, indicating centralized scripting:

- copy-trading-bot-hub
- polymarket-arbitrage-bot
- casino-bonus-2026
- agentest, AiSOC, arc-relay, customermates

### 3. Public event history = 100% star (WatchEvent)

Sampled bot accounts show that all their public activity is starring 
repositories — no commits, no PRs, no issues. Example:

[Insert /users/<bot>/events/public output]

## Full List of Identified Bot Accounts

[Attach: block-list.txt with <N> usernames]

## What We Have Done

- Blocked all <N> accounts at the org level (GitHub UI: Settings → 
  Moderation → Blocked users)
- Star count on the affected repo: <X> → <Y> (drop of <Z>)
- Documented full filtering methodology in [internal doc]

We respect the platform's investigation process and are happy to 
provide any additional evidence on request.

Thank you,
<Your Name>
<Your Role>
<Org>
```

## 附件清单

提交时附上：
1. `block-list.txt` — 全部 bot 账号用户名
2. `block-YYYYMMDD-*.log` — 执行日志（含时间戳，可作为取证）
3. （可选）几个铁证账号的 profile 截图

## 后续

- GitHub 一般 7-14 天内响应
- 历史数据：研究表明 GitHub 会清除 ~62% 报告的 bot 账号
- 如果对方反复来刷，可以建一个长期 watchlist 在每次复发时 re-report

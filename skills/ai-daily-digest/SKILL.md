---
name: ai-daily-digest
description: "Fetch 90 top Hacker News blogs (curated by Karpathy), score/categorize/summarize articles using the agent's own model, then deliver a chat-first daily digest, save a full Markdown report locally, and sync it to Obsidian. No external API key needed. Use when user mentions 'daily digest', 'RSS digest', 'blog digest', 'tech news', 'tech blog summary', or runs /ai-daily-digest. Trigger command: /ai-daily-digest."
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "bins": ["bun"] },
        "install":
          [
            {
              "id": "bun",
              "kind": "npm",
              "pkg": "bun",
              "bins": ["bun"],
              "label": "Install Bun runtime (npm)",
            },
          ],
      },
  }
---

# Daily Digest Skill

Generate a curated daily digest from 90 top tech blogs (Karpathy's HN Popularity Contest 2025 list).

**Key difference from the original ai-daily-digest:** All AI analysis (scoring, categorization, summarization, trend highlights) is performed by YOU (the agent's main model) directly, no external Gemini/OpenAI API keys required.

**Default delivery order:**
1. **Chat-first digest**: send Lewei a concise but high-signal summary in chat, with **Top 10** must-read picks.
2. **Local artifact**: save a full Markdown report under the workspace `reports/ai-daily-digest/` directory.
3. **Obsidian sync**: copy the final Markdown into `40-Outputs/Daily Digests/` inside the default Obsidian vault.

Markdown rendering should use the template at `${SKILL_DIR}/references/digest-template.md`.

## Workflow

```
Step 0 → Check saved config (~/.daily-digest/config.json)
Step 1 → Collect parameters interactively
Step 2 → Run fetch script (pure RSS, no AI)
Step 3 → YOU score + categorize articles (batch of ~15)
Step 4 → YOU summarize Top N + generate trend highlights
Step 5 → Render chat digest + full markdown from template
Step 6 → Send chat summary first (Top 10)
Step 7 → Save local markdown and sync to Obsidian
Step 8 → Save config and confirm artifact locations
```

---

## Step 0: Check Saved Configuration

Read `~/.daily-digest/config.json`. If it exists, show the saved values and ask:

> 上次配置: 时间范围 {hours}h, Top {topN}, 语言 {lang}
> 是否沿用？(Y/n)

If user confirms, skip to Step 2. If not found or user wants to reconfigure, go to Step 1.

## Step 1: Collect Parameters

Ask the user for these parameters:

- `timeRange`: 24 / 48 / 72 / 168 hours, default `48`
- `topN`: 10 / 15 / 20, default `15`
- `lang`: `zh` / `en`, default `zh`

If the user gives a direct instruction in natural language, you may infer parameters without re-asking.

## Step 2: Run Fetch Script

Execute the RSS fetch script. `${SKILL_DIR}` resolves to this skill's directory.

```bash
npx -y bun ${SKILL_DIR}/scripts/fetch.ts --hours {timeRange} --output /tmp/daily-digest-articles.json
```

This outputs a JSON file with structure:

```json
{
  "fetchedAt": "...",
  "hours": 48,
  "totalFeeds": 90,
  "totalArticles": 1234,
  "filteredCount": 56,
  "articles": [
    {
      "title": "...",
      "link": "...",
      "pubDate": "2026-04-01T12:00:00.000Z",
      "description": "...",
      "sourceName": "simonwillison.net",
      "sourceUrl": "https://simonwillison.net"
    }
  ]
}
```

After execution, report briefly: `已抓取 {filteredCount} 篇文章（来自 {successFeeds}/{totalFeeds} 个源），开始 AI 分析...`

If `filteredCount` is 0, tell the user to try a larger `--hours` value and stop.

## Step 3: Score and Categorize (YOU do this)

Process all fetched articles. Work in batches of about 15 articles. For each article, assign:

### Scoring (1-10 each)
- **Relevance**: relevance to a tech-savvy audience
- **Quality**: depth, originality, and signal
- **Timeliness**: urgency or importance right now

### Category (one of)
| ID | Emoji | Label |
|---|---|---|
| `ai-ml` | 🤖 | AI / ML |
| `security` | 🔒 | 安全 |
| `engineering` | ⚙️ | 工程 |
| `tools` | 🛠 | 工具 / 开源 |
| `opinion` | 💡 | 观点 / 杂谈 |
| `other` | 📝 | 其他 |

### Keywords
Assign 3-5 concise keywords per article.

After scoring, sort by total score descending and take Top N.

## Step 4: Summarize Top N + Trend Highlights (YOU do this)

For each Top N article, generate:
- `titleZh`: Chinese translation when `lang=zh`
- `summary`: 3-5 sentence summary in the chosen language
- `reason`: one sentence on why it is worth reading

Then produce:
- **oneLineTakeaway**: one sentence capturing the single most important conclusion from today's digest
- **trendHighlights**: 2-3 macro trends synthesized into a cohesive paragraph

If a source description is sparse, say the summary is based on limited available metadata.

## Step 5: Render Chat Digest + Full Markdown

Use `${SKILL_DIR}/references/digest-template.md` as the default template.

### Chat digest requirements
The chat version is the **primary deliverable**. It must be concise enough to read in chat, but substantial enough to be useful without opening the Markdown file.

It should include:
- title and date
- one-line takeaway
- 2-3 trend bullets or a short trend paragraph
- **Top 10 must-read picks**
  - rank
  - Chinese title if applicable
  - source
  - 1-2 sentence summary
  - why worth reading
- a brief closing note indicating the full report has been saved locally and synced to Obsidian

### Full markdown requirements
The Markdown file is the **secondary artifact**. It should include:
- one-line takeaway
- trend highlights
- Top N full picks
- statistics table
- category pie chart
- keyword bar chart
- ASCII keyword bars
- tag cloud
- category-organized expanded sections
- local and Obsidian paths
- generation timestamp and config

## Step 6: Send Chat Summary First

Send the chat digest before writing about file paths in detail.

Preferred chat structure:

```markdown
# 📰 AI 博客每日精选 — {YYYY-MM-DD}

一句话判断：{oneLineTakeaway}

今日趋势：
- ...
- ...
- ...

今日 Top 10：
1. {titleZh}｜{sourceName}
   - 摘要：...
   - 为什么值得读：...
...
10. ...

已为你同步生成完整 Markdown，并准备写入本地与 Obsidian。
```

If the platform is sensitive to long messages, keep each item compact rather than dropping coverage below Top 10.

## Step 7: Save Local Markdown and Sync to Obsidian

### Local path
Save the full report to:

```text
reports/ai-daily-digest/digest-{YYYYMMDD}.md
```

Create the directory if needed.

### Obsidian path
Sync the same final Markdown content to:

```text
/Users/luotto/Documents/Obsidian Vault/40-Outputs/Daily Digests/AI Daily Digest - {YYYY-MM-DD}.md
```

If the target directory does not exist, create it.

Reasoning: this is a recurring aggregated output, so it belongs in `40-Outputs/` rather than single-article reading notes under `20-Knowledge/`.

## Step 8: Save Config and Confirm Artifact Locations

Save configuration to `~/.daily-digest/config.json`:

```json
{
  "timeRange": {hours},
  "topN": {topN},
  "language": "{lang}",
  "lastUsed": "{ISO timestamp}"
}
```

Then briefly confirm:
- local path
- Obsidian path
- number of sources scanned
- total articles fetched
- filtered article count
- final Top N

## Error Handling

- If fetch fails, check whether `bun` exists, and suggest `npm i -g bun` if missing.
- If filtered article count is 0, suggest increasing `--hours`.
- If some feeds fail with 429 / timeout / socket errors, treat that as partial network variance unless failure rate is high.
- If Obsidian write fails, still send the chat digest and save the local file, then clearly report the Obsidian sync failure.

## Notes

- The fetch script outputs progress to stderr, article JSON to the output file.
- All AI analysis is done by YOU. No external model calls, no external API keys.
- Be honest in scoring. Avoid uniform score inflation.
- Chat delivery comes first. Local and Obsidian persistence are part of completion, not optional extras.
- For this skill, chat-only completion is not enough, and file-only completion is also not enough. The task is complete only when **chat summary has been sent**, **local Markdown has been written**, and **Obsidian sync has succeeded** or been explicitly reported as failed.

---
name: ai-daily-digest
description: "Fetch 90 top Hacker News blogs (curated by Karpathy), score/categorize/summarize articles using the agent's own model, and generate a daily Markdown digest with bilingual titles, Mermaid charts, tag cloud, and trend highlights. No external API key needed. Use when user mentions 'daily digest', 'RSS digest', 'blog digest', 'tech news', 'tech blog summary', or runs /ai-daily-digest. Trigger command: /ai-daily-digest."
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

**Key difference from the original ai-daily-digest:** All AI analysis (scoring, categorization, summarization, trend highlights) is performed by YOU (the agent's main model) directly — no external Gemini/OpenAI API keys required.

## Workflow

```
Step 0 → Check saved config (~/.daily-digest/config.json)
Step 1 → Collect parameters interactively
Step 2 → Run fetch script (pure RSS, no AI)
Step 3 → YOU score + categorize articles (batch of ~15)
Step 4 → YOU summarize Top N + generate trend highlights
Step 5 → Assemble and write Markdown report
Step 6 → Display Top 3 preview to user
```

---

## Step 0: Check Saved Configuration

Read `~/.daily-digest/config.json`. If it exists, show the saved values and ask:

> 上次配置: 时间范围 {hours}h, Top {topN}, 语言 {lang}
> 是否沿用？(Y/n)

If user confirms, skip to Step 2. If not found or user wants to reconfigure, go to Step 1.

## Step 1: Collect Parameters

Ask the user for these parameters using `question()`:

```
question({
  text: "选择时间范围",
  key: "timeRange",
  options: [
    { label: "24 小时", value: "24" },
    { label: "48 小时（推荐）", value: "48" },
    { label: "72 小时", value: "72" },
    { label: "7 天", value: "168" }
  ],
  defaultValue: "48"
})
```

```
question({
  text: "精选文章数量",
  key: "topN",
  options: [
    { label: "10 篇", value: "10" },
    { label: "15 篇（推荐）", value: "15" },
    { label: "20 篇", value: "20" }
  ],
  defaultValue: "15"
})
```

```
question({
  text: "输出语言",
  key: "lang",
  options: [
    { label: "中文（推荐）", value: "zh" },
    { label: "English", value: "en" }
  ],
  defaultValue: "zh"
})
```

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

After execution, read the JSON file and report: "已抓取 {filteredCount} 篇文章（来自 {totalFeeds} 个源），开始 AI 分析..."

If `filteredCount` is 0, tell the user to try a larger `--hours` value and stop.

## Step 3: Score and Categorize (YOU do this)

Process ALL fetched articles. Work in batches of ~15 articles. For each batch, analyze the articles and assign:

**Scoring (each 1-10):**
- **Relevance**: How relevant to a tech-savvy audience (developers, engineers, researchers)
- **Quality**: Writing quality, depth of insight, originality
- **Timeliness**: How timely/important right now

**Category** (one of):
| ID | Emoji | Label |
|---|---|---|
| `ai-ml` | 🤖 | AI / ML |
| `security` | 🔒 | 安全 |
| `engineering` | ⚙️ | 工程 |
| `tools` | 🛠 | 工具 / 开源 |
| `opinion` | 💡 | 观点 / 杂谈 |
| `other` | 📝 | 其他 |

**Keywords**: 3-5 keywords per article.

After scoring all articles, sort by total score (relevance + quality + timeliness) descending, take Top N.

## Step 4: Summarize Top N + Trend Highlights (YOU do this)

For each Top N article, generate:
- **titleZh**: Chinese translation of the title (if lang=zh; skip if lang=en)
- **summary**: 4-6 sentence summary (in the chosen language)
- **reason**: One sentence explaining why it's worth reading

Then, looking at all Top N articles together, write **2-3 macro trend highlights** — what patterns or themes emerge from today's top articles. Write this as a cohesive paragraph (3-5 sentences).

## Step 5: Assemble Markdown Report

Build the report and write it to `./output/digest-{YYYYMMDD}.md` (create the `output/` directory if needed). Use this exact structure:

```markdown
# 📰 AI 博客每日精选 — {YYYY-MM-DD}

> 来自 Karpathy 推荐的 90 个顶级技术博客，AI 精选 Top {N}

## 📝 今日看点

{trend highlights paragraph}

---

## 🏆 今日必读

🥇 **{titleZh or title}**

[{original title}]({link}) — {sourceName} · {relative time} · {category emoji} {category label}

> {summary}

💡 **为什么值得读**: {reason}

🏷️ {keywords joined by ", "}

🥈 **{...}**
...

🥉 **{...}**
...

---

## 📊 数据概览

| 扫描源 | 抓取文章 | 时间范围 | 精选 |
|:---:|:---:|:---:|:---:|
| {successFeeds}/{totalFeeds} | {totalArticles} 篇 → {filteredCount} 篇 | {hours}h | **{topN} 篇** |

### 分类分布

```mermaid
pie showData
    title "文章分类分布"
    "{emoji} {label}" : {count}
    ...
```

### 高频关键词

```mermaid
xychart-beta horizontal
    title "高频关键词"
    x-axis [{keywords as quoted strings}]
    y-axis "出现次数" 0 --> {max+2}
    bar [{counts}]
```

<details>
<summary>📈 纯文本关键词图（终端友好）</summary>

```
{keyword padded} │ {█ bar} {count}
...
```

</details>

### 🏷️ 话题标签

{top 20 keywords: top 3 bolded — word(count) · word(count) · ...}

---

## {category emoji} {category label}

### {index}. {titleZh or title}

[{original title}]({link}) — **{sourceName}** · {relative time} · ⭐ {totalScore}/30

> {summary}

🏷️ {keywords}

---

{repeat for all categories, sorted by article count descending}

*生成于 {YYYY-MM-DD} {HH:mm} | 扫描 {successFeeds} 源 → 获取 {totalArticles} 篇 → 精选 {topN} 篇*
*基于 [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/) RSS 源列表，由 [Andrej Karpathy](https://x.com/karpathy) 推荐*
```

### Relative Time Format

- < 60 min: "{n} 分钟前"
- < 24 hours: "{n} 小时前"
- < 7 days: "{n} 天前"
- Otherwise: YYYY-MM-DD

### Chart Details

- **Pie chart**: All categories that have articles, sorted by count descending.
- **Bar chart**: Top 12 keywords by frequency across all Top N articles.
- **ASCII bar chart**: Top 10 keywords, max bar width 20 chars (█ for filled, ░ for empty).
- **Tag cloud**: Top 20 keywords, top 3 are **bold**, format: `word(count)` joined by ` · `.

## Step 6: Save Config and Display Results

1. Save configuration to `~/.daily-digest/config.json`:
```json
{
  "timeRange": {hours},
  "topN": {topN},
  "language": "{lang}",
  "lastUsed": "{ISO timestamp}"
}
```

2. Display results to user:
```
✅ 日报生成完成！

📄 文件: ./output/digest-{YYYYMMDD}.md
📊 统计: 扫描 {totalFeeds} 源 → {totalArticles} 篇 → 精选 {topN} 篇
⏱️ 时间范围: {hours} 小时

🏆 Top 3 预览:
1. {titleZh} — {sourceName} (⭐ {score}/30)
2. {titleZh} — {sourceName} (⭐ {score}/30)
3. {titleZh} — {sourceName} (⭐ {score}/30)
```

## Error Handling

- If fetch script fails: check if `bun` is installed, suggest `npm i -g bun`.
- If 0 articles after filtering: suggest increasing `--hours`.
- If network errors on most feeds: warn user about network connectivity.

## Notes

- The fetch script outputs progress to stderr, article JSON to the output file.
- All AI analysis is done by YOU — no external model calls, no API keys needed.
- The scoring should be based on the article title + description snippet. Be honest in scoring — don't inflate scores uniformly.
- When generating summaries, base them on the description available. If the description is sparse, note that the summary is based on limited information.

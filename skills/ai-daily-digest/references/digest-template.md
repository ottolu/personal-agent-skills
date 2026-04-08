# 📰 AI 博客每日精选 — {date}

> 来自 Karpathy 推荐的 90+ 个顶级技术博客，AI 精选 Top {topN}

## 📝 今日总览

**一句话判断**

{oneLineTakeaway}

**今日趋势**

{trendHighlights}

---

## 💬 发给 Lewei 的聊天版摘要（Top 10）

> 这部分是默认优先在聊天里发送的内容。

### 你今天最值得先看的 10 篇

{chatTop10}

---

## 📊 数据概览

| 扫描源 | 成功源 | 抓取文章 | 时间范围 | 精选 |
|:---:|:---:|:---:|:---:|:---:|
| {totalFeeds} | {successFeeds} | {totalArticles} 篇 → {filteredCount} 篇 | {hours}h | **Top {topN}** |

### 分类分布

```mermaid
pie showData
    title "文章分类分布"
{categoryPieLines}
```

### 高频关键词

```mermaid
xychart-beta horizontal
    title "高频关键词"
    x-axis [{keywordLabels}]
    y-axis "出现次数" 0 --> {keywordMax}
    bar [{keywordCounts}]
```

<details>
<summary>📈 纯文本关键词图（终端友好）</summary>

```
{keywordAsciiBars}
```

</details>

### 🏷️ 话题标签

{tagCloud}

---

## 🏆 完整精选

{fullTopSection}

---

## 📚 分类展开

{categorySections}

---

## 🔗 产物与归档

- 本地文件：`{localPath}`
- Obsidian：`{obsidianPath}`
- 生成时间：{generatedAt}
- 配置：{hours}h / Top {topN} / {lang}

*基于 [Hacker News Popularity Contest 2025](https://refactoringenglish.com/tools/hn-popularity/) RSS 源列表，由 [Andrej Karpathy](https://x.com/karpathy) 推荐*

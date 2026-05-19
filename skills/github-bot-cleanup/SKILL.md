---
name: github-bot-cleanup
description: "清理 GitHub 仓库的 star-farming bot 账号——拉取 stargazers、识别 bot、批量 block。仅在用户显式调用时使用：`/github-bot-cleanup <org/repo>` 或明确提及 'github bot 清理'、'清除虚假 star'、'star 农场'、'block bot 账号'。日常对话不要主动加载。"
---

# GitHub Bot Star Cleanup

## 用途

针对被 star-farming bot 攻击的 GitHub 仓库，自动化识别 + 批量 block 虚假账号。

**这是一个显式调用 skill**——日常对话不要主动加载。仅在用户明确说要清理 bot star 时调用。

## 前置条件检查

调用此 skill 时**第一步必须确认**：

1. **目标 org/repo** —— 用户必须给出，格式 `OpenSenseNova/SenseNova-U1`
2. **gh auth scope** —— 必须含 `admin:org`
   ```bash
   gh auth status | grep "Token scopes"
   # 若缺：gh auth refresh -h github.com -s admin:org
   ```
3. **org 角色** —— 用户必须是 org admin/owner
   ```bash
   gh api "/orgs/<ORG>/memberships/$(gh api /user --jq .login)" --jq '.role'
   # 期望: "admin"
   ```

任何一条不满足，**停下来告诉用户怎么补**，不要继续。

## 工作流（5 步）

### Step 1: 拉取 stargazers（含 starred_at）

```bash
mkdir -p /tmp/botclean
gh api -H "Accept: application/vnd.github.star+json" \
  "/repos/<ORG>/<REPO>/stargazers?per_page=100" \
  --paginate > /tmp/botclean/stargazers.json
```

输出基线：按日期分布看哪天是攻击波峰
```bash
jq -r '.[] | .starred_at[0:10]' /tmp/botclean/stargazers.json | sort | uniq -c
```

### Step 2: 筛候选池

两种策略，根据规模选：

**A. 全量扫描（精确但慢）**：每个 stargazer 都拉 profile

**B. 命名预筛 + 全量扫描混合**：先用命名后缀筛出明显候选，再补充新增日全量
- 命名正则参考（GitHub-themed 后缀）：
  ```
  -(bot|netizen|hue|ship-it|cmyk|oss|byte|gif|alt|wq|cloud|sketch|coder|ux|
    crypto|max|lgtm|ai|a11y|blip|glitch|star|sudo|commits|cmd|cyber|patch|
    fork|merge|push|pull|repo|tag|release|edge|node|web|app|cli|api|dev|
    prod|stage|main|head|base|init|setup|config|secret|token|key|hash|
    blob|tree|core|ware|ml|deploy|env|droid|boop|hub|tech|dot|ctrl|beep|
    spec|create|creator|code|collab|afk|art|lab|ops|source|design|prog|
    del|svg|jpg|png|maker|stack|ui|sys|bit|rgb|lang|cell|arch|maker)$
  ```

> **教训**：命名预筛会漏掉"普通名字 bot"（如 `kafei2026`、`liyuan0258`），如果只看命名会有盲区。推荐**对攻击日全量扫描**。

### Step 3: 批量拉 profile（GraphQL）

用 `scripts/fetch-profiles.sh` 实现，每批 10 个用户。

关键字段：
```graphql
user(login: "...") {
  login
  createdAt
  bio
  allRepos: repositories { totalCount }
  issuesOpened: issues { totalCount }
  prsOpened: pullRequests { totalCount }
  gists { totalCount }
  followers { totalCount }
  following { totalCount }
  contributionsCollection {
    totalCommitContributions
    totalIssueContributions
    totalPullRequestContributions
  }
}
```

**坑警告**（必看 [references/PITFALLS.md](references/PITFALLS.md)）：
- `hasAnyContributions` 字段**不可靠**（0 commit 的账号也常为 true）
- GraphQL 批量超过 10 个/批容易丢数据，最后一批可能不返回
- `followers/following` 数**不能**作为"真实用户"证据（bot 互相 follow 刷活跃度）

### Step 4: 应用保守过滤规则

**Block 条件（满足任一即 block）**：

1. **零产出**（满足以下全部）：
   - `allRepos == 0`（连 fork 都没有）
   - `issuesOpened == 0`
   - `prsOpened == 0`
   - `gists == 0`
   - `totalCommitContributions == 0`
   - `totalIssueContributions == 0`
   - `totalPullRequestContributions == 0`

2. **bio PR 农场铁证**：
   - bio 匹配正则 `prs_[0-9a-f]+`（PR 农场任务 ID）
   - 即使有 fork 活动也是 bot

**Keep 条件**（不 block）：
- 不满足上述任一 = 保留
- 即使只有 1 个 fork 也保留（宽松，避免误伤）

jq 实现：
```bash
jq -c '
. + {
  should_block: (
    (.allRepos.totalCount == 0 and
     .issuesOpened.totalCount == 0 and
     .prsOpened.totalCount == 0 and
     .gists.totalCount == 0 and
     .contributionsCollection.totalCommitContributions == 0 and
     .contributionsCollection.totalIssueContributions == 0 and
     .contributionsCollection.totalPullRequestContributions == 0)
    or
    (.bio // "" | test("prs_[0-9a-f]+"; "i"))
  )
}
' profiles.jsonl | jq -r 'select(.should_block) | .login' > block-list.txt
```

### Step 5: 批量 block

用 `scripts/batch-block.sh`（详见脚本注释）：

```bash
# 必须先 dry-run
bash <skill_dir>/scripts/batch-block.sh <ORG> block-list.txt

# 确认后真执行
bash <skill_dir>/scripts/batch-block.sh <ORG> block-list.txt --apply
```

脚本特性：
- 幂等（已 block 的会跳过）
- 限流 0.3s/请求
- 实时日志：`block-YYYYMMDD-HHMMSS.log`
- 失败可见，跑完一目了然

## 验证 block 效果

```bash
# Stargazers 实际数（带缓存延迟，几分钟同步）
gh api "/repos/<ORG>/<REPO>" --jq '.stargazers_count'

# 实际 stargazers API 计数
gh api "/repos/<ORG>/<REPO>/stargazers?per_page=100" --paginate | jq -s 'flatten | length'

# Org 已 block 总数
gh api "/orgs/<ORG>/blocks?per_page=100" --paginate --jq '.[].login' | wc -l
```

## 持续监控（可选）

如果攻击持续，可以做增量扫描：

```bash
# 拉最新 stargazers，与上次 snapshot 对比
# 新增账号自动跑过滤 + block
# 详见 scripts/incremental-cleanup.sh
```

## 必读的注意事项

- **任何 block 都是 org-level 公开行为**，谨慎执行，先 dry-run
- **不要把 follower/following 数当真实证据**，bot 也会互相 follow
- **不要因为命名"正常"就放过**，agent 农场用真实人名做伪装
- **不要因为有 fork 就保留**，bot 会 fork 加密货币诈骗 repo 装活跃
- 保留**审计日志**（block-*.log），对外说明时是关键证据
- 如果用户对单个账号判定有疑虑，**单独拉该用户的 events**（star 历史、PR 历史）做证据展示

## 生成 abuse report

block 完后建议向 GitHub 提交 abuse report：
- 入口：<https://support.github.com/contact/report-abuse>
- 类型选 "Disrupting the experience" / "fake stars / rank abuse"
- 附上 block list、prs_ bio 证据、同批 fork repo 列表
- 详见 [references/abuse-report-template.md](references/abuse-report-template.md)

## 相关文件

- `scripts/fetch-profiles.sh` —— GraphQL 批量拉 profile
- `scripts/filter-bots.sh` —— 应用过滤规则
- `scripts/batch-block.sh` —— 批量 block（核心脚本）
- `scripts/incremental-cleanup.sh` —— 增量监控
- `references/PITFALLS.md` —— 踩过的坑
- `references/abuse-report-template.md` —— 提交 GitHub 举报模板

# 踩过的坑（必读）

实战中遇到的判定坑，避免重复犯错。

## GitHub API 字段陷阱

### `contributionsCollection.hasAnyContributions` 不可靠
0 commit / 0 issue / 0 PR 的账号也常返回 `true`。**不要**把它作为"有活动"证据。
只看具体的：
- `totalCommitContributions`
- `totalIssueContributions`
- `totalPullRequestContributions`

### `followers` / `following` 不能作为真实证据
- bot 农场账号会互相 follow 刷活跃度
- 见过 0 repo / 0 commit / 但 13 followers 的明显 bot
- 真实用户里也有大量 0 follower 的小号

### GraphQL 批量大小
- 每批超过 10 个 user 容易丢数据（最后几个不返回）
- 解决：批次 = 10，并在主流程后补查丢失的（fetch-profiles.sh 已实现）

### `stargazers_count` 字段有缓存延迟
block 完后几分钟内，repo 主页 `stargazers_count` 仍可能是旧值。
看实际数要用 `/repos/X/stargazers --paginate | jq length`。

## 命名规则的盲区

只用"`-bot/-hue/-cmyk` 后缀"会漏掉**伪装升级版 bot**：
- 普通中文人名风格：`kafei2026`、`liyuan0258`、`muqqq627`
- 普通英文名风格：`ChrisYoungYoung`、`Brookluli`
- 这些只能通过"零产出"或"prs_ bio"识别

**推荐**：攻击日做全量扫描，不要只信命名筛选。

## "看起来活跃"的 bot 伪装

农场会做这几种伪装，单看任一字段会被骗：
1. **批量 fork 同一组 repo** → "我有 13 个 repo"（但全是 fork）
2. **互相 follow** → "我有 8 个 follower"（互相刷）
3. **占位原创 repo** → 名字是 `-`、`Aimen`、`Fri` 这种空 repo
4. **真实人名 + 默认头像** → 显示 "Abdullah Al Imran" 让账号像人

## 老账号陷阱

注册时间 > 1 年 的账号也可能是 bot：
- **休眠账号被劫持**：2020/2021 注册但 0 活动，被农场买来用
- **`prs_` bio 出现在 2021/2024 注册的账号**上（我们见过 `Alif8900` 2021 注册 + `prs_f7bb87` bio）

**结论**：注册时间老 ≠ 真实用户。还是看实际产出。

## fork 内容的判定信号

如果一定要看 fork 内容来判断，注意这些**典型 bot fork 主题**：
- 加密货币交易 bot：`copy-trading-bot-hub`, `polymarket-arbitrage-bot`, `solana-copytrading-bot`
- 赌博：`casino-bonus-2026`
- DDoS 工具：`free-ip-stresser`
- 同批 AI/agent 项目（农场调度同步 star）：`agentest`, `AiSOC`, `arc-relay`, `customermates`, `hermes-agent-mission-control`

## 误判过的真实用户类型

不要因为这些特征就 block：
- 中文 GitHub 处理 `firstname-lastname` 命名（如 `liu-hua-joe`、`xiefan-guo`、`AFeng-x`）
- 注册时间在攻击波附近的小白账号
- 0 follower 但有几个原创 repo 的初学者（如学生账号）
- 真实命名后缀（`-ai`、`-dev`）但有明显原创内容

## 二次核验该看什么

如果一个账号边界难判，看这两条最可靠：
1. **公开事件历史**（`/users/X/events/public`）—— bot 的事件几乎全是 `WatchEvent`（star 行为）
2. **fork 的 repo 内容**（`/users/X/repos`）—— 看名字是否集中在 spam 主题

实战发现的 bot 公开事件模式：
```
2026-05-18T03:11:10Z WatchEvent -> OpenSenseNova/SenseNova-U1
2026-05-16T02:36:01Z WatchEvent -> windowsMarketLab/polymarket-arbitrage-bot-v2
2026-05-15T14:58:19Z WatchEvent -> NeuralInverse/neuralinverse
... 10 个事件 100% 都是 WatchEvent
```
**100% WatchEvent = 100% bot**（账号只做 star，不做任何其他事）。

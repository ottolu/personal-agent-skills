---
name: value-invest-analysis
description: 价值投资深度分析框架。当用户请求对个股进行基本面分析、护城河评估、DCF/相对估值、财务质量诊断、商业模式拆解、管理层评估、安全边际测算、买入卖出决策、行业对比、价值陷阱识别、深度研报时使用。覆盖 A股（.SH/.SZ/.BJ）、港股（.HK）、美股（NYSE/NASDAQ）。触发词：价值投资、个股分析、基本面、护城河、moat、DCF、自由现金流、ROIC、安全边际、内在价值、巴菲特、芒格、能力圈、价值陷阱、深度研报、买入逻辑、卖出逻辑、估值。Value investing deep-dive framework — triggers on fundamental analysis, moat assessment, DCF/relative valuation, financial quality diagnosis, business model decomposition, management evaluation, margin of safety, buy/sell decision, peer comparison, value-trap detection. Covers A-shares, HK, US equities. Keywords: value investing, stock analysis, fundamentals, moat, DCF, FCF, ROIC, intrinsic value, margin of safety, Buffett, Munger, circle of competence, value trap.
---

# 价值投资分析 Skill（v2.0）

多流派融合的价值投资分析框架。融合巴菲特/芒格（质量优先）、格雷厄姆（深度价值）、段永平/张磊（商业模式与长期主义）三大流派，覆盖 A股/港股/美股三个市场。

> **v2.0 核心变化**：先识别公司原型（18 类 company_type）→ 加载对应 sector 与 schema_extension → 用二维决策矩阵裁决，废除单一 weighted_total 门槛。详见 §九。
> **真理源**：`V2_SPEC.md`，任何与之冲突的行为视为 bug。

## 一、何时触发

- 用户给出股票代码或公司名要求分析（"分析 600519.SH"、"看看茅台"）
- 用户问"贵不贵 / 值不值得买 / 现在能买吗"
- 用户问护城河、商业模式、财务质量、管理层、估值、安全边际
- 用户要求深度研报、同业对比、价值陷阱排查

## 二、输入解析与路由

### 2.1 股票代码标准化

强制要求市场后缀，未带后缀时主动追问或调用 `scripts/parse-ticker.py`：

- A股：`600519.SH` / `000858.SZ` / `300750.SZ` / `688981.SH` / `8xxxxx.BJ`
- 港股：`0700.HK`（保留 4 位前导零）
- 美股：`AAPL` 或 `AAPL.US`

用户给公司中文名时（如"腾讯"）必须追问港股 0700.HK 还是美股 ADR `TCEHY`，并提示 A+H、ADR 折溢价存在。

### 2.2 输入深度判定

| 输入类型 | 示例 | 执行 |
|---|---|---|
| 最小输入 | "分析 600519.SH" | 标准版深度分析：先识别 company_type → 6 维全评分 + 主市场模块 + sector 文件 + schema_extension |
| 中等输入 | "分析茅台的护城河" | 聚焦版：仍先识别 company_type → 仅加载护城河 + 方法论模块 + sector 文件 |
| 完整输入 | "从财务/护城河/估值分析 0700.HK，给买入建议" | 按指定维度加载，输出含决策评分 + sector 全量 |

追问规则：**最多追问 1 轮**，否则用保守默认值并显式标注。

### 2.3 references 按需加载路由（v2 新增 company_type 列）

#### 2.3.1 通用 references（按用户意图信号）

| 用户意图信号 | 必加载 references |
|---|---|
| 完整分析 / 深度研报 / 全面评估 | 全部 references + 全部 templates + 对应 sector + schema_extension |
| 仅护城河 / 商业模式 | `moat-business-model.md` + `methodology.md` + 对应 sector |
| 仅估值 / 贵不贵 / DCF | `valuation.md` + `financial-analysis.md` + 对应 sector |
| 仅财务 / 财报质量 / 会不会暴雷 | `financial-analysis.md` + `red-flags-checklist.md` + 对应 sector |
| 仅风险 / 价值陷阱 | `risk-behavioral.md` + `red-flags-checklist.md` |
| 代码 .SH/.SZ/.BJ | `market-cn.md` |
| 代码 .HK | `market-hk.md` |
| 美股代码 | `market-us.md` |
| 任何需要找数据的场景 | `data-sources.md` |

#### 2.3.2 公司原型路由表（v2 核心，与 V2_SPEC §十 同步）

| company_type | 必加载 sector 文件 | 必加载 schema_extension |
|---|---|---|
| `great_company_compounder` | `references/sectors/sector-great-company.md` | 无（用 base） |
| `tech_platform_network` | `references/sectors/sector-tech-platform.md` | 无（用 base） |
| `consumer_brand_premium` | `references/sectors/sector-consumer-brand.md` | 无（用 base） |
| `tech_hardware_ecosystem` | `references/sectors/sector-tech-hardware.md` | 无（用 base） |
| `high_growth_platform` | `references/sectors/sector-high-growth-platform.md` | 无（用 base） |
| `biotech_unprofitable` | `references/sectors/sector-biotech.md` | `templates/schema_extensions/biotech_unprofitable.json` |
| `pharma_mature` | `references/sectors/sector-pharma-mature.md` | 无（用 base） |
| `banking` | `references/sectors/sector-banking.md` | `templates/schema_extensions/banking.json` |
| `insurance` | `references/sectors/sector-insurance.md` | `templates/schema_extensions/insurance.json` |
| `brokerage_assetmgmt` | `references/sectors/sector-brokerage-assetmgmt.md` | 无（用 base） |
| `utility_infrastructure_reit` | `references/sectors/sector-utility.md` | `templates/schema_extensions/utility_infrastructure_reit.json` |
| `cyclical_commodity` | `references/sectors/sector-cyclical-commodity.md` | `templates/schema_extensions/cyclical_commodity.json` |
| `cyclical_industrial_ev` | `references/sectors/sector-cyclical-industrial-ev.md` | 无（用 base） |
| `real_estate` | `references/sectors/sector-real-estate.md` | `templates/schema_extensions/real_estate.json` |
| `holding_conglomerate` | `references/sectors/sector-holding-conglomerate.md` | `templates/schema_extensions/holding_conglomerate.json` |
| `distressed_turnaround` | `references/sectors/sector-distressed-turnaround.md` | 无（用 base） |
| `declining_cash_cow` | `references/sectors/sector-declining-cash-cow.md` | 无（用 base） |
| `cigarbutt_deep_value` | `references/sectors/sector-cigarbutt.md` | 无（用 base） |

**规则**：只加载相关 references 与 sector，避免一次性读全部消耗上下文。

### 2.4 company_type 识别流程（v2 新增，Step 0）

在执行 §三 七步法之前，**必须先完成 Step 0：公司原型识别**：

1. **初步分类**：依据收入构成、毛利率结构、行业属性、商业模式给出候选 `company_type`（V2_SPEC §二 锁定的 18 类枚举）。
2. **修饰符叠加**：从 V2_SPEC §三 的 `modifier_flags` 列表中选取适用项（`distressed` / `vie_structure` / `state_owned` / `regulated_heavily` / `pcaob_risk` 等），可叠加多个。
3. **加载对应文件**：按 §2.3.2 路由表加载 sector 文件与 schema_extension。
4. **写入 scorecard**：`company_classification.company_type` + `modifier_flags` + `rationale`（1-2 句判定理由）。
5. **冲突处理**：若公司跨多类（如比亚迪同时是制造与品牌），按主营收入占比 > 50% 的板块判定，并在 `rationale` 中说明跨界特征。

**禁止**：在未识别 company_type 之前执行任何评分或估值。

## 三、价值投资七步法（核心工作流）

```
[0] 公司原型识别 → [1] 理解生意 → [2] 管理层 → [3] 护城河 → [4] 财务质量 → [5] 估值 → [6] 风险 → [7] 决策
```

### 3.1 Step 0：公司原型识别（v2 新增）

见 §2.4。产出 `company_classification` 对象，决定后续所有步骤的指标体系、估值方法、红旗清单、同业池。

### 3.2 Step 1-7

| 步骤 | 核心问题 | 主导流派 | 详见 |
|---|---|---|---|
| 1. 理解生意 | 公司怎么赚钱？能力圈内吗？ | 段永平 + 芒格 | moat-business-model + 对应 sector |
| 2. 管理层 | 是否诚实、理性、资本配置能力强？ | 巴菲特 | moat-business-model |
| 3. 护城河 | 5–10 年后还在吗？ | 巴菲特 / 晨星 | moat-business-model + 对应 sector |
| 4. 财务质量 | 报表可信？现金流真实？（按 sector 替换失效指标） | 格雷厄姆 + 巴菲特 | financial-analysis + 对应 sector |
| 5. 估值 | 内在价值 vs 当前价格？（按 sector 选估值法） | 格雷厄姆 + DCF | valuation + 对应 sector |
| 6. 风险 | 最坏怎样？反过来想 | 芒格 | risk-behavioral |
| 7. 决策 | 二维决策矩阵 + 仓位 + 跟踪 | 张磊 + 段永平 | 本文件 §四 |

### 3.3 流派自适应路由（保留，作为 sector 补充）

| 公司类型 | 主流派 | 触发条件 |
|---|---|---|
| 消费品牌 | 巴菲特 | 毛利率>40%、品牌定价权、ROE 长期>15% |
| 科技平台 | 段永平 | 网络效应、双边市场、Take Rate 模式 |
| 周期/重资产/烟蒂股 | 格雷厄姆 | PB<1、行业底部、破净 |
| 困境反转 | 格雷厄姆 + 霍华德·马克斯 | 财务困境、催化剂可见 |
| 长期复利 | 张磊 | 长坡厚雪、结构红利 |
| 高研发科技 | 段永平 + 芒格 | 研发>10%、技术代际 |

路由优先级：商业模式 > 财务结构 > 行业 > 地域。

**终止条件**：任一步发现"能力圈外"或"重大红旗"或"一票否决触发"，立即停止并输出 PASS 建议。

## 四、决策评分卡（v2 二维决策矩阵）

**v2 关键变化**：废除 v1 的"weighted_total ≥ 8.0 → 重仓"单一门槛。weighted_total 仅作为参考字段保留，**决策完全由 quality_score × valuation_score 二维矩阵裁决**。

### 4.1 6 维评分（用 dimension_anchors 锚定打分）

scorecard.json 内置完整 6 维锚点参考表（V2_SPEC §四），每个维度评分必须显式声明 `anchor_used` 字段。维度与权重：

| 维度 | 权重 |
|---|---|
| business_quality | 20% |
| management | 15% |
| moat | 20% |
| financial_quality | 15% |
| valuation_margin_of_safety | 20% |
| risk | 10% |

### 4.2 两个核心分（v2）

```
quality_score   = (business_quality + management + moat + financial_quality + risk) / 5
valuation_score = valuation_margin_of_safety
weighted_total  = 0.20*biz + 0.15*mgmt + 0.20*moat + 0.15*fin + 0.20*val + 0.10*risk  (仅参考)
```

### 4.3 二维决策矩阵（V2_SPEC §五）

| quality_score | valuation_score | 评级 | 含义 |
|---|---|---|---|
| ≥ 8.0 | ≥ 7.0 | `heavy_buy_candidate` | 重仓候选 |
| ≥ 8.0 | 5.0-7.0 | `wishlist_quality_company` | 心仪公司池（好公司，等价格） |
| ≥ 8.0 | < 5.0 | `wishlist_overvalued` | 心仪公司池（明显高估） |
| 6.5-8.0 | ≥ 7.0 | `watchlist_buildable` | 观察清单可分批建仓 |
| 6.5-8.0 | < 7.0 | `watchlist_quality_only` | 观察清单（仅质量过关） |
| < 6.5 | 任意 | `pass` | PASS |

### 4.4 一票否决（独立于矩阵）

- 任一 6 维 ≤ 3 → 强制 PASS（在 `veto_check.vetoed_dimensions` 中列出）
- 能力圈 too-hard → 强制 PASS（`circle_of_competence_too_hard = true`）
- 价值陷阱 6 信号 ≥ 5 项触发 → 强制 PASS
- 数据时效 `data_freshness_ok = false` + 用户未明确同意 → 强制降级 `unverified_quick_look`

### 4.5 required_pct_margin_of_safety 公式（V2_SPEC §六）

```
required_pct = base_by_type[company_type] + adjustment
```

base_by_type 表见 V2_SPEC §六（great_company_compounder=25 / banking=25 / biotech_unprofitable=50 ...），adjustment 含质量分调整（≥8.0 → -5 / <6.0 → +10）与 modifier_flags 调整（distressed +10 / vie +5 / pcaob +5 / regulated_heavily +3）。

scorecard.json 的 `margin_of_safety.required_pct_breakdown` 必须显式记录 base / adjustment / modifier_adjustment 三段。

## 五、输出产物结构

生成位置：`outputs/{ticker}/{YYYY-MM-DD}/`

```
outputs/600519.SH/2026-05-15/
├── 01-full-report.md        # 完整研报（templates/full-report.md）
├── 02-scorecard.json        # 6 维评分卡 v2（templates/scorecard.json）
├── 03-data.json             # 结构化数据 v2 + sector_extension + data_lineage
├── 04-peer-comparison.md    # 同业对比（按 sector 匹配 ≥ 3 家）
├── 05-premortem.md          # 预先尸检（强制生成）
└── sources.md               # 全部引用 + 抓取时间戳
```

- `01-full-report.md` 内嵌指向 02/03/04/05 的相对链接
- `02-scorecard.json` 在 evidence 字段引用 01 的章节锚点
- `02` / `03` 均通过 `sector_extension.$ref` 指向对应行业的 schema_extension

聚焦版（只问单一维度）可只生成对应章节，但 **05-premortem.md 永远强制生成**。

## 六、与 web-access skill 协作（数据获取）

本 skill **不内置数据抓取**，所有实时财报/股价/公告通过 `web-access` skill 获取：

1. 路由阶段判定"需要联网数据"→ 调用 `Skill(web-access)`
2. 传结构化 query：
   ```
   {intent: "fetch_financials",
    ticker: "600519.SH",
    source_priority: ["巨潮资讯", "东方财富"],
    data: ["近5年三表", "最新季报", "近12月公告标题"]}
   ```
3. `references/data-sources.md` 提供分市场 URL 模板与字段映射
4. 抓取结果落盘到 `outputs/{ticker}/{date}/raw/`，sources.md 自动追加链接+时间戳，**同时写入 `03-data.json` 的 `data_lineage` 数组**（含 source / url / fetched_at / freshness_days）
5. **失败降级**：取不到时**显式标注"数据缺失"**而非估算

禁止：本 skill 不直接调用 WebFetch/WebSearch，统一走 web-access。

## 七、出报告前质量门控（v2 硬/软门控分级）

完成报告前必须逐项确认。**硬门控未通过 → 强制 `unverified_quick_look` 模式 + 在 §0 报告顶部显示 ⚠️ 警示**。软门控未通过可继续但显式标注。

### 7.1 硬门控（5 项，未通过强制降级）

| # | 检查项 | 含义 |
|---|---|---|
| H1 | `data_freshness_ok` | 财报 ≤ 90 天 + 股价 ≤ 7 天 |
| H2 | `sources_cited` | 所有定量数据有 source + fetched_at |
| H3 | `circle_of_competence_declared` | 显式声明本分析的能力圈与未能理解部分 |
| H4 | `no_deterministic_buy_sell` | 不给确定性 Buy/Sell，给概率化判断 + 框架 |
| H5 | `red_flag_checklist_done` | 红旗清单逐项过审（含 N/A 且有依据） |

**硬门控未通过的行为**：
- `quality_gate.mode` 自动设为 `unverified_quick_look`
- `quality_gate.output_downgraded = true`
- `quality_gate.downgrade_reasons` 填入未通过门控编号
- 报告顶部 §0 显示：`⚠️ 本报告未通过硬门控 [H1, H3]，已降级为 unverified_quick_look 模式，结论仅供参考。`

### 7.2 软门控（6 项，未通过显式标注但允许继续）

| # | 检查项 | 含义 |
|---|---|---|
| S1 | reverse_evidence_done | 反向证据三件套（≥ 3 条看空，看空字数 ≥ 看多 30%） |
| S2 | premortem_done | 预先尸检完成（5 年后亏 50% 的 3-5 个原因） |
| S3 | all_dimensions_scored | 6 维全部填写且有证据 |
| S4 | dcf_sensitivity_done | DCF 三大假设 ±20% 敏感性分析 |
| S5 | peer_comparison_done | 同业对比 ≥ 3 家（或显式 `incomparability_flag`） |
| S6 | ah_dual_listing_handled | AH / 双重上市 / ADR 折溢价处理（如适用） |

软门控未通过的行为：在报告对应章节显式标注 "⚠ 软门控 S2 未通过：未做预先尸检"，并在 `quality_gate.soft_gates_passed` 中标 false。

### 7.3 其他终止条件

- 任一 6 维 ≤ 3 → PASS
- too-hard 桶 → PASS
- 文件齐全性 → 必须 5 文件齐全（focus 模式除外）

## 八、参考资料导航

### 8.1 通用 references

| 文件 | 内容 |
|---|---|
| `references/methodology.md` | 价投核心理念：能力圈、安全边际、Mr. Market、Owner Earnings；各流派精髓 |
| `references/financial-analysis.md` | 三表勾稽、11 项核心指标 + 锚点、A/H/US 披露差异 |
| `references/moat-business-model.md` | 商业模式六维、护城河七型、管理层评估、6 种生意类型 |
| `references/valuation.md` | 10 种估值方法、交叉验证流程、假设审查、安全边际、价值/增长陷阱 |
| `references/risk-behavioral.md` | 风险分层、10 大黑天鹅、Pre-mortem、反向证据、能力圈、5 大偏差 |
| `references/market-cn.md` | A 股特有：监管、审计、股权质押、政策因子、ST 制度 |
| `references/market-hk.md` | 港股特有：仙股/老千股、AH 溢价、VIE、南向资金 |
| `references/market-us.md` | 美股特有：SEC 文件、Non-GAAP、SBC、做空报告、8-K |
| `references/data-sources.md` | 三市场公开数据源映射、字段提取规范 |
| `references/red-flags-checklist.md` | 32 项财务造假与治理红旗清单（强制过审） |

### 8.2 sector references（v2 新增，按 company_type 加载）

| 文件 | 对应 company_type |
|---|---|
| `references/sectors/sector-great-company.md` | great_company_compounder |
| `references/sectors/sector-tech-platform.md` | tech_platform_network |
| `references/sectors/sector-consumer-brand.md` | consumer_brand_premium |
| `references/sectors/sector-tech-hardware.md` | tech_hardware_ecosystem |
| `references/sectors/sector-high-growth-platform.md` | high_growth_platform |
| `references/sectors/sector-biotech.md` | biotech_unprofitable |
| `references/sectors/sector-pharma-mature.md` | pharma_mature |
| `references/sectors/sector-banking.md` | banking |
| `references/sectors/sector-insurance.md` | insurance |
| `references/sectors/sector-brokerage-assetmgmt.md` | brokerage_assetmgmt |
| `references/sectors/sector-utility.md` | utility_infrastructure_reit |
| `references/sectors/sector-cyclical-commodity.md` | cyclical_commodity |
| `references/sectors/sector-cyclical-industrial-ev.md` | cyclical_industrial_ev |
| `references/sectors/sector-real-estate.md` | real_estate |
| `references/sectors/sector-holding-conglomerate.md` | holding_conglomerate |
| `references/sectors/sector-distressed-turnaround.md` | distressed_turnaround |
| `references/sectors/sector-declining-cash-cow.md` | declining_cash_cow |
| `references/sectors/sector-cigarbutt.md` | cigarbutt_deep_value |

### 8.3 templates

| 模板 | 用途 |
|---|---|
| `templates/full-report.md` | 完整研报 15 节模板 |
| `templates/scorecard.json` | 6 维评分卡 v2 schema（内置 dimension_anchors + 决策矩阵 + 硬软门控） |
| `templates/structured-data.json` | 财务/估值结构化数据 v2 schema（含 sector_extension + data_lineage） |
| `templates/peer-comparison.md` | 同业对比表 |
| `templates/premortem.md` | 预先尸检模板 |
| `templates/schema_extensions/*.json` | 各 company_type 的字段扩展（首批 7 个） |

### 8.4 scripts

| 脚本 | 用途 |
|---|---|
| `scripts/parse-ticker.py` | 股票代码归一化、市场识别 |
| `scripts/valuation-calc.py` | DCF / EPV 计算辅助 |

## 九、V2 与 V1 的对比说明

本次 V1 → V2 升级的关键变化：

1. **公司原型识别先于分析框架**：新增 Step 0 + 18 类 `company_type` 锁定枚举 + `modifier_flags` 叠加机制。先判定原型，再调用对应 sector 的指标体系、估值方法、红旗清单与同业池。解决了 v1 把银行/biotech/REIT 用通用模板硬套导致 ROIC/FCF 等指标失效的问题。

2. **评分锚点 + 二维决策矩阵双轨**：scorecard.json 内置完整 6 维锚点参考表（每维 5 个分数点 + 代表案例），每个评分必须显式声明 `anchor_used`。决策不再依赖单一 weighted_total ≥ 8.0，改用 `quality_score × valuation_score` 二维矩阵裁决，分出 6 个评级，破除"高质量+高估值"被算成中等分的死锁。

3. **schema 严格约束 + 扩展机制公开**：禁止 agent 私自发明顶层字段。所有 sector-specific 字段（NIM / 不良率 / cash_runway / NAV / SBC 等）必须通过 `sector_extension.$ref` 加载对应 schema_extension，结构化字段不再"看心情"。

4. **质量门控硬化**：v1 的 10 项 checklist 现拆分为 5 项硬门控 + 6 项软门控。硬门控未通过 → 强制 `unverified_quick_look` 模式 + 报告顶部 ⚠️ 警示，机器可自动判定。`required_pct_margin_of_safety` 由公式自动计算（base_by_type + adjustment），透明可追溯。`data_lineage` 数组强制每个定量数据点带 source + url + fetched_at + freshness_days。

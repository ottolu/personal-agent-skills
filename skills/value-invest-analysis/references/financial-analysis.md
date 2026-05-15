# 财务质量分析参考（v2）

> **v2 与 v1 的本质差异**：v1 用一套 11 项通用指标"包打天下"，但对银行、保险、未盈利 biotech、地产、控股集团、周期股、公用事业/REIT 严重失真。v2 引入**行业差异化机制**——通用 11 项作为"工商企业默认体系"，7 类特殊行业改读各自的专属指标集（与 `templates/schema_extensions/{type}.json` 字段一一对应）。
>
> **本文件与其他参考的边界**：
> - 红旗（32 项）→ `red-flags-checklist.md`（v2 已按 company_type 自动 N/A）
> - 估值方法（DCF/EPV/SOTP/rNPV/DDM/PB-ROE）→ `valuation.md`
> - 数据源（披露 URL、API）→ `data-sources.md`
> - 各行业完整画像（商业模式 / 竞争格局 / 监管 / 经典案例）→ `references/sectors/sector-{type}.md`
> - 本文件只回答一个问题：**"对这家公司，财务质量应该怎么看、看哪些指标、警戒线怎么定？"**

---

## 一、价投视角与方法论（核心要义）

### 1.1 财报的两个用途

价值投资者读财报，**目标永远不是"算出公允价值"**。财报有两个、且仅有两个用途：

1. **排雷工具**：发现造假、关联输送、资本结构地雷、商业模式破绽 → 触发即 PASS
2. **商业模式验证**：印证"这门生意如管理层所讲那样赚钱"——定价权体现在毛利率、议价权体现在应收/应付、复利能力体现在 ROIC/ROE

财报**不能**告诉你的：未来 10 年生意会变成什么样、护城河会变宽还是变窄、行业格局会怎么演变。这些来自定性分析（参考 `moat-business-model.md`）。

### 1.2 阅读顺序（v2 强制化，作为软门控 S3）

**Skill 输出前，必须按以下顺序读完，缺一项标注 `soft_gate_failed: report_reading_order`**：

1. **现金流量表** → 真实性最高，先看经营现金流是否健康
2. **审计意见** → 任何非标意见（保留 / 否定 / 无法表示）直接 PASS
3. **附注：关联交易、商誉构成、表外负债** → 雷区集中地
4. **资产负债表** → 看负债结构、应收存货、商誉
5. **利润表** → 最后看，最容易粉饰
6. **致股东信 / MD&A** → 管理层语气、行业洞察、风险自我披露

不要从利润表开始读财报——那是新手做法。

### 1.3 优先级口诀

> **现金 > 审计 > 附注 > 资产负债 > 利润表 > 致股东信**
>
> **真钱 > 真账 > 真注 > 真家底 > 真利润 > 真话**

---

## 二、通用 11 项指标体系（工商企业默认 + 行业适用性标注）

适用范围：**除七类特殊行业外**的工商企业（消费、科技平台、硬件、医药成熟、高速增长平台、新能源车/工业周期成长、衰退现金牛、深度低估、困境反转、券商资管的工商部分）。

| # | 维度 | 指标 | 优秀锚点 | 警戒锚点 | 价投视角 | 行业 N/A 或替代 |
|---|---|---|---|---|---|---|
| 1 | 盈利能力 | ROE（5 年均） | > 15% | < 8% | 长期高 ROE 通常意味着护城河 | banking/insurance 保留但锚点不同；holding_conglomerate 失真（含浮存金）；biotech_unprofitable N/A；real_estate 改读 ROE on NAV |
| 2 | 盈利能力 | ROIC | > 12% 且 > WACC | < WACC | 比 ROE 更纯粹，剔除杠杆 | banking/insurance/real_estate N/A（杠杆天然高，ROIC 失去意义）；utility 改读 regulated_return；holding_conglomerate 失真 |
| 3 | 盈利能力 | 毛利率稳定性 | 标准差 < 3pct | 剧烈波动 | 稳定 = 定价权强 | banking 改读 NIM 净息差稳定性；insurance 改读 combined_ratio 稳定性；cyclical_commodity 改读"成本曲线分位"（毛利率天然随商品价波动） |
| 4 | 质量 | FCF / 净利润（5 年均） | > 0.8 | < 0.5 | 利润含金量 | banking/insurance N/A（FCF 概念在金融业不适用）；real_estate 改读 sales_amount/净利润（销售回款 vs 结算利润）；utility/REIT 改读 FFO/AFFO；biotech_unprofitable 改读 cash_runway_months |
| 5 | 质量 | 应收账款周转天数 | 稳定或下降 | 连年上升 | 渠道议价权 | banking N/A（贷款不是应收）；insurance 改读"应收保费/已赚保费"；real_estate 应收主要是合作方款，关注其他应收款异常 |
| 6 | 质量 | 经营现金流 / 营收 | > 15% | < 5% | 商业模式现金流属性 | banking 改读"存款日均增速 vs 贷款日均增速"；insurance N/A；biotech_unprofitable N/A（必为负） |
| 7 | 成长性 | 营收 CAGR（5 年） | 10–25% | < 0 或 > 40% | < 0 衰退、> 40% 可疑 | banking 改读"贷款增速 vs 名义 GDP"（贷款增速 > GDP 增速 1.5x 是过快扩张红旗）；insurance 改读 NBV 增速；cyclical_commodity 用正常化指标 |
| 8 | 成长性 | 再投资回报率 ΔNI/ΔIC | > 15% | < 10% | 增长是否创造价值 | banking N/A（资本扩表非"投资"）；real_estate 改读"新增土储 IRR" |
| 9 | 安全性 | 有息负债 / 净资产 | < 50% | > 100% | 杠杆水平 | banking/insurance N/A（天然高杠杆 10-15x）；real_estate 改读"净负债率 + 三道红线"；utility 改读 debt_to_ebitda |
| 10 | 安全性 | 利息保障倍数 | > 5x | < 2x | 偿债缓冲 | banking N/A（利息是主营成本）；insurance N/A；real_estate 改读"现金短债比" |
| 11 | 安全性 | 流动比率 | 1.5–2.5 | < 1 | 短期流动性 | banking N/A（资产负债结构概念不同）；insurance N/A；real_estate 关注度低 |

**通用 11 项的总评判**：5 年至少 8 项达标 = 财务质量分 7+；6-7 项达标 = 5-6 分；少于 6 项 = 3 分以下需触发"价值陷阱 6 信号"复核。

---

## 三、三表勾稽检查清单（通用，行业差异化部分见 §六）

### 3.1 利润表（看"赚的是不是真钱"）

| 检查项 | 警戒信号 |
|---|---|
| 营收结构 | 主业占比 < 80%；"其他业务收入/投资收益"贡献利润 > 20% |
| 毛利率 | 连续 3 年趋势异常波动（环比 > ±5pct）；与同业偏离 > 10pct |
| 销售/管理/研发费用率 | 突然下降——可能是费用资本化粉饰 |
| 营业利润 vs 净利润 | 差距大 → 非经常损益干扰严重 |
| 所得税率 | 长期低于法定税率 > 5pct，需查税收优惠真实性 |

### 3.2 资产负债表（看"家底干不干净"）

| 检查项 | 警戒信号 |
|---|---|
| 应收账款 vs 营收 | 应收增速持续高于营收 → 放宽信用换收入 |
| 存货周转天数 | 异常拉长 → 滞销或虚增 |
| 在建工程 | 长期不转固定资产 → 可能藏费用 |
| 商誉 | 商誉 / 净资产 > 30% → 减值地雷 |
| 货币资金 + 高息负债 | 存贷双高 → 康美式造假典型特征（**但对 cyclical_commodity 反向解读，见 §六.6**） |
| 其他应收款 / 预付账款 | 异常增长 → 资金占用、关联输送 |

### 3.3 现金流量表（最难造假，最关键）

| 检查项 | 健康标准 | 警戒信号 |
|---|---|---|
| 经营现金流净额 / 净利润（5 年均） | > 0.8 | < 0.5 |
| 销售商品收到现金 / 营业收入（含税） | ≥ 1.13（A 股，含 13% 增值税） / ≥ 1.0（美股） | < 1.0 / < 0.95 |
| 投资现金流方向 | 持续流出 + ROIC 上升 | 持续流出 + ROIC 不升 → 价值毁灭式扩张 |
| 筹资现金流（长期累计） | 净流出或平衡 | 长期净流入 → 不能自我造血 |

### 3.4 三表勾稽红旗

> **利润高增 + 经营现金流为负 + 应收/存货齐涨 = 高危组合**（财务造假特征三件套）
>
> 该组合一旦触发，强制 financial_quality ≤ 3，并写入 `red_flags.critical_flags`。

---

## 四、长期视角检查（10 年）

价值投资的核心是看**长期**。必查 10 年数据：

- **10 年 ROE 中位数**：> 15% 是优秀公司分水岭
- **10 年 ROE 最低值**：< 10% 说明熬过周期能力不足
- **10 年净利润复合增速 vs 净资产复合增速**：前者高于后者 → 资本效率改善
- **10 年累计经营现金流 vs 累计净利润**：> 1 是真现金流公司
- **10 年股东回报**（分红 + 回购）/ 累计净利润：> 50% 是股东友好型

**周期股例外**：cyclical_commodity 改用"10 年正常化 EPS / 10 年均 PB 分位 / 商品价 10 年分位"做穿越周期判断（详见 §六.6）。

---

## 五、A/H/US 财务披露差异

### 5.1 A 股（中国会计准则 CAS）

- 强制：季报 + 半年报 + 年报，年报 4 月底前
- 研发费用化/资本化弹性大，需手工还原（建议统一按 100% 费用化重算）
- 关注：交易所问询函、年报问询函（重大信号）
- 所得税率：高新企业 15%，部分行业可降至 10%
- **A 股银行特有**：拨备覆盖率监管红线 150%（系统重要性银行 130%），不良率 / 拨备 / 核充率每季披露
- **A 股地产特有**：三道红线监管（剔除预收负债率、净负债率、现金短债比），按颜色档管控融资增速
- **A 股周期股**：分红率窗口指导（部分央企 50%+），关注国资委市值管理

### 5.2 港股（HKFRS ≈ IFRS）

- 中报 + 年报为主，季报非强制；中报通常不审计
- 核数师变更 / "保留意见"是重大红旗
- 同股不同权（WVR）：管理层超额控制权，治理折价
- VIE 架构：法律层面非真实股权，估值应折价 15-25%
- **港股 biotech 特有（18A 章）**：上市时可未盈利，但每半年须披露 cash_runway + pipeline 进展；首发后 2 年内不得发行新股稀释超过 30%
- **港股 REIT 特有**：派息率 ≥ 90% 强制（如领展），FFO/AFFO 是核心
- **港股 H 股 vs A 股折价**：恒生 AH 溢价指数长期反映 A 股溢价 30-50%，H 股估值通常更"便宜"

### 5.3 美股（US GAAP）

- 10-Q 季报 + 10-K 年报，披露最详尽
- **Non-GAAP 调整泛滥**：必须还原 SBC（股权激励费用）作为真实成本
  - 对苹果：SBC 占净利润 8-10%
  - 对腾讯（ADR/H）：SBC 占净利润 15-25%
  - 对百济（18A/Nasdaq）：SBC 占营收 30%+，是真实成本，**不能加回**
- 商誉减值测试更严格（按 CGU）
- 8-K 临时公告（高管辞职、审计师变更、Restatement 重述）是即时信号
- Form 4：内部人交易披露
- **PCAOB 审计风险**：中概股可能被强制退市（HFCAA），加 `pcaob_risk` modifier_flag

### 5.4 跨市场归一化

建议把财报数据全部"归一化"到 IFRS 口径后再做对比，否则毛利率/ROIC 都没意义（如美股 SBC 不还原会高估 30-50% 的盈利能力）。

### 5.5 行业 × 市场交叉关注点

| 行业 | A 股关注 | 港股关注 | 美股关注 |
|---|---|---|---|
| 银行 | 拨备监管底线 150% | NIM 利率市场化敏感 | CET1 巴塞尔 III 终板规则 |
| Biotech | 科创板第五套上市标准 | 18A 章未盈利豁免 + 强制披露管线进度 | FDA PDUFA 日期 / Citizen Petition |
| 控股集团 | 极少（少数民营如复星） | 长和系 / 太古 | BRK 等，加披露 segment + look-through earnings |
| 周期股 | 国企央企股息率 + 市值管理诉求 | 中海油等高股息 | 储量披露 SEC 准则 |
| 地产 | 三道红线 + 商票逾期 | 美元债违约连锁 | REIT 派息率 ≥ 90% |

### 5.6 A/H 同股不同价的财务对比方法

- 财务数据**完全一致**（同一家公司）
- 估值差异 = 流动性差异 + 投资者结构差异 + 汇率差异 + 港股通税率差异
- **方法**：以 IFRS 报表（H 股）为基础做对比，A 股报表通常是 IFRS 报表的"中国本地化"版本
- **价投选择**：财务质量等同 → 选 H 股（折价 20-40%），但需评估流动性差异（small-cap H 股可能成交极低）

---

## 六、行业差异化指标体系（v2 核心新增）

> 以下 7 个 company_type 拥有 `schema_extensions/{type}.json`，必须替换或补充通用 11 项。每个子节给出"通用 11 项的替代/N/A 清单 + 行业专属指标 + 锚点"，与对应 schema_extension JSON 的 `financial_fields_extension.fields` 字段名**完全对应**。
>
> 完整行业画像见 `references/sectors/sector-{type}.md`，本节只给财务质量评估口径。

### 6.1 banking — 商业银行

参考：`sectors/sector-banking.md`、`schema_extensions/banking.json`

**通用 11 项替换表**：

| 通用指标 | 银行处理 | 说明 |
|---|---|---|
| ROE | 保留（锚点改） | 优秀 > 15%，警戒 < 10% |
| ROIC | N/A | 银行天然高杠杆，ROIC 失去意义 |
| 毛利率稳定性 | 改读 NIM 稳定性 | 净息差是银行毛利率 |
| FCF/NI | N/A | FCF 概念在银行不适用 |
| 应收周转 | N/A | 改读"贷款增速 vs 名义 GDP"（> 1.5x 警戒） |
| 经营现金流/营收 | N/A | 改读存贷增速差 |
| 营收 CAGR | 替换为"净利息收入 + 中收"CAGR | 5-10% 健康 |
| ΔNI/ΔIC | N/A | 资本扩表非投资 |
| 有息负债/净资产 | N/A | 银行天然 10-15x 杠杆 |
| 利息保障倍数 | N/A | 利息是主营成本 |
| 流动比率 | N/A | LCR/NSFR 替代 |

**银行专属 15 项**（与 `banking.json` 一一对应）：

| 字段名（schema） | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `nim_pct` | 净息差 NIM | > 2.0% | < 1.5% |
| `npl_ratio_pct` | 不良贷款率 | < 1.2% | > 2.0% |
| `provision_coverage_pct` | 拨备覆盖率 | > 250% | < 150% |
| `car_total_pct` | 资本充足率（总） | > 13% | < 11% |
| `car_tier1_pct` | 核心一级资本充足率 | > 11% | < 9% |
| `rwa` | 风险加权资产 | 稳定或缓增 | RWA 增速 > 总资产增速 |
| `retail_loan_share_pct` | 零售贷款占比 | > 50% | < 30% |
| `non_interest_income_share_pct` | 非息收入占比（中收） | > 30% | < 15% |
| `aum_cny_bn` | 客户管理资产 AUM | 持续增长 | 停滞或下滑 |
| `cost_to_income_ratio_pct` | 成本收入比 CIR | < 35% | > 45% |
| `demand_deposit_share_pct` | 活期存款占比 | > 45% | < 25% |
| `roa_pct` | ROA（替代 ROIC） | > 1.0% | < 0.7% |
| `roe_pct` | ROE | > 15% | < 10% |
| `loan_deposit_ratio_pct` | 贷存比 | 65-80% | > 85% 或 < 50% |
| `loan_to_deposit_growth_diff_pp` | 贷款增速 - 存款增速 | < 5pp | > 10pp（流动性恶化） |

**银行额外评分子项**（来自 banking.json 的 scorecard_extension）：
- `asset_quality`（隶属 financial_quality 权重 0.4）
- `capital_adequacy`（隶属 risk 权重 0.3）
- `deposit_franchise`（隶属 moat 权重 0.4）
- `non_interest_income_quality`（隶属 business_quality 权重 0.3）

---

### 6.2 insurance — 保险

参考：`sectors/sector-insurance.md`、`schema_extensions/insurance.json`

**通用 11 项替换表**：

| 通用指标 | 保险处理 |
|---|---|
| ROE | 保留（锚点：寿险 > 12%，财险 > 15%） |
| ROIC | N/A |
| FCF/NI | N/A（保费收入和理赔节奏不可比） |
| 应收周转 | 改读"应收保费 / 已赚保费"（> 15% 警戒） |
| 营收 CAGR | 改读"保费 CAGR + NBV CAGR" |
| 有息负债/净资产 | N/A（寿险准备金不是负债性质的有息负债） |
| 利息保障 / 流动比率 | N/A |

**保险专属 16 项**（与 `insurance.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `combined_ratio_pct` | 综合成本率（财险） | < 97% | > 100% |
| `embedded_value_cny_bn` | 内含价值 EV（寿险） | 增长 > 10% | < 5% 或下滑 |
| `nbv_cny_bn` | 新业务价值 NBV | 增速 > 10% | 负增长 |
| `nbv_margin_pct` | 新业务价值率 | > 30% | < 15% |
| `investment_yield_pct` | 总投资收益率 | > 5% | < 3.5% |
| `net_investment_yield_pct` | 净投资收益率（剔除买卖价差） | > 4.5% | < 3.5% |
| `reserves_cny_bn` | 准备金余额 | — | — |
| `solvency_ratio_pct` | 综合偿付能力充足率 | > 180% | < 130% |
| `core_solvency_ratio_pct` | 核心偿付能力充足率 | > 120% | < 70% |
| `premium_growth_yoy_pct` | 保费同比增速 | — | — |
| `expense_ratio_pct` | 费用率 | — | — |
| `loss_ratio_pct` | 赔付率 | — | — |
| `duration_assets_liabilities_match` | 资负久期匹配 | 缺口 < 2Y | 缺口 > 5Y |
| `policyholder_persistency_13m_pct` | 13 月继续率 | > 90% | < 80% |
| `float_cny_bn` | 浮存金 | — | — |
| `float_cost_pct` | 浮存金成本率 | < 0（承保盈利） | > 投资收益率 |

**估值口径**：寿险用 EV+NBV 多倍数估值（PEV）；财险用 PB-ROE；混合用 SOTP（参考 `valuation.md`）。

---

### 6.3 biotech_unprofitable — 未盈利创新药

参考：`sectors/sector-biotech-unprofitable.md`、`schema_extensions/biotech_unprofitable.json`

**通用 11 项替换表**：

| 通用指标 | Biotech 处理 |
|---|---|
| ROE / ROIC / 毛利率稳定性 / 营收 CAGR / ΔNI/ΔIC | **全部 N/A**（无营收或营收极低、亏损） |
| FCF/NI | N/A（NI 为负，FCF 必为负） |
| 经营现金流/营收 | N/A |
| 有息负债/净资产 | 保留但锚点放松（融资轮次多，关注 < 30% 即可） |
| 利息保障倍数 | N/A |
| 流动比率 | **关键保留**（关注是否 > 2，反映 cash runway） |

**Biotech 专属 14 项**（与 `biotech_unprofitable.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `cash_runway_months` | 现金跑道 | > 24 个月 | < 12 个月 |
| `rd_expense_cny_bn` | 研发费用 | — | — |
| `rd_expense_to_revenue_ratio` | 研发费用/营收 | < 1.0（接近商业化） | > 5（高烧钱） |
| `rd_efficiency` | 元营收/元研发（3 年滚动） | 上升 | 持续下降 |
| `sbc_cny_bn` | 股权激励 SBC（美股关键） | — | — |
| `sbc_to_revenue_ratio` | SBC/营收 | < 0.15 | > 0.50 |
| `pipeline_phases` | 管线列表 | 多个 Phase 2/3 | 仅临床前 |
| `approved_drugs_count` | 已上市药品数 | ≥ 1 | 0 |
| `key_partnerships_value_usd_mn` | 对外授权交易潜在价值 | > 1B | < 100M |
| `cumulative_loss_cny_bn` | 累计未弥补亏损 | — | — |
| `price_to_sales_ttm` | P/S TTM | — | > 30x 警惕 |
| `peak_sales_potential_by_drug` | 单药峰值销售预测 | 单药 > 1B USD | < 200M USD |
| `share_dilution_yoy_pct` | 股本同比稀释率 | < 5% | > 15% |
| `fda_milestones_next_12m` | 未来 12 月 FDA 里程碑 | ≥ 1 个 Ph3 readout | 无近期催化 |

**核心判定**：cash_runway < 12 个月 + 无近期里程碑 + 稀释率 > 15% = 三杀，financial_quality 直降 ≤ 3。

**估值口径**：rNPV（风险调整 NPV）+ EV/peak_sales，不用 DCF（参考 `valuation.md`）。

---

### 6.4 real_estate — 地产

参考：`sectors/sector-real-estate.md`、`schema_extensions/real_estate.json`

**通用 11 项替换表**：

| 通用指标 | 地产处理 |
|---|---|
| ROE / ROIC | 失真（结算节奏 vs 销售节奏错位），改读"新增土储 IRR" 和 ROE on NAV |
| FCF/NI | 失真（已售未结的合同负债扭曲），改读"销售回款 / 结算营收"（> 1.0 健康） |
| 营收 CAGR | 改读"销售金额 CAGR"（更前置） |
| 有息负债/净资产 | **关键保留**，但用"净负债率"且结合三道红线 |
| 利息保障 / 流动比率 | 改读"现金短债比"（核心） |

**地产专属 20 项**（与 `real_estate.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `nav_per_share` | NAV 每股（重估土储+持有物业） | — | — |
| `nav_methodology` | NAV 方法说明 | — | — |
| `land_bank_area_msqm` | 土储建面 | — | — |
| `land_bank_value_cny_bn` | 土储估值 | — | — |
| `land_bank_tier1_share_pct` | 土储一线占比 | > 30% | < 10% |
| `land_bank_tier12_share_pct` | 土储一二线合计占比 | > 70% | < 40% |
| `contract_liabilities_cny_bn` | 合同负债（已售未结） | — | — |
| `contract_liab_to_revenue_ratio` | 合同负债/年营收（业绩锁定度） | > 1.0 | < 0.5 |
| `net_debt_to_equity_pct` | 净负债率 | < 60% | > 100% |
| `cash_to_short_term_debt_ratio` | 现金短债比 | > 1.5 | < 1.0 |
| `liability_to_asset_ex_advance_pct` | 剔预收负债率 | < 70% | > 75% |
| `sales_amount_cny_bn` | 全口径销售金额 | — | — |
| `sales_area_msqm` | 销售面积 | — | — |
| `asp_cny_per_sqm` | 均价 | — | — |
| `three_red_lines_status` | 三道红线状态（绿/黄/橙/红） | green | orange/red |
| `rental_income_share_pct` | 经营性收入占比 | > 15% | < 5% |
| `investment_property_value_cny_bn` | 投资性物业公允价值 | — | — |
| `price_to_nav_ratio` | 市值/NAV | < 0.6（深度低估） | > 1.0 |
| `financing_cost_avg_pct` | 综合融资成本 | < 5% | > 8% |
| `commercial_paper_overdue` | 商票逾期/违约 | 无 | 有任何记录 → critical_flag |

**核心判定**：三道红线"橙/红"档 + 现金短债比 < 1 + 商票逾期 = 三杀，强制 financial_quality ≤ 3 + risk ≤ 3，触发一票否决（万科案例验证）。

**NAV 重估视角**：地产 ≠ 工商企业，估值锚是 NAV 而非 PE/PB；price_to_nav < 0.5 通常是周期底部信号（但需排除三道红线触发的"价值陷阱"）。

---

### 6.5 holding_conglomerate — 控股集团（伯克希尔/复星/长和模式）

参考：`sectors/sector-holding-conglomerate.md`、`schema_extensions/holding_conglomerate.json`

**通用 11 项的核心问题**：合并报表把保险、自有实业、公开持仓全部混在一起，**ROE 和 ROIC 失真严重**（浮存金是负债不是权益，但产生免费杠杆；公开持仓的市价波动扭曲 NI；分部业绩交叉补贴掩盖个体表现）。

**关键原则（v2 强制）**：

> **ROE / ROIC 对控股集团仅供参考，不可作为主指标使用。**
>
> 必须改用：**(1) Look-through Earnings（巴菲特口径）+ (2) 分部业绩 + (3) SOTP NAV 变化**

**Look-through Earnings 口径**：
- 合并净利润 + 公开持仓的"应享净利润份额"（按持股比例）- 已计入的股息（避免双计）
- 衡量"如果完全持有持仓所对应的实质盈利能力"

**通用 11 项替换表**：

| 通用指标 | 控股集团处理 |
|---|---|
| ROE | **失真，仅供参考**（含浮存金、公开持仓市价扰动） |
| ROIC | **失真，仅供参考** |
| 毛利率稳定性 | N/A（多业态合并无意义） |
| FCF/NI | N/A（保险准备金扭曲；改读 Look-through Earnings） |
| 营收 CAGR | N/A（合并营收会随收购大变） |
| 有息负债/净资产 | 保留但需"母公司层面"剥离子公司负债 |

**控股集团专属 11 项**（与 `holding_conglomerate.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `segment_data` | 分部数据（保险/全资子公司/公开持仓/现金/其他） | 多条腿独立健康 | 单条腿亏损拖累 |
| `sotp_valuation` | SOTP 各分部估值表 | sotp_per_share 稳步上升 | 长期不增长 |
| `float_value_cny_bn` | 保险浮存金总额 | 增长 + 成本为负 | 停滞或成本上升 |
| `float_cost_pct` | 浮存金成本率 | < 0%（承保盈利 = 免费杠杆） | > 3% |
| `investment_portfolio_top10` | 公开持仓前 10 | 集中度合理 + 优质资产 | 频繁换手 |
| `investment_portfolio_total_value` | 公开持仓市值 | — | — |
| `holdco_discount_pct` | 控股折价 = (SOTP-市值)/SOTP | < 10%（小折价或溢价） | > 30%（市场不信任） |
| `buyback_history_cny_bn` | 近 10 年回购历史 | 低于 PB 时大量回购 | 高估时仍发新股 |
| `cumulative_returns_vs_benchmark` | 长期跑赢基准 | 10 年 CAGR > 基准 + 300bp | 跑输基准 |
| `key_person_age` | 核心 CEO 年龄 | < 70 + 明确接班人 | > 80 + 接班人不明 |
| `succession_plan_clarity` | 继承计划清晰度 | clear | unclear |

**核心判定**：浮存金成本 > 投资收益率 → 模式破产；控股折价 > 50% 且 SOTP 持续不增长 → 价值陷阱信号。

**估值口径**：SOTP（参考 `valuation.md`），不用 DCF。

---

### 6.6 cyclical_commodity — 大宗商品周期股

参考：`sectors/sector-cyclical-commodity.md`、`schema_extensions/cyclical_commodity.json`

**通用 11 项的核心问题**：商品价格周期决定一切，单年财务指标在周期顶部"假繁荣"、底部"假崩溃"。**必须用 10 年正常化指标**。

**通用 11 项替换表**：

| 通用指标 | 周期股处理 |
|---|---|
| ROE | 改用 **10 年正常化 ROE**（10 年均价对应的 ROE） |
| ROIC | 改用 **10 年正常化 ROIC** |
| 毛利率稳定性 | 改读"成本曲线分位"（cost_curve_position < 25% 优秀） |
| FCF/NI | 改读"10 年累计 FCF / 10 年累计 NI"（穿越周期） |
| 营收 CAGR | **N/A**（受价格波动主导，无意义），改读"产量 CAGR + 储量寿命" |
| 有息负债/净资产 | 保留但宽松（周期底部需有杠杆） |

**周期股专属 17 项**（与 `cyclical_commodity.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `commodity_price_history_10y` | 商品价格 10 年历史 | — | — |
| `normalized_eps` | 10 年正常化 EPS | — | — |
| `normalized_pe` | 正常化 PE | < 12x（底部） | > 20x（顶部） |
| `pb_cycle_percentile` | PB 在 10 年分布中的分位 | < 30%（低估） | > 70%（高估） |
| `long_term_contract_share_pct` | 长协合同占比 | > 50% | < 20% |
| `cost_curve_position` | 全球成本曲线分位（0=最低成本） | < 25% | > 75% |
| `cash_cost_per_unit` | 现金生产成本 | — | — |
| `all_in_sustaining_cost_per_unit` | AISC 全成本 | — | — |
| `reserves_life_years` | 可采储量寿命 | > 20 年 | < 10 年 |
| `reserves_total_units` | 总可采储量 | — | — |
| `production_volume_units` | 年产量 | 稳定或缓增 | 持续下降 |
| `own_logistics_value` | 自有运输（铁路/港口/电厂） | 完整一体化 | 依赖第三方 |
| `payout_ratio_pct` | 派息率 | > 60% | < 30% |
| `dividend_yield_pct` | 股息率 | > 6% | < 3% |
| `net_cash_position_cny_bn` | 净现金（高点蓄水池） | 大额净现金 | 净负债 |
| `capex_to_da_ratio` | 资本支出/折旧 | 顶部 < 1.0（收缩） / 底部 > 1.0（逆周期） | 反向 |
| `cycle_position` | 周期位置 enum | trough/early_recovery 买点 | peak 卖点 |

**F6 反向解读（v2 关键）**：

> **通用红旗 F6"存贷双高"对工商企业是造假信号（康美式），但对 cyclical_commodity 必须反向解读：**
>
> 周期股在景气顶部大量囤积现金作为"周期蓄水池"，同时保留长期低息债（应对未来回收期），这是**优秀资本配置**而非造假信号。
>
> 判定方法：若公司处于商品价高位 + 净现金为正 + 长期债成本 < 5%，则 F6 标记为 N/A 并记录 `na_reason: "cyclical_commodity_top_cash_reserve_strategy"`。

**核心判定**：
- 买点：pb_cycle_percentile < 30% + cycle_position 为 trough/early_recovery + 成本曲线 < 50% 分位
- 卖点：pb_cycle_percentile > 70% + cycle_position 为 peak + 商品价 > 历史 80% 分位

**估值口径**：正常化 EPS × 正常化 PE（取代单年 DCF），10 年 PB 分位作辅助。

---

### 6.7 utility_infrastructure_reit — 公用事业 / 基础设施 / REIT

参考：`sectors/sector-utility.md`、`schema_extensions/utility_infrastructure_reit.json`

**通用 11 项替换表**：

| 通用指标 | 公用事业/REIT 处理 |
|---|---|
| ROE | 保留，但锚点参考 `regulated_return_pct`（监管允许的上限） |
| ROIC | 改读 `regulated_return_pct`（监管基础回报率，6-12% 为常态） |
| 毛利率 | 受监管定价，稳定但受调价周期影响 |
| FCF/NI | **替换为 FFO/AFFO**（REIT 关键） |
| 营收 CAGR | 改读"rate_base 增长 + 派息增长" |
| 有息负债/净资产 | 改读 `debt_to_ebitda_ratio` |
| 利息保障 | 改读 `interest_coverage_ratio` |
| 流动比率 | N/A |

**公用事业/REIT 专属 17 项**（与 `utility_infrastructure_reit.json` 一一对应）：

| 字段名 | 中文名 | 优秀锚点 | 警戒锚点 |
|---|---|---|---|
| `regulated_return_pct` | 监管允许 ROE | 8-12% | < 6% |
| `rate_base_cny_bn` | 受监管资产基础 | 稳定增长 | 停滞 |
| `regulated_revenue_share_pct` | 受监管收入占比 | > 80% | < 50% |
| `payout_ratio_pct` | 派息率 | 60-80% | > 95% 或 < 40% |
| `dividend_yield_pct` | 股息率 | > 4% | < 2.5% |
| `dividend_growth_5y_pct` | 5 年股息复合增长 | > 5% | < 0%（削减） |
| `dividend_payment_history_years` | 连续派息年数（贵族股标志） | > 25 | 中断过 |
| `ffo_funds_from_operations_cny_bn` | FFO | — | — |
| `affo_adjusted_ffo_cny_bn` | AFFO（剔除维持性 capex） | AFFO > 分红 | AFFO < 分红 |
| `p_to_ffo_multiple` | P/FFO | 12-18x | > 25x |
| `occupancy_rate_pct` | 出租率（REIT） | > 95% | < 90% |
| `weighted_avg_lease_term_years` | 加权租约期限 WALT | > 5 年 | < 2 年 |
| `duration_in_regulated_cycle_years` | 当前监管周期剩余年数 | — | — |
| `regulatory_lag_months` | 监管滞后期 | < 6 个月 | > 18 个月 |
| `debt_to_ebitda_ratio` | 净有息负债/EBITDA | < 5x | > 7x |
| `interest_coverage_ratio` | EBITDA/利息 | > 3x | < 2x |
| `renewable_energy_capex_share_pct` | 新能源转型 capex 占比 | 与战略匹配 | 落后于同业 |

**核心判定**：派息覆盖（AFFO > 分红）+ 监管资本回报达标（regulated_return 实现 > 80%）+ 杠杆可控（debt/EBITDA < 6x）= 合格。任一不达标 → financial_quality ≤ 5。

**估值口径**：DDM 戈登增长模型 + P/FFO 倍数（参考 `valuation.md`）。

---

### 6.8 行业差异化指标总览

| company_type | 通用 11 项保留数 | 行业专属新增 | 替代方法学要点 |
|---|---|---|---|
| banking | 1（ROE） | 15 项 | NIM/不良/拨备/核充四件套 |
| insurance | 1（ROE） | 16 项 | EV+NBV+偿付能力 |
| biotech_unprofitable | 1（流动比率） | 14 项 | Cash runway + 管线 + SBC |
| real_estate | 3（净负债、现金短债、ROE on NAV） | 20 项 | 三道红线 + NAV |
| holding_conglomerate | 0（ROE 仅供参考） | 11 项 | Look-through + SOTP + 浮存金 |
| cyclical_commodity | 0（用正常化指标） | 17 项 | 10 年正常化 + 周期位置 + F6 反向 |
| utility_infrastructure_reit | 2（ROE 弱化、利息保障） | 17 项 | FFO/AFFO + 监管回报 + 派息 |

---

## 七、跨市场（A/H/US）财务披露差异（与 §五 互补）

§五 已覆盖通用差异，此处补充 **"行业 × 市场" 交叉关注点**（已并入 §五.5，避免重复）。

需要特别强调：

- **A 股银行**：拨备覆盖率监管底线 150% 是硬约束，不达标无法分红。优秀银行（如招行）通常保持 400%+ 作为"调节器"。
- **港股 18A biotech**：未盈利豁免上市后，必须每半年披露 R&D 进度 + cash runway，6160.HK 百济神州案例。
- **美股 Non-GAAP**：SBC 必须还原。对苹果（库克薪酬大头是 RSU）/腾讯 ADR/百济（30%+ 营收占比的 SBC）尤其关键。**例外**：成熟工业企业的 Non-GAAP 通常可信度较高（如 PG、KO）。
- **A/H 同股不同价**：财务报表口径一致（IFRS），价差来自流动性 + 投资者结构 + 汇率 + 港股通税率。价投通常选 H 股（折价），但要评估流动性。

---

## 八、阅读财报的优先顺序（v2 强制化）

> **本条作为 SKILL.md §6 软门控 S3 (`report_reading_order`)：skill 在输出 scorecard 前必须按本顺序读完，否则在 `quality_gate.soft_gates_passed` 中标 false 并显式提示用户。**

**强制顺序**（同 §1.2，此处重申）：

1. **现金流量表** → 真实性最高
2. **审计意见** → 非标意见即 PASS
3. **附注：关联交易、商誉、表外负债** → 雷区
4. **资产负债表** → 家底
5. **利润表** → 最后看
6. **致股东信 / MD&A** → 管理层视角

**行业适应**：

- banking / insurance：第 1 步改读 **资本充足率公告（A 股季报；美股 10-Q FR Y-9C）** + 资产质量分类（不良/正常/关注）
- biotech_unprofitable：第 1 步改读 **cash runway 测算 + 管线披露**，附注中的 R&D 资本化政策必查
- real_estate：第 1 步改读 **三道红线披露 + 商票逾期清单 + 销售经营数据快报**
- holding_conglomerate：第 1 步改读 **分部报告（segment data）+ 致股东信**（巴菲特的致股东信是范本）
- cyclical_commodity：第 1 步改读 **储量披露 + 成本曲线 + 长协占比**

---

## 九、数据来源建议

详见 `data-sources.md`。简要：

- **A 股**：巨潮资讯网（cninfo）/ 上交所/深交所披露 / Choice / Wind / iFind
- **港股**：HKEXnews / 公司 IR / Bloomberg HK
- **美股**：EDGAR (SEC) / 10-K & 10-Q / 8-K 临时公告 / Form 4 内部人交易
- **银行额外**：央行金融统计 / 银保监会季度数据 / 美联储 FR Y-9C
- **保险额外**：银保监会保险业月度数据 / 公司 EV 报告独立精算师披露
- **Biotech 额外**：ClinicalTrials.gov / FDA Approval Tracker / EvaluatePharma / 公司管线披露页
- **地产额外**：克而瑞 / 中指研究院 / 国家统计局 70 城价格
- **周期股额外**：商品价格（LME / 上海期货所 / 长江有色 / EIA / Platts）

---

## 十、与 red-flags-checklist.md 的衔接

> **v2 红旗清单已按 company_type 自动 N/A**：
>
> 当用户的目标公司分类为 7 类特殊行业之一时，`red-flags-checklist.md` 中的工商企业默认红旗（如 F4 应收账款异常、F5 存货异常、F6 存贷双高、F9 ROIC < WACC 等）会按 sector 文件中的 `red_flag_rules.na_list` 规则自动标 N/A，并填入 `red_flags.na_count` 和 `red_flags.na_reason`。
>
> 例如银行业自动 N/A 的红旗约 9 项（FCF/应收/存货/有息负债等不适用），地产自动 N/A 约 5 项（结算节奏失真），biotech 自动 N/A 约 12 项（无营收/无 FCF/无 ROIC）。
>
> 各 sector 文件中已定义具体的 N/A 列表与替代红旗。本文件不再重复，仅给出连接说明。

---

## 十一、v2 vs v1 关键变化总结

| 改造点 | v1 | v2 |
|---|---|---|
| 适用范围 | 工商企业为主，金融/特殊行业不适用 | 7 类特殊行业有专属指标体系，与 schema_extensions 一一对应 |
| 11 项通用指标 | "包打天下" | 默认体系 + 每项标注"行业 N/A / 替代" |
| 阅读顺序 | 建议 | **强制（软门控 S3）** |
| 三表勾稽 | 通用 | F6 存贷双高对 cyclical_commodity 反向解读 |
| ROE/ROIC | 核心指标 | 对 holding_conglomerate **明确不可作主指标** |
| 财务指标与 schema 字段 | 无对应 | **字段名 1:1 对应 schema_extensions JSON** |
| 行业 N/A 红旗 | 手工标 | 自动 N/A + na_reason 必填（衔接 red-flags-checklist.md） |
| 估值口径 | 主要 DCF | 按行业分流（DCF/SOTP/rNPV/PB-ROE/PEV/DDM/正常化 PE，见 valuation.md） |
| A/H/US 差异 | 单独 §四 | 加 §五.5 "行业 × 市场" 交叉关注点 |

**升级路径**：分析任一公司前，先调 SKILL.md §2.3 路由表 → 加载对应 sector-{type}.md + schema_extension JSON → 用本文件 §六 对应子节做财务质量评估 → 配合 `red-flags-checklist.md` 与 N/A 规则过审 → 输出 scorecard.json 的 `financial_quality` 维度评分（带 anchor_used）。

---

**本文件版本**：v2.0
**生效日期**：2026-05-15
**真理源**：`V2_SPEC.md`（§四 锚点、§九 schema_extensions 范围）

# 红旗清单（v2 行业自适应版本）

> v2 关键变化：红旗按 `company_type` 自动**启用 / N/A / 改读 / 新增**——不再"32 项硬过审"。
> v1 的 32 项保留为"通用基线"，但每条都附 **适用性矩阵**；行业专属红旗从 7 个 `schema_extensions/*.json` 同步而来。
> 配合文件：`templates/schema_extensions/*.json`（权威新增/N/A 源） + `references/sectors/sector-*.md`（行业 §五 权威源）。

---

## 一、设计原则

1. **company_type 先行**：识别公司原型 → 加载对应 sector 文件 §五 + schema_extension `red_flags_na_rules` → 再应用本文件的通用查找表。
2. **过审而非过滤**：v1 的"任一红色 → PASS"保留；v2 新增"N/A 不计入完成率"。
3. **三级颜色 + 第四级 N/A**：🟢 绿 / 🟡 黄 / 🔴 红 / **⚪ N/A（行业不适用，必须给出理由）**。
4. **行业新增红旗权威源**：schema_extensions 的 `new_sector_flags` 与 sector 文件 §五 的"新增专属"应一致；如冲突以 **sector 文件**为准（用户面向 sector 文件输出）。
5. **加载顺序**：
   ```
   Step 1: 判定 company_type
   Step 2: 读 schema_extensions/{type}.json 的 red_flags_na_rules（如有）
   Step 3: 读 sectors/sector-{type}.md §五
   Step 4: 应用本文件第二章「通用红旗 F1-F15 / G1-G10 / 市场特定」并查 §四 启用矩阵
   Step 5: 应用第三章「行业新增红旗」
   Step 6: 按第五章规则评分与决策
   ```

---

## 二、通用红旗（v1 基线，加 v2 适用性标记）

### 2.1 财务红旗 F1-F15

#### F1: 经营现金流 / 净利润（5 年均） < 0.5
- **解读**：利润含金量差。
- **默认状态**：🟢 通用启用。
- **N/A company_type**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate` / `real_estate`
- **N/A 理由**：
  - banking / insurance：无 OCF 与净利润直接可比关系（准备金、存贷扩张扰动）。
  - biotech_unprofitable：净利润为负，比值无意义。
  - holding_conglomerate：含投资浮盈浮亏与保险准备金扰动。
  - real_estate：交付制收入确认，销售款进入合同负债扭曲 OCF。

#### F2: 经营现金流连续 2 年负 + 净利润为正
- **解读**：高危造假信号（典型康美/瑞幸式）。
- **默认**：🔴 严重信号。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：上述行业 OCF 概念与工商企业不同；biotech 净利润长期为负，不会触发"利润正 OCF 负"。

#### F3: 销售商品收到现金 / 营业收入（含税） < 1.0
- **解读**：收入回款异常。
- **默认**：🟡-🔴。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：金融业无"销售商品现金"科目；biotech 商业化前营收极小。

#### F4: 投资现金流持续大额流出但 ROIC 不升
- **解读**：价值毁灭式扩张。
- **默认**：🟡-🔴。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：银行/保险的投资活动是业务本质；biotech ROIC 长期为负；控股集团 ROIC 算法失真。

#### F5: 筹资现金流长期净流入（不能自我造血）
- **解读**：靠融资续命。
- **默认**：🟡-🔴。
- **N/A / 改读**：
  - `banking` / `insurance`：N/A（吸存/收保费即"筹资"性质入款，是业务本质）。
  - `biotech_unprofitable`：N/A（依赖股本融资是模型本身，关键看 BIO_F3 稀释率）。
  - `holding_conglomerate`：N/A。
- **改读**：
  - `banking` → `BANK_MOD_F5`：ROE < 权益成本（约 10-12%）持续 3 年。
  - `biotech_unprofitable` → `BIOTECH_MOD_F5`：累计 R&D 投入 vs 已上市药峰值销售比 < 1（研发产出效率低）。
  - `real_estate` → `RE_MOD_F5`：ROE < 综合融资成本 持续 2 年。
  - `cyclical_commodity` → `CYC_MOD_F5`：看 10 年正常化 ROIC（穿越周期），低点单年 ROIC 低不构成红旗。
  - `utility_infrastructure_reit` → `UTL_MOD_F5`：实际 ROE < 监管允许回报率 × 0.8 持续 2 年。
  - `insurance` → `INS_MOD_F5`：ROEV < 12% 持续 3 年。
  - `holding_conglomerate` → `HC_MOD_F5`：BVPS 增速 + 派息率 < 10% 长期。

#### F6: 存贷双高（货币资金 > 20% 总资产 且 有息负债 > 20% 总资产）
- **解读**：康美式典型造假信号。
- **默认**：🔴。
- **N/A / 反向解读**：
  - `banking` / `insurance` / `biotech_unprofitable`：N/A（业务本质就是吸存放贷 / 保险准备金 / IPO 募资留存）。
  - `holding_conglomerate`：**反向解读**——浮存金 + 现金 + 长债组合是业务本质，需结合 HC_F6（现金长期沉淀无配置）单独判断。
  - `cyclical_commodity`：**反向解读**——周期高点蓄水池策略，净现金积累 + 长债保留是优势；只有"无明确用途且短债成本高"才是红旗（见 CYC_MOD_F6）。
  - `utility_infrastructure_reit`：**反向解读**——高负债 + 持有优质收益资产是业务本质，要结合利息覆盖率 UTL_F5 判断。

#### F7: 商誉 / 净资产 > 30%
- **解读**：减值地雷。
- **默认**：🟡-🔴 通用启用。
- **N/A**：无（所有行业适用）。
- **改读**：
  - `biotech_unprofitable` → `BIOTECH_MOD_F11`：授权/并购管线占总管线 > 60% 且自研管线推进缓慢。
  - `holding_conglomerate` → `HC_MOD_F11`：商誉占股东权益 > 50% 且并购回报 ROIC < 8%。

#### F8: 应收账款增速 > 营收增速 × 1.5
- **解读**：放宽信用换收入。
- **默认**：🟡-🔴。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：银行/保险无应收账款主体科目；biotech 商业化前应收极小；控股集团合并意义不大。
- **改读**：
  - `banking` → `BANK_MOD_F8`：贷款增速 - 存款增速 > 5pp 持续 2 年（流动性紧张）。
  - `real_estate` → `RE_MOD_F8`：合同负债同比下滑 > 20%（业绩锁定度下降）。
  - `utility_infrastructure_reit` → `UTL_MOD_F8`：应收欠费规模异常增长（拖欠 / 政府欠款）。

#### F9: 存货周转天数连续 3 年上升
- **解读**：滞销或虚增。
- **默认**：🟡-🔴。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：金融业无存货；biotech 商业化前无存货周转概念。
- **改读**：
  - `real_estate` → `RE_MOD_F3`：去化周期（土储 / 年销售面积）> 5 年。

#### F10: 在建工程多年不转固定资产
- **解读**：可能藏费用。
- **默认**：🟢-🟡 通用启用。
- **N/A**：`biotech_unprofitable` / `holding_conglomerate`
- **N/A 理由**：biotech 无大量在建工程；控股集团合并扰动。

#### F11: 其他应收款 / 营收 > 10% 且明细不清
- **解读**：关联输送通道。
- **默认**：🟡-🔴 通用启用。
- **N/A**：无强制 N/A（但银行/保险需看合并口径合理性）。

#### F12: 毛利率显著高于同业（> 10pct）且无技术壁垒解释
- **解读**：收入或成本异常。
- **默认**：🟡-🔴。
- **N/A**：`banking` / `insurance` / `biotech_unprofitable`（未盈利） / `holding_conglomerate`
- **N/A 理由**：金融业用 NIM / 综合成本率替代毛利率；biotech 商业化早期毛利波动巨大；控股集团毛利率合并扰动。
- **改读**：
  - `banking` → 看 NIM 与同业差异。
  - `insurance` → `INS_MOD_F4`：综合成本率持续上升突破 100% 或 NBV margin 持续下滑。
  - `cyclical_commodity` → `CYC_MOD_F4`：毛利率下滑需归因（商品价 vs 自身竞争力），同行同步下滑是周期非个体问题。

#### F13: 研发费用资本化率突然提升
- **解读**：利润粉饰。
- **默认**：🟡 通用启用。
- **N/A**：无强制 N/A，但 `biotech_unprofitable` 研发费用化为主，资本化少见。

#### F14: 业绩集中在 Q4 确认（> 40%）
- **解读**：全年业绩调节。
- **默认**：🟡 通用启用。
- **N/A**：`real_estate`（地产交付集中在 Q4 是行业常态）；`banking` / `insurance`（按息差/保费稳定确认）。

#### F15: 收购溢价远超同业（PB / PE 倍数异常）
- **解读**：高额商誉埋雷。
- **默认**：🟡-🔴 通用启用。
- **N/A**：无（所有行业适用，控股集团需结合 HC_MOD_F11）。

---

### 2.2 治理红旗 G1-G10（全行业通用，差异化极小）

#### G1: 频繁更换审计机构 / 审计师出具非标意见
- **默认**：🔴 适用于所有公司类型。
- **N/A**：无。

#### G2: 实控人 / 高管密集离职（尤其 CFO）
- **默认**：🔴。
- **N/A**：无。
- **行业强化**：`biotech_unprofitable` 额外含核心科学家 / CMO 离职（见 BIO_F6）。

#### G3: 大股东股权质押 > 70%（A 股特别警惕）
- **默认**：🔴 适用于所有 A 股；港美股以"控制权 + 杠杆"形式呈现。
- **N/A**：无。

#### G4: 大股东 / 董监高近 6 个月减持 > 1% 流通股
- **默认**：🟡-🔴。
- **N/A**：无。

#### G5: 关联交易占营收 > 30%
- **默认**：🔴。
- **N/A**：无；`holding_conglomerate` 内部分部交易需单独披露与解释。

#### G6: 收到立案调查公告
- **默认**：🔴 **强制 PASS**。
- **N/A**：无。

#### G7: 收到交易所年报问询函 / 重大问询函
- **默认**：🟡（一般业务问询）→ 🔴（财务造假问询）。
- **N/A**：无。

#### G8: 频繁变更主营业务 / 跨界并购（港股老千股特征）
- **默认**：🟡-🔴。
- **N/A**：`holding_conglomerate`（业务多元是模式本身），但需结合 HC_MOD_F11 商誉/回报判断。

#### G9: 控股股东持股 < 30% 且分散持有（港股老千股特征）
- **默认**：🟡-🔴 主要适用于港股小盘。
- **N/A**：无强制；大盘蓝筹通常股权分散是常态，不直接红旗。

#### G10: 管理层薪酬中短期奖金占比过高（> 60%）
- **默认**：🟡。
- **N/A**：无。
- **行业强化**：`biotech_unprofitable` 额外看 SBC/营收（见 BIO_F4）。

---

### 2.3 市场特定红旗（v2 调整：按"市场后缀"自动启用）

> v2 调整：不再强制所有公司过审全部 7 项市场红旗。按 ticker 后缀 / 上市地自动启用对应分组。

#### A 股专属
| 编号 | 项目 | 启用条件 |
|---|---|---|
| **CN1** | ST / *ST 标识 / 退市风险警示 | ticker 后缀 .SH / .SZ / .BJ |
| **CN2** | 公司处于政策强收紧行业（教培归零、地产三道红线、平台反垄断等） | 同上；与 `modifier_flags: regulated_heavily` 联动 |

#### 港股专属
| 编号 | 项目 | 启用条件 |
|---|---|---|
| **HK1** | 5 年内 ≥ 2 次大比例配股 / 供股 | ticker 后缀 .HK |
| **HK2** | 5 年内 ≥ 1 次合股 | 同上 |
| **HK3** | 股价长期 < HK$1（仙股）+ 大股东分散 | 同上 |

#### 美股专属
| 编号 | 项目 | 启用条件 |
|---|---|---|
| **US1** | 知名做空机构发布做空报告（Hindenburg / Muddy Waters / Citron 等） | NYSE / NASDAQ 上市 |
| **US2** | 8-K 披露 Restatement / CFO 突然辞职 / 审计师变更 | 同上 |

#### 跨市场（modifier_flags 触发）
- **`vie_structure`**：增加 VIE 风险红旗 —— 协议控制有效性 / 利润汇出限制 / 监管态度变化。
- **`pcaob_risk`**：增加 PCAOB 审计风险红旗 —— 三年滚动审计不达标可能被强制退市。
- **`a_h_dual_listed` / `dual_primary_listing`**：检查 A 股与港股的同股权益差异 / 流动性差 / 折溢价。

---

## 三、行业新增红旗（v2 新增，从 schema_extensions/*.json 同步）

### 3.1 banking 专属红旗（BANK_F*）

来源：`templates/schema_extensions/banking.json` `red_flags_na_rules.new_sector_flags`

| ID | 描述 | 触发条件 |
|---|---|---|
| **BANK_F1** | 不良贷款率连续两年上升且 > 2% | `npl_ratio_pct_t > npl_ratio_pct_t-1 > npl_ratio_pct_t-2 AND npl_ratio_pct_t > 2.0` |
| **BANK_F2** | 拨备覆盖率跌破 150% 监管红线 | `provision_coverage_pct < 150` |
| **BANK_F3** | 核心一级资本充足率 < 监管线 + 1pp（缓冲极薄） | `car_tier1_pct - regulatory_minimum < 1.0` |
| **BANK_F4** | NIM 连续 3 年收窄且每年下降 > 10bp | NIM 连续 3 年同比下降 10bp+ |
| **BANK_F5** | 关注类贷款大幅上升暗示不良迁徙 | 关注类贷款占比同比上升 > 50bp |
| **BANK_F6** | 成本收入比连续上升 > 45% | `cost_to_income_ratio_pct > 45 AND 同比上升` |
| **BANK_F7** | 同业负债 / 总负债 > 30%（依赖批发资金） | `interbank_liab_share > 30%` |

### 3.2 insurance 专属红旗（INS_F*）

来源：`templates/schema_extensions/insurance.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **INS_F1** | 综合成本率连续两年 > 100% | combined_ratio_pct 连续两期 > 100 |
| **INS_F2** | 偿付能力跌破监管红线（综合 < 100% 或核心 < 50%） | `solvency_ratio_pct < 100 OR core_solvency_ratio_pct < 50` |
| **INS_F3** | NBV 连续两年负增长 | nbv_cny_bn 连续两期负增长 |
| **INS_F4** | 13 个月继续率 < 80%（保单流失严重） | `policyholder_persistency_13m_pct < 80` |
| **INS_F5** | 投资组合集中度过高（单一资产 / 单一发行人 > 10%） | `single_issuer_share > 10%` |
| **INS_F6** | 资产负债久期缺口 > 5 年 | `abs(asset_duration - liability_duration) > 5` |

### 3.3 biotech_unprofitable 专属红旗（BIO_F*）

来源：`templates/schema_extensions/biotech_unprofitable.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **BIO_F1** | 现金跑道 < 12 个月且无明确融资计划 | `cash_runway_months < 12 AND no_announced_financing` |
| **BIO_F2** | 关键管线临床 III 期主终点失败 | `phase_3_primary_endpoint_failed = true` |
| **BIO_F3** | 年稀释率 > 15% 持续两年 | `share_dilution_yoy_pct > 15` 连续两年 |
| **BIO_F4** | SBC / 营收 > 50%（伪利润） | `sbc_to_revenue_ratio > 0.5` |
| **BIO_F5** | 核心管线监管推迟或被发出 CRL | `FDA CRL OR NMPA 退审` |
| **BIO_F6** | 核心科学家 / CMO 突然离职 | `key_scientist_departure = true` |
| **BIO_F7** | 授权合作伙伴终止合作并退回权益 | `partnership_terminated = true` |

### 3.4 real_estate 专属红旗（RE_F*）

来源：`templates/schema_extensions/real_estate.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **RE_F1** | 三道红线踩 2 道以上 | `three_red_lines_status.color in ['orange','red']` |
| **RE_F2** | 现金短债比 < 1（短期偿债压力极大） | `cash_to_short_term_debt_ratio < 1` |
| **RE_F3** | 美元债境外违约或要求重组 | `offshore_bond_default = true` |
| **RE_F4** | 商票逾期 / 拒付 | `commercial_paper_overdue = true` |
| **RE_F5** | 销售连续两年下滑 > 20% | `sales_amount_yoy < -20%` 连续两年 |
| **RE_F6** | 拿地停滞超 12 个月 + 销售下滑（缩表信号） | `land_acquisition_months_since_last > 12 AND sales declining` |
| **RE_F7** | 投资性房地产公允价值大幅减值（> 5%） | `investment_property_impairment > 5%` |
| **RE_F8** | 境外融资渠道关闭 / 评级被下调至投机级 | `credit_rating_downgraded_to_junk = true` |

**三道红线**单列说明（v2 关键监管框架）：
1. 剔除预收款的资产负债率 ≤ 70%
2. 净负债率 ≤ 100%
3. 现金短债比 ≥ 1

| 踩 0 道 | 踩 1 道 | 踩 2 道 | 踩 3 道 |
|---|---|---|---|
| 绿档（有息负债年增 ≤ 15%） | 黄档（≤ 10%） | 橙档（≤ 5%） | 红档（**不得新增**） |

### 3.5 holding_conglomerate 专属红旗（HC_F*）

来源：`templates/schema_extensions/holding_conglomerate.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **HC_F1** | 浮存金成本由负转正且超过 3% | `float_cost_pct > 3` |
| **HC_F2** | BVPS 增速 < 通胀 + 长期国债收益率（毁灭股东价值） | `bvps_cagr_5y < (cpi + 10y_treasury_yield)` |
| **HC_F3** | 回购溢价过高（回购价 > 1.5x PB） | `buyback_avg_premium_to_pb > 1.5` |
| **HC_F4** | 核心人物年龄 > 90 且无清晰继承计划 | `key_person_age > 90 AND succession_plan_clarity == 'unclear'` |
| **HC_F5** | 分部信息劣化导致 SOTP 不可估算 | `sotp_transparency_score <= 3` |
| **HC_F6** | 现金长期占总资产 > 25% 且无并购出手（资本配置闲置） | `cash_share > 25%` 持续 3 年 |

### 3.6 cyclical_commodity 专属红旗（CC_F* / 在 schema 中以 CYC_F* 命名）

来源：`templates/schema_extensions/cyclical_commodity.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **CYC_F1** | 成本曲线分位上移 > 10pp（成本竞争力下滑） | `cost_curve_position` 同比上升 > 10 |
| **CYC_F2** | 储量寿命 < 10 年且补充乏力 | `reserves_life_years < 10 AND no_new_reserves` |
| **CYC_F3** | 周期高点大规模扩张资本支出（capex/DA > 2x） | `cycle_position in ['late_cycle','peak'] AND capex_to_da_ratio > 2` |
| **CYC_F4** | PB 在 10 年 90% 分位以上（周期高点估值警告） | `pb_cycle_percentile > 90` |
| **CYC_F5** | 长协占比连续下滑 + 价格大幅低于现货（销售竞争力下降） | `long_term_contract_share_pct` 持续下滑 |
| **CYC_F6** | 管理层在低点不回购也不分红反而高溢价并购 | `cycle_position == 'trough' AND major_acquisition_at_premium` |

### 3.7 utility_infrastructure_reit 专属红旗（UTIL_F* / 在 schema 中以 UTL_F* 命名）

来源：`templates/schema_extensions/utility_infrastructure_reit.json`

| ID | 描述 | 触发条件 |
|---|---|---|
| **UTL_F1** | 派息率 > 100% 长期不可持续 | `payout_ratio_pct > 100` 连续两年 |
| **UTL_F2** | 股息削减或暂停 | `dividend_cut_yoy > 0` |
| **UTL_F3** | 出租率连续下滑 + 跌破 90%（REIT） | `occupancy_rate_pct` 连续下滑 AND < 90 |
| **UTL_F4** | 监管裁定不利（提价被拒绝 / 监管允许回报下调） | `regulated_return_pct` 同比下降 |
| **UTL_F5** | 利息覆盖率 < 2 + 利率上行环境 | `interest_coverage_ratio < 2` |
| **UTL_F6** | 维持性 capex 大幅超 FFO（老化资产巨额翻新） | `maintenance_capex > 0.5 × FFO` |
| **UTL_F7** | 燃料 / 能源转型滞后导致搁浅资产风险 | `stranded_assets_at_risk = true` |

---

## 四、按 company_type 的红旗启用矩阵（v2 核心查找表）

> 列：每个 company_type 行为；行：通用红旗编号。
> 标记：✓ = 启用（默认）；**N/A** = 不适用；**改读** = 替换为行业指标（见第二章）；**反向↗** = 反向解读（蓄水池 / 业务本质）。

### 4.1 财务红旗矩阵 F1-F15

| 编号 | 通用 | banking | insurance | biotech_unprofitable | real_estate | holding_conglomerate | cyclical_commodity | utility/REIT |
|---|---|---|---|---|---|---|---|---|
| F1 OCF/NI | ✓ | N/A | N/A | N/A | N/A | N/A | ✓ | ✓ |
| F2 OCF负+NI正 | ✓ | N/A | N/A | N/A | ✓ | N/A | ✓ | ✓ |
| F3 销售现金/营收 | ✓ | N/A | N/A | N/A | ✓ | N/A | ✓ | ✓ |
| F4 投资CF不升ROIC | ✓ | N/A | N/A | N/A | ✓ | N/A | ✓ | ✓ |
| F5 筹资CF长期净流入 | ✓ | N/A→改读 | N/A→改读 | N/A→改读 | 改读 | N/A→改读 | 改读 | 改读 |
| F6 存贷双高 | ✓ | N/A | N/A | N/A | ✓ | 反向↗ | 反向↗ | 反向↗ |
| F7 商誉/净资产>30% | ✓ | ✓ | ✓ | 改读 | ✓ | 改读 | ✓ | ✓ |
| F8 应收增速>营收×1.5 | ✓ | N/A→改读 | N/A | N/A | 改读 | N/A | ✓ | 改读 |
| F9 存货周转上升 | ✓ | N/A | N/A | N/A | 改读 | N/A | ✓ | ✓ |
| F10 在建工程不转固 | ✓ | ✓ | ✓ | N/A | ✓ | N/A | ✓ | ✓ |
| F11 其他应收异常 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F12 毛利率异常高 | ✓ | N/A→改读 | N/A→改读 | N/A | ✓ | N/A | 改读 | ✓ |
| F13 研发资本化率突升 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F14 Q4集中确认 | ✓ | N/A | N/A | ✓ | N/A | ✓ | ✓ | ✓ |
| F15 收购溢价异常 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

### 4.2 治理红旗矩阵 G1-G10

| 编号 | 通用 | banking | insurance | biotech | real_estate | holding | cyclical | utility |
|---|---|---|---|---|---|---|---|---|
| G1 审计师更换/非标 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G2 实控人/高管离职 | ✓ | ✓ | ✓ | ✓+强化 | ✓ | ✓ | ✓ | ✓ |
| G3 股权质押>70% | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G4 6月减持>1% | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G5 关联交易>30% | ✓ | ✓ | ✓ | ✓ | ✓ | ✓+披露 | ✓ | ✓ |
| G6 立案调查 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G7 问询函 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G8 跨界并购 | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ |
| G9 控股股东<30% 分散 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| G10 短期奖金占比>60% | ✓ | ✓ | ✓ | ✓+SBC | ✓ | ✓ | ✓ | ✓ |

### 4.3 市场特定矩阵（按 ticker 后缀启用）

| 编号 | A 股 .SH/.SZ/.BJ | 港股 .HK | 美股 NYSE/NASDAQ |
|---|---|---|---|
| CN1 ST/退市 | ✓ | N/A | N/A |
| CN2 政策强收紧 | ✓ | 部分（互联网/教育） | N/A |
| HK1 配股/供股 | N/A | ✓ | N/A |
| HK2 合股 | N/A | ✓ | N/A |
| HK3 仙股 + 大股东分散 | N/A | ✓ | N/A |
| US1 做空机构报告 | N/A | 部分 ADR | ✓ |
| US2 8-K Restatement/CFO 辞职 | N/A | N/A | ✓ |

### 4.4 N/A 项汇总（按行业）

| company_type | N/A 财务项 | N/A 治理项 | N/A 市场项 | 合计 N/A |
|---|---|---|---|---|
| banking | F1, F2, F3, F4, F5, F6, F8, F9, F12（9 项） | 0 | 按市场 | **9** |
| insurance | F1, F2, F3, F4, F5, F6, F8, F9, F12, F14（10 项） | 0 | 按市场 | **10** |
| biotech_unprofitable | F1, F2, F3, F4, F5, F6, F8, F9, F10, F12（10 项） | 0 | 按市场 | **10** |
| real_estate | F1, F8（部分）, F14（4 项） | 0 | 按市场 | **3-4** |
| holding_conglomerate | F1, F2, F3, F4, F5, F6（反向）, F8, F9, F10, F12（10 项） | G8 | 按市场 | **10-11** |
| cyclical_commodity | F6（反向，非纯 N/A）（1 项） | 0 | 按市场 | **1** |
| utility_infrastructure_reit | F6（反向）（1 项） | 0 | 按市场 | **1** |

注：以上 N/A 数依据每个 schema_extension 的 `red_flags_na_rules.na_items` 直接归集，与 sector 文件 §五 互相印证。具体每条 N/A 理由见第二章 F1-F15 各条与 sector 文件。

---

## 五、过审与评分规则（v2 修订）

### 5.1 颜色判定

每项启用项标记：
- 🟢 **绿色**：未触发。
- 🟡 **黄色**：部分触发或处于警戒区。
- 🔴 **红色**：明显触发。
- ⚪ **N/A**：行业不适用（必须给出 `na_reason`，来自 sector 或 schema_extension）。

### 5.2 完成率定义（v2 新增）

```
启用项数 = 通用红旗启用数 - N/A 数 + 行业新增红旗数 + 市场特定启用数
完成率 = (已过审项 / 启用项数) × 100%

要求：完成率 = 100%（每个启用项都必须有结论）
```

**重要：N/A 不计入完成率分母**，但必须在 scorecard 的 `red_flags.na_count` 与 `red_flags.na_reason` 显式标注。

### 5.3 决策门槛

| 触发情形 | 行动 |
|---|---|
| 任一红色（启用项） | **强制 PASS**（除非"特殊解释"，如 G7 是正常业务问询） |
| 黄色 ≥ 3 项（启用项） | 显著提高安全边际要求（额外 + 15-25%）或建议 watchlist |
| 全绿（含 N/A 已合规标注） | 进入完整分析 |

### 5.4 硬门控 H5 判定（V2_SPEC §七）

`red_flag_checklist_done = true` 当且仅当：
1. 所有启用项（去 N/A 后）都已过审（🟢/🟡/🔴 三色）。
2. 所有 N/A 项有显式 `na_reason`。
3. scorecard.red_flags 字段完整填写 `red_count / yellow_count / green_count / na_count`。

未通过 → 输出降级为 `unverified_quick_look` 模式。

### 5.5 一票否决（独立于矩阵）

- G6 立案调查 → 强制 PASS。
- BIO_F2 临床 III 期主终点失败 → 强制 PASS（biotech）。
- RE_F3 美元债违约 → 强制 PASS（real_estate）。
- INS_F2 偿付能力跌破红线 → 强制 PASS（insurance）。
- BANK_F3 核心资本距监管线 < 1pp → 强制 PASS（banking）。

---

## 六、报告中的呈现规范（v2 强化）

完整研报必须含独立"红旗过审"章节。**必备四张表**：

### 表 1：通用财务红旗（F1-F15）

| 编号 | 项目 | 状态 | 适用性 | 证据 |
|---|---|---|---|---|
| F1 | OCF/NI 5 年均 | 🟢/🟡/🔴/⚪ | 自动启用 / N/A 理由 | 数值 + source + fetched_at |
| F2 | OCF 负 + NI 正 | ... | ... | ... |
| ... | | | | |

### 表 2：通用治理红旗（G1-G10）

| 编号 | 项目 | 状态 | 适用性 | 证据 |
|---|---|---|---|---|

### 表 3：市场特定红旗

| 编号 | 项目 | 状态 | 启用条件 | 证据 |
|---|---|---|---|---|

### 表 4：行业新增红旗（按 company_type）

| 编号 | 项目 | 状态 | 触发条件 | 证据 |
|---|---|---|---|---|
| BANK_F1 / BIO_F1 / RE_F1 / ... | ... | ... | ... | ... |

### 表 5：总结

```yaml
red_count: 1
yellow_count: 2
green_count: 14
na_count: 9   # banking 样本
na_reason: "见 schema_extensions/banking.json 与 sectors/sector-banking.md §五"
completion_rate: 100%
critical_flags: [F6]
hard_gate_H5: passed | failed
final_decision: PASS / Watchlist / 通过进入完整分析
```

---

## 七、与 sector 文件的衔接

每个 `sectors/sector-{type}.md` §五 "红旗 N/A / 改读规则" 是**该 type 的权威源**。本文件提供"通用查找表 + 启用矩阵 + 加载顺序"。

**冲突处理优先级**：
1. `sectors/sector-{type}.md` §五（最高，面向用户输出）
2. `templates/schema_extensions/{type}.json` `red_flags_na_rules`（结构化数据源）
3. 本文件第二章 / 第四章（通用基线）

**如果发现 sector 文件与 schema_extension 不一致**：
- 数量上以 sector 为准（如 banking 9 项 N/A）。
- 编号映射上以 schema_extension 为准（如 BANK_F1-F7 用此命名）。
- 报告输出时同时引用两个来源（增强可追溯性）。

---

## 八、使用规则（v1 保留 + v2 强化）

1. 这份清单是**最低安全标准**，不是充分条件。
2. **全绿不代表可买**，只代表"未踩雷"；还要看 6 维评分锚点（V2_SPEC §四）与决策矩阵（V2_SPEC §五）。
3. 每次分析必须执行此清单，**不可跳过**（硬门控 H5）。
4. 红旗信息要写进报告，让用户看到判断依据。
5. **N/A 必须有理由**，理由要可溯源到 sector 文件或 schema_extension。
6. **行业新增红旗与通用红旗同等权重**，不区分主次（例如 BANK_F2 拨备覆盖率跌破 150% 与 F6 存贷双高一样是 🔴 红色）。
7. 如有判断为"特殊解释"（如商誉高但被收购公司业绩极好），必须显式说明并提高风险权重。
8. **不可在报告里给"红色但买入"的结论**，除非用户明确签字承担风险并显式提高安全边际 ≥ 20pp。

---

**本文件即 v2 红旗清单的权威实施手册。任何与本文件冲突的旧 v1 流程视为废止。**

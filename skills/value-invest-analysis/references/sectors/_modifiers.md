# Modifier Flags 详解 (v2.0)

> **真理源**：`V2_SPEC.md` §三、§六。Modifier flags 是可叠加的特性描述，与主类型 `company_type` 正交，主要用于：
> 1. 修饰风险评分（risk 维度）
> 2. 调整 `required_pct_margin_of_safety` 公式中的 `modifier_adjustment` 项
> 3. 提醒分析师注意特殊监管/治理/披露问题

## 总览（10 个 flag）

| flag | 中文 | required_pct 影响 | 主要影响维度 |
|---|---|---|---|
| `with_policy_support` | 政策托底 | 0 | management / risk |
| `distressed` | 困境状态 | +10 | risk / financial_quality |
| `a_h_dual_listed` | A+H 双重上市 | 0 | valuation（套利） |
| `vie_structure` | VIE 架构 | +5 | risk / management |
| `adr_listed` | ADR 上市 | 0 | risk（退市/审计） |
| `dual_primary_listing` | 双重主要上市 | 0 | risk（缓解 ADR 风险）|
| `creator_led` | 创始人主导 | 0 | management（双刃） |
| `state_owned` | 国企背景 | 0 | management / 资本配置 |
| `regulated_heavily` | 强监管行业 | +3 | risk / valuation |
| `pcaob_risk` | PCAOB 审计风险 | +5 | risk / 一票否决预警 |

---

## 1. `with_policy_support`（政策托底）

- **含义**：行业受国家产业政策、补贴、行政性壁垒保护；或公司业务高度依赖政府订单 / 补贴
- **触发条件**：(a) 收入 / 利润中政府补贴占比 ≥ 10%；或 (b) 行业准入由国家审批；或 (c) 公司是国家战略产业链关键环节（半导体国产替代、电网、军工）
- **评分影响**：
  - business_quality：政策红利期可加 +0~+1，但需在 rationale 标注"政策红利不可持续"
  - risk：扣 -1 ~ -2（政策变向风险）
  - 不调 required_pct
- **案例**：比亚迪（新能源补贴退坡前）、中芯国际（国产替代）、中国神华（保供）

## 2. `distressed`（困境状态）

- **含义**：公司已进入财务困境 / 主业暴雷 / 战略受挫 / 治理重大动荡
- **触发条件**：(a) 财务红旗 ≥ 8 项；或 (b) 主营连续亏损 ≥ 2 年；或 (c) 现金流紧张（现金/短债 < 0.5）；或 (d) 管理层重大动荡 / 立案调查
- **评分影响**：
  - financial_quality：≤ 3 几乎必然
  - risk：≤ 3
  - **required_pct += 10**（巨幅提高安全边际要求）
  - 触发"价值陷阱 6 信号"自动加 2-3 项
- **案例**：万科 2024-2026（地产暴雷）、Boeing 2024（737 MAX）

## 3. `a_h_dual_listed`（A+H 双重上市）

- **含义**：A 股 + H 股双重上市（不区分先后顺序），不指 ADR
- **触发条件**：同时存在 SH/SZ 上市代码 + HKEX 上市代码
- **评分影响**：
  - 不影响六维评分
  - **估值需双轨**：必须用 A 股价 + H 股价 各计算 margin_of_safety；二者通常存在 10-40% 折溢价
  - 报告 `decision.suggested_position` 需注明 buy_a_or_h
- **案例**：招行 600036.SH / 3968.HK、平安、中石油、宁德时代

## 4. `vie_structure`（VIE 架构）

- **含义**：可变利益实体结构。境内运营实体非上市公司直接持股，通过协议控制
- **触发条件**：(a) 中概互联网公司在美 / 港上市绝大多数采 VIE；(b) 招股书 / 年报"风险因素"专章披露 VIE
- **评分影响**：
  - management：取决于 VIE 协议执行历史，通常 -0 ~ -1
  - risk：-1 ~ -2（政策不确定性）
  - **required_pct += 5**
- **案例**：阿里、京东、新东方、好未来（已暴雷案例：2021 教培）、拼多多

## 5. `adr_listed`（ADR 上市）

- **含义**：仅以 ADR（美国存托凭证）形式在美上市，无港股双重主要上市保护
- **触发条件**：(a) 仅在 NYSE/NASDAQ 上市；(b) 未在港股完成 dual_primary_listing
- **评分影响**：
  - risk：-1 ~ -2（HFCAA 退市风险 / PCAOB 审计、SEC 摘牌）
  - 不直接调 required_pct（与 pcaob_risk 联动判断）
- **案例**：贝壳找房（2023 转双重主要上市前）、富途控股、知乎

## 6. `dual_primary_listing`（双重主要上市）

- **含义**：同一公司在 HKEX + US 同时为主要上市（而非 secondary listing）。受双重监管，减轻 ADR 退市风险
- **触发条件**：HKEX 招股书明确"双重主要上市"
- **评分影响**：
  - risk：相对 `adr_listed` 单上市可 +0.5 ~ +1（更安全）
  - 不调 required_pct
- **案例**：京东 9618.HK / JD US（2022 完成）、贝壳 2423.HK、阿里巴巴 9988.HK（2024 完成）

## 7. `creator_led`（创始人主导）

- **含义**：公司由创始人 CEO / 董事长长期掌舵，且持股比例 / 表决权显著（≥ 10% 或采取双层股权）
- **触发条件**：(a) 创始人仍任 CEO/Chairman；(b) 持股 ≥ 10% 或拥有特别表决权
- **评分影响**：双刃剑
  - 优秀创始人（贝索斯、张一鸣、马斯克、马化腾、王传福）：management +1 ~ +2
  - 治理瑕疵创始人（黄峥不沟通 / 早期马云风险）：management -1
  - 风险：继任风险 / 接班不确定性 / 个人风险 → risk -1
- **案例**：比亚迪（王传福）、特斯拉（马斯克）、英伟达（黄仁勋）、Meta（扎克伯格）

## 8. `state_owned`（国企背景）

- **含义**：国资委 / 财政部 / 地方政府为实际控制人
- **触发条件**：实际控制人为中央 / 地方政府或国资委
- **评分影响**：
  - management：资本配置可能效率不高（-0 ~ -1）；但稳定性强（+0.5）
  - business_quality：行业地位通常稳固
  - 不直接调 required_pct
  - 注意：国企分红率通常较高且稳定 → 有利于 cash_cow / utility 类
- **案例**：工行、中石油、长江电力、中国神华、招行（间接）

## 9. `regulated_heavily`（强监管行业）

- **含义**：行业受到价格管制 / 资本管制 / 准入审批 / 产品审批等强监管
- **触发条件**：(a) 收费标准受政府核定；(b) 业务开展需牌照且牌照稀缺；(c) 行业 GP 政策直接影响盈利能力
- **评分影响**：
  - moat：监管壁垒可贡献 +1 ~ +2
  - risk：政策风险 -1 ~ -2
  - **required_pct += 3**
- **案例**：所有 banking / insurance / brokerage_assetmgmt / utility 默认带此 flag；教培（已立案）、互联网平台反垄断、医保集采下的 pharma_mature

## 10. `pcaob_risk`（PCAOB 审计风险）

- **含义**：中概股审计底稿无法被 PCAOB 检查的风险（HFCAA 法案）
- **触发条件**：(a) 中国境内运营 + 美国上市；(b) 审计师为中国大陆所；(c) 未完成 PCAOB 联合审计
- **评分影响**：
  - risk：-1 ~ -3
  - **required_pct += 5**
  - 触发软门控"AH/双重上市处理"
- **当前状态**：2022 PCAOB 中美审计监管协议达成后风险大幅缓解，但仍需保留 flag 以备政策反复
- **案例**：所有未在港双重主要上市的中概股（百济曾经、富途控股、知乎）

---

## 调用示例（写入 scorecard.json）

```jsonc
"company_classification": {
  "company_type": "real_estate",
  "modifier_flags": ["distressed", "a_h_dual_listed", "state_owned"],
  "rationale": "万科为综合性地产开发商，主营开发销售；2024-2026 进入财务困境（净负债飙升、销售腰斩、管理层动荡），A+H 双重上市，深圳地铁国资入主成为实际控制人"
}
```

对应 `required_pct` 计算：
```
base = 40 (real_estate)
adjustment = +10 (quality_score 4.0 < 6.0)
modifier_adjustment = +10 (distressed) + 0 (a_h_dual_listed) + 0 (state_owned) = +10
required_pct = 40 + 10 + 10 = 60%
```

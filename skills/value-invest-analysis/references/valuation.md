# 估值方法论参考（v2）

**版本**：v2.0 — 与 `V2_SPEC.md` 联动，扩展为 16 种估值方法 + 7 个行业子节
**核心原则**：估值是科学外衣下的艺术。**输出区间，不输出点估计**。多方法交叉验证，假设比模型更重要。

---

## 一、原则（保留 v1，强化"区间 + 交叉"）

1. **估值是科学外衣下的艺术**：数学只是把假设外推到结果的传送带；模型的精度永远不超过假设的可靠度。
2. **输出区间不输出点估计**：任何"目标价 = ¥X"都是伪精确。合格估值给 `[low, base, high]` 三档，并说明区间宽度的来源。
3. **多方法交叉验证**：≥ 2 种方法独立得出区间，取共识带；若方法间差异 > 30%，差异本身就是信息（用于定位最敏感假设）。
4. **公司原型先于估值方法**（v2 新增）：先判定 `company_type`（V2_SPEC §二 18 类），再调用对应的估值方法组合（本文件 §八）。错配方法 = 错配现金流口径 = 错配结论。
5. **假设比模型更重要**：DCF 的精确数学掩盖了 g/WACC/利润率 三个假设的脆弱；多方法 + 反向 DCF 检验是唯一防线。
6. **安全边际公式化**（v2 新增）：v1 的"伟大公司 20-30%、平庸 35-50%"模糊建议，替换为 V2_SPEC §六 的 `required_pct = base_by_type[company_type] + adjustment` 公式。

---

## 二、通用估值工具箱（v2 扩展为 16 种）

> v1 有 10 种通用方法，v2 新增 6 种行业专用方法（标 ✅）。所有 16 种方法都可能在某些公司类型中出现，但适配窗口不同——务必先看 §八 的 company_type 推荐组合再选方法。

| 方法 | 适用场景 | 关键假设 | 常见陷阱 | v2 新增 |
|---|---|---|---|---|
| **DCF-FCFF** 自由现金流折现 | 资本结构变动大、可比少的成熟企业；非金融、非未盈利、非控股集团 | WACC 稳定；FCFF = NOPAT - ΔWC - NetCapex 可预测；永续期 ROIC ≈ WACC（无超额回报） | 永续价值占比 > 70%；WACC 微调致估值剧变；忽略 SBC / 经营租赁还原 | — |
| **DCF-FCFE** 股权自由现金流折现 | 杠杆稳定的金融股（保险）、地产开发、稳定派息企业 | Ke 股权成本；FCFE = 净利润 - ΔBV（含资本注入）；分红 ≈ FCFE 时退化为 DDM | 银行用 FCFF 双重计税；分红 ≠ FCFE（留存可能毁灭价值） | — |
| **PE / PEG** | 盈利稳定的消费 / 科技成长股；增长 15-30%、利润率稳定 | EPS 质量高（非一次性）；PEG: PE/g ≈ 1 公允 | 周期顶部低 PE 陷阱（§八 8.6）；PEG 对低增长（< 10%）和高增长（> 30%）均失真；EPS 含 SBC 失真 | — |
| **PB** 市净率 | 重资产 / 金融 / 周期股 | 账面价值反映清算或重置价值；ROE 稳定 | 商誉占比高失真；轻资产（软件 / 品牌）完全失效；周期顶部 PB 低不代表便宜 | — |
| **PS** 市销率 | 未盈利成长股、SaaS、早期周期股 | 利润率终将回归行业均值；营收质量真实（非渠道压货） | 烧钱模式可能永远不盈利；GMV ≠ Revenue | — |
| **EV / EBITDA** | 跨资本结构对比、重资产并购视角、消除税率差异 | 折旧 ≈ 维护性 Capex（关键）；EBITDA 反映经营现金流 | 忽略真实 Capex（电信 / 航空 / 半导体陷阱）；杠杆收购包装利器 | — |
| **DDM 股息折现** | 银行 / 保险 / 公用事业 / REIT / 高股息周期股（v2 升级为多类首选） | 派息率稳定；Ke > g；股利政策可持续 | 一次性高分红误判；g 接近 Ke 时永续项爆炸；不分红时退化失效 | — |
| **清算价值** | 困境股、破净周期股、地产困境、烟蒂股辅助 | 资产可变现性；负债真实性（含表外） | 表外负债、存货跌价、商誉归零；变现折扣不足 | — |
| **SOTP 分部加总** | 多元化集团、控股公司、含金融牌照的产业集团 | 分部独立可估；协同 / 控股折价合理（10-25%） | 控股折价被忽略；分部数据披露不全；浮存金成本调整错位 | — |
| **隐含增长率反推 (Reverse-DCF)** | 检验市场预期是否合理；任何已上市公司 | 反推 g 与历史 / 行业对照；用于"市场错在哪" | 不能作为定价依据；输入 WACC 决定输出 g | — |
| **rNPV 风险调整 NPV** | Biotech 管线估值；未盈利创新药每条管线独立 | 各阶段 PoS（成功概率）× peak sales × 专利剩余年限；折现率 12-15% | 单点估计；PoS 过乐观（行业均值参考 §八 8.3）；peak sales 锚定难 | ✅ |
| **正常化 PE (Normalized PE)** | 周期股；用 10 年均盈利或穿周期 EPS | 10 年涵盖一个完整周期；正常化 EPS = avg(过去 10 年 EPS) 或 mid-cycle EPS | 周期延长（如煤炭超级周期）导致正常化失真；新业务无 10 年数据 | ✅ |
| **PB-ROE** | 银行 / 重资产；戈登模型变形 | ROE 稳定且 > Ke；股利政策稳定 | 周期顶部 ROE 失真（息差顶 / 不良前夜）；ROE 中含一次性收益 | ✅ |
| **RIM 残差收益模型** | 银行 / 重资产；账面 + 超额收益现值 | V = B₀ + Σ(ROE_t - Ke) × B_{t-1} / (1+Ke)^t；预测期 ROE / 永续 ROE 假设 | 永续 ROE 假设极其敏感；2-3 阶段预测期更稳健 | ✅ |
| **NAV 重估** | 地产 / 控股集团 / REIT | 资产 mark-to-market 减负债；土地 / 持仓 / 经营物业用 cap rate | 土地估值时点性（牛熊差异 ±30%）；持仓估值波动；隐藏负债 | ✅ |
| **NCAV 净流动资产价值** | 烟蒂股；格雷厄姆经典 | 流动资产 - 总负债 < 0.67 × 市值即买入；商业模式终结的安全垫 | 流动资产含存货跌价 / 应收坏账；LIFO 储备等隐藏价值未识别 | ✅ |
| **重置成本** | 周期股 / 公用事业 / 重资产 | 重建该资产组合的成本（土地 + 设备 + 流动资本） | 技术折旧（化工产能淘汰）；区位差异（旧厂 vs 新厂）；环保成本上升 | ✅ |
| **实物期权 (Real Options)** | Biotech 管线 / 困境反转 / 资源勘探 | Black-Scholes 或二叉树；波动率 σ、行权价、剩余期限 | 波动率假设主观；不适合分红型资产；模型复杂度掩盖假设脆弱 | ✅ |
| **FFO / AFFO multiple** | REIT；GAAP 净利润被折旧严重扭曲 | FFO = 净利润 + 折旧 - 资产出售收益；AFFO = FFO - 维护性 Capex；倍数与利率联动 | 维护性 Capex 估计不准；高分红包装；杠杆 REIT 倍数低不代表便宜 | ✅ |

> 注：表中 19 行实际方法 = 10 v1 + 6 v2 新增 + 3 v1 已存在但 v2 强化（DDM / SOTP / 隐含增长反推）。"工具箱 16 种"指核心方法，FFO 与 AFFO 合并算 1 种估值技术。

---

## 三、多方法交叉验证（v2 修订：允许"独一档"跳过区间）

### 3.1 选方法（按 company_type）

参见 §八 各行业子节。常规要求：≥ 2 种主方法 + ≥ 1 种校验方法（如反向 DCF）。

### 3.2 取区间规则（v2 升级）

| 情景 | 规则 |
|---|---|
| **常规公司**（多数 type） | 取 ≥ 2 种方法的 25-75 分位作为 consensus_range |
| **独一档公司**（如 BRK.B、茅台早期阶段） | SOTP / DCF 作主方法 + 其他方法作参考，允许单一区间但必须给敏感性 |
| **未盈利公司**（biotech_unprofitable / 早期 high_growth） | rNPV 或实物期权 + EV/Sales 做对照，情景概率加权（牛 / 中 / 熊 × P_i） |
| **周期股**（cyclical_commodity） | 正常化 PE + PB 周期分位 + 重置成本，三种方法交叉，禁用单年 PE |
| **困境反转 / 烟蒂股** | 清算价值 + NCAV + 反转后 DCF（情景概率加权） |

### 3.3 一致性检查

若方法间差异 > 30%，定位分歧来源：
- **增长率假设**？（DCF 高、PE 低 → DCF 隐含 g 是否激进）
- **利润率假设**？（DCF 与 EV/Sales 差异 → 利润率回归水平不一致）
- **折现率/资本成本**？（DDM 与 DCF 差异 → Ke vs WACC 视角）
- **资产端 vs 盈利端**？（NAV 与 PE 差异 → 地产、控股集团常见）

差异本身就是信息：**差异大 → 公司估值高度依赖某个不确定假设 → 安全边际要求更高**（V2_SPEC §六 quality_score 调整项隐含此逻辑）。

---

## 四、假设审查清单（v2 修订：加行业例外）

### 4.1 通用 DCF 必查项（保留 v1）

- [ ] **永续增长率 g** ≤ 长期名义 GDP（中国 3-4% / 美国 2-2.5% / 香港 3%）
- [ ] **g < WACC - 2pct**（否则永续价值爆炸）
- [ ] **WACC 合理带**：A 股 8-12% / 美股 7-10% / 新兴市场 + 1-2pct 风险溢价
- [ ] **预测期 EBIT 利润率** 不超历史峰值 + 2pct，需说明扩张逻辑
- [ ] **ROIC > WACC** 才有增长价值，否则增长毁灭价值
- [ ] **PEG 适用区**：增长 15-30%、利润率稳定；周期股 / 微利股禁用
- [ ] **PB 失效场景**：轻资产（软件 / 医药 / 品牌消费） → 改用 PS 或 EV/Sales
- [ ] **一次性损益、SBC、经营租赁** 必须还原
- [ ] **红旗**：预测期现金流 > 历史峰值 × 1.5、永续期 Capex < 折旧

### 4.2 行业特定假设例外（v2 新增）

| company_type | 例外规则 | 来源案例 |
|---|---|---|
| `banking` | **g_terminal ≤ 名义 GDP × 1.1**（不是 ≤ GDP）——息差长期跟随名义增长率；Ke 用 CAPM；不用 WACC | 招行 V1 报告应用 DDM/PB-ROE |
| `biotech_unprofitable` | 永续期不适用，全部用阶段折现；折现率 12-15%（venture rate）；rNPV 每条管线独立 | 百济 6160.HK 必须用此框架 |
| `cyclical_commodity` | **g_terminal 可为负**（结构性衰退如煤炭、传统石油）——v1 假设 g ≤ GDP 在神华案例被破坏；正常化 EPS 必填 10 年均值 | 神华 ≈ 长期 g 为负但仍优质资产 |
| `holding_conglomerate` | g 应分段（保险 / 投资组合 / 子公司各自 g）；不存在统一 WACC；集团折价 10-25% 必填 | BRK.B 必须 SOTP，禁用单一 PE |
| `utility_infrastructure_reit` | g 锚定监管允许的 rate base growth（通常 2-5%）；用 DDM/AFFO，禁用 GAAP PE | 领展 / National Grid |
| `real_estate` | 困境状态下 NAV 加 30-50% haircut；预售款 / 合约负债不计入营收口径 | 万科 V1 报告 |
| `insurance` | EV = 调整净资产 + 有效业务价值；NBV multiple 替代 PE；偿付能力充足率作为软门控 | 平安 / 中国人寿 |

---

## 五、WACC 拆解 + 行业适配（v2 修订）

### 5.1 通用 WACC 公式（保留 v1）

```
WACC = Ke × (E / V) + Kd × (1 - t) × (D / V)
Ke = Rf + β × ERP
```

- **Rf**：A 股取 10Y 国债 2.5-3%；港股 10Y 美债 + 港币溢价；美股 10Y 美债
- **ERP（股权风险溢价）**：A 股 5-6%（散户化波动） / 港股 6-7%（流动性折价） / 美股 4.5-5.5%
- **β**：5 年月度回归对沪深 300 / 恒生 / S&P 500，剔除杠杆做对比

### 5.2 行业特定折现率（v2 新增）

| company_type | 折现率口径 | 取值 / 公式 | 说明 |
|---|---|---|---|
| `banking` | **Ke（股权成本）** | CAPM：Rf + β × ERP，无独立债务概念 | 银行负债 = 客户存款，不是融资 |
| `insurance` | Ke（股权成本） | 同上，但 β 通常 0.8-1.2 | 寿险贴现率含投资回报率假设 |
| `biotech_unprofitable` | **VC 风险折现率 12-15%** | 不用 WACC；早期管线 15%，Phase III 12% | 无负债 + SBC 占大头，CAPM 不适用 |
| `holding_conglomerate` | **分部各自 WACC** | 保险用 Ke / 子公司用 WACC / 投资组合用 long-term equity return | 不存在统一 WACC |
| `utility_infrastructure_reit` | 监管允许回报率反推 + Ke 平均 | 美国电力 9-10% / 中国电网 6-8% / REIT 6-8% | 监管模型决定上限 |
| `cyclical_commodity` | WACC（但 β 用穿周期均值） | β 取 1.2-1.5（高） + Rf + ERP | 单一时点 β 失真 |
| `real_estate` | WACC，但负债真实成本（隐性融资） | 加 1-2pct 风险溢价反映杠杆 | 三道红线后融资成本上行 |

---

## 六、安全边际框架（v2：用 V2_SPEC §六 公式替代）

### 6.1 公式化要求（必须）

直接引用 **V2_SPEC §六** 的 `required_pct = base_by_type[company_type] + adjustment` 公式：

```python
base_by_type = {
  "great_company_compounder":   25,
  "tech_platform_network":      30,
  "consumer_brand_premium":     25,
  "tech_hardware_ecosystem":    25,
  "high_growth_platform":       40,
  "biotech_unprofitable":       50,
  "pharma_mature":              30,
  "banking":                    25,
  "insurance":                  25,
  "brokerage_assetmgmt":        35,
  "utility_infrastructure_reit": 20,
  "cyclical_commodity":         35,
  "cyclical_industrial_ev":     35,
  "real_estate":                40,
  "holding_conglomerate":       20,
  "distressed_turnaround":      50,
  "declining_cash_cow":         40,
  "cigarbutt_deep_value":       50,
}

# 质量分调整
if quality_score >= 8.0:    adjustment = -5
elif quality_score < 6.0:   adjustment = +10
else:                       adjustment = 0

# modifier_flags 调整
if "distressed" in modifier_flags:         adjustment += 10
if "vie_structure" in modifier_flags:      adjustment += 5
if "pcaob_risk" in modifier_flags:         adjustment += 5
if "regulated_heavily" in modifier_flags:  adjustment += 3

required_pct = base_by_type[company_type] + adjustment
```

### 6.2 v1 描述性参考（仅作直觉对照）

| 公司类型 | 描述性安全边际（仅参考） | 来源 |
|---|---|---|
| 伟大公司（高 ROIC + 护城河 + 高确定性） | 20-30% | 以定性确定性为主 |
| 平庸公司 | 35-50% | 定量折扣为主 |
| 周期股 | 正常化盈利 × 低位 PE，再打 30% | 周期位置判断 |
| 困境反转 | 50%+，或破净 0.6 × PB 以下 | 资产保护 + 催化剂 |
| 高成长未盈利 | 不用安全边际，用情景概率加权 | 期权式定价（牛/中/熊三档 × 概率） |

**注意**：v1 表只作直觉对照，**实际取值必须用 §6.1 公式**，且 scorecard.json `margin_of_safety.required_pct_breakdown` 必须显式给出 `{base, adjustment, modifier_adjustment}` 三项。

---

## 七、反估值陷阱清单（保留 v1 + v2 量化判定）

### 7.1 价值陷阱 6 信号（v2 量化化）

| # | 信号 | 量化阈值 |
|---|---|---|
| 1 | PB / PE 持续低于行业 + ROE 同期下滑 | PB 或 PE ≥ 3 年位于行业 20 分位下，且 ROE 同期下滑 ≥ 3pct |
| 2 | FCF 与净利润背离 | 背离 ≥ 2 年，背离幅度（\|FCF - NI\|/NI）> 30% |
| 3 | 行业容量持续过剩 | CR5 上行（集中度提高）+ 行业整体 ROIC < WACC ≥ 2 年 |
| 4 | 大股东减持 + 分红率骤降 | 大股东减持 ≥ 1% 流通股 + 分红率（payout ratio）下滑 > 50% |
| 5 | 表观便宜来自一次性收益 | 当期 EPS 中一次性收益（资产出售 / 政府补贴 / 投资收益）≥ 30% |
| 6 | 行业结构性恶化 | 人口拐点 / 技术替代（如传统媒体 / 教培监管 / 燃油车）/ 监管归零 |

### 7.2 v2 强制规则

**触发 ≥ 5 信号 → 强制 PASS**（参见 V2_SPEC §五 一票否决），且在 scorecard.json 的 `veto_check.value_trap_signals_triggered` 字段记录命中数。

### 7.3 增长陷阱信号（保留 v1）

- DCF 永续期价值占比 > 75%
- 隐含增长率反推后，需要 > 20% 维持 10 年+
- TAM 假设占现有市场 100% 以上
- 估值倍数处于历史 90 分位 + 行业 β > 1.5
- 利润率假设超过全行业最优秀公司

### 7.4 双重检验

- 对**疑似价值股**：反推"市场预期了什么坏情况"，若市场预期已极悲观且基本面未恶化 → 真便宜
- 对**疑似成长股**：反推"需要多好才能撑起估值"，若超越历史最佳 → 陷阱

---

## 八、行业特定估值（v2 核心新增，按 company_type）

> 以下 7 个行业子节与各自的 `templates/schema_extensions/*.json` 中 `valuation_methods_priority` 字段**完全一致**（primary / secondary / avoid 三层）。报告中 §六（估值）必须按本节模板选 ≥ 2 主方法。

---

### 8.1 banking 商业银行

**Schema 引用**：`banking.json` → `valuation_methods_priority`

- **primary**：`DDM`、`PB-ROE`、`FCFE`、`RIM`
- **secondary**：`P/PPOP`（拨备前利润倍数）、`EV/AUM`（对应零售 / 财富业务）
- **avoid**：`DCF-FCFF`（银行无独立 Capex / 营运资本概念）、`EV/EBITDA`（EBITDA 对负债经营银行无意义）

**公式细节**：

```
DDM:    V = D1 / (Ke - g)
        其中 D1 = EPS × payout_ratio；Ke 用 CAPM
        
PB-ROE: V/B = (ROE - g) / (Ke - g)          (戈登模型变形)
        即可持续 ROE 决定合理 PB
        
RIM:    V = B0 + Σ_{t=1..T} (ROE_t - Ke) × B_{t-1} / (1+Ke)^t + 终值
        T = 5-10 年预测期 + 永续阶段
        
FCFE:   V = Σ FCFE_t / (1+Ke)^t
        FCFE 银行 ≈ 净利润 - ΔBV（受资本充足率约束）
```

**关键假设**：
- 长期 ROE（可持续值，不是周期顶部）—— 招行 V1 取 16-17%
- 派息率 payout（招行 32% / 工行 30% / 美国大行 40-60%）
- Ke = Rf + β × ERP（β 通常 0.8-1.0）
- g_terminal ≤ 名义 GDP × 1.1（见 §4.2）

**禁用理由**：
- DCF-FCFF：银行的"现金流"在客户存款里循环，FCFF 口径混乱
- EBITDA：银行的核心成本（利息支出）被剔除后毫无意义

**v1 应用样本**：招行 600036.SH（V1 报告应用 DDM + PB-ROE，V2 须加 RIM）。

---

### 8.2 insurance 保险

**Schema 引用**：`insurance.json` → `valuation_methods_priority`

- **primary**：`DDM`、`EV+NBV multiple`（内含价值 + 新业务价值倍数法）、`PB-ROE`
- **secondary**：`P/EV` 历史分位、`PE on operating earnings`（财险）
- **avoid**：`DCF-FCFF`（准备金计提扰动 FCFF）、`EV/EBITDA`（无意义）

**公式细节**：

```
EV 内含价值 = 调整后净资产 (ANW) + 有效业务价值 (VIF)
V_寿险      = EV + NBV × multiple
              其中 multiple = 10-25×（取决于 NBV 增长 / ROEV / 久期）

P/EV multiple = 当前价 / 每股 EV  → 与历史 5 年分位比
P/PPOP        = 财险拨备前利润倍数

PB-ROE 用法同银行
```

**关键假设**：
- 长期投资回报率（中国 5% / 美国 4-5%）
- 死差 / 费差 / 利差三差源拆解
- 偿付能力充足率（≥ 100% 为软门控）
- 准备金贴现率假设（10Y 国债 + 综合溢价）

**注意点**：
- 寿险三差源（死差 + 费差 + 利差）必须拆解，利差占比 > 60% 时利率敏感性高
- 财险用承保利润 + 投资收益拆分 PE，综合成本率 < 100% 是基础门槛

**v2 推荐样本**：平安 / 中国人寿 / MetLife。

---

### 8.3 biotech_unprofitable 未盈利创新药

**Schema 引用**：`biotech_unprofitable.json` → `valuation_methods_priority`

- **primary**：`rNPV`（每条管线独立 risk-adjusted NPV）、`EV/Sales`、`EV/peak sales`、`real options`
- **secondary**：管线 SOTP（按阶段折价后加总）、可比交易倍数（last licensing deal）
- **avoid**：`DCF-FCFF`（需 20+ 年外推不稳健）、`PE`、`PEG`、`EV/EBITDA`（无 E）

**rNPV 公式**：

```
rNPV_per_asset = Σ over phases:
                 PoS_phase × NPV_post_approval - cost_phase / (1+r)^t

NPV_post_approval = Σ_{t=launch..patent_expiry}
                    peak_sales × adoption_curve(t) × margin × tax_factor / (1+r)^t

公司总估值 V = Σ rNPV_per_asset - 公司层级费用现值 + 现金
```

**典型 PoS 参数**（行业均值，FDA / NDA 数据库）：
- **Preclinical → Phase I**：5-10%
- **Phase I → Phase II**：10-15%
- **Phase II → Phase III**：30-50%
- **Phase III → NDA/BLA**：60-70%
- **NDA/BLA → approval**：85-90%

**折现率**：12-15%（venture capital rate，不是 WACC）

**关键假设**：
- peak sales 锚定（参考已上市同适应症药物或 last licensing deal）
- 上市曲线（adoption curve，通常 5-7 年 ramp 至 peak）
- 专利剩余年限（核心专利 + 数据保护期）
- cash runway months（schema_extensions/biotech_unprofitable.json 已定义）

**实物期权法**：用于早期管线（Phase I 之前），将管线视为 call option，σ 取 60-100%，T = 剩余开发时间。

**v2 推荐样本**：百济神州 6160.HK（V1 PASS 4.80 → V2 用 rNPV + 实物期权重估）、Moderna、再鼎医药。

---

### 8.4 real_estate 地产

**Schema 引用**：`real_estate.json` → `valuation_methods_priority`

- **primary**：`NAV (Net Asset Value 重估)`、`清算价值`、`SOTP (开发业务 + 持有物业)`
- **secondary**：`PB 历史分位`、`DCF`（仅限龙湖等稳定经营性物业占比高的）、`股息率 + 持有物业重估`
- **avoid**：单一 PE（已售未结导致严重滞后）、`EV/EBITDA`（不能反映土储重估价值）

**NAV 公式**：

```
NAV = 已售未结锁定毛利（按完工进度确认）
    + 土储 mark-to-market (按当地市场可比地价 × 容积率 × 利润率)
    + 经营性物业 cap rate × 租金 (cap rate 一般 4-6%)
    + 投资性物业公允价
    - 净负债 (有息负债 - 现金 - 受限货币资金)
    - 少数股东权益按比例
    
每股 NAV = NAV / 总股本
合理价值 = NAV × (1 - haircut)
         haircut = 0%（健康）/ 30-50%（distressed）
```

**关键假设**：
- 土储重估法：当地住宅 / 商业楼面价；牛熊周期影响 ±30%
- 经营物业 cap rate：一线 4-5% / 二线 5-6% / 三四线 6-8%
- 困境状态（万科）：NAV 加 30-50% haircut；同时三道红线触发的资金链断裂概率
- 销售回款节奏（合约负债 → 营收转化）

**SOTP 应用**：
- 开发业务（项目储备）× PB 或 NAV × (1 - 30%)
- 持有物业（万象城 / 龙湖天街）× cap rate
- 物业管理（万物云 / 龙湖智创）× 独立 PE
- 长租公寓 / 商业地产 × EV/EBITDA

**v1 应用样本**：万科 000002.SZ（V1 PASS 4.30 → V2 NAV + 清算价值 + distressed haircut）、龙湖、华润置地。

---

### 8.5 holding_conglomerate 控股集团

**Schema 引用**：`holding_conglomerate.json` → `valuation_methods_priority`

- **primary**：`SOTP (Sum-of-the-parts)`（核心，几乎无替代）
- **secondary**：`PB-book_value (with float adjustment)`、`Look-through earnings`（公开股票按比例并表收益）
- **avoid**：`DCF-FCFF`、单一 `PE`、`EV/EBITDA`（整体现金流口径混乱）

**SOTP 结构**（以伯克希尔为模板）：

```
V_SOTP = 保险账面价值 + 浮存金 × (0.5 ~ 1.0×)
       + 上市股票持仓 × 公允价 × (1 - 折价 15-25%)
       + 完全控股子公司 × PE 或 EV/EBITDA × (1 - 集团折价 10-25%)
       + 现金与国债 × 1.0
       - 公司层级负债

合理价值 = V_SOTP × (1 - holdco_discount)
holdco_discount 通常 10-25%（伯克希尔 ≈ 10-15% / 一般控股 20-25%）
```

**浮存金乘数（float multiplier）**：
- 浮存金成本 < 0（承保盈利）：乘数 0.8-1.0
- 浮存金成本 0-2%：乘数 0.5-0.7
- 浮存金成本 > 3%：乘数 0.2-0.4 或视为负债

**关键假设**：
- 分部 g 应分段（保险 g_a / 投资组合 g_b / 实业子公司 g_c）
- 控股折价基于：信息不对称、资本配置自由度、税收效率
- Look-through earnings：被投资公司净利润 × 持股比例累加

**v2 推荐样本**：BRK.B、Markel、复星国际、长江实业。

---

### 8.6 cyclical_commodity 大宗商品周期股

**Schema 引用**：`cyclical_commodity.json` → `valuation_methods_priority`

- **primary**：`正常化 PE` (on normalized EPS)、`PB 周期分位法`、`重置成本法`、`DDM`（高分红周期股如神华）
- **secondary**：保守 DCF（用穿周期均价）、`EV/储量`
- **avoid**：单年 `PE`（顶部最低、底部最高，方向相反）、`PEG`、高点 `EV/EBITDA`

**正常化 PE 公式**：

```
Normalized EPS = avg(过去 10 年 EPS)                  最简单
              或 mid-cycle EPS = avg(volume) × avg(price) × avg(margin)   更稳健
              或 trough-to-peak smoothed EPS                            穿周期视角

合理价 = Normalized EPS × 周期中位 PE（通常 8-12×）
```

**PB 周期分位法**：
- 取过去 10-15 年 PB 历史分位
- PB < 25 分位 + ROE > 历史均值 → 周期底部可能性高
- PB > 75 分位 + ROE 处于历史峰 → 周期顶部警示

**重置成本法**：
- 现有产能 × 当地新建成本（含土地 + 设备 + 环保 + 运输）
- 注意技术折旧（老化工产能可能被淘汰）和区位差异

**关键警示**：
- **周期顶部低 PE 陷阱**：单年 EPS 在景气高点最高，PE 看上去最低
- **g_terminal 可为负**（如煤炭长期衰退、传统石油），见 §4.2 神华案例
- 长协占比高（如电力煤炭）→ 利润稳定性 + 估值贴近 utility

**v2 推荐样本**：神华 601088.SH、紫金矿业、中石化、Exxon、Freeport-McMoRan。

---

### 8.7 utility_infrastructure_reit 公用事业 / 基础设施 / REIT

**Schema 引用**：`utility_infrastructure_reit.json` → `valuation_methods_priority`

- **primary**：`DDM`（Dividend Discount Model）、`FFO multiple (P/FFO)`、`AFFO multiple`
- **secondary**：重置成本法、`Rate Base × allowed_return`（监管资产法）、`NAV (REIT)`
- **avoid**：`PE on GAAP earnings`（折旧扭曲）、`EV/EBITDA without considering rate base`

**关键公式**：

```
DDM:    V = D1 / (Ke - g)
        g 锚定监管允许的 rate base growth（通常 2-5%）
        
FFO   = 净利润 + 折旧 + 摊销 - 资产出售收益
AFFO  = FFO - 维护性 Capex - 直线租金调整
P/FFO multiple = 当前价 / 每股 FFO（参考行业 12-18×）
P/AFFO multiple = 当前价 / 每股 AFFO（参考 15-22×）

Rate Base 监管法：
合理价 = (Rate Base × allowed_return) / Ke × payout_factor
       Rate Base = 资产净值（监管核定）
       allowed_return = 监管允许 ROE（如美国 9-10%）
```

**关键假设**：
- 监管允许回报率（美国 FERC 9-10% / 中国电网 6-8% / 英国 Ofgem 5-7%）
- 派息率历史稳定性（REIT 法定 ≥ 90%）
- 维护性 Capex 占折旧的 % （AFFO 计算关键，通常 50-80%）
- 利率联动：长债利率 +100bp → REIT 估值 -10~15%

**v2 推荐样本**：领展 0823.HK、Realty Income、National Grid、长江基建。

---

### 8.8 distressed_turnaround / cigarbutt_deep_value（补充节）

**说明**：这两个 type 在首批 7 个 schema_extensions 中未独立创建，但估值方法明确：

- **distressed_turnaround**（如 Boeing）
  - **primary**：清算价值 + 反转后 DCF（情景概率加权 牛 40% / 中 40% / 熊 20%）+ 实物期权
  - **secondary**：PB 周期底 + EV/Sales 行业均值
  - 必加 50% 安全边际（V2_SPEC §六 base = 50）

- **cigarbutt_deep_value**（NCAV 候选）
  - **primary**：NCAV + 清算价值
  - NCAV 公式：流动资产 - 总负债（注意 LIFO 储备等隐藏价值要还原）
  - 格雷厄姆经典：买入价 < 0.67 × NCAV
  - 必加 50% 安全边际

---

## 九、跨市场（A / H / US）估值差异处理（缩减版）

### 9.1 无风险利率

- A 股：10Y 国债（2.5-3%）
- 港股：10Y 美债 + 港币溢价 或 HIBOR
- 美股：10Y 美债

### 9.2 估值水位惯例（参考中枢）

| 行业 | A 股 | 港股 | 美股 |
|---|---|---|---|
| 银行 | 5-7x PE | 4-6x PE | 10-14x PE |
| 消费龙头 | 25-35x PE | 18-25x PE | 20-30x PE |
| 互联网 | — | 15-25x PE | 25-40x PE |

### 9.3 A / H 折溢价

- 恒生 AH 溢价指数中枢 130-150（A 股相对 H 股溢价 30-50%）
- 估值时以 H 股为锚（机构定价更纯粹），A 股溢价归因于流动性 / 散户偏好
- 同公司 DCF 结果应一致，差异仅在市场情绪贴现

### 9.4 中概股 ADR / VIE

- VIE + 地缘风险，相比港股同标的折价 10-20%
- 双重上市（如 BABA / 9988）以港股流动性主导后趋同
- 跨市场比较统一以美元计价；**现金流币种与折现率币种必须匹配**

---

## 十、报告中估值章节的强制结构（v2 新增）

报告 §六（估值）必须满足以下硬性要求：

- [x] **方法选择**：按 `company_type` 选 ≥ 2 主方法（参考本文件 §八），并显式说明为什么选 / 不选某些方法
- [x] **区间输出**：必须给出 `ranges_by_method`，每方法的 `{low, base, high}` + `consensus_range`
- [x] **敏感性分析**：≥ 2 维 × 2 变量（如 g × WACC、margin × revenue growth）
- [x] **反向 DCF 检验**：用当前价反推隐含 g，对照历史 / 行业判断合理性
- [x] **安全边际**：显式标注 `required_pct`，从 V2_SPEC §六 公式取，给出 `{base, adjustment, modifier_adjustment}` 拆解
- [x] **禁止单一目标价**：所有"目标价 X 元"必须改为"价值区间 [L, H]，对应当前价折价 P%"

---

## 十一、与 `scripts/valuation-calc.py` 的衔接

`valuation-calc.py` 在 Stage 2 由 Agent G 扩展。本文件 §八 各方法应在脚本中有对应子命令：

| 估值方法 | 脚本子命令（计划） |
|---|---|
| DCF-FCFF | `dcf` |
| DCF-FCFE | `dcf-fcfe` |
| DDM | `ddm` |
| PB-ROE | `pb-roe` |
| RIM | `rim` |
| rNPV | `rnpv` |
| NAV | `nav` |
| SOTP | `sotp` |
| 正常化 PE | `normalized-pe` |
| NCAV | `ncav` |
| FFO/AFFO | `ffo-multiple` |
| 反向 DCF | `reverse-dcf` |
| 实物期权 | `real-option` |
| 重置成本 | `replacement-cost` |
| 清算价值 | `liquidation` |

> 命名以 Agent G 最终实现为准，本表为对接约定。

---

## 十二、辅助资源

- 计算辅助：`scripts/valuation-calc.py`（v2 扩展中）
- 同业对比数据：`templates/peer-comparison.md`
- 数据源：`data-sources.md`
- Schema 扩展：`templates/schema_extensions/{banking, insurance, biotech_unprofitable, real_estate, holding_conglomerate, cyclical_commodity, utility_infrastructure_reit}.json`
- 上游规约：`V2_SPEC.md`（真理源，本文件公式 / 阈值 / 安全边际均以其为准）

---

**版本注**：v2.0 — 2026-05-15。任何与 `V2_SPEC.md` 冲突的本文件内容，以 V2_SPEC 为准。

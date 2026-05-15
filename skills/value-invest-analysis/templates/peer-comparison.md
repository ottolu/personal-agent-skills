# {公司名} ({TICKER}) 同业对比 (v2)

**对比基准日期**：{YYYY-MM-DD}
**版本**：v2.0（适配 V2_SPEC §九 schema_extensions / 18 类 company_type）

> 本模板按 V2 规约改造，废除 v1"硬性 3-5 家"约束，引入 `incomparability_flag` 与 7 类子模板（generic + banking + biotech + holding_conglomerate + cyclical_commodity + real_estate + utility + unprofitable_growth_general）。

---

## v2 关键变化

- **新增 `incomparability_flag`**：处理 BRK.B / 单一龙头 / 全市场 first-in-class biotech 等"独一档"公司
- **按 `company_type` 选择适用子模板**：避免对 banking / biotech 硬套通用 PE / ROE / FCF CAGR
- **同业数量弹性**：不再硬性 3-5 家，允许 0-2 家 + 文字说明（独一档情境）
- **子模板指标行业相关**：banking 用 NIM / 不良 / 拨备 / 核充；biotech 用 cash_runway / R&D 强度 / EV-peak-sales 而非 PE / PEG / ROE
- **新增 §四 决策表**：明确 `incomparability_flag` 的触发条件（4 类）

---

## 0. 元信息

| 字段 | 值 | 说明 |
|---|---|---|
| `company_type` | <填 18 类枚举之一> | 参见 V2_SPEC §二 |
| `incomparability_flag` | `false` / `true` | 触发条件见 §四 |
| `incomparability_reason` | （独一档时填）| 1-2 句说明为什么独一档 |
| `adopted_subtemplate` | `generic` / `banking` / `biotech` / `holding` / `cyclical` / `real_estate` / `utility` / `unprofitable_growth` | 决定 §二 加载哪个分块 |
| `peer_count` | 整数 | 实际选取同业数（独一档可 < 3）|
| `peer_basis` | 同市场 / 全球 / 同模式 / 近似可比 | 同业池来源描述 |

**独一档示例**：
- BRK.B → `holding_conglomerate` + `incomparability_flag=true`，因规模 + 资本配置历史 + 投资组合属性独一档
- 茅台 → `great_company_compounder` + 全球类似复利机器作"近似可比"
- 百济神州 BTK 二代 → `biotech_unprofitable`，若主管线为 first-in-class 则 `incomparability_flag=true`

---

## 一、同业选取理由（按 company_type 自适应）

### 1.1 同业范围决策树

按 `company_type` 选择同业池来源：

| company_type | 同业池来源 | 备注 |
|---|---|---|
| `great_company_compounder` | 全球类似复利机器（不限市场） | 茅台 vs Diageo / Pernod；可口可乐 vs 百事 / Monster |
| `tech_platform_network` | 全球同模式平台（中美对照常见） | 腾讯 vs Meta / LINE；Visa vs Mastercard / Amex |
| `consumer_brand_premium` | 同档次品牌同品类 | LVMH vs Kering / Richemont / Hermes |
| `tech_hardware_ecosystem` | 同生态深度公司 | 苹果常 `incomparability_flag=true`，近似 Sony / Samsung |
| `high_growth_platform` | 同增长阶段同模式平台 | PDD vs Sea / Shopify / MELI |
| `biotech_unprofitable` | 同适应症 / 同治疗领域 / 同发展阶段（不限市场） | BTK 抑制剂 vs Imbruvica / Calquence |
| `pharma_mature` | 同治疗领域大药企 | 恒瑞 vs Roche / Merck oncology 业务 |
| `banking` | 同市场 + 同规模 + 同业务模式 | 避免"国有 vs 股份 vs 城商"混选 |
| `insurance` | 同保险类型（寿险 / 财险 / 综合）+ 同市场 | 平安 vs 国寿 / 太保（寿险板块） |
| `brokerage_assetmgmt` | 同业务结构（投行 / 经纪 / 资管比例） | 中信证券 vs 海通 / 国君 |
| `utility_infrastructure_reit` | 同监管区域 + 类似资产组合 | 领展 vs SPH REIT；National Grid vs Duke Energy |
| `cyclical_commodity` | 同商品（煤 / 油 / 铜 / 金）+ 同区位 | 神华 vs 中煤 / 兖矿；Exxon vs Chevron |
| `cyclical_industrial_ev` | 同产品组合 + 同区域市场 | 比亚迪 vs Tesla / Toyota（EV 业务） |
| `real_estate` | 同市场 + 国央企 vs 民营分组 | 万科 vs 保利 / 招商蛇口（国企组）/ 龙湖 vs 旭辉（民营组）|
| `holding_conglomerate` | "小伯克希尔" + Markel + Loews + Brookfield | BRK.B 通常独一档 |
| `distressed_turnaround` | 历史困境反转案例 + 同行业当前同行 | Boeing vs Airbus + GE 历史困境反转 |
| `declining_cash_cow` | 同衰退阶段行业内现金牛 | 烟草 BTI vs PM vs Altria |
| `cigarbutt_deep_value` | 同行业小盘 + PB 区间筛选 | NCAV / 净流动资产值 < 70% 的同行业小盘 |

### 1.2 同业数量

- **生效情况下**（`incomparability_flag=false`）：≥ 3 家，上限 5 家
- **独一档情况下**（`incomparability_flag=true`）：允许 1-2 家"近似可比"或 0 家 + 文字说明
- **超过 5 家不推荐**：会稀释焦点，应聚焦最具可比性的 top 5

### 1.3 同业列表

| 公司 | 代码 | 市场 | 业务相似度 | 选取理由 | 近似可比？ |
|---|---|---|---|---|---|
| {主体公司} | {TICKER} | {...} | — | — | — |
| 同业 1 | | | 高/中/低 | | 是/否 |
| 同业 2 | | | 高/中/低 | | 是/否 |
| 同业 3 | | | 高/中/低 | | 是/否 |
| 同业 4（可选）| | | | | |
| 同业 5（可选）| | | | | |

**跨市场补充说明**：
- 若涉及 PCAOB / VIE / 监管 / 流动性差异，需在此说明
- 若 A 股独占龙头，必须补全球 / 跨市场近似可比

---

## 二、对比维度（按 `adopted_subtemplate` 自适应）

> **使用规则**：根据 §0 元信息中的 `adopted_subtemplate` 仅填写对应一节，其余子模板留空或删除。

---

### 2.1 通用子模板（`generic`，适用大多数 company_type）

适用：great_company_compounder / tech_platform_network / consumer_brand_premium / tech_hardware_ecosystem / pharma_mature / declining_cash_cow / cigarbutt_deep_value

#### 2.1.1 规模与盈利

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 | 排序 |
|---|---|---|---|---|---|
| 市值（亿） | | | | | |
| 营业收入（亿） | | | | | |
| 净利润（亿） | | | | | |
| 毛利率 % | | | | | |
| 净利率 % | | | | | |
| ROE % | | | | | |
| ROIC % | | | | | |

#### 2.1.2 成长性（5 年）

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 营收 CAGR 5Y % | | | | |
| 净利润 CAGR 5Y % | | | | |
| FCF CAGR 5Y % | | | | |
| 毛利率变化趋势 | | | | |
| 市场份额变化 | | | | |

#### 2.1.3 财务健康

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 资产负债率 % | | | | |
| 有息负债 / 净资产 | | | | |
| 利息保障倍数 | | | | |
| OCF / 净利润 | | | | |
| 商誉 / 净资产 % | | | | |

#### 2.1.4 估值水位

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 | 行业中位 |
|---|---|---|---|---|---|
| PE TTM | | | | | |
| PE 5Y 历史分位 | | | | | |
| PB | | | | | |
| PS | | | | | |
| EV / EBITDA | | | | | |
| 股息率 % | | | | | |

#### 2.1.5 护城河与商业模式

| 维度 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 主要护城河类型 | | | | |
| 护城河宽度 | | | | |
| 护城河深度 | | | | |
| 商业模式可持续性 | | | | |
| 关键差异化 | | | | |

#### 2.1.6 管理层与治理

| 维度 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 主要股东结构 | | | | |
| 创始人 / 长期 CEO 在位 | | | | |
| 资本配置历史 | | | | |
| 分红 + 回购比率 | | | | |
| 红旗数量 | | | | |

---

### 2.2 banking 子模板（`banking`，v2 新增）

适用：`banking`。**禁用 PE/PB 单独作为估值锚**，需配合 ROE 看 PB-ROE 隐含资本成本。

#### 2.2.1 银行规模与定位

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 总资产（万亿） | | | | |
| 净资产（亿） | | | | |
| 贷款余额（万亿） | | | | |
| 存款余额（万亿） | | | | |
| AUM 资管规模（万亿） | | | | |
| 中收占比 % | | | | |
| 零售贷款占比 % | | | | |
| 活期存款占比 % | | | | |

#### 2.2.2 银行业绩与质量

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 净息差 NIM % | | | | |
| 净利差 % | | | | |
| 不良贷款率 % | | | | |
| 关注类贷款率 % | | | | |
| 拨备覆盖率 % | | | | |
| 拨贷比 % | | | | |
| 核心一级资本充足率 % | | | | |
| 资本充足率 % | | | | |
| 成本收入比 % | | | | |
| ROA % | | | | |
| ROE % | | | | |

#### 2.2.3 银行估值水位

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| PB | | | | |
| PE | | | | |
| 股息率 % | | | | |
| 隐含 ROE / 资本成本比 | | | | |
| PB / ROE | | | | |
| 5Y PB 历史分位 | | | | |

#### 2.2.4 银行护城河

| 维度 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 客户黏性（活期占比） | | | | |
| 跨业务能力（中收占比） | | | | |
| 风控质量（不良 / 拨备） | | | | |
| 监管牌照（业务广度） | | | | |
| 渠道护城河（网点 / APP MAU） | | | | |
| 财富管理 AUM 排名 | | | | |

---

### 2.3 biotech 子模板（`biotech`，v2 新增）

适用：`biotech_unprofitable`。**禁用 PE / PEG / ROE / FCF CAGR / 分红比率**（这些指标在未盈利创新药公司全部失效）。

#### 2.3.1 Biotech 规模与定位

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 市值（亿） | | | | |
| EV 企业价值（亿） | | | | |
| 已批准药物数量 | | | | |
| 平台技术 | | | | |
| 临床阶段管线数 | | | | |
| Phase 3 管线数 | | | | |
| Phase 1/2 管线数 | | | | |
| 治疗领域聚焦 | | | | |

#### 2.3.2 Biotech 关键管线对比（按适应症）

| 适应症 | 主体（药物 / 阶段） | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 例：BTK 抑制剂 | 泽布替尼（II line+，已批） | Imbruvica（1st gen，已批） | Calquence | — |
| 例：PD-1/PD-L1 | | | | |
| 例：CAR-T | | | | |
| 例：ADC | | | | |
| ... | | | | |

**说明**：管线对比应突出是否为 first-in-class / best-in-class、是否 head-to-head 试验、是否已获批 / 销售峰值预期。

#### 2.3.3 Biotech 财务（不用 PE/PEG/ROE）

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 营收 TTM（亿） | | | | |
| 营收增速 YoY % | | | | |
| 净亏损（亿） | | | | |
| 净亏损率 % | | | | |
| 现金 + 短期投资（亿） | | | | |
| 现金跑道 cash_runway（月） | | | | |
| R&D 费用（亿） | | | | |
| R&D 强度（% 营收 或 % 现金） | | | | |
| R&D 效率（peak_sales_per_RD_dollar） | | | | |
| SBC / 营收 % | | | | |
| 合作交易 BD 金额（首付 + 里程碑） | | | | |
| 合作交易数量（近 3 年） | | | | |

#### 2.3.4 Biotech 估值（rNPV / EV-peak-sales / EV-Sales）

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| EV / 当前销售 | | | | |
| EV / 峰值销售（共识） | | | | |
| rNPV per share（DCF 风险调整） | | | | |
| Sum-of-pipeline rNPV | | | | |
| Phase 3 资产数 × 平均 rNPV | | | | |
| 市值 / 已批药物销售 | | | | |

**说明**：估值核心是 **rNPV**（按试验成功率风险调整的净现值），其次是 EV / peak sales 横向对照。

---

### 2.4 holding_conglomerate 子模板（`holding`，v2 新增，独一档常见）

适用：`holding_conglomerate`。**BRK.B 等通常 `incomparability_flag=true`**，对比聚焦"业务组合相似度"而非"指标相似度"。

#### 2.4.1 控股组合的相似度

| 维度 | 主体（如 BRK.B） | 近似可比 1（如 Markel） | 近似可比 2（如 Brookfield） | 近似可比 3（如 Loews） |
|---|---|---|---|---|
| 保险业务占比 | | | | |
| 完全控股子公司占比 | | | | |
| 上市持仓占比 | | | | |
| 浮存金（float）规模 | | | | |
| 浮存金成本（< 0 / 0 / +） | | | | |
| 长期资本配置 IRR | | | | |
| 长期股东回报 CAGR（20Y） | | | | |
| vs 大盘超额收益 | | | | |
| CEO / 资本配置者特质 | | | | |
| 文化与组织结构 | | | | |

#### 2.4.2 估值与折价

| 指标 | 主体 | 近似可比 1 | 近似可比 2 |
|---|---|---|---|
| 当前 P / SOTP | | | |
| BV 增长 CAGR（5Y/10Y/20Y） | | | |
| 控股折价中枢 % | | | |
| 控股折价当前 % | | | |
| 控股折价历史分位 | | | |
| 长期股东回报 CAGR | | | |

**说明**：控股集团的"同业对比"不在于指标排名，而在于：
- 业务组合结构的相似性（保险/控股/持仓 三者比例）
- 资本配置者的长期 track record
- SOTP（分部估值）的折价水平历史比较

---

### 2.5 cyclical_commodity 子模板（`cyclical`，v2 新增）

适用：`cyclical_commodity`。**禁用单年 PE 比较**，必须看 10 年正常化指标 + 周期分位。

#### 2.5.1 周期股专属对比

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 资源储量寿命（年） | | | | |
| 长协占比 %（含量价机制） | | | | |
| 成本曲线分位（0=最低成本） | | | | |
| 单位成本（元/吨 或 $/桶） | | | | |
| 自有运输 / 物流资产 | | | | |
| 一体化程度（上下游延伸） | | | | |
| 现金 + 国债 / 市值 | | | | |
| 资产负债率 % | | | | |
| 10 年正常化 PE | | | | |
| 10 年正常化 ROE % | | | | |
| 当前 PB / 10 年 PB 分位 | | | | |
| 股息率（最近 5 年均） % | | | | |
| 商品价格 5 年分位 | | | | |
| 商品价格 vs 现金成本线安全垫 | | | | |

---

### 2.6 real_estate 子模板（`real_estate`，v2 新增）

适用：`real_estate`。**国企组 vs 民营组分开对比**（融资成本与生存概率差异巨大）。

#### 2.6.1 地产专属对比

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 土储面积（万㎡） | | | | |
| 土储货值（亿） | | | | |
| 一二线占比 % | | | | |
| 销售金额（亿） | | | | |
| 销售金额 YoY % | | | | |
| 净负债率 % | | | | |
| 三道红线状态（红/橙/黄/绿） | | | | |
| 现金短债比 | | | | |
| 经营性物业占比 % | | | | |
| 物业 / 长租 NOI（亿） | | | | |
| 平均融资成本 % | | | | |
| 央国企 / 民营标签 | | | | |
| PB | | | | |
| 隐含 NAV / 当前价 | | | | |
| 隐含 NAV 折价 % | | | | |

---

### 2.7 utility 子模板（`utility`，v2 新增）

适用：`utility_infrastructure_reit`。**核心是 DDM + AFFO 倍数**，PE 失效。

#### 2.7.1 公用事业 / REIT 专属

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 监管允许回报率 % | | | | |
| 监管资产基数 RAB（亿） | | | | |
| AFFO（亿） | | | | |
| P / AFFO 倍数 | | | | |
| 派息率 % AFFO | | | | |
| 派息覆盖倍数 | | | | |
| 资产基础年限（剩余寿命） | | | | |
| 5 年股息增长率 % | | | | |
| 股息率 % | | | | |
| 隐含 DDM 折现率 | | | | |
| 杠杆率（净债 / EBITDA） | | | | |

---

### 2.8 unprofitable_growth_general 子模板（`unprofitable_growth`，v2 新增）

适用：`high_growth_platform` 中尚未盈利的 / 早期 SaaS 等。**禁用 PE，重点看单位经济**。

#### 2.8.1 单位经济与增长质量

| 指标 | 主体 | 同业 1 | 同业 2 | 同业 3 |
|---|---|---|---|---|
| 营收 TTM（亿） | | | | |
| 营收增速 YoY % | | | | |
| 毛利率 % | | | | |
| LTV / CAC | | | | |
| CAC 回收期（月） | | | | |
| 净留存率 NRR % | | | | |
| 总留存率 GRR % | | | | |
| Rule of 40（增速 + EBIT 利润率） | | | | |
| 经营杠杆趋势（亏损率 YoY 变化） | | | | |
| 现金跑道（月） | | | | |
| SBC / 营收 % | | | | |
| EV / Sales | | | | |
| EV / Sales / 增速（PSG）| | | | |

---

## 三、综合结论

### 3.1 主体公司在同业中的相对位置（按 `adopted_subtemplate`）

| 维度 | 主体相对位置 | 备注 |
|---|---|---|
| 规模 | 第 {n} 位 / N | |
| 盈利能力或现金跑道 | 优于 / 接近 / 低于中位 | |
| 成长性或管线丰富度 | | |
| 财务健康或资本充足 | | |
| 估值水位 | | |
| 护城河 | | |

### 3.2 关键发现

1. **结构性优势**：（主体公司在同业中独特的优势）
2. **结构性劣势**：（弱项）
3. **同业中最值得对照的标的**：（指明一家"镜像同业"用于持续追踪）

### 3.3 同业对比对估值的影响

- 是否支持主体公司享受溢价 / 折价？
- 估值显著偏离同业（> 30%）的原因？是基本面差异 / 流动性 / 监管 / 还是错杀？
- 若 `incomparability_flag = true`：用"近似可比"趋势作为辅助判断，明确"独一档溢价"或"独一档折价"是否合理
- 同业均值回归方向：是主体下移 / 同业上移 / 还是各自维持？

### 3.4 对评分锚点的反向校验

- **business_quality 锚点**：同业对比是否支持当前打分？是否需要参考茅台 / 可口可乐 10 分锚点
- **moat 锚点**：与同业对比，护城河宽度更宽 / 类似 / 更窄
- **valuation_margin_of_safety 锚点**：相对同业是 ≥ 50% 折价（10 分）/ 20-40% 折价（7 分）/ 公允（5 分）/ 溢价（3 分）

---

## 四、`incomparability_flag` 触发条件（v2 决策表）

下列任一条件成立时，`incomparability_flag = true`：

| # | 触发条件 | 案例 |
|---|---|---|
| 1 | `company_type = holding_conglomerate` | BRK.B / Markel / Brookfield |
| 2 | 主体在同业中市值排名 > 同业第 2 × 5 倍（量级压制） | 茅台市值远超 5 朗珠 / 五粮液合计 ×5；苹果 vs Sony |
| 3 | biotech 主管线为 first-in-class，全市场无 head-to-head 同业 | 首个全球获批的某靶点药物 |
| 4 | 控股 50%+ 股份的实控人控制其他可比公司（关联输送嫌疑） | 同实控人控制的"可比公司"实际不可比 |
| 5 | 独占市场或牌照绝对排他（如全国仅 1 家） | 某些央企独家牌照 |
| 6 | 商业模式独创且尚无模仿者 | 早期阶段创新平台 |

**触发后允许**：
- 同业数量 < 3 家
- 用"近似可比"（业务部分相似的公司）替代严格同业
- 必须**明确说明**"独一档"的优势 / 劣势及对估值的含义
- 必须在 §3.3 给出"为什么市场愿意给 / 不给独一档溢价"的判断

**触发后禁止**：
- 直接报告"无同业可比，无法分析"——必须找到至少 1-2 家"业务部分相似"或"功能近似"的公司做对照
- 用"独一档"作为高估值的免责理由（仍需说明溢价合理性）

---

## 五、模板使用 Checklist

- [ ] §0 已填 `company_type` / `incomparability_flag` / `adopted_subtemplate`
- [ ] §1.3 同业数量符合规则（≥ 3 家，或 incomparability_flag 触发时 0-2 家 + 说明）
- [ ] §二 仅填写 `adopted_subtemplate` 对应的一节
- [ ] §二 子模板指标行业相关（biotech 不用 PE，banking 用 NIM 等）
- [ ] §三 给出主体在同业中的相对位置 + 3 条关键发现
- [ ] §3.4 反向校验评分锚点
- [ ] 若 `incomparability_flag=true`，§3.3 明确"独一档"对估值的含义
- [ ] §四 决策表至少匹配 1 条触发条件（若 flag=true）

---

**本模板与 V2_SPEC §九 schema_extensions 配套使用。同业指标可机器读取自 sector_extension.extension_data 字段。**

# Sector: 未盈利创新药 (`biotech_unprofitable`)

**典型公司**：
- A 股：无典型（A 股上市要求高，少数 18A 通道）
- 港股：百济神州 6160.HK、信达生物 1801.HK、君实生物、再鼎医药
- 美股：Moderna MRNA、BioNTech BNTX、Vertex VRTX（已盈利但仍研发驱动）、Beam BEAM、Arrowhead ARWR

**v2 schema_extension**：`biotech_unprofitable.json` （cash_runway_months / R&D efficiency / pipeline_phases / FDA_milestones / SBC_ratio / 合作交易）
**主流派路由**：能力圈"硬+软计数法"判定 → 多数普通投资者超出能力圈，归入 too-hard

## 一、公司原型识别信号

- 连续亏损（净利润为负），主营业务以 R&D 为核心
- 收入主要来自里程碑付款 / 授权 BD 收入 / 早期商业化品种
- 拥有 ≥ 3 条临床管线（Phase II / III 阶段）
- R&D 费用 / 营收 ≥ 50%
- 现金储备 ≥ 12 个月 burn rate
- 估值反映管线 NPV 而非当期 PE

## 二、商业模式六维适配

- **价值主张**：尚未兑现 —— 治愈或显著改善疾病的潜力
- **收入结构**：商业化品种 + License-out 里程碑 + 合作研发分成
- **成本结构**：R&D 是主体（临床试验 + 注册 + 管理）；SBC 占比通常高
- **客户结构**：医院 / 患者（已上市品种）+ 大药企（BD 合作）
- **再投资循环**：研发再投入 + 商业化建设；常年股权融资稀释
- **关键资源**：管线 / 科学家团队 / 临床数据 / 知识产权 / 制造能力

## 三、护城河重点

最适用：**专利 / 临床数据 / 监管壁垒**（但单个药物专利有时效）

锚点：
- 7 分：管线丰富 + 一两个 Best-in-class 或 First-in-class 药物（百济泽布替尼）
- 5 分：单一明星管线 + 跟随类似物
- 验证：(a) 临床数据头对头优于竞品；(b) FDA / NMPA 突破性疗法 / 优先审评；(c) 大药企并购或 BD 出价（市场定价信号）

## 四、核心财务指标（参考 schema_extension: biotech_unprofitable.json）

| 指标 | 优秀 | 警戒 |
|---|---|---|
| Cash Runway (months) | ≥ 36 | < 18 |
| Net Cash Burn Rate（季度） | 稳定或改善 | 加速恶化 |
| R&D 效率（NPV per dollar） | 难测但看里程碑达成率 | 多个管线连续失败 |
| Pipeline Diversity | ≥ 3 个 Phase II/III | 单一管线赌注 |
| SBC / Total Comp | ≤ 30% | > 50% |
| 已上市品种收入增长率 | ≥ 40%（早期）/ ≥ 20%（成熟期） | 低于行业 |
| BD 合作收入 | 有大额合作（Merck / Pfizer 等） | 无外部认可 |
| 主营毛利率（商业化品种） | ≥ 80% | < 60%（仿制 / 红海） |
| FDA 突破性 / 加速审批数量 | ≥ 1 | 0 |
| 股本稀释率（年） | ≤ 10% | > 20% |

## 五、红旗清单 N/A / 改读规则

- **N/A 项**：F1（营收增速）— 当前无意义；F4（毛利率）— 商业化前 N/A；F6（连续亏损）— 默认；F7（ROIC 低）— 默认；F10（杠杆）— 多数现金充足 / 股权融资；F15-17 经营周转类全 N/A；F22（存货周转）— N/A
- **改读项**：
  - F2（应收账款）：BD 里程碑回款延迟需追踪
  - F14（SBC）：≤ 30% 可接受；> 50% 严重稀释
  - F19（现金枯竭）：cash runway < 18 月为红色警报
- **新增类型专属红旗**：
  - BT1：核心管线 Phase III 失败（FDA Complete Response Letter）
  - BT2：主要科学家 / CEO 离任
  - BT3：股本年稀释 > 20%（融资能力存疑或市场预期低）
  - BT4：核心专利争议 / 仿制冲击（如 IPR 程序、专利悬崖）
  - BT5：大额负面诉讼 / 患者死亡事件
  - BT6：FDA / EMA / NMPA 监管警告（黑框警告）
  - BT7：核心管线被竞品 Best-in-class 超越（如 PD-1 后来 PD-L1 + ADC）

## 六、估值方法优先级

1. **rNPV（风险调整净现值）** — 主方法。逐管线给出成功概率（PoS）× 峰值销售 × 利润率 × 折现
2. **Sum-of-Parts** — 多管线分别 rNPV 后加总 + 现金减负债
3. **BD 交易可比** — 类似管线在 Phase II/III 的 license-out 价格
4. **Reverse DCF / Reverse rNPV** — 检验市场对管线成功率的隐含假设

关键假设：
- PoS 参考行业基准：Phase II → III 约 35%；Phase III → 上市约 60%；Pre-clinical → 上市约 5-10%
- WACC 取 10-12%（早期 biotech 风险溢价）
- 峰值销售估算需基于流行病学 + 价格 + 渗透率三因子

## 七、同业对比策略

- **同业范围**：全球（按治疗领域：肿瘤 BeiGene vs Genentech vs Innovent；mRNA Moderna vs BioNTech）
- **同业数量**：3-5 家可比
- **对比维度**：管线丰富度、cash runway、商业化进度、BD 合作历史、研发效率

## 八、关键风险与黑天鹅

1. 核心管线临床失败（Phase III CRL）
2. 监管延期 / 拒批
3. 现金耗尽被迫低价融资 / 卖身
4. 专利诉讼失败 / 仿制冲击
5. 关键科学家流失
6. 商业化进度严重慢于预期（销售团队 / 渠道问题）
7. 中概 biotech：FDA 对中国数据接受度（如 PD-1 出海受阻案例）
8. 行业政策（医保集采 / 灵魂砍价 / 美国 IRA）

## 九、required_pct 默认值

`base = 50%`（V2_SPEC §六，最高之一）

调整：
- 优秀 biotech（百济、信达）：50% - 5%（若 quality_score ≥ 8）= **45%**
- 含 VIE + PCAOB 中概：50% + 5 + 5 = **60%**

## 十、数据源补充

- 主要数据源 1：ClinicalTrials.gov（管线临床试验进度）
- 主要数据源 2：FDA / EMA / NMPA 官网（审评进度、突破性疗法认定）
- 主要数据源 3：年报 + 季报 + 临床数据 readout 公告
- 主要数据源 4：BiopharmaCatalyst / Endpoints News（行业事件追踪）
- 主要数据源 5：ASCO / ASH / ESMO 等大型学术会议数据披露

## 十一、典型案例参考

**百济神州 6160.HK / BGNE**：泽布替尼（百悦泽）Best-in-class BTK 抑制剂全球商业化，2024 销售突破 25 亿美元。多管线 + 美中港三地上市。previous V1 给出 PASS 4.80（财务质量 3 / 估值 3 / 风险 4），V2 应用 rNPV 后估值若仍贵则 PASS 合理。叠加 `[a_h_dual_listed, pcaob_risk]`。

**Moderna MRNA**：mRNA 平台技术，COVID 疫苗暴利后管线进入低谷。2024 出现现金消耗与商业化乏力并存。估值已严重缩水，但 rNPV 框架下 cancer mRNA 管线仍有故事。

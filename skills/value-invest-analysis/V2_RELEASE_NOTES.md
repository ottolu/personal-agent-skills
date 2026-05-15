# value-invest-analysis Skill V2 发版说明

**版本**：v2.0
**发布日期**：2026-05-15
**改造范围**：基于 9 位 reviewer × 10 份样本 × 98 条评审发现的完整重塑

---

## 一、V2 vs V1 一句话总结

> **V1 是单一工业制造导向的"打分系统"，V2 是先识别公司原型再调用对应行业框架的"识别+分析系统"。**

V1 的核心问题：
- 6 维加权 + ≥8.0 门槛**永远无法触发"重仓"**（5 家伟大公司全部锁死 7.2-8.1）
- company_type 无约束，10 份样本出现 10 种不同值
- 银行/Biotech/控股/周期/地产 全部不适配
- 评分锚点缺失，跨样本不可比
- 质量门控形同虚设
- 报告像"卖方研报作业"非"个人投资人 cheat sheet"

V2 的核心改进：
- **二维决策矩阵**替代单一加权门槛 → 伟大公司能进入合理评级
- **18 类 company_type 枚举** + 7 个 schema_extensions → 行业自动适配
- **dimension_anchors 内置 6 维评分锚点表** → 跨样本可比
- **硬+软门控分离** + data_freshness 警告顶部化 → 质量门控真起作用
- **5 分钟决策卡作 §0 强制章节** + 卖出三类触发结构化 → UX 革命

---

## 二、4 阶段改造成果

### 阶段 1：地基重塑（3 agents 并行）

| Agent | 产出 | 行数/字节 |
|---|---|---|
| A: schema 重构 | `SKILL.md` (330) + `scorecard.json` (11KB v2 schema) + `structured-data.json` (4KB) | — |
| B: sector 框架 | `references/sectors/` 18 个 sector 文件 + `_index.md` + `_modifiers.md` | 2537 行 |
| C: schema_extensions | `templates/schema_extensions/` 7 个 JSON + `_index.md` | 75KB |
| 真理源 | `V2_SPEC.md` | 393 行 |

### 阶段 2：模块改造（8 agents 并行）

| Agent | 文件 | 行数 | 关键交付 |
|---|---|---|---|
| D | `financial-analysis.md` | 605 | 7 行业子节 + 11 项 N/A 矩阵 |
| E | `red-flags-checklist.md` | 522 | 15×8 启用矩阵 + 47 行业新增红旗 |
| F | `valuation.md` | 581 | 16 种方法 + 8 行业子节 |
| G | `valuation-calc.py` | 943 | 12 子命令（v1 的 4 + v2 新增 8） |
| H | `cross-listing.md` (新建) | 421 | AH 决策树 + VIE 分级 + 双重上市分类 |
| I | `moat-business-model.md` | 612 | 11 型护城河 + 持久性否决 + 双轨评分 |
| J | `data-sources.md` | 497 | 130+ 行业专属源 |
| K | `peer-comparison.md` | 487 | 8 子模板（含 banking/biotech/holding） |

### 阶段 3：UX + 工具链（4 agents 并行）

| Agent | 文件 | 行数 | 关键交付 |
|---|---|---|---|
| L | `full-report.md` | 680 | §0 5 分钟决策卡 7 子节 + 卖出三类触发 |
| M | `risk-behavioral.md` | 549 | 能力圈硬+软计数法 + 反向证据三件套 + 8 偏差 |
| N | `parse-ticker.py` | 848 | COMPANY_MAP 192 条 + 37/37 测试通过 |
| O | `premortem.md` | 458 | 9 类外部冲击情景 + 10 行业专属子节 |

### 阶段 4：回归验证（3 agents 并行）

| 公司 | V1 结论 | V2 结论 | 关键改进 |
|---|---|---|---|
| **万科 A** | 4.30 PASS | quality **2.8** / val 5.0 / weighted 3.15 PASS | company_type 规范化、AH 决策树、NAV 主导估值、四重一票否决叠加 |
| **招商银行** | 7.475 Watchlist | quality 7.4 / val 6.0 / **watchlist_quality_only** | banking schema_extension 35+ 字段、DDM/PB-ROE/RIM 三方法、AH 按持有人决策 |
| **百济神州** | 4.80 PASS (**too-hard**) | quality 5.6 / val 4.0 / **PASS（非 too-hard）** | **核心修复**：能力圈不再一刀切，biotech 豁免 #3/#5 → 可继续分析；财务从 3 → 5；改用 rNPV 估值 |

---

## 三、目录结构对比

```
~/.claude/skills/value-invest-analysis/
├── V2_SPEC.md                          [v2 新增] 真理源
├── V2_RELEASE_NOTES.md                 [v2 新增] 本文件
├── SKILL.md                            [v2 重写] 330 行（含 18 类路由表）
├── references/
│   ├── methodology.md                  [v1 保留] 103 行
│   ├── market-cn.md / market-hk.md / market-us.md  [v1 保留]
│   ├── financial-analysis.md           [v2 重写] 605 行
│   ├── moat-business-model.md          [v2 重写] 612 行
│   ├── valuation.md                    [v2 重写] 581 行
│   ├── risk-behavioral.md              [v2 重写] 549 行
│   ├── red-flags-checklist.md          [v2 重写] 522 行
│   ├── data-sources.md                 [v2 重写] 497 行
│   ├── cross-listing.md                [v2 新增] 421 行
│   └── sectors/                        [v2 新增] 18 sector + index + modifiers
│       ├── _index.md / _modifiers.md
│       ├── sector-banking.md
│       ├── sector-biotech-unprofitable.md
│       ├── sector-real-estate.md
│       ├── sector-holding-conglomerate.md
│       ├── sector-cyclical-commodity.md
│       └── ...（共 18 个 sector 文件）
├── templates/
│   ├── full-report.md                  [v2 重写] 680 行
│   ├── scorecard.json                  [v2 重写] dimension_anchors + decision_matrix
│   ├── structured-data.json            [v2 重写] sector_extension + data_lineage
│   ├── peer-comparison.md              [v2 重写] 487 行 8 子模板
│   ├── premortem.md                    [v2 重写] 458 行 9 类情景
│   └── schema_extensions/              [v2 新增]
│       ├── _index.md
│       ├── banking.json
│       ├── biotech_unprofitable.json
│       ├── real_estate.json
│       ├── holding_conglomerate.json
│       ├── cyclical_commodity.json
│       ├── insurance.json
│       └── utility_infrastructure_reit.json
└── scripts/
    ├── parse-ticker.py                 [v2 扩展] 848 行 192 条映射
    └── valuation-calc.py               [v2 扩展] 943 行 12 子命令
```

**总规模**：~10500 行代码/规约 + 50+ 文件（V1 时 ~3000 行 + 17 文件）

---

## 四、V2 核心机制速查

### 4.1 决策矩阵（破除 V1 加权死锁）

```
quality_score = (生意 + 管理层 + 护城河 + 财务 + 风险) / 5
valuation_score = 估值/安全边际

quality_score ≥ 8.0 + valuation_score ≥ 7.0 → heavy_buy_candidate
quality_score ≥ 8.0 + valuation_score 5-7   → wishlist_quality_company
quality_score ≥ 8.0 + valuation_score < 5   → wishlist_overvalued
quality_score 6.5-8.0 + valuation_score ≥ 7 → watchlist_buildable
quality_score 6.5-8.0 + valuation_score < 7 → watchlist_quality_only
quality_score < 6.5                         → pass
```

### 4.2 一票否决（独立于矩阵）

- 任一 6 维 ≤ 3 → 强制 PASS
- 能力圈 too-hard → 强制 PASS
- 价值陷阱 6 信号 ≥ 5 项触发 → 强制 PASS
- data_freshness_ok = false → 强制降级 unverified_quick_look

### 4.3 required_pct 公式（V2 公式化）

```python
required_pct = base_by_type[company_type] + quality_adjustment + modifier_adjustment

base_by_type ∈ {15-50}
quality_adjustment ∈ {-5 (q≥8), 0, +10 (q<6)}
modifier_adjustment: distressed +10, vie_structure +5, pcaob_risk +5, regulated_heavily +3
```

### 4.4 能力圈硬+软计数法

```
硬条件（任一触发 → too-hard）:
  #1 无法 3 句解释商业模式
  #2 核心技术超出训练数据

软条件（≥ 2 项触发 → too-hard）:
  #3 5 年内 2 次技术颠覆
  #4 收入确认规则需会计师解释
  #5 单一未上市变量
  #6 24 个月内监管重大变化（方向不清）

行业适配:
  biotech_unprofitable: 不计 #3 / #5
  high_growth_platform: 不计 #6
  A 股政策敏感: #6 改读"方向是否清晰"
```

### 4.5 反向证据三件套（替代字数配额）

每条必须满足：
1. **具名出处**：机构名 + 报告标题 + 时间（**禁止"虚拟代表 X 风格"**）
2. **具体数字预测**：≥ 1 条量化预测
3. **概率重定标**：基于该看空逻辑重估失败概率

至少 3 条满足三件套。

---

## 五、关键回归验证发现

### 5.1 万科：价值陷阱识别更精准

V1 已正确 PASS，V2 进一步细化：
- company_type 从自创"distressed_cyclical_potential_value_trap"规范为 `real_estate` + 4 modifier_flags
- AH 决策树触发 `distressed flag → 观察名单`（不持任何一档）
- NAV 重估 + 三道红线 + 销售跟踪 作为 sector_extension 自动字段
- required_pct = 40+10+10+3 = 63%（V1 模糊"50%+"）
- 四重一票否决叠加：维度≤3 + too_hard + 价值陷阱 6/6 + data_freshness

### 5.2 招行：银行业框架真正落地

V1 评级正确但用通用工具临时手工补丁，V2 实现完整自动化：
- `banking.json` schema_extension 自动加载 NIM/不良/拨备/核充/CIR/AUM/中收占比 等 35+ 字段
- 9 项财务红旗自动 N/A，无需手工附录
- DDM/PB-ROE/RIM 三方法通过 `valuation-calc.py` 子命令可复现（脚本输出可贴）
- AH 决策树按持有人类型给出精确建议：mainland_long 选 A / oversea 选 H / 港股通选 A（30% 总税不划算）
- 评级从笼统"Watchlist 7.475"细化为 `watchlist_quality_only`（quality 7.4 / valuation 6.0）

### 5.3 百济：能力圈机制核心修复

**V2 最重要的修复案例**：
- V1：能力圈触发 5/6 项即归 too-hard → 强制 PASS
- V2：biotech 行业豁免 #3/#5 后 → 软条件仅触发 #4（1 项）< 2 → **不归 too-hard**
- 财务质量：V1 用通用 ROE/ROIC/FCF 全负打 3 分一票否决 → V2 通过 biotech.json N/A 6 项 + cash_runway/R&D/SBC 专属评分得 5 分
- 估值：V1 缺 rNPV → V2 通过 `valuation-calc.py rnpv` 子命令 + 多管线 PoS 加权
- 结果仍 PASS，但**路径完全不同**：从"一刀切能力圈"变为"具体可观测的财务+估值证据"

---

## 六、未完成 / 后续工作

### P1 backlog（V2.1 候选）
- WACC 拆解对银行/Biotech/控股退化处理细化
- AH 折溢价"市场情绪溢价 vs 流动性折价"分解
- A 股政策因子定量传导框架
- 6 维评分卡"情景调整"机制（牛市 / 熊市权重重定）
- `qualitative_adjustment` 字段合法化 + ±0.5 限制
- 渐进式披露路由表强制执行（AI 记录加载的 references）

### P2 backlog
- EPV 列入工具箱
- §七 8 项 checklist 补 SBC / 经营租赁还原
- 引导问题按 company_type 差异化
- 工具脚本输出国际化（中英双语）
- 模板视觉化（mermaid 流程图）

### 待补 schema_extensions（其他 11 类）
当前 7 类（banking/insurance/biotech/real_estate/holding/cyclical_commodity/utility）已实现。
其他 11 类（great_company_compounder / tech_platform_network / consumer_brand_premium / tech_hardware_ecosystem / high_growth_platform / pharma_mature / brokerage_assetmgmt / cyclical_industrial_ev / distressed_turnaround / declining_cash_cow / cigarbutt_deep_value）暂用 base schema，按需在 V2.x 补充。

---

## 七、致谢

V2 的诞生来自第一轮 review 的 9 位 reviewer（方法论/财务/护城河/估值/风险/跨市场/工程化/横向对比/UX）共 98 条发现，以及 10 份 V1 样本生成 agent 主动反馈的 38 条 GAP。

特别提及：
- 拼多多 agent 通过反推 g + 反向证据 + 预先尸检四件套形成"增长陷阱过滤器"
- 万科 agent 通过价值陷阱 6/6 信号 + 一票否决组合证实了 V1 的 PASS 兜底有效
- 伯克希尔 agent 主动报告 9 条 schema 不适配，成为 V2 schema_extension 机制的起点

---

## 八、版本历史

- **v1.0** (2026-05-15)：初版发布，单一工业制造导向框架
- **v2.0** (2026-05-15)：基于 review 全面重塑，18 类 company_type + 行业差异化 + 二维决策矩阵 + 5 分钟决策卡

后续版本应基于实战案例继续迭代，特别关注 V2 在以下场景的表现：
- 首次实战使用 V2 的 5 分钟决策卡是否真能在 5 分钟内决策
- 不同 modifier_flag 组合下 required_pct 公式是否合理
- 18 类 company_type 之外的边界情形（如：AI 软件公司、稳定币运营、量子计算）

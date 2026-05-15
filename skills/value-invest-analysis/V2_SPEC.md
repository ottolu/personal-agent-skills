# value-invest-analysis Skill V2 改造锁定规约

**版本**：v2.0-spec
**生效日期**：2026-05-15
**状态**：第二轮改进的真理源，所有 stage 1-4 agent 必须严格遵守

> 本文件由 SYNTHESIS.md 评审结论凝结而来，是 V1 → V2 改造的唯一规约。任何变动必须先修改本文件再修改实现，禁止agent 私自发明字段名 / 枚举值 / 公式。

---

## 一、核心设计原则（V2 的灵魂）

1. **公司原型识别先于分析框架** —— 先判定 company_type，再调用对应原型的分析逻辑
2. **评分锚点 + 决策矩阵 双轨** —— 评分由锚点参考表给出，决策由二维矩阵裁决（破除加权死锁）
3. **schema 严格约束 + 扩展机制公开** —— 禁止私自顶层字段，所有 sector-specific 走 schema_extensions
4. **行业差异化覆盖全栈** —— 红旗 / 财务指标 / 估值方法 / 数据源 / 同业 都按 company_type 自动适配
5. **质量门控可机器验证** —— 硬门控未通过强制降级输出，软门控可放行但显式标注
6. **UX 优先：5 分钟决策 + 15 分钟版** —— 报告先服务"个人投资者下单决策"，再服务"机构卖方研报"

---

## 二、18 类 company_type 枚举（锁定，禁止增减）

| # | enum 值 | 中文名 | 代表案例 |
|---|---|---|---|
| 1 | `great_company_compounder` | 伟大公司复利机器 | 茅台 / 可口可乐 |
| 2 | `tech_platform_network` | 科技平台/网络效应 | 腾讯 / Meta / Visa |
| 3 | `consumer_brand_premium` | 高端消费品牌 | LVMH / 雅诗兰黛 |
| 4 | `tech_hardware_ecosystem` | 硬件生态 | 苹果 |
| 5 | `high_growth_platform` | 高速增长平台/电商 | PDD / Sea / Shopify |
| 6 | `biotech_unprofitable` | 未盈利创新药 | 百济 / Moderna |
| 7 | `pharma_mature` | 成熟制药 | 恒瑞 / Pfizer |
| 8 | `banking` | 商业银行 | 招行 / JPM |
| 9 | `insurance` | 保险 | 平安 / MetLife |
| 10 | `brokerage_assetmgmt` | 券商/资管 | 中信证券 / BlackRock |
| 11 | `utility_infrastructure_reit` | 公用事业/基础设施/REIT | 领展 / National Grid |
| 12 | `cyclical_commodity` | 大宗商品周期股 | 神华 / Exxon / 紫金 |
| 13 | `cyclical_industrial_ev` | 新能源车/工业周期成长 | 比亚迪 / 特斯拉 |
| 14 | `real_estate` | 地产 | 万科 / 龙湖 |
| 15 | `holding_conglomerate` | 控股集团 | BRK.B / Markel |
| 16 | `distressed_turnaround` | 困境反转 | Boeing |
| 17 | `declining_cash_cow` | 衰退中现金牛 | 部分烟草 / 传统媒体 |
| 18 | `cigarbutt_deep_value` | 深度低估烟蒂股 | NCAV 候选 |

## 三、modifier_flags（可叠加，描述补充特性）

```yaml
modifier_flags:
  - with_policy_support      # 政策托底（国企/受补贴行业）
  - distressed               # 困境状态（万科）
  - a_h_dual_listed          # A+H 双重上市
  - vie_structure            # VIE 架构
  - adr_listed               # ADR 上市
  - dual_primary_listing     # 双重主要上市
  - creator_led              # 创始人主导
  - state_owned              # 国企背景
  - regulated_heavily        # 强监管行业
  - pcaob_risk               # PCAOB 审计风险
```

## 四、6 维评分锚点参考表（强制 schema 内置）

scorecard.json 必须内置以下 `dimension_anchors` 字段：

### 4.1 business_quality（生意质量，权重 20%）
| 分数 | 锚点描述 | 代表案例 |
|---|---|---|
| 0 | 明确造假 / 烂生意 / 即将归零 | 教培被监管归零 |
| 3 | 普通竞争激烈 / 无定价权 / 低质增长 | 普通家电制造、低端零售 |
| 5 | 平凡但稳定 / 有一定市场地位 | 中游制造业龙头 |
| 7 | 好生意有壁垒 / 长期回报合理 / 可预测现金流 | 苹果、比亚迪 |
| 10 | 极致复利机器（最高分） | 茅台 / 可口可乐 / Visa / Moody's |

### 4.2 management（管理层，权重 15%）
| 分数 | 锚点描述 | 代表案例 |
|---|---|---|
| 0 | 造假 / 关联输送 / 毁灭股东价值 | 已立案造假案 |
| 3 | 能力或诚信存疑 / 信息披露严重不足 | 拼多多治理透明度问题 |
| 5 | 平稳称职 / 中规中矩 | 多数国企平均水平 |
| 7 | 优秀资本配置者 / 长期主义 | 库克、马化腾 |
| 10 | 巴菲特级 | 巴菲特、芒格 |

### 4.3 moat（护城河，权重 20%）
| 分数 | 锚点描述 | 代表案例 |
|---|---|---|
| 0 | 无壁垒 / 红海竞争 | 部分中小制造业 |
| 3 | 有壁垒但持续收窄 / 单一来源 | 平庸消费品 |
| 5 | 稳定护城河 / 一种来源 | 中等品牌 |
| 7 | 宽护城河 / 多来源 | 苹果、招行 |
| 10 | 多重壁垒持续变宽 | 茅台（品牌+稀缺）、腾讯（网络+切换+生态）|

### 4.4 financial_quality（财务质量，权重 15%）
| 分数 | 锚点描述 | 代表案例 |
|---|---|---|
| 0 | 明显造假 / 即将崩溃 | 财务造假已暴露 |
| 3 | 持续疲软 / 多个红旗 / 一票否决预警 | 万科当前 / 百济未盈利 |
| 5 | 稳健 / 合规 / 无明显红旗 | 多数中规中矩公司 |
| 7 | 优秀质量 / FCF > 净利润 / 低负债 | 招行、比亚迪 |
| 10 | 堡垒级现金流（最高分） | 茅台、苹果、Visa |

### 4.5 valuation_margin_of_safety（估值/安全边际，权重 20%）
| 分数 | 锚点描述 |
|---|---|
| 0 | ≥ 2 倍内在价值（严重高估） |
| 3 | 10-30% 溢价（贵） |
| 5 | 公允价附近（±10%） |
| 7 | 20-40% 折价（便宜） |
| 10 | ≥ 50% 折价（深度低估） |

### 4.6 risk（风险，权重 10%）
| 分数 | 锚点描述 | 代表案例 |
|---|---|---|
| 0 | 已存在重大致命单点风险 | 监管立案、关键人物突逝、客户崩盘 |
| 3 | 多个重大风险并存 | 万科 = 2 / 拼多多 = 5 |
| 5 | 可控 | 多数公司 |
| 7 | 低风险 | 招行 |
| 10 | 反脆弱（黑天鹅有利或免疫） | 罕见 |

---

## 五、决策矩阵（破除加权死锁，替代单一 weighted_total ≥ 8.0）

### 5.1 计算

```
quality_score = (business_quality + management + moat + financial_quality + risk) / 5
valuation_score = valuation_margin_of_safety

# weighted_total 保留为参考（不作为决策基础）：
weighted_total = 0.20*business + 0.15*mgmt + 0.20*moat + 0.15*fin + 0.20*val + 0.10*risk
```

### 5.2 二维决策矩阵

| quality_score | valuation_score | 评级 | 含义 |
|---|---|---|---|
| ≥ 8.0 | ≥ 7.0 | `heavy_buy_candidate` | 重仓候选 |
| ≥ 8.0 | 5.0-7.0 | `wishlist_quality_company` | 心仪公司池（好公司，等价格） |
| ≥ 8.0 | < 5.0 | `wishlist_overvalued` | 心仪公司池（明显高估） |
| 6.5-8.0 | ≥ 7.0 | `watchlist_buildable` | 观察清单可分批建仓 |
| 6.5-8.0 | < 7.0 | `watchlist_quality_only` | 观察清单（仅质量过关） |
| < 6.5 | 任意 | `pass` | PASS |

### 5.3 一票否决（独立于矩阵）

- 任一 6 维 ≤ 3 → 强制 PASS（标记 `vetoed_dimensions`）
- 能力圈 too-hard → 强制 PASS
- 价值陷阱 6 信号 ≥ 5 项触发 → 强制 PASS
- 数据时效 data_freshness_ok = false + 用户未明确同意 → 输出降级为 `unverified_quick_look` 模式

---

## 六、required_pct_margin_of_safety 公式（取代 v1 的"伟大公司 20-30%"模糊建议）

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

# 调整项（基于质量分）
if quality_score >= 8.0:    adjustment = -5
elif quality_score < 6.0:   adjustment = +10
else:                       adjustment = 0

# 修饰符调整
if "distressed" in modifier_flags:         adjustment += 10
if "vie_structure" in modifier_flags:      adjustment += 5
if "pcaob_risk" in modifier_flags:         adjustment += 5
if "regulated_heavily" in modifier_flags:  adjustment += 3

required_pct = base_by_type[company_type] + adjustment
```

---

## 七、scorecard.json schema 强制结构（v2）

```jsonc
{
  "$schema": "value-invest-scorecard-v2",
  "meta": {
    "ticker": "string",
    "company_name_cn": "string",
    "company_name_en": "string",
    "report_date": "YYYY-MM-DD",
    "skill_version": "v2.0",
    "primary_school": "buffett | graham | duan | zhang | mixed",
    "skill_feedback": [/* 用于记录 skill 不适配点，仅作为元注释，不影响评分 */]
  },
  "company_classification": {
    "company_type": "<必须是 18 个枚举之一>",
    "modifier_flags": [/* 0 个或多个 modifier 字符串 */],
    "rationale": "判定理由 1-2 句"
  },
  "dimension_anchors": {
    /* 此处必须内置完整 6 维锚点表的副本（从本规约 §四 复制） */
  },
  "scorecard": {
    "business_quality":          {"score": 0-10, "evidence": [], "anchor_used": "X 分锚点描述"},
    "management":                {"score": 0-10, "evidence": [], "anchor_used": "..."},
    "moat":                      {"score": 0-10, "evidence": [], "anchor_used": "..."},
    "financial_quality":         {"score": 0-10, "evidence": [], "anchor_used": "..."},
    "valuation_margin_of_safety":{"score": 0-10, "evidence": [], "anchor_used": "..."},
    "risk":                      {"score": 0-10, "evidence": [], "anchor_used": "..."}
  },
  "computed": {
    "quality_score": 0.0,
    "valuation_score": 0.0,
    "weighted_total": 0.0
  },
  "veto_check": {
    "any_dimension_le_3": false,
    "vetoed_dimensions": [],
    "circle_of_competence_too_hard": false,
    "value_trap_signals_triggered": 0
  },
  "decision": {
    "rating": "heavy_buy_candidate | wishlist_quality_company | wishlist_overvalued | watchlist_buildable | watchlist_quality_only | pass",
    "rationale": "1-2 句话",
    "suggested_position_pct_range": [number, number]
  },
  "value_range": {
    "currency": "string",
    "ranges_by_method": [
      {"method": "DCF", "low": number, "base": number, "high": number},
      {"method": "PB-ROE", "low": number, "base": number, "high": number}
    ],
    "consensus_range": {"low": number, "high": number}
  },
  "margin_of_safety": {
    "required_pct": "由 §六 公式计算",
    "required_pct_breakdown": {"base": number, "adjustment": number, "modifier_adjustment": number},
    "actual_pct": number,
    "meets_requirement": boolean
  },
  "red_flags": {
    "red_count": int,
    "yellow_count": int,
    "green_count": int,
    "na_count": int,
    "na_reason": "依据 sector_extension 中规则",
    "critical_flags": []
  },
  "sector_extension": {
    "$ref": "templates/schema_extensions/{company_type}.json",
    /* 加载对应行业的扩展字段；若该 type 无 schema_extension 则为 null */
    "extension_data": {}
  },
  "tracking_metrics": {
    "business_logic": [],
    "financial": [],
    "valuation": [],
    "price_triggers": {
      "add_below": number,
      "trim_above": number,
      "exit_above": number
    }
  },
  "sell_triggers": {
    "logic_invalidation": [],
    "management_breach": [],
    "valuation_extreme": [],
    "opportunity_cost": []
  },
  "quality_gate": {
    "mode": "full | quick_look | unverified_quick_look",
    "hard_gates_passed": {/* 5 项硬门控 */},
    "soft_gates_passed": {/* 6 项软门控 */},
    "output_downgraded": boolean,
    "downgrade_reasons": []
  }
}
```

**硬门控**（5 项，未通过强制 `unverified_quick_look` 模式）：
1. `data_freshness_ok` —— 财报 ≤ 90 天 + 股价 ≤ 7 天
2. `sources_cited` —— 所有定量数据有 source + fetched_at
3. `circle_of_competence_declared` —— 显式声明能力圈
4. `no_deterministic_buy_sell` —— 不给确定性 Buy/Sell
5. `red_flag_checklist_done` —— 红旗清单逐项过审（含 N/A）

**软门控**（6 项，未通过显式标注但允许继续）：
- 反向证据三件套
- 预先尸检完成
- 6 维全部填写
- DCF 敏感性分析
- 同业对比有 ≥ 3 家（或 incomparability_flag）
- AH/双重上市处理（如适用）

---

## 八、structured-data.json 扩展机制

```jsonc
{
  "$schema": "value-invest-structured-data-v2",
  "meta": { /* 同 v1 */ },
  "company_classification": {/* 引用 scorecard 的分类 */},
  // ... v1 字段保留 ...
  "sector_extension": {
    "$ref": "templates/schema_extensions/{company_type}.json",
    "extension_data": {
      /* 按 company_type 加载对应字段集 */
    }
  },
  "data_lineage": [
    {
      "field": "annual_financials.revenue",
      "source": "EDGAR 10-K 2024",
      "url": "...",
      "fetched_at": "2026-05-15T10:00:00Z",
      "freshness_days": 120
    }
  ]
}
```

---

## 九、Schema Extensions 范围（v2 首批 7 个）

stage 1 必须创建以下 7 个 schema_extensions JSON 文件：

1. `banking.json` —— NIM / 不良率 / 拨备覆盖率 / 核充率 / RWA / 零售贷款占比 / AUM / 中收占比 / 资本充足率分级
2. `insurance.json` —— 综合成本率 / 内含价值 EV / NBV 新业务价值 / 投资收益率 / 准备金 / 偿付能力
3. `biotech_unprofitable.json` —— cash_runway_months / R&D efficiency / pipeline_phases / FDA_milestones / SBC_ratio / 合作交易
4. `real_estate.json` —— NAV / 土储 / 净负债率 / 合约负债 / 销售金额 / 现金短债比 / 三道红线
5. `holding_conglomerate.json` —— segment_data / sotp_valuation / float_value / investment_portfolio_nav / 控股折价
6. `cyclical_commodity.json` —— commodity_price_history / normalized_eps / pb_cycle_percentile / 长协占比 / 自有运输/采矿成本曲线
7. `utility_infrastructure_reit.json` —— DDM 参数 / regulated_return / 派息率历史 / 资产基础

其他 11 个类型先用 base schema，本 stage 不强制创建（stage 2 按需补）。

---

## 十、SKILL.md §2.3 路由表（v2 必须新增 company_type 列）

| company_type | 必加载 sector 文件 | 必加载 schema_extension |
|---|---|---|
| great_company_compounder | sector-great-company.md | 无（base） |
| tech_platform_network | sector-tech-platform.md | 无 |
| banking | sector-banking.md | banking.json |
| biotech_unprofitable | sector-biotech.md | biotech_unprofitable.json |
| real_estate | sector-real-estate.md | real_estate.json |
| holding_conglomerate | sector-holding-conglomerate.md | holding_conglomerate.json |
| cyclical_commodity | sector-cyclical-commodity.md | cyclical_commodity.json |
| utility_infrastructure_reit | sector-utility.md | utility_infrastructure_reit.json |
| ... | ... | ... |

（其他 type 类似）

---

## 十一、回归验证基线（stage 4 用）

V2 完工后必须用以下 3 家公司重跑并对比 V1 报告：

| 公司 | V1 结论 | V2 必须证明 |
|---|---|---|
| 万科 000002.SZ | PASS 4.30 | V2 仍 PASS，且价值陷阱 6 信号识别更清晰；地产 schema_extension 使用 |
| 招行 600036.SH | Watchlist 7.475 | V2 用银行专属指标（NIM/不良/核充）替代失效的 ROIC，加载 banking schema_extension，财务红旗 N/A 9 项有明确依据 |
| 百济 6160.HK | PASS 4.80 | V2 用 biotech 框架 rNPV 估值，加载 biotech schema_extension，能力圈"硬+软计数法"判定 |

---

## 十二、命名约定与禁止事项

- 文件命名：`sector-{type-with-hyphens}.md`（不用下划线），schema 用下划线
- 顶层私自扩展字段：**禁止**。所有 sector-specific 字段进 `sector_extension.extension_data`
- skill_feedback 注释：放 `meta.skill_feedback` 数组里，不污染结构化字段
- 评分锚点必须显式引用：每个 score 必须配 `anchor_used` 字段说明用了哪个锚点
- 一票否决与综合分独立：不要"加权调整"再触发，规则要清晰

---

**本规约即真理源。任何与本规约冲突的实现都视为 bug。**

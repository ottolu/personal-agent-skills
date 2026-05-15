# Sectors 总览索引 (v2.0)

> **真理源**：本目录 18 个 sector 文件均依据 `/Users/luotto/.claude/skills/value-invest-analysis/V2_SPEC.md` 第二节 18 类 `company_type` 枚举建立。

## 一、18 类 company_type 速查表

| # | enum 值 | 中文名 | 代表案例 | schema_extension | 路由文件 |
|---|---|---|---|---|---|
| 1 | `great_company_compounder` | 伟大公司复利机器 | 茅台 / 可口可乐 / Moody's | 无（base） | sector-great-company.md |
| 2 | `tech_platform_network` | 科技平台/网络效应 | 腾讯 / Meta / Visa | 无 | sector-tech-platform.md |
| 3 | `consumer_brand_premium` | 高端消费品牌 | LVMH / 雅诗兰黛 / 爱马仕 | 无 | sector-consumer-brand-premium.md |
| 4 | `tech_hardware_ecosystem` | 硬件生态 | 苹果 / 小米生态 | 无 | sector-tech-hardware-ecosystem.md |
| 5 | `high_growth_platform` | 高速增长平台/电商 | PDD / Sea / Shopify | 无 | sector-high-growth-platform.md |
| 6 | `biotech_unprofitable` | 未盈利创新药 | 百济 / Moderna / 信达 | biotech_unprofitable.json | sector-biotech-unprofitable.md |
| 7 | `pharma_mature` | 成熟制药 | 恒瑞 / Pfizer / 强生 | 无 | sector-pharma-mature.md |
| 8 | `banking` | 商业银行 | 招行 / JPM / 工行 | banking.json | sector-banking.md |
| 9 | `insurance` | 保险 | 平安 / 友邦 / MetLife | insurance.json | sector-insurance.md |
| 10 | `brokerage_assetmgmt` | 券商/资管 | 中信证券 / BlackRock | 无 | sector-brokerage-assetmgmt.md |
| 11 | `utility_infrastructure_reit` | 公用事业/基础设施/REIT | 领展 / 长江电力 / National Grid | utility_infrastructure_reit.json | sector-utility.md |
| 12 | `cyclical_commodity` | 大宗商品周期股 | 神华 / Exxon / 紫金 | cyclical_commodity.json | sector-cyclical-commodity.md |
| 13 | `cyclical_industrial_ev` | 新能源车/工业周期成长 | 比亚迪 / 特斯拉 / 宁德 | 无 | sector-cyclical-industrial-ev.md |
| 14 | `real_estate` | 地产 | 万科 / 龙湖 / 华润置地 | real_estate.json | sector-real-estate.md |
| 15 | `holding_conglomerate` | 控股集团 | BRK.B / Markel / 复星 | holding_conglomerate.json | sector-holding-conglomerate.md |
| 16 | `distressed_turnaround` | 困境反转 | Boeing / 福耀（早期） | 无 | sector-distressed-turnaround.md |
| 17 | `declining_cash_cow` | 衰退中现金牛 | Altria / 传统媒体 | 无 | sector-declining-cash-cow.md |
| 18 | `cigarbutt_deep_value` | 深度低估烟蒂股 | NCAV 候选 / 净净股 | 无 | sector-cigarbutt-deep-value.md |

## 二、路由判定流程（按顺序执行）

```
STEP 1: 业务识别
├── 是否未盈利 + 主营研发管线？ → biotech_unprofitable
├── 是否纯收存放贷 + 受银保监监管？ → banking
├── 是否承保 + 投资双业务？ → insurance
├── 是否经纪佣金 + AUM 管理费 ≥ 50%？ → brokerage_assetmgmt
├── 是否受规管回报 / 自然垄断 / REIT 结构？ → utility_infrastructure_reit
├── 主营开发销售房地产？ → real_estate
└── 进入 STEP 2

STEP 2: 周期 / 成长属性
├── 主营大宗商品 (能源/金属/煤炭)？ → cyclical_commodity
├── 主营工业 + 强周期 + 仍在扩张？ → cyclical_industrial_ev
├── 主营成熟药品（已盈利）？ → pharma_mature
└── 进入 STEP 3

STEP 3: 业务模式
├── 控股 + SOTP > 70% 价值来自子公司投资？ → holding_conglomerate
├── 平台 + 网络效应 + 高 ROIC + 轻资产？ → tech_platform_network
├── 硬件 + 生态系统 + 服务收入占比上升？ → tech_hardware_ecosystem
├── 平台 + 高速增长（>30%）+ 商业模式未稳态？ → high_growth_platform
└── 进入 STEP 4

STEP 4: 阶段 / 估值状态
├── 已严重困境 / 主业受冲击但有翻转机会？ → distressed_turnaround
├── 业务衰退但现金流稳定 / 高股息？ → declining_cash_cow
├── PB < 1 / NCAV / 烟蒂股？ → cigarbutt_deep_value
└── 进入 STEP 5

STEP 5: 兜底分类
├── 高端品牌 / 极强定价权 / 奢侈品？ → consumer_brand_premium
├── 极高 ROIC 长期稳健 + 多重护城河（茅台型）？ → great_company_compounder
└── 否则按主营属性归类（pharma_mature / cyclical_industrial_ev 等）
```

## 三、多类型重叠优先级规则

某些公司同时符合多个类型时，按以下优先级判定**主类型**（其他归入 modifier 或在 rationale 中标注）：

1. **强监管行业优先** —— 银行 / 保险 / 券商 / 公用事业 / 地产判定为主类型时，先于通用类型（如某地产 REIT 同时算 real_estate 与 utility_infrastructure_reit，按经营性质判：自持收租 → utility/REIT；开发销售 → real_estate）
2. **业务模式 > 估值状态** —— 一家好公司即使被低估，仍按业务主类型；不要因低估改判为 cigarbutt
3. **盈利状态优先** —— biotech_unprofitable 优先于 pharma_mature（一旦持续盈利 3 年改判）
4. **great_company_compounder 是最严格的最高阶称号** —— 必须 ROIC ≥ 20% × 10 年 + 多重护城河 + 财务堡垒；腾讯 / 苹果可同时归入 tech_platform_network 与 great_company_compounder，**主类型选行业属性更强的 tech_platform_network，great_company 通过 modifier 或 rationale 体现**
5. **困境/衰退是临时状态** —— distressed_turnaround / declining_cash_cow 优先于稳态业务类型（如波音应判 distressed_turnaround，而非 cyclical_industrial_ev）

## 四、Modifier 叠加规则

所有 sector 主类型均可叠加 `modifier_flags`（见 `_modifiers.md`）。例如：
- 招行：`banking` + `[a_h_dual_listed, state_owned, regulated_heavily]`
- 万科：`real_estate` + `[distressed, a_h_dual_listed, state_owned]`
- 阿里：`tech_platform_network` + `[vie_structure, adr_listed, dual_primary_listing]`
- 比亚迪：`cyclical_industrial_ev` + `[a_h_dual_listed, creator_led, with_policy_support]`

## 五、Schema Extension 加载机制

- 7 个类型有专属 schema_extension（见上表第 5 列），分析时必须按 `templates/schema_extensions/{type}.json` 加载
- 其余 11 个类型在 stage 1 暂用 base schema；后续 stage 2 按需补
- 通用财务字段（revenue / net_profit / ROE 等）始终在 base schema，sector 字段只补充行业特有项

## 六、文件清单

```
sectors/
├── _index.md                          # 本文件
├── _modifiers.md                      # 10 个 modifier_flags 详解
├── sector-great-company.md
├── sector-tech-platform.md
├── sector-consumer-brand-premium.md
├── sector-tech-hardware-ecosystem.md
├── sector-high-growth-platform.md
├── sector-biotech-unprofitable.md
├── sector-pharma-mature.md
├── sector-banking.md
├── sector-insurance.md
├── sector-brokerage-assetmgmt.md
├── sector-utility.md
├── sector-cyclical-commodity.md
├── sector-cyclical-industrial-ev.md
├── sector-real-estate.md
├── sector-holding-conglomerate.md
├── sector-distressed-turnaround.md
├── sector-declining-cash-cow.md
└── sector-cigarbutt-deep-value.md
```

# Schema Extensions Index (V2)

本目录提供 7 个行业 `schema_extensions` JSON 文件。它们是 `scorecard.json` 与 `structured-data.json` 在特定 `company_type` 下的扩展规约，用于补充行业专属字段、调整红旗清单、约束估值方法和数据源选取。

> 真理源：`V2_SPEC.md §九`、`§十`。所有扩展必须遵守"顶层私自字段禁止、行业字段进 `sector_extension.extension_data`"原则。

---

## 一、7 个 Extension 速览

| 文件 | 对应 company_type | 关键字段 | default_required_pct |
|---|---|---|---|
| `banking.json` | `banking` | NIM / 不良率 / 拨备覆盖率 / 核充率 / RWA / 中收占比 / AUM / ROA | 25 |
| `insurance.json` | `insurance` | 综合成本率 / EV / NBV / 偿付能力 / 投资收益率 / 浮存金成本 | 25 |
| `biotech_unprofitable.json` | `biotech_unprofitable` | cash_runway_months / 管线 / SBC/营收 / rNPV / FDA 里程碑 | 50 |
| `real_estate.json` | `real_estate` | NAV / 土储 / 合同负债 / 三道红线 / 净负债率 / 现金短债比 | 40 |
| `holding_conglomerate.json` | `holding_conglomerate` | segment_data / sotp_valuation / 浮存金 / 控股折价 / 13F 组合 | 20 |
| `cyclical_commodity.json` | `cyclical_commodity` | 正常化 EPS / PB 周期分位 / 成本曲线 / 长协 / 储量寿命 / 派息 | 35 |
| `utility_infrastructure_reit.json` | `utility_infrastructure_reit` | 监管允许回报 / Rate Base / FFO/AFFO / 派息历史 / 出租率 / WALT | 20 |

> 其余 11 个 company_type（great_company_compounder / tech_platform_network / consumer_brand_premium / tech_hardware_ecosystem / high_growth_platform / pharma_mature / brokerage_assetmgmt / cyclical_industrial_ev / distressed_turnaround / declining_cash_cow / cigarbutt_deep_value）首批使用 base schema，stage 2 按需补充。

---

## 二、加载路由规则

在 SKILL.md §2.3 路由判定 `company_type` 后：

```
if company_type in [banking, insurance, biotech_unprofitable, real_estate,
                    holding_conglomerate, cyclical_commodity,
                    utility_infrastructure_reit]:
    # 在 scorecard.json 和 structured-data.json 中：
    sector_extension.$ref = "templates/schema_extensions/{company_type}.json"
    sector_extension.extension_data = {} # 按 financial_fields_extension.fields 填充
else:
    sector_extension = null  # 走 base schema
```

每个 extension 包含 8 个顶级字段：

1. `applies_to_company_type` —— 严格枚举绑定
2. `extension_purpose` —— 为什么这个行业需要扩展
3. `scorecard_extension.additional_dimensions` —— 在 6 维评分内嵌套的子维度锚点
4. `financial_fields_extension.fields` —— `structured-data.json.sector_extension.extension_data` 应填的字段表
5. `red_flags_na_rules` —— v1 32 项红旗清单的 N/A 项 + 修改项 + 新增行业红旗
6. `valuation_methods_priority` —— primary / secondary / avoid 三档
7. `data_sources_required` —— 必查数据源清单（监管文件 / 行业数据库等）
8. `peer_comparison_strategy` —— 同业选取规则与 incomparability 默认值
9. `modifier_flags_common` —— 该行业常见叠加的 modifier
10. `default_required_pct` —— 安全边际基线（必须与 V2_SPEC §六 一致）
11. `examples_in_samples` —— 案例公司

---

## 三、与 base structured-data.json 的关系

```jsonc
{
  "$schema": "value-invest-structured-data-v2",
  "meta": { /* 通用 */ },
  "annual_financials": { /* 通用三表 */ },
  "balance_sheet_quality": { /* 通用 */ },
  "cash_flow_quality": { /* 通用 */ },
  "company_classification": { "company_type": "banking", "modifier_flags": [...] },
  "sector_extension": {
    "$ref": "templates/schema_extensions/banking.json",
    "extension_data": {
      "nim_pct": 2.41,
      "npl_ratio_pct": 0.95,
      "provision_coverage_pct": 437.7,
      "car_total_pct": 17.95,
      "car_tier1_pct": 14.86,
      "retail_loan_share_pct": 53,
      "non_interest_income_share_pct": 36,
      "demand_deposit_share_pct": 60,
      "roa_pct": 1.39,
      "...": "..."
    }
  },
  "data_lineage": [ /* 通用 */ ]
}
```

`sector_extension.extension_data` 中的 key 必须严格匹配该 JSON 的 `financial_fields_extension.fields[].field_name`，agent 禁止私自发明字段名。

---

## 四、与 scorecard.json 的关系

```jsonc
{
  "scorecard": {
    "business_quality": {"score": 8, "evidence": [...], "anchor_used": "好生意有壁垒..."},
    /* ... 其余 5 维 ... */
  },
  "sector_extension": {
    "$ref": "templates/schema_extensions/banking.json",
    "extension_data": {
      "asset_quality_subscore": {"score": 9, "evidence": ["不良率 0.95%, 拨备 437%"], "anchor_used": "10 分: 不良率 < 0.9%、拨备 > 400%"},
      "capital_adequacy_subscore": {"score": 8, ...},
      "deposit_franchise_subscore": {"score": 9, ...},
      "non_interest_income_quality_subscore": {"score": 8, ...}
    }
  }
}
```

`additional_dimensions[].name` 在 `extension_data` 中以 `{name}_subscore` 形式落地，并继承 `parent_dimension` 的权重分配（在父维度内的子权重见 `weight_within_parent_dimension`）。

---

## 五、维护准则

- 任何字段命名 / 计算口径变更必须先修改对应 JSON 与 V2_SPEC
- 新增行业 extension 时遵守 8 个顶级字段结构
- 严禁顶层私自字段污染 base schema
- 案例公司 examples_in_samples 必须可被 sectors/* 复用做回归

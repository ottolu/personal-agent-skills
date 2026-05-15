# 数据源参考（v2 行业专属版）

> **版本**：v2.0
> **生效日期**：2026-05-15
> **真理源**：本文件依据 `V2_SPEC.md` §七 / §八 / §九 重写，新增 §三 行业专属数据源（7 个子节，对应首批 7 个 schema_extensions）。

---

## 一、使用原则

1. **本 skill 不直接联网** —— 所有数据通过 `web-access` skill 抓取。本文件仅提供 URL 模板、字段提取规范、source priority。
2. **数据可追溯** —— 每个数据点必须含 `data_lineage` 字段（source / url / fetched_at / freshness_days，参见 §九）。
3. **数据时效硬门控** —— 见 §七，超时即触发 `unverified_quick_look` 模式（参见 V2_SPEC §七）。
4. **数据缺失即信号** —— 不可凭训练记忆估算；必须显式标注 `[数据缺失]`（参见 §八）。
5. **行业差异化** —— 不同 company_type 需调用不同的行业专属源（参见 §三 与对应 `schema_extensions/{type}.json` 的 `data_sources_required` 字段）。
6. **三层 source priority**：(a) 公司法定披露 → (b) 监管机构 / 行业协会 → (c) 第三方聚合（雪球 / Macrotrends / 同花顺等）。决策性数据必须能追溯到 (a) 或 (b)。

---

## 二、三市场通用数据源

### A 股

#### 法定披露（最权威）

| 数据源 | URL 模板 | 关键字段 |
|---|---|---|
| 巨潮资讯网（证监会指定信披平台）| `http://www.cninfo.com.cn` | 年报 / 季报 / 临时公告 PDF 原文、问询函、董事会决议、招股说明书 |
| 上交所 | `http://www.sse.com.cn` | 上市公司公告、问询函、互动易 |
| 深交所 | `http://www.szse.cn` | 上市公司公告、互动易、信用记录 |
| 北交所 | `http://www.bse.cn` | 北交所上市公司公告（专精特新中小企业） |
| 全国股转系统（新三板） | `http://www.neeq.com.cn` | 新三板挂牌公司公告（拟转板北交所候选） |

#### 财务指标 / 二次加工

| 数据源 | URL 模板 | 用途 |
|---|---|---|
| 同花顺 F10 | `http://stockpage.10jqka.com.cn/{6位代码}/` | 财务摘要、股东结构、龙虎榜 |
| 东方财富 F10 | `https://emweb.securities.eastmoney.com/PC_HSF10/pages/index.html?type=web&code={SH/SZ}{6位代码}` | 财务三表、行业对比 |
| 雪球 | `https://xueqiu.com/S/{SH/SZ}{6位代码}` | 龙虎榜、北向资金、社区讨论 |
| 新浪财经 | `https://finance.sina.com.cn/realstock/company/{sh/sz}{6位代码}/nc.shtml` | 历史财务、股权变动 |

#### 监管 / 行业研究

| 数据源 | URL | 用途 |
|---|---|---|
| 证监会 | `http://www.csrc.gov.cn` | 立案调查、行政处罚、并购重组审核 |
| 交易所互动平台 | 上证 e 互动 / 互动易 | 公司答投资者问 |
| 中证协 | `http://www.sac.net.cn` | 券商研报库（部分免费） |
| 各大券商研究所 | 中信 / 中金 / 国君 / 招商 / 中泰 / 海通 | 行业深度研报（部分需付费） |
| Wind / Choice（东财） | 终端 | 全量研报、宏观、行业数据 |

### 港股

#### 法定披露

| 数据源 | URL | 用途 |
|---|---|---|
| 披露易 HKEXnews | `https://www.hkexnews.hk/index_c.htm` | 所有公告 PDF（年报 / 中报 / 配股 / 合股 / 关联交易） |
| 港交所主板 / 创业板 | `https://www.hkex.com.hk` | 上市规则、合规情况、新股招股 |
| 证监会 SFC | `https://www.sfc.hk` | 监管纪律行动、市场失当行为通报 |

> **要点**：配股 / 供股 / 合股历史记录是识别老千股的核心；披露易支持按公司搜索全部历史公告。

#### 财务指标

| 数据源 | URL 模板 | 用途 |
|---|---|---|
| AAStocks | `http://www.aastocks.com/sc/stocks/analysis/company-fundamental/basic-information/{4位代码}` | 财务摘要、估值数据 |
| 富途牛牛 | `https://www.futunn.com/stock/{ticker}-HK` | 财报、研报、估值 |
| 老虎证券 | 全球账户股票详情页 | 港股财报、研报 |
| 雪球港股 | `https://xueqiu.com/S/{4位代码}` 或 `S/HK{4位代码}` | 社区讨论、AH 溢价 |
| 港股 100 强 / etnet | `https://www.etnet.com.hk` | 港股深度数据 |
| Hong Kong Money | 财华社 | 港股专项研报 |

#### AH 溢价与南向资金

| 数据源 | 用途 |
|---|---|
| 恒生 AH 溢价指数（HKEX 官方） | 历史折溢价区间 |
| 港股通持股记录（HKEX） | 单股南向资金累计持仓 |
| Choice / 东方财富 | 每日南向资金流向 |

### 美股

#### 法定披露（最权威）

| 数据源 | URL 模板 | 用途 |
|---|---|---|
| SEC EDGAR | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={CIK号}` | 10-K / 10-Q / 8-K / Proxy / Form 4 |
| EDGAR Full-Text Search | `https://efts.sec.gov/LATEST/search-index?q={关键词}&forms={form-type}` | 跨公司关键词检索（如重述、关联交易） |
| SEC FAQ / Compliance | `https://www.sec.gov/divisions/corpfin/cf-noaction` | 监管解读 |

#### 关键文件类型

| Form | 含义 | 必读情景 |
|---|---|---|
| 10-K | 年报（最详尽）| 必读 |
| 10-Q | 季报 | 季度跟踪 |
| 8-K | 临时报告 | 高管变动、并购、财务重述 |
| DEF 14A | 股东大会代理委托书 | 高管薪酬、ESG 提案 |
| Form 4 | 内部人交易 | 单次披露 |
| SC 13D/G | 大股东持仓（≥ 5%） | 主动 vs 被动 |
| 13F-HR | 机构持仓季报 | 抄作业 |
| 20-F | 外国发行人年报 | ADR 上市公司 |
| F-1 | 外国发行人 IPO | 中概股招股书 |
| S-1 | 美国 IPO 招股书 | 新股 |

#### 公司 IR 与电话会

- 公司官网 Investor Relations 页面
- Earnings call transcript（季度业绩说明会，可在 Seeking Alpha / Motley Fool / 公司 IR 找到）
- Guidance 指引、Investor Day 演示

#### 财务指标 / 二次数据

| 数据源 | URL 模板 | 用途 |
|---|---|---|
| Yahoo Finance | `https://finance.yahoo.com/quote/{ticker}` | 实时股价、财务摘要 |
| Macrotrends | `https://www.macrotrends.net/stocks/charts/{ticker}/{company-name}/` | 10-20 年长期财务数据 |
| Stockanalysis.com | `https://stockanalysis.com/stocks/{ticker}/` | 财务摘要、指标计算 |
| Koyfin（免费档） | `https://www.koyfin.com` | 跨市场对比、宏观仪表盘 |
| Simply Wall St | `https://simplywall.st/stocks/us/{ticker}` | 可视化估值快照 |
| Roic.ai | `https://roic.ai/{ticker}` | ROIC / WACC 历史 |

#### 内部人 / 机构

| 数据源 | URL 模板 | 用途 |
|---|---|---|
| OpenInsider | `http://openinsider.com/screener?s={ticker}` | 内部人买卖 |
| WhaleWisdom | `https://whalewisdom.com/stock/{ticker}` | 13F 机构持仓 |
| Dataroma | `https://www.dataroma.com/m/stock.php?sym={ticker}` | 价值投资大师持仓 |

#### 多空观点

- **Seeking Alpha**：`https://seekingalpha.com/symbol/{ticker}` —— 多空文章混合
- **Substack**：知名独立分析师专栏（如 Doomberg / Bear Cave）
- **Twitter/X $cashtag 检索**：$NVDA / $TSLA 等

---

## 三、行业专属数据源（v2 核心新增）

> **重要**：每个 company_type 触发对应子节；具体字段需求详见 `templates/schema_extensions/{company_type}.json` 的 `data_sources_required` 字段。

### 3.1 银行（`company_type: banking`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 货币政策 / 利率 | 中国人民银行 | `http://www.pbc.gov.cn` | 政策利率 / LPR / MLF / 准备金率 |
| 银行业整体 | 国家金融监督管理总局（原银保监会）| `https://www.nfra.gov.cn` | 不良率 / 净息差 / 拨备覆盖 / 资本充足率 |
| 行业月度 | 央行金融统计数据报告 | `http://www.pbc.gov.cn/diaochatongjisi/116219/index.html` | 社融 / M2 / 信贷规模 |
| A 股上市银行季报 | 巨潮资讯网（A 股法定信披） | 通用 | NIM / 不良 / 核充率 / RWA / 中收 |
| 港股上市银行 | 披露易 HKEXnews | 通用 | 同上 + 国际化数据 |
| 招股书 / 重大公告 | 巨潮 / 披露易 | 招股说明书 PDF | 业务结构、分行表现、单一最大客户暴露 |
| 行业研报 | 国君银行 / 中信银行 / 招商证券银行组 | 券商 PDF | 同业对比、专题分析 |
| 信用债 / 同业 | 中央结算公司 / 上清所 | `https://www.chinabond.com.cn` | 同业存单收益率、银行二级资本债 |
| 美国银行业 | FFIEC Call Reports | `https://cdr.ffiec.gov/public/` | 美国所有银行季度财务 |
| 美国银行 FDIC | FDIC SDI | `https://banks.data.fdic.gov` | 存款保险、银行健康度 |
| 美国系统重要性 | Federal Reserve | `https://www.federalreserve.gov/supervisionreg/banking.htm` | CCAR / DFAST 压力测试 |
| 跨境对比 | The Banker（FT 集团）| 付费 | 全球银行 Top 1000 排行 |
| 跨境对比 | S&P Global Market Intelligence | 付费 | 全球银行指标库 |

> 对应 schema：`schema_extensions/banking.json` —— NIM / 不良率 / 拨备覆盖率 / 核充率 / RWA / 零售贷款占比 / AUM / 中收占比 / 资本充足率分级

---

### 3.2 保险（`company_type: insurance`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 行业整体（国内）| 国家金融监督管理总局保险司 | `https://www.nfra.gov.cn` | 保费、综合成本率行业均值、偿付能力 |
| 行业月度数据 | 中国银保信 / 中国保险行业协会 | `http://www.iachina.cn` | 行业月度保费数据 |
| 内含价值 EV / NBV | 上市公司中报 / 年报附录 | 公司 IR | EV 模型假设、新业务价值率 |
| 投资组合 | 上市公司精算报告附录 | 公司 IR | 资产配置 / 久期匹配 |
| 美国保险 | NAIC（全国保险监督官协会）| `https://content.naic.gov` | 各州 statutory 报表 |
| 美国保险 10-K | SEC EDGAR | 通用 | GAAP 报表 + 保留准备金 |
| 全球再保 | Munich Re / Swiss Re 年报 | 公司 IR | 再保险定价周期 |
| 财产险数据 | 欧洲 EIOPA / 英国 PRA | 各国监管 | Solvency II 报告 |
| 行业研报 | 国君 / 中信非银金融组、Autonomous Research（美）| 付费 | 行业景气、估值 |
| 投资端 | 公司 IR 季度投资组合披露 | 同上 | 权益 / 固收 / 另类比例 |

> 对应 schema：`schema_extensions/insurance.json` —— 综合成本率 / EV / NBV / 投资收益率 / 准备金 / 偿付能力

---

### 3.3 Biotech / 创新药（`company_type: biotech_unprofitable`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 临床试验注册与进度 | ClinicalTrials.gov | `https://clinicaltrials.gov/ct2/results?cond=&term={药物名}` | NCT 编号、phase、enrollment、primary completion date |
| 全球临床试验 | WHO ICTRP | `https://trialsearch.who.int` | 全球登记数据 |
| 中国临床试验 | 国家药监局药品审评中心（CDE） | `http://www.cde.org.cn` | 国内 IND/NDA 进度 |
| FDA 已批准药物 | FDA Drugs@FDA + Orange Book | `https://www.accessdata.fda.gov/scripts/cder/ob/index.cfm` | 批准日期、专利到期 |
| FDA 提交 / 突破性 | FDA Calendar / Adcom | `https://www.fda.gov/advisory-committees/advisory-committee-calendar` | PDUFA date、专家组讨论 |
| FDA 警告函 | FDA Warning Letters | `https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/compliance-actions-and-activities/warning-letters` | 临床 / 生产违规 |
| 中国药监局（NMPA） | NMPA 官网 | `https://www.nmpa.gov.cn` | 国内审批、ANDA |
| 集采价格 / 国谈 | 国家医保局 | `http://www.nhsa.gov.cn` | 集采中标价 / 量、国谈降幅 |
| ASCO 大会（肿瘤）| ASCO Meeting Library | `https://meetings.asco.org` | 6 月年会摘要 |
| ASH 大会（血液）| ASH Annual Meeting | `https://www.hematology.org` | 12 月年会摘要 |
| AACR 大会（基础研究）| AACR Annual Meeting | `https://www.aacr.org` | 4 月年会摘要 |
| ESMO 大会（欧洲肿瘤）| ESMO Congress | `https://www.esmo.org` | 9 月年会 |
| 论文检索 | PubMed | `https://pubmed.ncbi.nlm.nih.gov` | 临床数据论文 |
| 药物管线数据库 | EvaluatePharma | 付费 | 全球管线、销售预测 |
| 药物管线数据库 | GlobalData Pharma | 付费 | 同上 |
| 药物管线数据库 | Citeline Pharmaprojects | 付费 | 同上 |
| 专利数据库 | Cortellis | 付费 | 化合物专利、Patent Cliff |
| 专利搜索（免费）| Google Patents / USPTO | `https://patents.google.com` | 专利说明书 |
| BD 交易数据 | BioPharma Catalysts / BioCentury | 付费 | License / M&A 估值参考 |
| 医药行业研报 | 中泰证券医药 / 国君医药 / 中信医药 | 国内 | 国内创新药专题 |
| 美股医药研报 | Leerink / SVB / Stifel | 付费 | 美股 biotech 专家 |
| 二级市场情绪 | Endpoints News / FierceBiotech / STAT News | 免费 / 部分付费 | 行业即时新闻 |

> 对应 schema：`schema_extensions/biotech_unprofitable.json` —— cash_runway_months / R&D efficiency / pipeline_phases / FDA_milestones / SBC_ratio / 合作交易

---

### 3.4 房地产（`company_type: real_estate`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 全国销售数据 | 国家统计局 | `http://www.stats.gov.cn` | 商品房销售面积 / 金额 / 待售面积 |
| 70 城房价 | 国家统计局 70 大中城市住宅销售价格指数 | 同上 | 一手 / 二手房价指数 |
| 100 城销售 | 克而瑞 CRIC | `https://www.cric.com/` | TOP200 房企销售排行 |
| 100 城市场 | 中指研究院 | `https://www.cih-index.com` | 城市市场数据 |
| 土地拍卖 | 自然资源部（原国土资源部）/ 各地土地交易中心 | 同上 | 集中供地结果 / 流拍率 |
| 三道红线 | 公司年报 / 半年报附录 | 巨潮 / 披露易 | 净负债率 / 现金短债比 / 剔预资产负债率 |
| 商品房库存 | 易居研究院 / Wind 库存监测 | 部分付费 | 一二三线去化周期 |
| 城投债 | 中国城投债信息披露平台 | `https://www.chinabondportfolio.com` | 城投发行 / 兑付 |
| 城投债 | Wind 城投债库 / Choice | 付费 | 同上 + 信用利差 |
| 海外做空研究 | GMT Research（专注亚太地产 & 银行） | `https://www.gmtresearch.com` | 报表质量做空报告 |
| 海外做空研究 | Muddy Waters / Coatue Insights | 同前 | 中资地产做空报告 |
| 海外做空研究 | Anne Stevenson-Yang / Jim Chanos | 公开演讲、Substack | 中国地产做空观点 |
| 物业评估 | 中房协 / 中诚信国际 / 联合资信 | 部分付费 | 信用评级、专项报告 |
| 香港 REIT | HKEX REIT 板块 | `https://www.hkex.com.hk` | REIT 季报、AFFO |
| 内地 REIT | 上交所 / 深交所基础设施 REITs | 各交易所 | 国内 REIT 信息披露 |
| 美国 REIT | NAREIT | `https://www.reit.com` | 美国 REIT 行业数据 |
| 美国 REIT 公司 | SEC 10-K + Supplemental | EDGAR | NOI / FFO / AFFO / 同店增长 |
| 销售签约月报 | 公司公告（克而瑞抓取） | 公司 IR | 月度销售签约金额 |

> 对应 schema：`schema_extensions/real_estate.json` —— NAV / 土储 / 净负债率 / 合约负债 / 销售金额 / 现金短债比 / 三道红线

---

### 3.5 煤炭 / 能源（`company_type: cyclical_commodity`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 秦皇岛 5500 大卡煤价 | CCTD 中国煤炭市场网 | `http://www.cctd.com.cn` | 现货 / 长协价、运价 |
| 煤炭港口库存 | 上海煤炭交易所 | `http://www.sh-cce.com.cn` | 秦皇岛 / 京唐港库存 |
| 长协煤价（年度）| 国家能源集团 / 煤炭运销协会 | `http://www.coal.org.cn` | 5500 大卡年度长协基准价 |
| 全球煤价 | Argus / Platts | 付费 | API2（鹿特丹）/ Newcastle 价 |
| 焦煤 | 大商所焦煤期货 | `http://www.dce.com.cn` | DCE 焦煤期货曲线 |
| 动力煤 / 焦煤指数 | 中国煤炭工业协会 | `http://www.coalchina.org.cn` | 行业月度运行 |
| 双碳 / 政策 | 国家能源局 | `http://www.nea.gov.cn` | 能源转型、电力规划 |
| 双碳 / 政策 | 国家发改委 | `https://www.ndrc.gov.cn` | 双碳路线图、煤电规划 |
| 全球煤炭储量 / 产能 | Wood Mackenzie | 付费 | 煤矿生产成本曲线 |
| 全球能源数据 | IEA（国际能源署）| `https://www.iea.org` | World Energy Outlook |
| 美国煤炭 | EIA（美国能源信息署）| `https://www.eia.gov` | 美国煤炭产销、库存 |
| 石油 | EIA Petroleum + OPEC Monthly | 同上 + `https://www.opec.org` | 全球供需平衡表 |
| 天然气 | Henry Hub / TTF / JKM | CME / ICE | 全球气价基准 |
| 国内电厂日耗 / 库存 | CCTD / Wind | 部分付费 | 沿海 8 省电厂日耗 |
| 矿产开采成本曲线 | Wood Mackenzie / SNL Metals | 付费 | 各矿成本分位 |
| 大宗商品期货 | LME / SHFE / DCE / NYMEX / CME | 各交易所 | 期货曲线、库存 |
| 有色金属 | 上海有色网（SMM） | `https://www.smm.cn` | 铜铝铅锌镍现货 / 库存 |
| 钢铁 | Mysteel | `https://www.mysteel.com` | 钢价、库存、产量 |

> 对应 schema：`schema_extensions/cyclical_commodity.json` —— commodity_price_history / normalized_eps / pb_cycle_percentile / 长协占比 / 自有运输 / 采矿成本曲线

---

### 3.6 汽车 / 新能源车（`company_type: cyclical_industrial_ev`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 月度乘用车销量（国内） | 乘联会 CPCA | `http://www.cpcaauto.com` | 厂商批发 / 零售、新能源渗透率 |
| 月度汽车销量（含商用车） | 中汽协 CAAM | `http://www.caam.org.cn` | 全行业销量 |
| 单车型销量 | 乘联会分品牌 / ChinaEV100 | 同上 | 周 / 月销量榜 |
| 新能源车终端 | EV Sales Blog / CleanTechnica | 公开 | 全球 EV 月销 |
| 欧洲销量 | ACEA | `https://www.acea.auto` | 欧盟 27 国月度 |
| 美国销量 | 各厂商 IR + Cox Automotive | 公开 | 月度交付 |
| 海外销量 | 公司 IR + 当地协会 | 同上 | 出口国别 |
| 海外贸易壁垒 | 各国海关 + 商务部 | `http://www.mofcom.gov.cn` | 反补贴 / 反倾销 / 关税 |
| 二手车残值 | 中国汽车流通协会 | `http://www.cada.cn` | 残值率 |
| 充电桩数据 | 中国充电联盟 | `http://www.evcipa.org.cn` | 充电桩保有量、运营数据 |
| 电池供应链 | SNE Research（韩） | `https://www.sneresearch.com` | 全球动力电池装机 |
| 电池 / 能源金属 | BNEF（彭博新能源财经）| 付费 | 锂电池均价、能源转型预测 |
| 锂资源 | 上海有色网 SMM | 同前 | 碳酸锂 / 氢氧化锂现货 |
| 行业研究 | 中信汽车 / 中泰汽车 / 国君汽车 / 招商汽车 | 国内券商 | 行业月报、车型周报 |
| 海外车厂研究 | Wedbush（Dan Ives） / Morgan Stanley（Adam Jonas）| 付费 | 特斯拉 / 美股车厂 |
| 智能驾驶数据 | 工信部 / 高工智能汽车 | 部分免费 | L2/L3 渗透率、芯片 |
| 自动驾驶里程 | CA DMV（加州交管局）/ 公司 IR | 公开 | Waymo / 小鹏 / 蔚来路测 |

---

### 3.7 公用事业 / 基础设施 / REIT（`company_type: utility_infrastructure_reit`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 国内监管允许回报率 | 国家发改委（电力 / 燃气）| `https://www.ndrc.gov.cn` | 输配电价、永久回报基础 |
| 电网 / 电力 | 国家能源局 | `http://www.nea.gov.cn` | 全国电力供需 |
| 长江电力 / 水电 | 公司 IR + 国家电网年报 | 同前 | 水电来水、上网电价 |
| 国电南瑞 / 电网设备 | 国家电网 / 南方电网年度招标 | 各自 IR | 电网投资计划 |
| 美国电力 / 天然气 | FERC | `https://www.ferc.gov` | 跨州输配电、费率裁定 |
| 美国电力 | NERC | `https://www.nerc.com` | 北美电网可靠性 |
| 美国天然气 | EIA Natural Gas | `https://www.eia.gov/naturalgas/` | 储气、价格 |
| 港股 REIT | 港交所 + 公司 IR | HKEX | AFFO / DPU / 派息率 |
| 内地 REIT | 上交所 / 深交所 REITs 专板 | 各交易所 | 季报、租金回款 |
| 美国 REIT | NAREIT + SEC 10-K | 同 §3.4 | FFO / AFFO / 同店 NOI |
| 公用事业海外比较 | Edison Electric Institute / 国际公用事业协会 | `https://www.eei.org` | 跨国对比 |
| 收费公路 | 交通运输部年报 | `https://www.mot.gov.cn` | 高速公路通行量 |
| 港口 / 机场 | 各港口 / 机场年报 + 民航局 | `http://www.caac.gov.cn` | 吞吐量、客货数据 |

> 对应 schema：`schema_extensions/utility_infrastructure_reit.json` —— DDM 参数 / regulated_return / 派息率历史 / 资产基础

---

### 3.8 控股集团 / 投资组合（`company_type: holding_conglomerate`）

| 数据需求 | 推荐源 | URL 模板 | 关键字段 |
|---|---|---|---|
| 巴菲特 13F 持仓 | WhaleWisdom | `https://whalewisdom.com/filer/berkshire-hathaway-inc` | 季度持仓变动 |
| 巴菲特 13F 持仓 | Dataroma | `https://www.dataroma.com/m/holdings.php?m=brk` | 同上 |
| 巴菲特 13F 原始 | SEC EDGAR (BRK 13F-HR) | `https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0001067983` | 原始文件 |
| 巴菲特致股东信 | berkshirehathaway.com | `https://www.berkshirehathaway.com/letters/letters.html` | 1965-now 全套 PDF |
| BRK 年报 / 10-K | SEC EDGAR | 同前 | segment 数据 |
| 13D/G 大额变动 | SEC EDGAR | EDGAR Form 13D / 13G 检索 | 主动 vs 被动持仓 |
| Form 4 内部交易 | OpenInsider | 同 §二 | BRK 高管买卖 |
| 价值大师 13F | Mohnish Pabrai / Howard Marks / Seth Klarman / Bill Ackman | 各自基金 13F | 季度持仓 |
| 价值大师 13F 聚合 | Dataroma | `https://www.dataroma.com/m/managers.php` | 名家持仓库 |
| 段永平公开发言 | 雪球 ID @大道无形我有型 | `https://xueqiu.com/2032993651` | 公开问答 |
| 段永平 OFollow | NextBigWhat / 唐朝老唐 / 雪球转述 | 公开 | 持仓、投资观 |
| Markel 年报 | Markel Group IR | 公司 IR | Markel-style float |
| Loews / Fairfax 等 | 各自 IR + SEC | 同前 | 控股折价历史 |
| 港股控股集团 | 复星 / 中信泰富 / 太古 年报 | 披露易 | NAV 分部估值 |
| SOTP 模板参考 | Damodaran 估值数据 / Aswath 学院 | `https://pages.stern.nyu.edu/~adamodar/` | 行业 multiple、控股折价 |

> 对应 schema：`schema_extensions/holding_conglomerate.json` —— segment_data / sotp_valuation / float_value / investment_portfolio_nav / 控股折价

---

### 3.9 周期股 / 大宗商品汇总（跨 3.5 与其他周期）

| 数据需求 | 推荐源 |
|---|---|
| 大宗商品价格 | LME / SHFE / DCE / NYMEX / CME / ICE |
| 全球供需平衡表 | 各商品行业协会（如世界钢铁协会、ICSG 铜、ILZSG 锌）|
| 期货价格曲线 | 各交易所 + Bloomberg COMS GO |
| 库存 | LME / SHFE / Cushing 原油 / 秦皇岛煤 |
| 矿产储量 | 公司年报 + Wood Mackenzie / SNL Metals + USGS Mineral Commodity Summaries |
| 国内产能 / 限产政策 | 工信部 + 各省经信厅 |
| 海运费 | 波罗的海干散货指数 BDI / Clarksons |
| 农产品 | USDA WASDE / FAO + 国家粮油信息中心 |

---

## 四、跨行业通用工具

| 工具 | 用途 | 付费档 |
|---|---|---|
| Wind 万得 | 中文最完整金融终端 | 高 |
| Choice 东方财富 | A+H+US 全覆盖 | 中 |
| Bloomberg Terminal | 全球金融数据 | 高 |
| Refinitiv Eikon (LSEG) | 全球金融数据 | 高 |
| Capital IQ | M&A + 私募市场 | 高 |
| TIKR Terminal | 国际估值建模 | 中 |
| Koyfin | 跨市场对比 + 宏观仪表盘 | 部分免费 |
| Finchat / Wisesheets | 财务数据 API | 部分免费 |
| Roic.ai | ROIC / WACC 历史 | 部分免费 |
| Stockanalysis.com | 跨市场财务摘要 | 免费 |
| Macrotrends | 长期历史财务 | 免费 |
| Damodaran Online | 行业 multiple / 风险溢价 | 免费 |
| GuruFocus | 巴菲特指标、价投筛选 | 部分免费 |

---

## 五、做空 / 看空研报源（v2 强化为反向证据搜索核心入口）

价值投资必读（对应 V2_SPEC 软门控"反向证据三件套"）：

| 机构 | URL | 专长 |
|---|---|---|
| Hindenburg Research | `https://hindenburgresearch.com` | 财务造假、关联交易、估值操纵 |
| Muddy Waters | `https://www.muddywatersresearch.com` | 中概股、新兴市场 |
| Citron Research | `https://citronresearch.com` | 科技股、生物医药 |
| Wolfpack Research | `https://www.wolfpackresearch.com` | 中概股、SPAC |
| Spruce Point Capital | `https://www.sprucepointcap.com` | 中小盘、SaaS、消费 |
| GMT Research | `https://www.gmtresearch.com` | 亚太地产、银行（专注会计质量） |
| Coatue Insights / Kerrisdale | 公开发布 | 多空对冲基金研究 |
| Bear Cave（Edwin Dorsey）| `https://thebearcave.substack.com` | 美国中小盘做空 Substack |
| Bonitas Research | `https://www.bonitasresearch.com` | 中概股 |
| Blue Orca Capital | `https://www.blueorcacapital.com` | 亚洲股票做空 |
| Glaucus / J Capital | 历史报告 | 中概股早期做空者 |

> **使用方法**：每份分析必须主动搜索目标公司的做空报告，若找不到也必须记录"已搜索 X 个机构、N/A"。

---

## 六、数据获取查询模板（v2 标准化，与 web-access 协作）

调用 `web-access` 时建议传以下结构（与 V2_SPEC §八 `data_lineage` 衔接）：

```yaml
intent: fetch_company_data
ticker: 600519.SH
company_name_cn: 贵州茅台
company_type: great_company_compounder
modifier_flags: [state_owned]
data_needs:
  - 近 10 年三表（利润 / 资产负债 / 现金流量）
  - 最新季报关键数据
  - 近 12 个月公告标题
  - 股东持股变动 / 大额减持
  - 同业对比 ≥ 3 家（参考 sector-{type}.md 推荐对标）
  - 行业特定数据（详见 schema_extensions/{type}.json 的 data_sources_required）
source_priority:
  - 巨潮资讯网（A 股法定信披源）       # tier 1
  - 上交所 / 深交所 / 北交所            # tier 1
  - 同花顺 F10 / 东方财富 F10            # tier 2
  - 雪球 / 富途 / 老虎                   # tier 3
  - 行业专属源（依 §三 子节）            # tier 1-2 视情况
output_format: structured_markdown_with_data_lineage
data_lineage_required: true
expected_freshness_days:
  financials: 90
  price: 7
  industry_news: 30
  regulatory: 14
```

### 行业触发示例（按 company_type 自动追加源）

| company_type | 必加 source_priority |
|---|---|
| banking | 国家金融监督管理总局 / 央行 / FFIEC / FDIC |
| biotech_unprofitable | ClinicalTrials.gov / FDA Drugs@FDA / NMPA / ASCO Library |
| real_estate | 国家统计局 / 克而瑞 / 三道红线披露附录 |
| cyclical_commodity | CCTD / Argus / Wood Mackenzie / EIA |
| holding_conglomerate | WhaleWisdom / Dataroma / SEC 13F |
| utility_infrastructure_reit | 发改委 / FERC / NAREIT |
| insurance | 国家金融监督管理总局保险司 / NAIC |

---

## 七、数据时效性硬门控（V2_SPEC §七 H1）

| 数据类型 | 最大时效（硬门控） | 超时处理 |
|---|---|---|
| 财报数据（最新季报 / 半年报 / 年报） | ≤ 90 天 | 触发 `unverified_quick_look` + 警告 |
| 股价 / 估值 | ≤ 7 天 | 触发降级 |
| 行业新闻 / 政策 | ≤ 30 天 | 显式标注 |
| 监管动态 / 问询函 | ≤ 14 天 | 显式标注 |
| 临床试验状态（biotech） | ≤ 30 天 | 触发降级 |
| 大宗商品现货价（周期） | ≤ 14 天 | 触发降级 |
| 高频销售数据（汽车 / 地产）| ≤ 30 天 | 触发降级 |

任何硬门控未通过 → `quality_gate.mode = unverified_quick_look` + 输出顶部强制 `⚠️` 警告。

---

## 八、数据缺失处理原则（保留 v1，v2 强化）

1. **禁止凭训练记忆估算 / 推测 / 跳过**
2. **必须显式标注 `[数据缺失]`** 并说明影响哪些结论
3. 数据缺失本身是 governance 信号 —— 持续披露不全可能映射治理或会计质量问题
4. 在 `outputs/{ticker}/{date}/sources.md` 中维护缺失清单
5. 若关键定量字段缺失影响硬门控（如最新季报未发布），触发 `unverified_quick_look`

---

## 九、引用与可追溯（v2 schema 强化）

每个量化数据点必须含 `data_lineage` 条目（V2_SPEC §八）：

```json
{
  "field": "annual_financials.revenue",
  "source": "招商银行 2024 年年度报告",
  "url": "http://www.cninfo.com.cn/new/disclosure/detail?...",
  "fetched_at": "2026-05-15T10:00:00Z",
  "report_period": "2024-12-31",
  "freshness_days": 120,
  "tier": 1
}
```

字段说明：

- `field`：JSON path 到结构化数据中的具体字段
- `source`：人类可读的来源名（公司年报 / 央行公告 / 同花顺 F10 等）
- `url`：可点击核验链接
- `fetched_at`：抓取时刻（ISO 8601）
- `report_period`：数据本身的报告期
- `freshness_days`：(now - report_period) 天数
- `tier`：source priority 层级（1 = 法定披露，2 = 监管 / 行业，3 = 第三方聚合）

写入 `outputs/{ticker}/{date}/sources.md` 作为报告附件，且在 `structured-data.json.data_lineage` 数组中机器可读。

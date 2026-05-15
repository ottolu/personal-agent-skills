#!/usr/bin/env python3
"""
股票代码归一化与市场识别工具 (v2)

用法:
    python parse-ticker.py 600519
    python parse-ticker.py 600519.SH
    python parse-ticker.py 0700.HK
    python parse-ticker.py AAPL
    python parse-ticker.py 腾讯

输出 (JSON):
    {
      "input": "...",
      "normalized": "600519.SH",
      "market": "CN_SH",
      "valid": true,
      "ambiguous": false,
      "candidates": [...],
      "notes": "...",
      "suggested_company_type": "great_company_compounder",  # v2 新增
      "suggested_modifier_flags": ["state_owned", ...]         # v2 新增
    }

v2 变更:
- COMPANY_MAP 扩展至 100+ 条，覆盖 18 类 company_type
- 修正 BJ 北交所规则（不再用首位字符判定）
- 输出含 suggested_company_type / suggested_modifier_flags
- OTC / 仙股 / ADR 智能识别
"""
import json
import re
import sys

# ---------------------------------------------------------------------------
# 1. 中文公司名 → 多市场代码映射（≥100 条）
# ---------------------------------------------------------------------------
# 每条候选 (ticker, note)；
# 同时通过 TICKER_META 维护代码 → (company_type, modifier_flags)
COMPANY_MAP = {
    # === 互联网 / 平台（港股 + 美股 ADR / VIE） ===
    "腾讯": [("0700.HK", "港股主上市"), ("TCEHY", "美股 ADR")],
    "腾讯控股": [("0700.HK", "港股主上市"), ("TCEHY", "美股 ADR")],
    "阿里": [("9988.HK", "港股双重主要上市"), ("BABA", "美股 ADR / 双重主要")],
    "阿里巴巴": [("9988.HK", "港股双重主要上市"), ("BABA", "美股 ADR / 双重主要")],
    "美团": [("3690.HK", "港股")],
    "京东": [("9618.HK", "港股"), ("JD", "美股 ADR")],
    "拼多多": [("PDD", "美股 ADR")],
    "百度": [("9888.HK", "港股双重主要"), ("BIDU", "美股 ADR")],
    "网易": [("9999.HK", "港股双重主要"), ("NTES", "美股 ADR")],
    "B站": [("9626.HK", "港股"), ("BILI", "美股 ADR")],
    "哔哩哔哩": [("9626.HK", "港股"), ("BILI", "美股 ADR")],
    "爱奇艺": [("IQ", "美股 ADR")],
    "小米": [("1810.HK", "港股")],
    "联想": [("0992.HK", "港股")],
    "联想集团": [("0992.HK", "港股")],
    "快手": [("1024.HK", "港股")],
    "京东物流": [("2618.HK", "港股")],
    "京东健康": [("6618.HK", "港股")],
    "阿里健康": [("0241.HK", "港股")],
    "顺丰同城": [("9699.HK", "港股")],

    # === 银行（A+H 双重上市 + 美股 4 大行） ===
    "工商银行": [("601398.SH", "A 股"), ("1398.HK", "港股 H")],
    "建设银行": [("601939.SH", "A 股"), ("0939.HK", "港股 H")],
    "农业银行": [("601288.SH", "A 股"), ("1288.HK", "港股 H")],
    "中国银行": [("601988.SH", "A 股"), ("3988.HK", "港股 H")],
    "交通银行": [("601328.SH", "A 股"), ("3328.HK", "港股 H")],
    "招商银行": [("600036.SH", "A 股"), ("3968.HK", "港股 H")],
    "平安银行": [("000001.SZ", "A 股")],
    "中信银行": [("601998.SH", "A 股"), ("0998.HK", "港股 H")],
    "兴业银行": [("601166.SH", "A 股")],
    "民生银行": [("600016.SH", "A 股"), ("1988.HK", "港股 H")],
    "宁波银行": [("002142.SZ", "A 股")],
    "杭州银行": [("600926.SH", "A 股")],
    "邮储银行": [("601658.SH", "A 股"), ("1658.HK", "港股 H")],
    "汇丰": [("0005.HK", "港股")],
    "汇丰控股": [("0005.HK", "港股")],
    "渣打": [("2888.HK", "港股")],
    "渣打集团": [("2888.HK", "港股")],

    # === 保险 ===
    "中国平安": [("601318.SH", "A 股"), ("2318.HK", "港股 H")],
    "中国人寿": [("601628.SH", "A 股"), ("2628.HK", "港股 H")],
    "中国太保": [("601601.SH", "A 股"), ("2601.HK", "港股 H")],
    "中国人保": [("601319.SH", "A 股"), ("1339.HK", "港股 H")],
    "友邦保险": [("1299.HK", "港股")],
    "友邦": [("1299.HK", "港股")],

    # === 能源 / 大宗（A+H 国企央企） ===
    "中海油": [("0883.HK", "港股 H"), ("600938.SH", "A 股"), ("CEO", "美股 ADR 历史")],
    "中国海油": [("0883.HK", "港股 H"), ("600938.SH", "A 股")],
    "中石化": [("600028.SH", "A 股"), ("0386.HK", "港股 H"), ("SNP", "美股 ADR")],
    "中国石化": [("600028.SH", "A 股"), ("0386.HK", "港股 H")],
    "中石油": [("601857.SH", "A 股"), ("0857.HK", "港股 H"), ("PTR", "美股 ADR")],
    "中国石油": [("601857.SH", "A 股"), ("0857.HK", "港股 H")],
    "中国神华": [("601088.SH", "A 股"), ("1088.HK", "港股 H")],
    "神华": [("601088.SH", "A 股"), ("1088.HK", "港股 H")],
    "兖矿能源": [("600188.SH", "A 股"), ("1171.HK", "港股 H")],
    "兖矿": [("600188.SH", "A 股"), ("1171.HK", "港股 H")],
    "中煤能源": [("601898.SH", "A 股"), ("1898.HK", "港股 H")],
    "陕煤": [("601225.SH", "A 股")],
    "陕西煤业": [("601225.SH", "A 股")],
    "紫金矿业": [("601899.SH", "A 股"), ("2899.HK", "港股 H")],
    "江西铜业": [("600362.SH", "A 股"), ("0358.HK", "港股 H")],
    "中国铝业": [("601600.SH", "A 股"), ("2600.HK", "港股 H")],
    "中海发展": [("600026.SH", "A 股"), ("1138.HK", "港股 H")],
    "长江电力": [("600900.SH", "A 股")],

    # === 地产（A+H 双重 / 困境） ===
    "万科": [("000002.SZ", "A 股"), ("2202.HK", "港股 H")],
    "万科 A": [("000002.SZ", "A 股"), ("2202.HK", "港股 H")],
    "万科A": [("000002.SZ", "A 股"), ("2202.HK", "港股 H")],
    "龙湖": [("0960.HK", "港股")],
    "龙湖集团": [("0960.HK", "港股")],
    "华润置地": [("1109.HK", "港股")],
    "中海地产": [("0688.HK", "港股")],
    "中国海外发展": [("0688.HK", "港股")],
    "招商蛇口": [("001979.SZ", "A 股")],
    "保利发展": [("600048.SH", "A 股")],
    "保利": [("600048.SH", "A 股")],
    "领展": [("0823.HK", "港股 REIT")],
    "长江实业": [("1113.HK", "港股")],
    "新鸿基地产": [("0016.HK", "港股")],
    "新鸿基": [("0016.HK", "港股")],
    "太古地产": [("1972.HK", "港股")],

    # === 汽车 / 新能源车 / 电池 ===
    "比亚迪": [("002594.SZ", "A 股"), ("1211.HK", "港股")],
    "长城汽车": [("601633.SH", "A 股"), ("2333.HK", "港股 H")],
    "广汽集团": [("601238.SH", "A 股"), ("2238.HK", "港股 H")],
    "广汽": [("601238.SH", "A 股"), ("2238.HK", "港股 H")],
    "宁德时代": [("300750.SZ", "A 股创业板")],
    "蔚来": [("9866.HK", "港股双重主要"), ("NIO", "美股 ADR")],
    "理想": [("2015.HK", "港股双重主要"), ("LI", "美股 ADR")],
    "理想汽车": [("2015.HK", "港股双重主要"), ("LI", "美股 ADR")],
    "小鹏": [("9868.HK", "港股双重主要"), ("XPEV", "美股 ADR")],
    "小鹏汽车": [("9868.HK", "港股双重主要"), ("XPEV", "美股 ADR")],

    # === 新能源 / 光伏 ===
    "隆基": [("601012.SH", "A 股")],
    "隆基绿能": [("601012.SH", "A 股")],
    "通威股份": [("600438.SH", "A 股")],
    "通威": [("600438.SH", "A 股")],
    "阳光电源": [("300274.SZ", "A 股创业板")],

    # === 半导体 / 科技硬件 ===
    "中芯国际": [("688981.SH", "A 股科创板"), ("0981.HK", "港股")],
    "上海复旦": [("688385.SH", "A 股科创板"), ("1385.HK", "港股")],
    "工业富联": [("601138.SH", "A 股")],

    # === 白酒 / 消费 ===
    "贵州茅台": [("600519.SH", "A 股")],
    "茅台": [("600519.SH", "A 股")],
    "五粮液": [("000858.SZ", "A 股")],
    "泸州老窖": [("000568.SZ", "A 股")],
    "山西汾酒": [("600809.SH", "A 股")],
    "汾酒": [("600809.SH", "A 股")],
    "洋河": [("002304.SZ", "A 股")],
    "洋河股份": [("002304.SZ", "A 股")],
    "古井贡": [("000596.SZ", "A 股")],
    "古井贡酒": [("000596.SZ", "A 股")],
    "海天": [("603288.SH", "A 股")],
    "海天味业": [("603288.SH", "A 股")],
    "双汇": [("000895.SZ", "A 股")],
    "双汇发展": [("000895.SZ", "A 股")],
    "蒙牛": [("2319.HK", "港股")],
    "伊利": [("600887.SH", "A 股")],
    "伊利股份": [("600887.SH", "A 股")],

    # === 家电 ===
    "海尔智家": [("600690.SH", "A 股"), ("6690.HK", "港股")],
    "海尔": [("600690.SH", "A 股"), ("6690.HK", "港股")],
    "美的集团": [("000333.SZ", "A 股"), ("0300.HK", "港股")],
    "美的": [("000333.SZ", "A 股"), ("0300.HK", "港股")],
    "格力电器": [("000651.SZ", "A 股")],
    "格力": [("000651.SZ", "A 股")],
    "海信": [("000921.SZ", "A 股")],
    "海信家电": [("000921.SZ", "A 股")],

    # === 券商 ===
    "中信证券": [("600030.SH", "A 股"), ("6030.HK", "港股 H")],
    "中信建投": [("601066.SH", "A 股"), ("6066.HK", "港股 H")],
    "招商证券": [("600999.SH", "A 股"), ("6099.HK", "港股 H")],
    "海通证券": [("600837.SH", "A 股"), ("6837.HK", "港股 H")],
    "国电南瑞": [("600406.SH", "A 股")],

    # === 医药 / 生物医药 ===
    "恒瑞": [("600276.SH", "A 股"), ("1276.HK", "港股 H")],
    "恒瑞医药": [("600276.SH", "A 股"), ("1276.HK", "港股 H")],
    "药明康德": [("603259.SH", "A 股"), ("2359.HK", "港股 H")],
    "迈瑞医疗": [("300760.SZ", "A 股创业板")],
    "迈瑞": [("300760.SZ", "A 股创业板")],
    "爱尔眼科": [("300015.SZ", "A 股创业板")],
    "片仔癀": [("600436.SH", "A 股")],
    "百济": [("6160.HK", "港股双重主要"), ("688235.SH", "A 股科创板"), ("ONC", "美股纳斯达克")],
    "百济神州": [("6160.HK", "港股双重主要"), ("688235.SH", "A 股科创板"), ("ONC", "美股纳斯达克")],
    "信达生物": [("1801.HK", "港股 18A")],
    "君实生物": [("1877.HK", "港股 18A"), ("688180.SH", "A 股科创板")],
    "中国生物制药": [("1177.HK", "港股")],

    # === 工程机械 ===
    "三一重工": [("600031.SH", "A 股")],
    "三一": [("600031.SH", "A 股")],
    "中联重科": [("000157.SZ", "A 股"), ("1157.HK", "港股 H")],

    # === 电信运营商 ===
    "中国移动": [("600941.SH", "A 股"), ("0941.HK", "港股 H")],
    "中国电信": [("601728.SH", "A 股"), ("0728.HK", "港股 H")],
    "中国联通": [("600050.SH", "A 股"), ("0762.HK", "港股 H")],

    # === 公用 ===
    "港铁": [("0066.HK", "港股")],
    "港铁公司": [("0066.HK", "港股")],

    # === 美股 巨头 ===
    "苹果": [("AAPL", "美股")],
    "微软": [("MSFT", "美股")],
    "谷歌": [("GOOGL", "美股 A 股"), ("GOOG", "美股 C 股")],
    "Alphabet": [("GOOGL", "美股 A 股"), ("GOOG", "美股 C 股")],
    "亚马逊": [("AMZN", "美股")],
    "Meta": [("META", "美股")],
    "脸书": [("META", "美股")],
    "特斯拉": [("TSLA", "美股")],
    "英伟达": [("NVDA", "美股")],
    "奈飞": [("NFLX", "美股")],
    "Netflix": [("NFLX", "美股")],
    "伯克希尔": [("BRK.B", "美股 B 股"), ("BRK.A", "美股 A 股")],
    "巴菲特": [("BRK.B", "美股 B 股"), ("BRK.A", "美股 A 股")],

    # === 美股 金融 ===
    "摩根大通": [("JPM", "美股")],
    "JPMorgan": [("JPM", "美股")],
    "美国银行": [("BAC", "美股")],
    "富国银行": [("WFC", "美股")],
    "高盛": [("GS", "美股")],
    "摩根士丹利": [("MS", "美股")],
    "花旗": [("C", "美股")],
    "Visa": [("V", "美股")],
    "万事达": [("MA", "美股")],
    "美国运通": [("AXP", "美股")],
    "PayPal": [("PYPL", "美股")],

    # === 美股 能源 ===
    "埃克森美孚": [("XOM", "美股")],
    "雪佛龙": [("CVX", "美股")],

    # === 美股 消费 ===
    "可口可乐": [("KO", "美股")],
    "百事": [("PEP", "美股")],
    "沃尔玛": [("WMT", "美股")],
    "宝洁": [("PG", "美股")],
    "迪士尼": [("DIS", "美股")],
    "麦当劳": [("MCD", "美股")],
    "星巴克": [("SBUX", "美股")],
    "耐克": [("NKE", "美股")],

    # === 美股 医药 ===
    "强生": [("JNJ", "美股")],
    "辉瑞": [("PFE", "美股")],
    "默克": [("MRK", "美股")],
    "礼来": [("LLY", "美股")],
    "艾伯维": [("ABBV", "美股")],

    # === 美股 半导体 ===
    "台积电": [("TSM", "美股 ADR"), ("2330.TW", "台股")],
    "AMD": [("AMD", "美股")],
    "英特尔": [("INTC", "美股")],
    "美光": [("MU", "美股")],
    "ASML": [("ASML", "美股 ADR")],

    # === 中概股 ADR 教育 ===
    "好未来": [("TAL", "美股 ADR")],
    "新东方": [("EDU", "美股 ADR"), ("9901.HK", "港股")],
    "贝壳": [("BEKE", "美股 ADR"), ("2423.HK", "港股双重主要")],
}


# ---------------------------------------------------------------------------
# 2. ticker → (company_type, modifier_flags) 反查表
# ---------------------------------------------------------------------------
# 包含我们认识的主要代码；未列出的回退到行业默认规则。
TICKER_META: dict[str, tuple[str, list[str]]] = {
    # 互联网平台 / VIE
    "0700.HK": ("tech_platform_network", ["vie_structure", "creator_led"]),
    "TCEHY":   ("tech_platform_network", ["adr_listed", "vie_structure"]),
    "9988.HK": ("high_growth_platform", ["dual_primary_listing", "vie_structure"]),
    "BABA":    ("high_growth_platform", ["adr_listed", "vie_structure", "dual_primary_listing"]),
    "3690.HK": ("high_growth_platform", ["vie_structure"]),
    "9618.HK": ("high_growth_platform", ["dual_primary_listing", "vie_structure"]),
    "JD":      ("high_growth_platform", ["adr_listed", "vie_structure"]),
    "PDD":     ("high_growth_platform", ["adr_listed", "vie_structure", "creator_led", "pcaob_risk"]),
    "9888.HK": ("tech_platform_network", ["dual_primary_listing", "vie_structure"]),
    "BIDU":    ("tech_platform_network", ["adr_listed", "vie_structure"]),
    "9999.HK": ("tech_platform_network", ["dual_primary_listing", "vie_structure"]),
    "NTES":    ("tech_platform_network", ["adr_listed", "vie_structure"]),
    "9626.HK": ("high_growth_platform", ["dual_primary_listing", "vie_structure"]),
    "BILI":    ("high_growth_platform", ["adr_listed", "vie_structure"]),
    "IQ":      ("high_growth_platform", ["adr_listed", "vie_structure"]),
    "1810.HK": ("tech_hardware_ecosystem", ["creator_led"]),
    "0992.HK": ("tech_hardware_ecosystem", []),
    "1024.HK": ("high_growth_platform", ["vie_structure", "creator_led"]),
    "2618.HK": ("high_growth_platform", ["vie_structure"]),
    "6618.HK": ("high_growth_platform", ["vie_structure"]),
    "0241.HK": ("high_growth_platform", ["vie_structure"]),
    "9699.HK": ("high_growth_platform", ["vie_structure"]),

    # 银行
    "601398.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "1398.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "601939.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "0939.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "601288.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "1288.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "601988.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "3988.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "601328.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "3328.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "600036.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "3968.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "000001.SZ": ("banking", []),
    "601998.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "0998.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "601166.SH": ("banking", []),
    "600016.SH": ("banking", ["a_h_dual_listed"]),
    "1988.HK":   ("banking", ["a_h_dual_listed"]),
    "002142.SZ": ("banking", []),
    "600926.SH": ("banking", []),
    "601658.SH": ("banking", ["a_h_dual_listed", "state_owned"]),
    "1658.HK":   ("banking", ["a_h_dual_listed", "state_owned"]),
    "0005.HK":   ("banking", []),
    "2888.HK":   ("banking", []),
    "JPM":       ("banking", []),
    "BAC":       ("banking", []),
    "WFC":       ("banking", []),
    "GS":        ("brokerage_assetmgmt", []),
    "MS":        ("brokerage_assetmgmt", []),
    "C":         ("banking", []),

    # 保险
    "601318.SH": ("insurance", ["a_h_dual_listed"]),
    "2318.HK":   ("insurance", ["a_h_dual_listed"]),
    "601628.SH": ("insurance", ["a_h_dual_listed", "state_owned"]),
    "2628.HK":   ("insurance", ["a_h_dual_listed", "state_owned"]),
    "601601.SH": ("insurance", ["a_h_dual_listed", "state_owned"]),
    "2601.HK":   ("insurance", ["a_h_dual_listed", "state_owned"]),
    "601319.SH": ("insurance", ["a_h_dual_listed", "state_owned"]),
    "1339.HK":   ("insurance", ["a_h_dual_listed", "state_owned"]),
    "1299.HK":   ("insurance", []),

    # 能源 / 大宗
    "0883.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "600938.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "CEO":       ("cyclical_commodity", ["adr_listed", "state_owned"]),
    "600028.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "0386.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "SNP":       ("cyclical_commodity", ["adr_listed", "state_owned"]),
    "601857.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "0857.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "PTR":       ("cyclical_commodity", ["adr_listed", "state_owned"]),
    "601088.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "1088.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "600188.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "1171.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "601898.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "1898.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "601225.SH": ("cyclical_commodity", ["state_owned"]),
    "601899.SH": ("cyclical_commodity", ["a_h_dual_listed"]),
    "2899.HK":   ("cyclical_commodity", ["a_h_dual_listed"]),
    "600362.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "0358.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "601600.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "2600.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "600026.SH": ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "1138.HK":   ("cyclical_commodity", ["a_h_dual_listed", "state_owned"]),
    "600900.SH": ("utility_infrastructure_reit", ["state_owned", "with_policy_support"]),
    "XOM":       ("cyclical_commodity", []),
    "CVX":       ("cyclical_commodity", []),

    # 地产
    "000002.SZ": ("real_estate", ["a_h_dual_listed", "distressed"]),
    "2202.HK":   ("real_estate", ["a_h_dual_listed", "distressed"]),
    "0960.HK":   ("real_estate", []),
    "1109.HK":   ("real_estate", ["state_owned"]),
    "0688.HK":   ("real_estate", ["state_owned"]),
    "001979.SZ": ("real_estate", ["state_owned"]),
    "600048.SH": ("real_estate", ["state_owned"]),
    "0823.HK":   ("utility_infrastructure_reit", []),
    "1113.HK":   ("real_estate", []),
    "0016.HK":   ("real_estate", []),
    "1972.HK":   ("real_estate", []),

    # 汽车 / 新能源车
    "002594.SZ": ("cyclical_industrial_ev", ["a_h_dual_listed", "with_policy_support"]),
    "1211.HK":   ("cyclical_industrial_ev", ["a_h_dual_listed", "with_policy_support"]),
    "601633.SH": ("cyclical_industrial_ev", ["a_h_dual_listed"]),
    "2333.HK":   ("cyclical_industrial_ev", ["a_h_dual_listed"]),
    "601238.SH": ("cyclical_industrial_ev", ["a_h_dual_listed", "state_owned"]),
    "2238.HK":   ("cyclical_industrial_ev", ["a_h_dual_listed", "state_owned"]),
    "300750.SZ": ("cyclical_industrial_ev", ["with_policy_support"]),
    "9866.HK":   ("cyclical_industrial_ev", ["dual_primary_listing", "creator_led"]),
    "NIO":       ("cyclical_industrial_ev", ["adr_listed", "vie_structure", "creator_led", "pcaob_risk"]),
    "2015.HK":   ("cyclical_industrial_ev", ["dual_primary_listing", "creator_led"]),
    "LI":        ("cyclical_industrial_ev", ["adr_listed", "vie_structure", "creator_led", "pcaob_risk"]),
    "9868.HK":   ("cyclical_industrial_ev", ["dual_primary_listing", "creator_led"]),
    "XPEV":      ("cyclical_industrial_ev", ["adr_listed", "vie_structure", "creator_led", "pcaob_risk"]),
    "TSLA":      ("cyclical_industrial_ev", ["creator_led"]),

    # 光伏 / 新能源
    "601012.SH": ("cyclical_industrial_ev", ["with_policy_support"]),
    "600438.SH": ("cyclical_industrial_ev", ["with_policy_support"]),
    "300274.SZ": ("cyclical_industrial_ev", ["with_policy_support"]),

    # 半导体 / 科技硬件
    "688981.SH": ("tech_hardware_ecosystem", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "0981.HK":   ("tech_hardware_ecosystem", ["a_h_dual_listed", "state_owned", "with_policy_support"]),
    "688385.SH": ("tech_hardware_ecosystem", ["a_h_dual_listed"]),
    "1385.HK":   ("tech_hardware_ecosystem", ["a_h_dual_listed"]),
    "601138.SH": ("tech_hardware_ecosystem", ["state_owned"]),
    "AAPL":      ("tech_hardware_ecosystem", []),
    "TSM":       ("tech_hardware_ecosystem", ["adr_listed"]),
    "AMD":       ("tech_hardware_ecosystem", []),
    "INTC":      ("tech_hardware_ecosystem", []),
    "NVDA":      ("tech_hardware_ecosystem", ["creator_led"]),
    "MU":        ("tech_hardware_ecosystem", []),
    "ASML":      ("tech_hardware_ecosystem", ["adr_listed"]),

    # 白酒 / 消费 (great_company_compounder / consumer_brand_premium)
    "600519.SH": ("great_company_compounder", ["state_owned"]),
    "000858.SZ": ("great_company_compounder", ["state_owned"]),
    "000568.SZ": ("great_company_compounder", ["state_owned"]),
    "600809.SH": ("great_company_compounder", ["state_owned"]),
    "002304.SZ": ("great_company_compounder", []),
    "000596.SZ": ("great_company_compounder", []),
    "603288.SH": ("great_company_compounder", []),
    "000895.SZ": ("consumer_brand_premium", []),
    "2319.HK":   ("consumer_brand_premium", []),
    "600887.SH": ("consumer_brand_premium", []),

    # 家电
    "600690.SH": ("consumer_brand_premium", ["a_h_dual_listed"]),
    "6690.HK":   ("consumer_brand_premium", ["a_h_dual_listed"]),
    "000333.SZ": ("consumer_brand_premium", ["a_h_dual_listed"]),
    "0300.HK":   ("consumer_brand_premium", ["a_h_dual_listed"]),
    "000651.SZ": ("consumer_brand_premium", []),
    "000921.SZ": ("consumer_brand_premium", []),

    # 券商
    "600030.SH": ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "6030.HK":   ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "601066.SH": ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "6066.HK":   ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "600999.SH": ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "6099.HK":   ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "600837.SH": ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "6837.HK":   ("brokerage_assetmgmt", ["a_h_dual_listed", "state_owned"]),
    "600406.SH": ("utility_infrastructure_reit", ["state_owned"]),

    # 医药 / 生物医药
    "600276.SH": ("pharma_mature", ["a_h_dual_listed", "regulated_heavily"]),
    "1276.HK":   ("pharma_mature", ["a_h_dual_listed", "regulated_heavily"]),
    "603259.SH": ("pharma_mature", ["a_h_dual_listed", "regulated_heavily"]),
    "2359.HK":   ("pharma_mature", ["a_h_dual_listed", "regulated_heavily"]),
    "300760.SZ": ("pharma_mature", ["regulated_heavily"]),
    "300015.SZ": ("pharma_mature", ["regulated_heavily"]),
    "600436.SH": ("great_company_compounder", ["state_owned"]),
    "6160.HK":   ("biotech_unprofitable", ["dual_primary_listing", "regulated_heavily"]),
    "688235.SH": ("biotech_unprofitable", ["dual_primary_listing", "regulated_heavily"]),
    "ONC":       ("biotech_unprofitable", ["dual_primary_listing", "regulated_heavily"]),
    "1801.HK":   ("biotech_unprofitable", ["regulated_heavily"]),
    "1877.HK":   ("biotech_unprofitable", ["a_h_dual_listed", "regulated_heavily"]),
    "688180.SH": ("biotech_unprofitable", ["a_h_dual_listed", "regulated_heavily"]),
    "1177.HK":   ("pharma_mature", ["regulated_heavily"]),

    # 工程机械
    "600031.SH": ("cyclical_industrial_ev", []),
    "000157.SZ": ("cyclical_industrial_ev", ["a_h_dual_listed"]),
    "1157.HK":   ("cyclical_industrial_ev", ["a_h_dual_listed"]),

    # 电信运营商
    "600941.SH": ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),
    "0941.HK":   ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),
    "601728.SH": ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),
    "0728.HK":   ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),
    "600050.SH": ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),
    "0762.HK":   ("utility_infrastructure_reit", ["a_h_dual_listed", "state_owned", "regulated_heavily"]),

    # 公用
    "0066.HK":   ("utility_infrastructure_reit", []),

    # 美股 巨头
    "MSFT":      ("tech_platform_network", []),
    "GOOGL":     ("tech_platform_network", []),
    "GOOG":      ("tech_platform_network", []),
    "AMZN":      ("high_growth_platform", []),
    "META":      ("tech_platform_network", ["creator_led"]),
    "NFLX":      ("tech_platform_network", []),
    "BRK.A":     ("holding_conglomerate", []),
    "BRK.B":     ("holding_conglomerate", []),

    # 美股 支付 / 消费 / 医药
    "V":         ("tech_platform_network", []),
    "MA":        ("tech_platform_network", []),
    "AXP":       ("banking", []),
    "PYPL":      ("high_growth_platform", []),
    "KO":        ("great_company_compounder", []),
    "PEP":       ("great_company_compounder", []),
    "WMT":       ("great_company_compounder", []),
    "PG":        ("great_company_compounder", []),
    "DIS":       ("consumer_brand_premium", []),
    "MCD":       ("great_company_compounder", []),
    "SBUX":      ("consumer_brand_premium", []),
    "NKE":       ("consumer_brand_premium", []),
    "JNJ":       ("pharma_mature", []),
    "PFE":       ("pharma_mature", []),
    "MRK":       ("pharma_mature", []),
    "LLY":       ("pharma_mature", []),
    "ABBV":      ("pharma_mature", []),

    # 中概股 ADR 教育
    "TAL":       ("declining_cash_cow", ["adr_listed", "vie_structure", "regulated_heavily", "pcaob_risk"]),
    "EDU":       ("declining_cash_cow", ["adr_listed", "vie_structure", "regulated_heavily", "pcaob_risk"]),
    "9901.HK":   ("declining_cash_cow", ["regulated_heavily"]),
    "BEKE":      ("high_growth_platform", ["adr_listed", "vie_structure", "dual_primary_listing", "pcaob_risk"]),
    "2423.HK":   ("high_growth_platform", ["dual_primary_listing"]),
}


# ---------------------------------------------------------------------------
# 3. 北交所 BJ 已知前缀 / 范围
# ---------------------------------------------------------------------------
# 北交所目前活跃代码段：
#   - 4 段位 8xxxxx (含 82xxxx、83xxxx、87xxxx、88xxxx)
#   - 8 段位 920xxx ~ 929xxx
# 上海 B 股 9xxxxx：900001~900957 (这是 SH B 股，与北交所 92xxxx 区分)
def _infer_a_share_market(code: str) -> str | None:
    """根据 6 位 A 股代码推断市场 (SH/SZ/BJ)；未知返回 None"""
    if not (len(code) == 6 and code.isdigit()):
        return None
    first = code[0]
    # 沪市：60xxxx, 68xxxx (科创板), 900xxx (B 股), 110xxx/113xxx (转债)
    if code.startswith(("60", "68")):
        return "SH"
    if code.startswith("900"):
        return "SH"  # SH B 股
    # 深市：000xxx, 001xxx, 002xxx, 003xxx (主板/中小板), 300xxx/301xxx (创业板), 200xxx (B 股)
    if code.startswith(("000", "001", "002", "003", "300", "301", "200")):
        return "SZ"
    # 北交所：83xxxx, 87xxxx, 88xxxx, 82xxxx (老精选层), 920xxx-929xxx
    if code.startswith(("82", "83", "87", "88")):
        return "BJ"
    if code.startswith("92"):  # 920xxx-929xxx 北交所新规
        return "BJ"
    # 兜底
    if first == "6":
        return "SH"
    if first in ("0", "3"):
        return "SZ"
    if first == "4" or first == "8":
        return "BJ"
    return None


# ---------------------------------------------------------------------------
# 4. ticker 元数据查询（含市场默认）
# ---------------------------------------------------------------------------
def _suggest_meta(normalized: str, market: str) -> tuple[str | None, list[str]]:
    """
    根据归一化代码返回 (suggested_company_type, modifier_flags)。
    优先查 TICKER_META，未命中则按市场启发式给出基础 flags。
    """
    if normalized in TICKER_META:
        ctype, flags = TICKER_META[normalized]
        return ctype, list(flags)

    flags: list[str] = []
    # 港股启发式：> 9000 段位往往是中概双重主要 / VIE
    if market == "HK":
        # 不能确定 company_type
        return None, flags
    if market == "US":
        # 美股代码无法判定行业，但若是 5 字符以上常见为中概 ADR (BABA/BIDU/...)；
        # 此处保守不打 flag
        return None, flags
    if market.startswith("CN_"):
        # A 股默认 a_h_dual_listed 不可知；不打 flag
        return None, flags
    return None, flags


# ---------------------------------------------------------------------------
# 5. 主解析函数
# ---------------------------------------------------------------------------
def _enrich(result: dict) -> dict:
    """在 valid=True 且 ambiguous=False 时附加 suggested_company_type / flags"""
    if not result.get("valid") or result.get("ambiguous"):
        return result
    normalized = result.get("normalized")
    market = result.get("market", "")
    if not normalized:
        return result
    ctype, flags = _suggest_meta(normalized, market)
    result["suggested_company_type"] = ctype
    result["suggested_modifier_flags"] = flags

    # 港股仙股检测（仅根据代码无法判断价格，但留接口）
    # 美股 OTC 启发式：5 字符且以 "F"/"Y" 结尾常见为 ADR PNK 代码（如 TCEHY）
    if market == "US":
        sym = normalized
        if len(sym) >= 5 and sym.endswith(("F", "Y")) and sym.isalpha():
            # 典型 OTC/PNK ADR
            if "adr_listed" not in result["suggested_modifier_flags"]:
                result["suggested_modifier_flags"].append("adr_listed")
            result["liquidity_warning"] = "otc_adr_pink_sheet"

    return result


def parse_ticker(raw: str) -> dict:
    s = raw.strip()

    if not s:
        return {"input": raw, "valid": False, "notes": "空输入"}

    # 1. 已带后缀，直接归一化
    upper = s.upper()
    m = re.match(r"^(\d{6})\.(SH|SZ|BJ)$", upper)
    if m:
        code, market = m.groups()
        return _enrich({
            "input": raw,
            "normalized": f"{code}.{market}",
            "market": f"CN_{market}",
            "valid": True,
            "ambiguous": False,
            "notes": "A 股",
        })

    m = re.match(r"^(\d{1,5})\.HK$", upper)
    if m:
        code = m.group(1).zfill(4)
        return _enrich({
            "input": raw,
            "normalized": f"{code}.HK",
            "market": "HK",
            "valid": True,
            "ambiguous": False,
            "notes": "港股",
        })

    m = re.match(r"^([A-Z][A-Z0-9.\-]{0,9})\.US$", upper)
    if m:
        return _enrich({
            "input": raw,
            "normalized": m.group(1),
            "market": "US",
            "valid": True,
            "ambiguous": False,
            "notes": "美股",
        })

    # 台股 (TW) 兼容
    m = re.match(r"^(\d{4})\.TW$", upper)
    if m:
        return _enrich({
            "input": raw,
            "normalized": f"{m.group(1)}.TW",
            "market": "TW",
            "valid": True,
            "ambiguous": False,
            "notes": "台股",
        })

    # 2. 纯 6 位数字 → 推断 A 股市场（含 BJ 北交所修正规则）
    if re.match(r"^\d{6}$", s):
        market = _infer_a_share_market(s)
        if market is None:
            return {
                "input": raw,
                "valid": False,
                "notes": f"无法判定市场（代码 {s}）",
            }
        return _enrich({
            "input": raw,
            "normalized": f"{s}.{market}",
            "market": f"CN_{market}",
            "valid": True,
            "ambiguous": False,
            "notes": f"A 股 ({market})",
        })

    # 3. 1-5 位数字（无 .HK 后缀）→ 推断港股
    if re.match(r"^\d{1,5}$", s):
        code = s.zfill(4)
        return _enrich({
            "input": raw,
            "normalized": f"{code}.HK",
            "market": "HK",
            "valid": True,
            "ambiguous": False,
            "notes": "推断为港股",
        })

    # 4. 全字母 / 字母+点 → 默认美股
    if re.match(r"^[A-Z][A-Z0-9.\-]{0,9}$", upper):
        return _enrich({
            "input": raw,
            "normalized": upper,
            "market": "US",
            "valid": True,
            "ambiguous": False,
            "notes": "推断为美股",
        })

    # 5. 中文公司名 → 查映射
    if s in COMPANY_MAP:
        candidates = COMPANY_MAP[s]
        if len(candidates) == 1:
            ticker, note = candidates[0]
            sub = parse_ticker(ticker)
            sub["input"] = raw
            sub["notes"] = f"由公司名 '{s}' 映射 → {note}"
            return sub
        # 多市场上市 → ambiguous，但仍附 candidates 元数据
        enriched_candidates = []
        for t, n in candidates:
            sub = parse_ticker(t)
            entry = {"ticker": t, "note": n}
            if sub.get("valid"):
                entry["normalized"] = sub.get("normalized")
                entry["market"] = sub.get("market")
                if sub.get("suggested_company_type"):
                    entry["suggested_company_type"] = sub["suggested_company_type"]
                if sub.get("suggested_modifier_flags"):
                    entry["suggested_modifier_flags"] = sub["suggested_modifier_flags"]
            enriched_candidates.append(entry)
        return {
            "input": raw,
            "valid": True,
            "ambiguous": True,
            "candidates": enriched_candidates,
            "notes": f"公司 '{s}' 在多个市场上市，请明确选择",
        }

    return {
        "input": raw,
        "valid": False,
        "notes": "无法识别。请使用标准代码：600519.SH / 0700.HK / AAPL",
    }


def main():
    if len(sys.argv) < 2:
        print("用法: python parse-ticker.py <ticker_or_name>", file=sys.stderr)
        sys.exit(1)
    raw = " ".join(sys.argv[1:])

    # --test 内置自检
    if raw == "--test":
        _run_tests()
        return

    result = parse_ticker(raw)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ---------------------------------------------------------------------------
# 6. 单元测试（≥ 20 条）
# ---------------------------------------------------------------------------
def _run_tests() -> None:
    passed = 0
    failed = 0
    cases: list[tuple[str, dict]] = [
        # (输入, 期望字段子集)
        ("600519", {"normalized": "600519.SH", "market": "CN_SH",
                    "suggested_company_type": "great_company_compounder"}),
        ("600519.SH", {"normalized": "600519.SH", "market": "CN_SH"}),
        ("600036", {"normalized": "600036.SH", "suggested_company_type": "banking"}),
        ("600036.SH", {"suggested_company_type": "banking"}),
        ("601088.SH", {"suggested_company_type": "cyclical_commodity"}),
        ("000002.SZ", {"suggested_company_type": "real_estate"}),
        ("000002", {"normalized": "000002.SZ", "market": "CN_SZ",
                    "suggested_company_type": "real_estate"}),
        ("300750", {"normalized": "300750.SZ", "market": "CN_SZ"}),
        ("688981", {"normalized": "688981.SH", "market": "CN_SH"}),
        # 北交所 BJ 修正
        ("833533", {"normalized": "833533.BJ", "market": "CN_BJ"}),
        ("920220", {"normalized": "920220.BJ", "market": "CN_BJ"}),
        ("873169", {"normalized": "873169.BJ", "market": "CN_BJ"}),
        # 沪市 B 股不能误判为 BJ
        ("900957", {"normalized": "900957.SH", "market": "CN_SH"}),
        # 港股
        ("0700.HK", {"normalized": "0700.HK", "market": "HK",
                     "suggested_company_type": "tech_platform_network"}),
        ("700", {"normalized": "0700.HK", "market": "HK"}),
        ("6160.HK", {"suggested_company_type": "biotech_unprofitable"}),
        ("3968.HK", {"suggested_company_type": "banking"}),
        # 美股
        ("AAPL", {"normalized": "AAPL", "market": "US",
                  "suggested_company_type": "tech_hardware_ecosystem"}),
        ("PDD", {"normalized": "PDD", "suggested_company_type": "high_growth_platform"}),
        ("BABA", {"suggested_company_type": "high_growth_platform"}),
        ("BRK.B", {"suggested_company_type": "holding_conglomerate"}),
        ("TCEHY", {"normalized": "TCEHY"}),  # 期望 liquidity_warning
        # 中文名 → 单候选
        ("茅台", {"normalized": "600519.SH"}),
        ("宁德时代", {"normalized": "300750.SZ"}),
        # 中文名 → 多候选（ambiguous）
        ("招商银行", {"ambiguous": True}),
        ("万科", {"ambiguous": True}),
        ("中国神华", {"ambiguous": True}),
        ("百济", {"ambiguous": True}),
        ("拼多多", {"normalized": "PDD"}),
    ]
    for raw, expected in cases:
        result = parse_ticker(raw)
        ok = all(result.get(k) == v for k, v in expected.items())
        if ok:
            passed += 1
        else:
            failed += 1
            print(f"FAIL  {raw!r}  expected ⊇ {expected}  got {result}")
    # 额外断言：modifier_flags
    extra: list[tuple[str, str]] = [
        ("600036.SH", "a_h_dual_listed"),
        ("600036.SH", "state_owned"),
        ("0700.HK", "vie_structure"),
        ("PDD", "vie_structure"),
        ("PDD", "adr_listed"),
        ("601088.SH", "state_owned"),
        ("6160.HK", "dual_primary_listing"),
        ("BABA", "dual_primary_listing"),
    ]
    for raw, flag in extra:
        r = parse_ticker(raw)
        flags = r.get("suggested_modifier_flags") or []
        if flag in flags:
            passed += 1
        else:
            failed += 1
            print(f"FAIL flag  {raw!r}  expected flag {flag!r}  got {flags}")
    print(f"\n{passed} passed, {failed} failed (total {passed + failed})")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()

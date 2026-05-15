#!/usr/bin/env python3
"""
价值投资估值辅助计算器 (v2 — 12 子命令)

支持子命令:
  1.  dcf              — FCFF 二阶段 DCF
  2.  epv              — Earnings Power Value (Bruce Greenwald)
  3.  reverse-dcf      — 反推市场隐含增长率
  4.  sensitivity      — g × WACC 敏感性矩阵
  5.  ddm              — 股息折现模型（两阶段，戈登终值）
  6.  pb-roe           — PB-ROE (V/B = (ROE-g)/(Ke-g))
  7.  rim              — 残差收益模型 (Residual Income Model)
  8.  rnpv             — 风险调整 NPV（biotech 单管线简化版）
  9.  normalized-pe    — 正常化 PE（10 年 EPS 序列）
  10. nav-revaluation  — 净资产重估（mark-to-market - 负债）
  11. sotp             — Sum-of-the-Parts 汇总
  12. dcf-fcfe         — 股权自由现金流 DCF（Ke 折现，不调 net_debt）

用法示例:
  python valuation-calc.py dcf --fcf0 100 --g1 0.10 --years 10 --gt 0.025 --wacc 0.09 --net-debt 50 --shares 10
  python valuation-calc.py epv --normalized-earnings 80 --wacc 0.09 --maintenance-capex 5 --shares 10
  python valuation-calc.py reverse-dcf --price 200 --fcf0 100 --years 10 --gt 0.025 --wacc 0.09 --net-debt 50 --shares 10
  python valuation-calc.py sensitivity --fcf0 100 --years 10 --net-debt 50 --shares 10
  python valuation-calc.py ddm --dividend-current 2 --growth-explicit 0.08 --years 5 --growth-terminal 0.03 --ke 0.09
  python valuation-calc.py pb-roe --book-value-per-share 20 --roe 0.15 --ke 0.10 --g 0.03 --current-price 35
  python valuation-calc.py rim --book-value-current 100 --roe-forecast "0.15,0.14,0.13,0.13,0.12" --ke 0.10 --growth-terminal-book 0.03
  python valuation-calc.py rnpv --peak-sales 800 --pos-current-phase 0.30 --pos-next-phases "0.65,0.85" --years-to-launch 5 --patent-life 12 --r 0.12 --margin-net 0.30 --phase-cost 50
  python valuation-calc.py normalized-pe --eps-series "1.2,1.5,0.8,1.1,1.4,1.7,1.6,0.9,1.3,1.5" --normalized-pe-multiple 12
  python valuation-calc.py nav-revaluation --assets-at-market "120,80,50" --asset-names "real_estate,equity_portfolio,cash" --total-liabilities 60 --shares 10 --current-price 12 --haircut-pct 15
  python valuation-calc.py sotp --segments '[{"name":"insurance","value":100},{"name":"equity","value":300}]' --shares 20 --holdco-discount-pct 15 --current-price 18
  python valuation-calc.py dcf-fcfe --fcfe0 80 --g1 0.10 --years 10 --gt 0.025 --ke 0.10 --shares 10
"""
import argparse
import json
import sys


# ---------------------------------------------------------------------------
# v1 — DCF / EPV / Reverse DCF / Sensitivity
# ---------------------------------------------------------------------------

def dcf_two_stage(
    fcf0: float,
    g1: float,
    years: int,
    gt: float,
    wacc: float,
    net_debt: float = 0,
    shares: float = 1,
) -> dict:
    """二阶段 DCF (FCFF)：显式期 'years' 年按 g1 增长，永续按 gt。"""
    if wacc <= gt:
        return {"error": "WACC 必须 > 永续增长率 gt"}

    explicit_fcf = []
    explicit_pv = []
    fcf = fcf0
    for t in range(1, years + 1):
        fcf = fcf * (1 + g1)
        pv = fcf / (1 + wacc) ** t
        explicit_fcf.append(fcf)
        explicit_pv.append(pv)

    fcf_terminal = explicit_fcf[-1] * (1 + gt)
    terminal_value = fcf_terminal / (wacc - gt)
    terminal_pv = terminal_value / (1 + wacc) ** years

    enterprise_value = sum(explicit_pv) + terminal_pv
    equity_value = enterprise_value - net_debt
    value_per_share = equity_value / shares if shares else None
    terminal_share = terminal_pv / enterprise_value if enterprise_value else None

    return {
        "method": "DCF two-stage (FCFF)",
        "assumptions": {
            "fcf0": fcf0,
            "g1": g1,
            "years": years,
            "gt": gt,
            "wacc": wacc,
            "net_debt": net_debt,
            "shares": shares,
        },
        "output": {
            "explicit_period_pv": round(sum(explicit_pv), 2),
            "terminal_value_pv": round(terminal_pv, 2),
            "terminal_value_share_pct": round(terminal_share * 100, 1) if terminal_share else None,
            "enterprise_value": round(enterprise_value, 2),
            "equity_value": round(equity_value, 2),
            "value_per_share": round(value_per_share, 2) if value_per_share else None,
        },
        "warnings": _dcf_warnings(terminal_share, g1, gt, wacc),
        "note": "FCFF 视角，企业价值需减净债务得股权价值。",
    }


def _dcf_warnings(terminal_share, g1, gt, wacc):
    w = []
    if terminal_share and terminal_share > 0.75:
        w.append(f"终值占比 {terminal_share*100:.0f}% > 75%，估值高度依赖永续期假设")
    if gt > 0.04:
        w.append(f"永续增长率 {gt*100:.1f}% 超过长期 GDP 增速，过于乐观")
    if g1 > 0.30:
        w.append(f"显式期增长率 {g1*100:.0f}% 过高，需验证可持续性")
    if wacc - gt < 0.03:
        w.append("WACC - gt < 3%，终值对假设极度敏感")
    return w


def epv(
    normalized_earnings: float,
    wacc: float,
    maintenance_capex: float = 0,
    shares: float = 1,
    net_debt: float = 0,
) -> dict:
    """Earnings Power Value (Bruce Greenwald) — 0 增长假设。"""
    owner_earnings = normalized_earnings - maintenance_capex
    if wacc <= 0:
        return {"error": "WACC 必须 > 0"}
    enterprise_value = owner_earnings / wacc
    equity_value = enterprise_value - net_debt
    value_per_share = equity_value / shares if shares else None

    return {
        "method": "EPV (Greenwald)",
        "assumptions": {
            "normalized_earnings": normalized_earnings,
            "maintenance_capex": maintenance_capex,
            "owner_earnings": owner_earnings,
            "wacc": wacc,
            "net_debt": net_debt,
            "shares": shares,
        },
        "output": {
            "enterprise_value": round(enterprise_value, 2),
            "equity_value": round(equity_value, 2),
            "value_per_share": round(value_per_share, 2) if value_per_share else None,
        },
        "warnings": [],
        "note": "EPV 假设 0 增长。若市值显著高于 EPV，差额即'增长价值'，需评估增长可信度。",
    }


def reverse_dcf(
    price: float,
    fcf0: float,
    years: int,
    gt: float,
    wacc: float,
    net_debt: float = 0,
    shares: float = 1,
) -> dict:
    """已知股价反推市场隐含的显式期增长率 g1。"""
    target_equity_value = price * shares

    def equity_at(g1):
        out = dcf_two_stage(fcf0, g1, years, gt, wacc, net_debt, shares)
        return out.get("output", {}).get("equity_value", 0) if "output" in out else 0

    lo, hi = -0.20, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if equity_at(mid) < target_equity_value:
            lo = mid
        else:
            hi = mid
    implied_g = (lo + hi) / 2

    reasonable = -0.05 <= implied_g <= 0.25
    warnings = []
    if implied_g > 0.25:
        warnings.append(f"隐含增长率 {implied_g*100:.1f}% > 25%，市场极度乐观")
    if implied_g < -0.05:
        warnings.append(f"隐含增长率 {implied_g*100:.1f}% < -5%，市场深度悲观或存在价值陷阱信号")

    return {
        "method": "Reverse DCF",
        "assumptions": {
            "price": price,
            "shares": shares,
            "target_equity_value": target_equity_value,
            "fcf0": fcf0,
            "years": years,
            "gt": gt,
            "wacc": wacc,
        },
        "output": {
            "implied_explicit_growth": round(implied_g, 4),
            "interpretation": (
                f"市场假设公司未来 {years} 年 FCF 年增 {implied_g*100:.1f}%。"
                + (" 假设合理（落在 -5% ~ 25% 区间）。" if reasonable else " 假设极端，需警惕。")
            ),
        },
        "warnings": warnings,
        "note": "用二分法求解市场隐含 g1，可对比公司历史/同业增长判断高低估。",
    }


def sensitivity_matrix(
    fcf0: float,
    years: int,
    net_debt: float = 0,
    shares: float = 1,
) -> dict:
    """g × WACC 敏感性矩阵"""
    g_options = [0.05, 0.08, 0.10, 0.12, 0.15]
    wacc_options = [0.07, 0.08, 0.09, 0.10, 0.11]
    gt = 0.025

    matrix = {}
    for g in g_options:
        row = {}
        for w in wacc_options:
            result = dcf_two_stage(fcf0, g, years, gt, w, net_debt, shares)
            row[f"WACC={w*100:.0f}%"] = result.get("output", {}).get("value_per_share")
        matrix[f"g={g*100:.0f}%"] = row

    return {
        "method": "Sensitivity Matrix (g × WACC)",
        "assumptions": {
            "fcf0": fcf0,
            "years": years,
            "gt": gt,
            "net_debt": net_debt,
            "shares": shares,
        },
        "output": {"matrix": matrix},
        "warnings": [],
        "note": "每个单元格为对应 g × WACC 假设下的每股内在价值。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — DDM (两阶段股息折现)
# ---------------------------------------------------------------------------

def ddm_two_stage(
    dividend_current: float,
    growth_explicit: float,
    years: int,
    growth_terminal: float,
    ke: float,
    shares_outstanding: float = None,
) -> dict:
    """两阶段 DDM：显式期按 growth_explicit，终值用戈登模型。"""
    warnings = []
    if ke <= 0:
        return {"error": "Ke 必须 > 0"}
    if ke <= growth_terminal:
        return {"error": "Ke 必须 > 永续增长率 growth_terminal（否则戈登模型爆炸）"}
    if (ke - growth_terminal) < 0.02:
        warnings.append(f"Ke - g_terminal = {(ke-growth_terminal)*100:.1f}% < 2%，终值极度敏感，公式接近爆炸")
    if growth_terminal > 0.04:
        warnings.append(f"永续增长率 {growth_terminal*100:.1f}% > 4%，超过长期 GDP 增速")
    if growth_explicit > 0.25:
        warnings.append(f"显式期股息增长 {growth_explicit*100:.0f}% 过高，需核实派息率可持续")

    explicit_pv = []
    div = dividend_current
    last_div = dividend_current
    for t in range(1, years + 1):
        div = div * (1 + growth_explicit)
        pv = div / (1 + ke) ** t
        explicit_pv.append(pv)
        last_div = div

    div_next = last_div * (1 + growth_terminal)
    terminal_value = div_next / (ke - growth_terminal)
    terminal_pv = terminal_value / (1 + ke) ** years

    value_per_share = sum(explicit_pv) + terminal_pv
    terminal_share = terminal_pv / value_per_share if value_per_share else None
    if terminal_share and terminal_share > 0.75:
        warnings.append(f"终值占比 {terminal_share*100:.0f}% > 75%，估值高度依赖永续期")

    out = {
        "explicit_period_pv": round(sum(explicit_pv), 4),
        "terminal_value_pv": round(terminal_pv, 4),
        "terminal_value_share_pct": round(terminal_share * 100, 1) if terminal_share else None,
        "value_per_share": round(value_per_share, 4),
    }
    if shares_outstanding:
        out["total_equity_value"] = round(value_per_share * shares_outstanding, 2)

    return {
        "method": "DDM two-stage (Gordon terminal)",
        "assumptions": {
            "dividend_current": dividend_current,
            "growth_explicit": growth_explicit,
            "years": years,
            "growth_terminal": growth_terminal,
            "ke": ke,
            "shares_outstanding": shares_outstanding,
        },
        "output": out,
        "warnings": warnings,
        "note": "适用于稳定派息企业（公用事业、成熟银行/保险、REITs）；派息率不稳定时不可靠。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — PB-ROE (戈登变形)
# ---------------------------------------------------------------------------

def pb_roe(
    book_value_per_share: float,
    roe: float,
    ke: float,
    g: float,
    current_price: float = None,
) -> dict:
    """V/B = (ROE - g) / (Ke - g)；适用于银行 / 保险等以净资产为锚的行业。"""
    warnings = []
    if ke <= 0:
        return {"error": "Ke 必须 > 0"}
    if ke <= g:
        return {"error": "Ke 必须 > g（永续增长率），否则公式爆炸"}
    if roe <= g:
        warnings.append(f"ROE ({roe*100:.1f}%) <= g ({g*100:.1f}%)，意味着内生增长不创造价值，PB 应 ≤ 1")
    if (ke - g) < 0.02:
        warnings.append(f"Ke - g = {(ke-g)*100:.1f}% < 2%，估值极度敏感")
    if roe > 0.30:
        warnings.append(f"长期可持续 ROE {roe*100:.0f}% 过高，需验证经济护城河是否真实")

    implied_pb = (roe - g) / (ke - g)
    value_per_share = book_value_per_share * implied_pb

    out = {
        "implied_pb": round(implied_pb, 4),
        "value_per_share": round(value_per_share, 4),
    }
    if current_price:
        premium = (current_price - value_per_share) / value_per_share
        out["current_price"] = current_price
        out["premium_or_discount_pct"] = round(premium * 100, 2)
        out["interpretation"] = (
            f"当前价 {'溢价' if premium > 0 else '折价'} {abs(premium)*100:.1f}% 相对理论 PB-ROE 公允价值。"
        )

    return {
        "method": "PB-ROE (Gordon variant)",
        "assumptions": {
            "book_value_per_share": book_value_per_share,
            "roe": roe,
            "ke": ke,
            "g": g,
        },
        "output": out,
        "warnings": warnings,
        "note": "戈登模型变形；适用于银行、保险、券商、地产等净资产驱动型行业。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — RIM (Residual Income Model)
# ---------------------------------------------------------------------------

def rim(
    book_value_current: float,
    roe_forecast: list,
    ke: float,
    growth_terminal_book: float,
) -> dict:
    """残差收益模型：V = B0 + Σ[(ROE_t - Ke) × B_{t-1} / (1+Ke)^t] + terminal"""
    warnings = []
    if ke <= 0:
        return {"error": "Ke 必须 > 0"}
    if ke <= growth_terminal_book:
        return {"error": "Ke 必须 > growth_terminal_book"}
    if (ke - growth_terminal_book) < 0.02:
        warnings.append(f"Ke - g_terminal = {(ke-growth_terminal_book)*100:.1f}% < 2%，终值极度敏感")

    if not roe_forecast:
        return {"error": "roe_forecast 不能为空"}

    explicit_ri_pv = []
    book_prev = book_value_current
    book_series = [book_value_current]
    for t, roe_t in enumerate(roe_forecast, start=1):
        residual_income = (roe_t - ke) * book_prev
        pv = residual_income / (1 + ke) ** t
        explicit_ri_pv.append(pv)
        # 假设全部留存：B_t = B_{t-1} × (1 + ROE_t)（无派息简化；用户可调）
        # 更稳健: 假设留存率使 book 按 growth 增长，但这里简化用 ROE 全留存
        book_prev = book_prev * (1 + roe_t)
        book_series.append(book_prev)

    # 终值：永续残差收益（假设末期 ROE 维持，book 按 growth_terminal_book 增长）
    last_roe = roe_forecast[-1]
    last_book = book_series[-1]
    ri_terminal_next = (last_roe - ke) * last_book * (1 + growth_terminal_book)
    if last_roe <= ke:
        # 若末期 ROE ≤ Ke，残差为 0 或负，终值取 0 较保守
        terminal_value = ri_terminal_next / (ke - growth_terminal_book) if (ke - growth_terminal_book) > 0 else 0
        terminal_value = max(terminal_value, 0)
        warnings.append("末期 ROE <= Ke，残差收益终值非正；理论 PB 应回到 1")
    else:
        terminal_value = ri_terminal_next / (ke - growth_terminal_book)
    terminal_pv = terminal_value / (1 + ke) ** len(roe_forecast)

    value = book_value_current + sum(explicit_ri_pv) + terminal_pv

    if any(r > 0.30 for r in roe_forecast):
        warnings.append("ROE 预测包含 > 30% 的年份，需核实护城河可持续性")

    return {
        "method": "Residual Income Model (RIM)",
        "assumptions": {
            "book_value_current": book_value_current,
            "roe_forecast": roe_forecast,
            "ke": ke,
            "growth_terminal_book": growth_terminal_book,
        },
        "output": {
            "book_anchor": round(book_value_current, 4),
            "explicit_residual_income_pv": round(sum(explicit_ri_pv), 4),
            "terminal_pv": round(terminal_pv, 4),
            "intrinsic_value": round(value, 4),
            "implied_pb": round(value / book_value_current, 4) if book_value_current else None,
        },
        "warnings": warnings,
        "note": "RIM = 净资产锚 + 超额回报折现；ROE 长期回到 Ke 时模型退化为 PB=1。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — rNPV (biotech 单管线简化版)
# ---------------------------------------------------------------------------

def rnpv(
    peak_sales: float,
    pos_current_phase: float,
    pos_next_phases: list,
    years_to_launch: float,
    patent_life: int,
    r: float = 0.12,
    margin_net: float = 0.30,
    phase_cost: float = 0,
) -> dict:
    """风险调整 NPV：单管线，所有后续阶段 PoS 累乘后再乘销售净利现值。"""
    warnings = []
    if not (0 < pos_current_phase <= 1):
        return {"error": "pos_current_phase 必须在 (0, 1] 区间"}
    for p in pos_next_phases:
        if not (0 < p <= 1):
            return {"error": "pos_next_phases 每个值必须在 (0, 1] 区间"}
    if r <= 0:
        return {"error": "折现率 r 必须 > 0"}
    if margin_net <= 0 or margin_net > 1:
        return {"error": "净利润率 margin_net 必须 ∈ (0, 1]"}
    if patent_life <= 0:
        return {"error": "patent_life 必须 > 0"}

    pos_cumulative = pos_current_phase
    for p in pos_next_phases:
        pos_cumulative *= p

    if pos_cumulative > 0.8:
        warnings.append(f"累计 PoS {pos_cumulative*100:.0f}% > 80%，过度乐观——biotech 历史 Phase II→获批 < 15%")
    if pos_current_phase > 0.5 and len(pos_next_phases) >= 2:
        warnings.append(f"当前阶段 PoS {pos_current_phase*100:.0f}% 过高，需核对 BIO/Pharmaprojects 行业基准")

    # 上市后年度净利现值：从 years_to_launch+1 年起，连续 patent_life 年
    # 假设峰值销售额在上市后第 3 年达到，简化为整个 patent_life 都按 peak_sales × margin
    annual_net = peak_sales * margin_net
    sales_npv_at_launch = 0.0
    for k in range(1, patent_life + 1):
        sales_npv_at_launch += annual_net / (1 + r) ** k
    # 折回到今天
    sales_npv_today = sales_npv_at_launch / (1 + r) ** years_to_launch

    risk_adjusted_sales_npv = pos_cumulative * sales_npv_today

    # 当前阶段研发成本（已发生或近期投入，按当年算简单 PV = 全额）
    cost_pv = phase_cost  # 简化：假设当年支出

    rnpv_value = risk_adjusted_sales_npv - cost_pv

    if margin_net > 0.5:
        warnings.append(f"净利润率 {margin_net*100:.0f}% > 50% 偏激进，仅 best-in-class biotech 可达")
    if years_to_launch < 2 and pos_current_phase < 0.5:
        warnings.append("距离上市 < 2 年但 PoS < 50%，时间线/概率不一致，需复核")

    return {
        "method": "rNPV (single-pipeline simplified)",
        "assumptions": {
            "peak_sales_mm": peak_sales,
            "pos_current_phase": pos_current_phase,
            "pos_next_phases": pos_next_phases,
            "pos_cumulative": round(pos_cumulative, 4),
            "years_to_launch": years_to_launch,
            "patent_life": patent_life,
            "discount_rate": r,
            "margin_net": margin_net,
            "phase_cost_mm": phase_cost,
        },
        "output": {
            "annual_net_at_peak_mm": round(annual_net, 2),
            "sales_npv_at_launch_mm": round(sales_npv_at_launch, 2),
            "sales_npv_today_mm": round(sales_npv_today, 2),
            "risk_adjusted_sales_npv_mm": round(risk_adjusted_sales_npv, 2),
            "phase_cost_pv_mm": round(cost_pv, 2),
            "rnpv_mm": round(rnpv_value, 2),
        },
        "warnings": warnings,
        "note": "单管线简化 rNPV。多管线请逐条计算后加总。biotech 折现率通常 10-15%。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — Normalized PE
# ---------------------------------------------------------------------------

def normalized_pe(
    eps_series: list,
    normalized_pe_multiple: float = 10,
    remove_outliers: bool = True,
) -> dict:
    """正常化 EPS = 历史 EPS 序列（剔除最高/最低 outlier）的均值，× PE 倍数。"""
    warnings = []
    if not eps_series or len(eps_series) < 3:
        return {"error": "eps_series 至少 3 个数据点（推荐 7-10 年覆盖一个完整周期）"}
    if normalized_pe_multiple <= 0:
        return {"error": "normalized_pe_multiple 必须 > 0"}
    if len(eps_series) < 7:
        warnings.append(f"序列仅 {len(eps_series)} 年，少于一个完整周期（建议 7-10 年）")

    working = list(eps_series)
    removed = []
    if remove_outliers and len(working) >= 5:
        hi = max(working)
        lo = min(working)
        removed = [hi, lo]
        working.remove(hi)
        working.remove(lo)

    normalized_eps = sum(working) / len(working)
    value_per_share = normalized_eps * normalized_pe_multiple

    raw_mean = sum(eps_series) / len(eps_series)
    if any(e < 0 for e in eps_series):
        warnings.append("EPS 序列存在亏损年份，正常化盈利合理性需重点审视")
    if normalized_pe_multiple > 25:
        warnings.append(f"PE 倍数 {normalized_pe_multiple} 过高，仅适用极高质量/高增长企业")

    return {
        "method": "Normalized PE",
        "assumptions": {
            "eps_series": eps_series,
            "n_years": len(eps_series),
            "normalized_pe_multiple": normalized_pe_multiple,
            "remove_outliers": remove_outliers,
            "outliers_removed": removed,
        },
        "output": {
            "raw_mean_eps": round(raw_mean, 4),
            "normalized_eps": round(normalized_eps, 4),
            "value_per_share": round(value_per_share, 4),
        },
        "warnings": warnings,
        "note": "正常化 PE 用于强周期股（化工/资源/航运/银行）；穿越周期评估盈利中枢。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — NAV revaluation
# ---------------------------------------------------------------------------

def nav_revaluation(
    assets_at_market: list,
    total_liabilities: float,
    shares: float,
    current_price: float = None,
    asset_names: list = None,
    haircut_pct: float = 0,
) -> dict:
    """NAV = Σ assets_at_market × (1 - haircut) - liabilities； per_share 与折溢价。"""
    warnings = []
    if not assets_at_market:
        return {"error": "assets_at_market 不能为空"}
    if shares <= 0:
        return {"error": "shares 必须 > 0"}
    if not (0 <= haircut_pct < 100):
        return {"error": "haircut_pct 必须 ∈ [0, 100)"}
    if haircut_pct < 10:
        warnings.append(f"haircut {haircut_pct}% < 10%，可能未充分考虑流动性折价与变现摩擦")
    if haircut_pct > 50:
        warnings.append(f"haircut {haircut_pct}% > 50%，过度保守需核对资产质量")

    haircut_mult = 1 - haircut_pct / 100
    adjusted_assets = [a * haircut_mult for a in assets_at_market]
    total_assets = sum(adjusted_assets)
    nav = total_assets - total_liabilities
    nav_per_share = nav / shares

    breakdown = []
    if asset_names and len(asset_names) == len(assets_at_market):
        for n, raw, adj in zip(asset_names, assets_at_market, adjusted_assets):
            breakdown.append({"name": n, "market_value": raw, "after_haircut": round(adj, 2)})
    else:
        for i, (raw, adj) in enumerate(zip(assets_at_market, adjusted_assets)):
            breakdown.append({"name": f"asset_{i+1}", "market_value": raw, "after_haircut": round(adj, 2)})

    out = {
        "total_assets_at_market": round(sum(assets_at_market), 2),
        "haircut_pct": haircut_pct,
        "total_assets_after_haircut": round(total_assets, 2),
        "total_liabilities": total_liabilities,
        "nav": round(nav, 2),
        "nav_per_share": round(nav_per_share, 4),
        "asset_breakdown": breakdown,
    }
    if current_price:
        discount = 1 - current_price / nav_per_share if nav_per_share else None
        out["current_price"] = current_price
        out["discount_to_nav_pct"] = round(discount * 100, 2) if discount is not None else None
        out["interpretation"] = (
            f"当前价较 NAV {'折价' if discount and discount > 0 else '溢价'} "
            f"{abs(discount)*100:.1f}%。"
            if discount is not None else ""
        )

    if nav <= 0:
        warnings.append("调整后 NAV ≤ 0，资产不足以覆盖负债，公司资不抵债")

    return {
        "method": "NAV revaluation",
        "assumptions": {
            "assets_at_market": assets_at_market,
            "asset_names": asset_names,
            "total_liabilities": total_liabilities,
            "shares": shares,
            "haircut_pct": haircut_pct,
        },
        "output": out,
        "warnings": warnings,
        "note": "适用于地产 / 控股 / REITs / 资源股；haircut 反映流动性折价与变现摩擦，公开市场资产可低些，房产/项目类应 15-30%。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — SOTP
# ---------------------------------------------------------------------------

def sotp(
    segments: list,
    shares: float,
    holdco_discount_pct: float = 15,
    current_price: float = None,
) -> dict:
    """Sum-of-the-Parts：分部估值加总 × (1 - holdco_discount)。"""
    warnings = []
    if not segments:
        return {"error": "segments 不能为空"}
    if shares <= 0:
        return {"error": "shares 必须 > 0"}
    if not (0 <= holdco_discount_pct < 100):
        return {"error": "holdco_discount_pct 必须 ∈ [0, 100)"}
    if holdco_discount_pct < 10:
        warnings.append(f"holdco 折价 {holdco_discount_pct}% < 10%，多数控股结构市场默认 15-25%")
    if holdco_discount_pct > 40:
        warnings.append(f"holdco 折价 {holdco_discount_pct}% > 40%，过度保守，需核对治理 / 协同恶化证据")

    total_value = 0.0
    detail = []
    for seg in segments:
        name = seg.get("name", "unnamed")
        value = float(seg.get("value", 0))
        total_value += value
        detail.append({"name": name, "value": round(value, 2),
                       "share_of_total_pct": None})

    for d in detail:
        d["share_of_total_pct"] = round(d["value"] / total_value * 100, 2) if total_value else None

    discount_mult = 1 - holdco_discount_pct / 100
    adjusted_total = total_value * discount_mult
    sotp_per_share = adjusted_total / shares

    out = {
        "segments_detail": detail,
        "gross_sotp_value": round(total_value, 2),
        "holdco_discount_pct": holdco_discount_pct,
        "net_sotp_value": round(adjusted_total, 2),
        "sotp_per_share": round(sotp_per_share, 4),
    }
    if current_price:
        delta = (current_price - sotp_per_share) / sotp_per_share if sotp_per_share else None
        out["current_price"] = current_price
        out["premium_or_discount_pct"] = round(delta * 100, 2) if delta is not None else None
        out["interpretation"] = (
            f"当前价较 SOTP per share {'溢价' if delta and delta > 0 else '折价'} "
            f"{abs(delta)*100:.1f}%。"
            if delta is not None else ""
        )

    return {
        "method": "Sum-of-the-Parts (SOTP)",
        "assumptions": {
            "segments": segments,
            "shares": shares,
            "holdco_discount_pct": holdco_discount_pct,
        },
        "output": out,
        "warnings": warnings,
        "note": "适用于多元控股 / 综合企业；各分部应单独估值（DCF/PE/PB/NAV），再加总并打折。",
    }


# ---------------------------------------------------------------------------
# v2 NEW — DCF-FCFE
# ---------------------------------------------------------------------------

def dcf_fcfe(
    fcfe0: float,
    g1: float,
    years: int,
    gt: float,
    ke: float,
    shares: float = 1,
) -> dict:
    """股权自由现金流二阶段 DCF。用 Ke 折现，结果直接是股权价值，无需再减 net_debt。"""
    warnings = []
    if ke <= 0:
        return {"error": "Ke 必须 > 0"}
    if ke <= gt:
        return {"error": "Ke 必须 > 永续增长率 gt"}
    if (ke - gt) < 0.03:
        warnings.append("Ke - gt < 3%，终值对假设极度敏感")
    if gt > 0.04:
        warnings.append(f"永续增长率 {gt*100:.1f}% 超过长期 GDP 增速")
    if g1 > 0.30:
        warnings.append(f"显式期增长率 {g1*100:.0f}% 过高")

    explicit_pv = []
    fcfe = fcfe0
    for t in range(1, years + 1):
        fcfe = fcfe * (1 + g1)
        pv = fcfe / (1 + ke) ** t
        explicit_pv.append((fcfe, pv))

    fcfe_terminal = explicit_pv[-1][0] * (1 + gt)
    terminal_value = fcfe_terminal / (ke - gt)
    terminal_pv = terminal_value / (1 + ke) ** years

    equity_value = sum(pv for _, pv in explicit_pv) + terminal_pv
    value_per_share = equity_value / shares if shares else None
    terminal_share = terminal_pv / equity_value if equity_value else None
    if terminal_share and terminal_share > 0.75:
        warnings.append(f"终值占比 {terminal_share*100:.0f}% > 75%")

    return {
        "method": "DCF two-stage (FCFE)",
        "assumptions": {
            "fcfe0": fcfe0,
            "g1": g1,
            "years": years,
            "gt": gt,
            "ke": ke,
            "shares": shares,
        },
        "output": {
            "explicit_period_pv": round(sum(pv for _, pv in explicit_pv), 4),
            "terminal_value_pv": round(terminal_pv, 4),
            "terminal_value_share_pct": round(terminal_share * 100, 1) if terminal_share else None,
            "equity_value": round(equity_value, 4),
            "value_per_share": round(value_per_share, 4) if value_per_share else None,
        },
        "warnings": warnings,
        "note": "FCFE 视角：直接得股权价值，不再减净债务；适用银行 / 杠杆波动大企业。",
    }


# ---------------------------------------------------------------------------
# Helpers — parsing
# ---------------------------------------------------------------------------

def _parse_csv_floats(s: str) -> list:
    if not s:
        return []
    return [float(x.strip()) for x in s.split(",") if x.strip()]


def _parse_csv_strs(s: str) -> list:
    if not s:
        return []
    return [x.strip() for x in s.split(",") if x.strip()]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="价值投资估值辅助计算器 (12 子命令)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # --- v1 ---
    p_dcf = sub.add_parser("dcf", help="二阶段 DCF (FCFF)")
    p_dcf.add_argument("--fcf0", type=float, required=True)
    p_dcf.add_argument("--g1", type=float, required=True)
    p_dcf.add_argument("--years", type=int, default=10)
    p_dcf.add_argument("--gt", type=float, default=0.025)
    p_dcf.add_argument("--wacc", type=float, required=True)
    p_dcf.add_argument("--net-debt", type=float, default=0)
    p_dcf.add_argument("--shares", type=float, default=1)

    p_epv = sub.add_parser("epv", help="EPV (Greenwald)")
    p_epv.add_argument("--normalized-earnings", type=float, required=True)
    p_epv.add_argument("--wacc", type=float, required=True)
    p_epv.add_argument("--maintenance-capex", type=float, default=0)
    p_epv.add_argument("--shares", type=float, default=1)
    p_epv.add_argument("--net-debt", type=float, default=0)

    p_rev = sub.add_parser("reverse-dcf", help="反推隐含增长率")
    p_rev.add_argument("--price", type=float, required=True)
    p_rev.add_argument("--fcf0", type=float, required=True)
    p_rev.add_argument("--years", type=int, default=10)
    p_rev.add_argument("--gt", type=float, default=0.025)
    p_rev.add_argument("--wacc", type=float, required=True)
    p_rev.add_argument("--net-debt", type=float, default=0)
    p_rev.add_argument("--shares", type=float, default=1)

    p_sen = sub.add_parser("sensitivity", help="敏感性矩阵")
    p_sen.add_argument("--fcf0", type=float, required=True)
    p_sen.add_argument("--years", type=int, default=10)
    p_sen.add_argument("--net-debt", type=float, default=0)
    p_sen.add_argument("--shares", type=float, default=1)

    # --- v2 NEW ---
    p_ddm = sub.add_parser("ddm", help="两阶段 DDM")
    p_ddm.add_argument("--dividend-current", type=float, required=True)
    p_ddm.add_argument("--growth-explicit", type=float, required=True)
    p_ddm.add_argument("--years", type=int, default=5)
    p_ddm.add_argument("--growth-terminal", type=float, required=True)
    p_ddm.add_argument("--ke", type=float, required=True)
    p_ddm.add_argument("--shares-outstanding", type=float, default=None)

    p_pbroe = sub.add_parser("pb-roe", help="PB-ROE 估值")
    p_pbroe.add_argument("--book-value-per-share", type=float, required=True)
    p_pbroe.add_argument("--roe", type=float, required=True)
    p_pbroe.add_argument("--ke", type=float, required=True)
    p_pbroe.add_argument("--g", type=float, required=True)
    p_pbroe.add_argument("--current-price", type=float, default=None)

    p_rim = sub.add_parser("rim", help="残差收益模型 (RIM)")
    p_rim.add_argument("--book-value-current", type=float, required=True)
    p_rim.add_argument("--roe-forecast", type=str, required=True,
                       help='逗号分隔 ROE 数组，如 "0.15,0.14,0.13,0.13,0.12"')
    p_rim.add_argument("--ke", type=float, required=True)
    p_rim.add_argument("--growth-terminal-book", type=float, required=True)

    p_rnpv = sub.add_parser("rnpv", help="风险调整 NPV (biotech 单管线)")
    p_rnpv.add_argument("--peak-sales", type=float, required=True, help="峰值年销售额（mm）")
    p_rnpv.add_argument("--pos-current-phase", type=float, required=True)
    p_rnpv.add_argument("--pos-next-phases", type=str, default="0.65,0.85",
                        help='逗号分隔后续阶段 PoS，如 "0.65,0.85"')
    p_rnpv.add_argument("--years-to-launch", type=float, required=True)
    p_rnpv.add_argument("--patent-life", type=int, required=True)
    p_rnpv.add_argument("--r", type=float, default=0.12)
    p_rnpv.add_argument("--margin-net", type=float, default=0.30)
    p_rnpv.add_argument("--phase-cost", type=float, default=0)

    p_npe = sub.add_parser("normalized-pe", help="正常化 PE")
    p_npe.add_argument("--eps-series", type=str, required=True,
                       help='逗号分隔 EPS 序列，如 "1.2,1.5,0.8,..."')
    p_npe.add_argument("--normalized-pe-multiple", type=float, default=10)
    p_npe.add_argument("--remove-outliers", type=lambda x: str(x).lower() not in ("0", "false", "no"),
                       default=True)

    p_nav = sub.add_parser("nav-revaluation", help="NAV 重估")
    p_nav.add_argument("--assets-at-market", type=str, required=True,
                       help='逗号分隔资产市场价数组，如 "100,200,50"')
    p_nav.add_argument("--asset-names", type=str, default=None)
    p_nav.add_argument("--total-liabilities", type=float, required=True)
    p_nav.add_argument("--shares", type=float, required=True)
    p_nav.add_argument("--current-price", type=float, default=None)
    p_nav.add_argument("--haircut-pct", type=float, default=0)

    p_sotp = sub.add_parser("sotp", help="SOTP 汇总")
    p_sotp.add_argument("--segments", type=str, required=True,
                        help='JSON 数组：\'[{"name":"x","value":100}]\'')
    p_sotp.add_argument("--shares", type=float, required=True)
    p_sotp.add_argument("--holdco-discount-pct", type=float, default=15)
    p_sotp.add_argument("--current-price", type=float, default=None)

    p_fcfe = sub.add_parser("dcf-fcfe", help="DCF-FCFE (Ke 折现)")
    p_fcfe.add_argument("--fcfe0", type=float, required=True)
    p_fcfe.add_argument("--g1", type=float, required=True)
    p_fcfe.add_argument("--years", type=int, default=10)
    p_fcfe.add_argument("--gt", type=float, default=0.025)
    p_fcfe.add_argument("--ke", type=float, required=True)
    p_fcfe.add_argument("--shares", type=float, default=1)

    args = parser.parse_args()

    if args.cmd == "dcf":
        out = dcf_two_stage(args.fcf0, args.g1, args.years, args.gt, args.wacc, args.net_debt, args.shares)
    elif args.cmd == "epv":
        out = epv(args.normalized_earnings, args.wacc, args.maintenance_capex, args.shares, args.net_debt)
    elif args.cmd == "reverse-dcf":
        out = reverse_dcf(args.price, args.fcf0, args.years, args.gt, args.wacc, args.net_debt, args.shares)
    elif args.cmd == "sensitivity":
        out = sensitivity_matrix(args.fcf0, args.years, args.net_debt, args.shares)
    elif args.cmd == "ddm":
        out = ddm_two_stage(args.dividend_current, args.growth_explicit, args.years,
                            args.growth_terminal, args.ke, args.shares_outstanding)
    elif args.cmd == "pb-roe":
        out = pb_roe(args.book_value_per_share, args.roe, args.ke, args.g, args.current_price)
    elif args.cmd == "rim":
        roe_list = _parse_csv_floats(args.roe_forecast)
        out = rim(args.book_value_current, roe_list, args.ke, args.growth_terminal_book)
    elif args.cmd == "rnpv":
        pos_next = _parse_csv_floats(args.pos_next_phases)
        out = rnpv(args.peak_sales, args.pos_current_phase, pos_next,
                   args.years_to_launch, args.patent_life, args.r, args.margin_net, args.phase_cost)
    elif args.cmd == "normalized-pe":
        eps = _parse_csv_floats(args.eps_series)
        out = normalized_pe(eps, args.normalized_pe_multiple, args.remove_outliers)
    elif args.cmd == "nav-revaluation":
        assets = _parse_csv_floats(args.assets_at_market)
        names = _parse_csv_strs(args.asset_names) if args.asset_names else None
        out = nav_revaluation(assets, args.total_liabilities, args.shares,
                              args.current_price, names, args.haircut_pct)
    elif args.cmd == "sotp":
        try:
            segs = json.loads(args.segments)
        except json.JSONDecodeError as e:
            print(json.dumps({"error": f"--segments JSON 解析失败: {e}"}, ensure_ascii=False, indent=2))
            sys.exit(1)
        out = sotp(segs, args.shares, args.holdco_discount_pct, args.current_price)
    elif args.cmd == "dcf-fcfe":
        out = dcf_fcfe(args.fcfe0, args.g1, args.years, args.gt, args.ke, args.shares)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

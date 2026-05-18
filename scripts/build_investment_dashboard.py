#!/usr/bin/env python3

import argparse
import datetime as dt
import html
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "research" / "dashboard" / "index.html"
DISCLAIMER = "仅供研究 · 非交易信号 · 不构成投资建议"
PROXY_ONLY_WARNING = "正式资料未接入：尚未取得正式核验过的基本面、估值或事件资料，不能清除行动门槛；只能用于观察和排序。"
ACTION_STATES = {"buy_candidate", "accumulate", "hold", "trim", "sell_candidate"}
WATCH_STATES = {"watch", "watch_only"}
AVOID_STATES = {"avoid", "no_action", "blocked"}
RESEARCH_ACTION_ORDER = ("consider", "confirm", "observe", "avoid")
HARD_RESEARCH_BLOCKERS = {
    "symbol_risk_veto",
    "symbol_recent_adverse_breach",
    "downtrend_regime",
    "price_below_ma20_and_ma60",
    "range_pos_60_below_0_12",
}
REASON_LABELS = {
    "cost_gate_failed": "成本/边际不足",
    "downtrend_regime": "趋势偏弱",
    "event_risk_policy": "政策风险",
    "event_risk_quote_stale": "行情日期滞后",
    "event_risk_unknown": "事件风险未知",
    "hk_halt_or_no_turnover_suspected": "疑似停牌/无成交",
    "cn_limit_down_liquidity_block": "跌停流动性风险",
    "cn_limit_up_chase_block": "涨停追高风险",
    "low_volume_ratio_20_below_0_6": "量能严重不足",
    "market_range_pos_60_above_action_limit": "市场位置偏高",
    "market_proxy_missing": "市场参考资料缺失",
    "nontechnical_component_missing": "非技术面组件缺失",
    "nontechnical_evidence_date_missing": "非技术面日期缺失",
    "nontechnical_evidence_from_future": "非技术面证据来自未来",
    "nontechnical_evidence_from_future_session": "非技术面证据来自未来时段",
    "nontechnical_evidence_missing": "非技术面证据缺失",
    "nontechnical_evidence_stale": "非技术面证据过期",
    "nontechnical_proxy_only": "正式资料未接入",
    "nontechnical_score_missing": "非技术分缺失",
    "nontechnical_score_below_action_min": "非技术分不足",
    "nontechnical_source_missing": "正式证据缺失",
    "not_theme_score_leader": "不是主题领先",
    "price_below_ma20_and_ma60": "跌破均线",
    "quote_trade_date_missing": "行情交易日缺失",
    "quote_trade_date_mismatch": "行情日期不匹配",
    "range_pos_60_below_0_12": "区间位置过低",
    "same_theme_best_peer_evidence_missing_or_failed": "同主题证据不足",
    "symbol_recent_adverse_breach": "近期逆向风险",
    "symbol_risk_veto": "个股风险否决",
    "volume_ratio_20_below_1_0": "量能不足",
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def output_stem(date: str, session: str) -> str:
    return date if session in {"close", "historical"} else f"{date}-{session}"


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def load_json(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None


def load_text(path: pathlib.Path | None) -> str | None:
    if path is None or not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def load_close_markdown(path: pathlib.Path | None) -> str | None:
    text = load_text(path)
    if text is not None:
        return text
    latest = path.parent / "latest.md" if path else ROOT / "research" / "products" / "daily_close" / "latest.md"
    return load_text(latest)


def file_metadata(path: pathlib.Path | None) -> dict[str, Any]:
    return {"path": str(path) if path else None, "exists": bool(path and path.exists())}


def nested_get(data: dict[str, Any] | None, keys: list[str], default: Any = None) -> Any:
    node: Any = data
    for key in keys:
        if not isinstance(node, dict):
            return default
        node = node.get(key)
    return node if node is not None else default


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def clean_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if value:
        return [str(value)]
    return []


def evidence_text_implies_proxy_only(value: Any) -> bool:
    text = " ".join(clean_list(value)) if isinstance(value, list) else str(value or "")
    return "status=proxy_only" in text or "nontechnical_proxy_only" in text or "proxy_only=True" in text


def recommendation_evidence_text(rec: dict[str, Any]) -> str:
    parts = clean_list(rec.get("evidence")) + clean_list(rec.get("nontechnical_evidence"))
    return " ".join(parts)


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            out.append(value)
    return out


def extract_markdown_headline(markdown: str | None) -> str | None:
    if not markdown:
        return None
    lines = [line.strip() for line in markdown.splitlines()]
    final_markers = {"## final result", "## final", "## \u6700\u7ec8\u7ed3\u679c"}
    for idx, line in enumerate(lines):
        if line.lower() in final_markers:
            for candidate in lines[idx + 1 :]:
                if candidate.startswith("-"):
                    return candidate.lstrip("- ").strip()
                if candidate and not candidate.startswith("#"):
                    return candidate
    for line in lines:
        if line.startswith("-"):
            return line.lstrip("- ").strip()
    for line in lines:
        if line.startswith("#"):
            return line.lstrip("# ").strip()
    return None


def recommendation_by_symbol(close_report: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for rec in (close_report or {}).get("recommendations", []):
        if isinstance(rec, dict) and rec.get("symbol"):
            rows[str(rec["symbol"])] = rec
    return rows


def classify_state(state: str | None, ranked_row: dict[str, Any] | None = None) -> str:
    normalized = str(state or "").strip().lower()
    if normalized in ACTION_STATES:
        return "action"
    if normalized in WATCH_STATES:
        return "watch"
    if normalized in AVOID_STATES:
        return "avoid"
    if ranked_row is not None:
        if ranked_row.get("qualified_for_action") is True:
            return "action"
        if ranked_row.get("qualified_for_watch") is True:
            return "watch"
    return "avoid"


def generated_headline(close_report: dict[str, Any] | None, markdown: str | None, symbols: list[dict[str, Any]]) -> str:
    recs = [row for row in symbols if row.get("recommendation_state")]
    actions = [row for row in recs if row.get("category") == "action"]
    watches = [row for row in recs if row.get("category") == "watch"]
    if actions:
        return "今日可行动候选：" + "、".join(str(row.get("symbol")) for row in actions[:5])
    if recs:
        watch_text = "、".join(str(row.get("symbol")) for row in watches[:5]) if watches else "无"
        return f"今日暂无可行动候选；观察名单：{watch_text}。"
    markdown_headline = extract_markdown_headline(markdown)
    if markdown_headline:
        return markdown_headline
    ranked_actions = [row for row in symbols if row.get("category") == "action"]
    if ranked_actions:
        return "Ranking 备用可行动候选：" + "、".join(str(row.get("symbol")) for row in ranked_actions[:5])
    return "未找到收盘推荐报告；当前展示 ranking 与证据备用结果。"


def nontechnical_status_from_raw(raw: dict[str, Any] | None) -> str:
    if not raw:
        return "missing"
    mode = str(raw.get("evidence_mode") or "").strip()
    if mode == "missing_fail_closed":
        return "missing"
    if mode == "automatic_local_proxy" or raw.get("proxy_only") is True:
        return "proxy_only"
    return "available"


def normalize_nontechnical(symbol: str, ranked_row: dict[str, Any], nontechnical: dict[str, Any] | None, recommendation_evidence: str = "") -> dict[str, Any]:
    profile = ranked_row.get("nontechnical_evidence") if isinstance(ranked_row.get("nontechnical_evidence"), dict) else {}
    symbols = (nontechnical or {}).get("symbols", {}) if isinstance((nontechnical or {}).get("symbols", {}), dict) else {}
    raw = symbols.get(symbol) if isinstance(symbols.get(symbol), dict) else {}
    status = profile.get("status") or nontechnical_status_from_raw(raw)
    raw_proxy = str(raw.get("evidence_mode") or "") == "automatic_local_proxy" or raw.get("proxy_only") is True
    proxy_only = bool(profile.get("proxy_only") is True or raw_proxy or status == "proxy_only" or evidence_text_implies_proxy_only(recommendation_evidence))
    if proxy_only:
        status = "proxy_only"
    total_score = profile.get("total_score") if profile.get("total_score") is not None else raw.get("total_score")
    return {
        "status": status,
        "proxy_only": proxy_only,
        "total_score": total_score,
        "event_risk": profile.get("event_risk") or raw.get("event_risk"),
        "source_count": profile.get("source_count") if profile.get("source_count") is not None else raw.get("source_count"),
        "proxy_source_count": profile.get("proxy_source_count") if profile.get("proxy_source_count") is not None else raw.get("proxy_source_count"),
        "warning": PROXY_ONLY_WARNING if proxy_only else None,
    }


def reason_label(reason: str) -> str:
    return REASON_LABELS.get(reason, reason)


def visible_reason_labels(reasons: Any) -> list[str]:
    return [reason_label(item) for item in clean_list(reasons)]


def display_name(value: Any) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    if " / " in text:
        text = text.split(" / ")[-1].strip()
    return text or None


def formal_blockers(row: dict[str, Any]) -> list[str]:
    return [item for item in clean_list(row.get("blockers")) if item in REASON_LABELS]


def research_action_for(row: dict[str, Any]) -> dict[str, Any]:
    blockers = formal_blockers(row)
    blocker_set = set(blockers)
    nontechnical = row.get("nontechnical_evidence") if isinstance(row.get("nontechnical_evidence"), dict) else {}
    score = as_float(row.get("score")) or 0.0
    state = str(row.get("recommendation_state") or "").lower()
    risk_cap = str(row.get("risk_cap") or "").lower()
    event_risk = str(nontechnical.get("event_risk") or "").lower()
    proxy_only = nontechnical.get("proxy_only") is True or evidence_text_implies_proxy_only(row.get("recommendation_evidence"))
    has_hard_blocker = bool(blocker_set & HARD_RESEARCH_BLOCKERS) or state in {"avoid", "blocked", "rejected"}
    has_soft_blocker = bool(blockers)
    has_action_state = state in ACTION_STATES and (not risk_cap or risk_cap in ACTION_STATES)

    if has_action_state and row.get("qualified_for_action") is True and not blockers and not proxy_only and event_risk not in {"unknown", "policy", "high"}:
        label = "可考虑研究"
        key = "consider"
        reason = "正式门槛已过，暂无阻断项。"
        upgrade = "已在研究候选层；仍需人工复核，不自动执行。"
        invalidation = "若出现阻断项、事件风险升高、置信度下降或不再通过正式门槛，立即降级。"
    elif has_hard_blocker or score < 20:
        label = "暂不碰"
        key = "avoid"
        reason = "存在硬阻断或状态不匹配，今日不纳入候选。"
        upgrade = "硬阻断消失、分数回到观察线后，才恢复观察。"
        invalidation = "硬性阻断未解除前，不升级。"
    elif row.get("qualified_for_watch") is True and (score >= 70 or proxy_only or event_risk in {"unknown", "policy", "high"} or has_soft_blocker):
        label = "等确认"
        key = "confirm"
        reason = "接近候选，但仍有关键确认项未满足。"
        upgrade = "阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。"
        invalidation = "若观察分数跌破门槛或状态转差，移出重点跟踪。"
    elif row.get("qualified_for_watch") is True or score >= 45:
        label = "继续观察"
        key = "observe"
        reason = "有跟踪价值，但当前强度或证据不足。"
        upgrade = "分数进入观察线且状态改善后，可升级为「等确认」。"
        invalidation = "若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。"
    else:
        label = "暂不碰"
        key = "avoid"
        reason = "信号不足或约束不通过，暂不投入研究时间。"
        upgrade = "重新通过观察门槛且无硬阻断后，可恢复观察。"
        invalidation = "硬性阻断未解除前，不升级。"

    return {
        "key": key,
        "label": label,
        "reason": reason,
        "reason_chips": [reason_label(item) for item in blockers[:4]],
        "upgrade": upgrade,
        "invalidation": invalidation,
        "research_only": True,
    }


def normalize_symbols(ranking: dict[str, Any] | None, close_report: dict[str, Any] | None, nontechnical: dict[str, Any] | None) -> list[dict[str, Any]]:
    recs = recommendation_by_symbol(close_report)
    ranked_rows = (ranking or {}).get("all_ranked", [])
    ranked_rows = ranked_rows if isinstance(ranked_rows, list) else []

    rows: list[dict[str, Any]] = []
    seen: set[str] = set()
    for idx, ranked in enumerate(ranked_rows):
        if not isinstance(ranked, dict) or not ranked.get("symbol"):
            continue
        symbol = str(ranked["symbol"])
        rec = recs.get(symbol, {})
        rec_evidence = recommendation_evidence_text(rec)
        state = rec.get("effective_state") or rec.get("state")
        judgment = str(state or ("action_candidate" if ranked.get("qualified_for_action") else "watch" if ranked.get("qualified_for_watch") else "avoid"))
        category = classify_state(str(state) if state else None, ranked)
        blockers = unique(clean_list(ranked.get("action_disqualifiers")) + clean_list(ranked.get("disqualifiers")) + clean_list(rec.get("blockers")) + clean_list(rec.get("risks")))
        score = as_float(ranked.get("score"))
        row = {
            "rank": idx + 1,
            "symbol": symbol,
            "name": ranked.get("name") or rec.get("name"),
            "display_name": display_name(ranked.get("name") or rec.get("name")),
            "judgment": judgment,
            "recommendation_state": state,
            "category": category,
            "qualified_for_action": bool(ranked.get("qualified_for_action")),
            "qualified_for_watch": bool(ranked.get("qualified_for_watch")),
            "score": round(score, 3) if score is not None else None,
            "confidence": rec.get("confidence") if rec.get("confidence") is not None else ranked.get("confidence"),
            "action_disqualifiers": blockers,
            "blockers": blockers,
            "blocker_labels": visible_reason_labels(blockers),
            "risk_cap": rec.get("risk_cap"),
            "risk_decision": rec.get("risk_decision"),
            "recommendation_evidence": rec_evidence,
            "nontechnical_evidence": normalize_nontechnical(symbol, ranked, nontechnical, rec_evidence),
        }
        row["research_action"] = research_action_for(row)
        rows.append(row)
        seen.add(symbol)

    for symbol, rec in recs.items():
        if symbol in seen:
            continue
        state = rec.get("effective_state") or rec.get("state")
        rec_evidence = recommendation_evidence_text(rec)
        category = classify_state(str(state) if state else None)
        row = {
            "rank": None,
            "symbol": symbol,
            "name": rec.get("name"),
            "display_name": display_name(rec.get("name")),
            "judgment": str(state or "recommendation"),
            "recommendation_state": state,
            "category": category,
            "qualified_for_action": category == "action",
            "qualified_for_watch": category in {"action", "watch"},
            "score": None,
            "confidence": rec.get("confidence"),
            "action_disqualifiers": unique(clean_list(rec.get("blockers")) + clean_list(rec.get("risks"))),
            "blockers": unique(clean_list(rec.get("blockers")) + clean_list(rec.get("risks"))),
            "blocker_labels": visible_reason_labels(unique(clean_list(rec.get("blockers")) + clean_list(rec.get("risks")))),
            "risk_cap": rec.get("risk_cap"),
            "risk_decision": rec.get("risk_decision"),
            "recommendation_evidence": rec_evidence,
            "nontechnical_evidence": normalize_nontechnical(symbol, {}, nontechnical, rec_evidence),
        }
        row["research_action"] = research_action_for(row)
        rows.append(row)
    return rows


def count_categories(symbols: list[dict[str, Any]]) -> dict[str, int]:
    return {
        "action": sum(1 for row in symbols if row.get("category") == "action"),
        "watch": sum(1 for row in symbols if row.get("category") == "watch"),
        "avoid": sum(1 for row in symbols if row.get("category") == "avoid"),
    }


def count_research_actions(symbols: list[dict[str, Any]]) -> dict[str, int]:
    return {key: sum(1 for row in symbols if (row.get("research_action") or {}).get("key") == key) for key in RESEARCH_ACTION_ORDER}


def evidence_metrics(close_report: dict[str, Any] | None, forward_eval: dict[str, Any] | None, evidence_ledger: dict[str, Any] | None, nontechnical: dict[str, Any] | None) -> dict[str, Any]:
    nontechnical_summary = (nontechnical or {}).get("summary", {}) if isinstance((nontechnical or {}).get("summary", {}), dict) else {}
    close_evidence = (close_report or {}).get("evidence", {}) if isinstance((close_report or {}).get("evidence", {}), dict) else {}
    close_nontech = nested_get(close_report, ["nontechnical", "evidence_summary"], {})
    if not isinstance(close_nontech, dict):
        close_nontech = {}
    return {
        "forward_logs": nested_get(evidence_ledger, ["summary", "forward_shadow_log_count"], nested_get(forward_eval, ["summary", "forward_shadow_log_count"], close_evidence.get("forward_shadow_logs"))),
        "matured_days": nested_get(evidence_ledger, ["shadow_evaluation_summary", "matured_forward_shadow_days"], nested_get(forward_eval, ["summary", "matured_forward_shadow_days"], close_evidence.get("matured_forward_days"))),
        "forward_samples": nested_get(evidence_ledger, ["shadow_evaluation_summary", "sample_count"], nested_get(forward_eval, ["summary", "sample_count"], close_evidence.get("forward_sample_count"))),
        "forward_win_rate": nested_get(evidence_ledger, ["shadow_evaluation_summary", "win_rate"], nested_get(forward_eval, ["summary", "win_rate"])),
        "curated_available": nontechnical_summary.get("curated_available_count", nontechnical_summary.get("available_count", close_nontech.get("curated_available_count", close_nontech.get("available_count")))),
        "proxy_only": nontechnical_summary.get("proxy_only_count", nontechnical_summary.get("automatic_proxy_count", close_nontech.get("proxy_only_count", close_nontech.get("automatic_proxy_count")))),
        "missing": nontechnical_summary.get("missing_count", close_nontech.get("missing_count")),
    }


def build_payload(
    date: str,
    session: str,
    close_report: dict[str, Any] | None,
    close_markdown: str | None,
    ranking: dict[str, Any] | None,
    nontechnical: dict[str, Any] | None,
    forward_eval: dict[str, Any] | None,
    evidence_ledger: dict[str, Any] | None,
    sources: dict[str, pathlib.Path | None],
) -> dict[str, Any]:
    payload_date = str((close_report or {}).get("date") or (ranking or {}).get("as_of_date") or date)
    payload_session = str((close_report or {}).get("session") or (ranking or {}).get("session") or session)
    symbols = normalize_symbols(ranking, close_report, nontechnical)
    counts = count_categories(symbols)
    return {
        "generated_at": utc_now(),
        "date": payload_date,
        "session": payload_session,
        "disclaimer": DISCLAIMER,
        "research_only": True,
        "no_trading_signal": True,
        "not_investment_advice": True,
        "headline": generated_headline(close_report, close_markdown, symbols),
        "counts": counts,
        "research_action_counts": count_research_actions(symbols),
        "reason_labels": REASON_LABELS,
        "symbols": symbols,
        "evidence": evidence_metrics(close_report, forward_eval, evidence_ledger, nontechnical),
        "proxy_only_warning": PROXY_ONLY_WARNING,
        "sources": {name: file_metadata(path) for name, path in sources.items()},
    }


def json_for_html(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False).replace("</", "<\\/")


def session_label(session: Any) -> str:
    return {"morning": "早盘", "midday": "午间", "close": "收盘", "historical": "历史"}.get(str(session), str(session))


def render_html(payload: dict[str, Any]) -> str:
    title = f"投资研究看板 - {payload['date']} {session_label(payload['session'])}"
    safe_title = html.escape(title)
    data_json = json_for_html(payload)
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>{safe_title}</title>
  <style>
    :root {{
      --ink: #18211f;
      --muted: #5b6761;
      --paper: #f7f2e8;
      --panel: #fffaf0;
      --line: #d9cdb8;
      --green: #1d6b4f;
      --amber: #a66a00;
      --red: #9c3528;
      --blue: #225a7a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      color: var(--ink);
      font-family: 'Microsoft YaHei', 'Noto Sans CJK SC', 'PingFang SC', 'Aptos', sans-serif;
      background:
        radial-gradient(circle at 12% 10%, rgba(34, 90, 122, 0.16), transparent 28rem),
        radial-gradient(circle at 85% 0%, rgba(166, 106, 0, 0.14), transparent 22rem),
        linear-gradient(135deg, #f7f2e8 0%, #efe3ce 100%);
    }}
    header {{ padding: 32px clamp(18px, 4vw, 56px) 20px; }}
    main {{ padding: 18px clamp(14px, 3vw, 36px) 36px; }}
    .disclaimer {{
      display: inline-block;
      margin-bottom: 18px;
      padding: 10px 14px;
      border: 2px solid var(--red);
      border-radius: 999px;
      color: var(--red);
      background: rgba(255, 250, 240, 0.88);
      font: 700 0.92rem 'Microsoft YaHei', sans-serif;
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(2rem, 5vw, 4rem); line-height: 1.05; }}
    .headline {{ max-width: 980px; margin: 0; color: var(--muted); font-size: clamp(1.05rem, 2vw, 1.35rem); }}
    .pillbar {{ display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 0 0 14px; }}
    .filter-pill, .status-pill {{ border: 1px solid var(--line); border-radius: 999px; padding: 8px 12px; background: rgba(255, 250, 240, 0.88); color: var(--ink); box-shadow: 0 6px 18px rgba(58, 45, 27, 0.05); font: 700 0.92rem 'Microsoft YaHei', sans-serif; }}
    .filter-pill {{ cursor: pointer; }}
    .filter-pill strong, .status-pill strong {{ margin-left: 6px; font-size: 1.05rem; }}
    .filter-pill.active {{ color: #fff; background: var(--blue); border-color: var(--blue); }}
    .filter-pill.action.active {{ background: var(--green); border-color: var(--green); }}
    .filter-pill.watch.active {{ background: var(--amber); border-color: var(--amber); }}
    .filter-pill.avoid.active {{ background: var(--red); border-color: var(--red); }}
    .status-pill {{ color: var(--blue); }}
    .card {{ border: 1px solid var(--line); border-radius: 18px; padding: 18px; background: rgba(255, 250, 240, 0.82); box-shadow: 0 14px 35px rgba(58, 45, 27, 0.08); }}
    .label {{ color: var(--muted); font: 700 0.82rem 'Microsoft YaHei', sans-serif; letter-spacing: 0.08em; }}
    .value {{ margin-top: 8px; font: 700 clamp(1.8rem, 4vw, 3rem) Georgia, 'Microsoft YaHei', serif; }}
    .value.action {{ color: var(--green); }} .value.watch {{ color: var(--amber); }} .value.avoid {{ color: var(--red); }} .value.evidence {{ color: var(--blue); }}
    .notice {{ margin: 16px 0 24px; padding: 14px 16px; border-left: 5px solid var(--amber); background: rgba(255, 250, 240, 0.9); }}
    .explain {{ margin: 14px 0 22px; color: var(--muted); line-height: 1.7; }}
    .symbol-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; margin: 14px 0 24px; }}
    .symbol-card h3 {{ margin: 0 0 4px; font-size: 1.2rem; }}
    .symbol-card .name {{ color: var(--muted); min-height: 1.2rem; }}
    .symbol-card .metric {{ margin-top: 12px; font-size: 1.05rem; }}
    .symbol-card .blockers {{ margin-top: 10px; color: var(--red); line-height: 1.5; }}
    .reason-pills {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }}
    .reason-pill {{ display: inline-flex; align-items: center; border-radius: 999px; padding: 4px 8px; background: rgba(156, 53, 40, 0.1); color: var(--red); font: 700 0.78rem 'Microsoft YaHei', sans-serif; }}
    details {{ margin-top: 20px; }}
    summary {{ cursor: pointer; padding: 14px 16px; border: 1px solid var(--line); border-radius: 14px; background: rgba(255, 250, 240, 0.88); font-weight: 700; }}
    .toolbar {{ display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 12px; margin: 22px 0 12px; }}
    .toolbar h2 {{ margin: 0; font-size: 1.6rem; }}
    #symbolSearch {{ width: min(100%, 420px); padding: 12px 14px; border: 1px solid var(--line); border-radius: 999px; background: var(--panel); color: var(--ink); font: 1rem 'Microsoft YaHei', sans-serif; }}
    table {{ width: 100%; border-collapse: collapse; overflow: hidden; border-radius: 18px; background: rgba(255, 250, 240, 0.9); }}
    th, td {{ padding: 12px 10px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }}
    th {{ color: var(--muted); font: 700 0.78rem 'Microsoft YaHei', sans-serif; letter-spacing: 0.06em; }}
    td {{ font-size: 0.96rem; }}
    .chip {{ display: inline-block; padding: 4px 8px; border-radius: 999px; font: 700 0.78rem 'Microsoft YaHei', sans-serif; background: #ece1cf; margin: 2px 4px 2px 0; }}
    .chip.action {{ color: #fff; background: var(--green); }} .chip.watch {{ color: #fff; background: var(--amber); }} .chip.avoid {{ color: #fff; background: var(--red); }} .chip.proxy {{ color: #fff; background: var(--blue); }}
    .small {{ color: var(--muted); font-size: 0.88rem; }}
    .empty {{ padding: 22px; color: var(--muted); background: rgba(255, 250, 240, 0.9); border-radius: 18px; }}
    .win-note {{ color: var(--muted); font-size: 0.92rem; margin-top: 6px; }}
    @media (max-width: 1100px) {{ .symbol-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 900px) {{ table, thead, tbody, th, td, tr {{ display: block; }} thead {{ display: none; }} tr {{ border: 1px solid var(--line); border-radius: 16px; margin-bottom: 12px; background: rgba(255, 250, 240, 0.92); }} td {{ border-bottom: 0; padding: 9px 12px; }} td::before {{ content: attr(data-label); display: block; color: var(--muted); font: 700 0.72rem 'Microsoft YaHei', sans-serif; letter-spacing: 0.06em; }} }}
    @media (max-width: 560px) {{ .symbol-grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <main>
    <section class=\"pillbar\" aria-label=\"筛选与胜率\">
      <button class=\"filter-pill active\" type=\"button\" data-filter=\"all\">全部 <strong id=\"totalCount\">0</strong></button>
      <button class=\"filter-pill action\" type=\"button\" data-filter=\"consider\">可考虑研究 <strong id=\"considerCount\">0</strong></button>
      <button class=\"filter-pill watch\" type=\"button\" data-filter=\"confirm\">等确认 <strong id=\"confirmCount\">0</strong></button>
      <button class=\"filter-pill watch\" type=\"button\" data-filter=\"observe\">继续观察 <strong id=\"observeCount\">0</strong></button>
      <button class=\"filter-pill avoid\" type=\"button\" data-filter=\"avoid\">暂不碰 <strong id=\"avoidCount\">0</strong></button>
      <span class=\"status-pill\">当前前向胜率 <strong id=\"winRate\">暂无</strong><span class=\"win-note\" id=\"winRateNote\"></span></span>
    </section>
    <p class=\"explain\"><strong>分数怎么理解：</strong>分数是“研究优先级/排序分”，用于决定先看哪些标的；它不是上涨概率，也不是买入信号。只有通过可行动关卡、风险审查和证据门槛后，才可能进入可行动候选。</p>
    <section class=\"card\" aria-label=\"证据进度\">
      <div class=\"label\">证据进度</div>
      <p id=\"evidenceMetrics\"></p>
    </section>
    <div class=\"notice\"><strong>正式资料未接入提示：</strong>{PROXY_ONLY_WARNING}</div>
    <section>
      <div class=\"toolbar\"><h2>今日重点研究队列</h2><span class=\"small\">默认只展示前 8 个，完整池子在下方折叠区。</span></div>
      <div id=\"topCards\" class=\"symbol-grid\"></div>
    </section>
    <details>
      <summary>查看全部标的明细（需要深挖时再展开）</summary>
      <div class=\"toolbar\">
        <h2>全部标的</h2>
        <input id=\"symbolSearch\" type=\"search\" placeholder=\"搜索代码、名称、建议或障碍项\" aria-label=\"搜索个股判断\">
      </div>
      <div id=\"emptyState\" class=\"empty\" hidden>未找到匹配标的。</div>
      <table id=\"symbolTable\">
        <thead><tr><th>代码/名称</th><th>系统建议</th><th>正式关卡</th><th>研究优先级</th><th>置信度</th><th>主要障碍</th><th>升级/失效</th><th>非技术面证据</th></tr></thead>
        <tbody id=\"symbolRows\"></tbody>
      </table>
    </details>
  </main>
  <script id=\"dashboard-data\" type=\"application/json\">{data_json}</script>
  <script>
    const payload = JSON.parse(document.getElementById('dashboard-data').textContent);
    const text = (value) => value === null || value === undefined || value === '' ? '暂无' : String(value);
    const boolText = (value) => value ? '是' : '否';
    const categoryText = (value) => value === 'action' ? '可行动' : value === 'watch' ? '观察' : value === 'avoid' ? '回避' : text(value);
    const judgmentText = (value) => ({{buy_candidate: '买入候选', accumulate: '可累积', hold: '持有观察', trim: '减仓候选', sell_candidate: '卖出候选', watch: '观察', watch_only: '仅观察', avoid: '回避', no_action: '不行动', blocked: '被阻断', action_candidate: '行动候选'}}[value] || text(value));
    const evidenceText = (value) => ({{proxy_only: '正式资料未接入', available: '可用', missing: '缺失'}}[value] || text(value));
    const researchAction = (row) => row.research_action || {{key: 'avoid', label: '暂不碰', reason: '暂无研究动作。', upgrade: '等待新证据。', invalidation: '约束未改善前不升级。'}};
    const researchKind = (key) => key === 'consider' ? 'action' : key === 'confirm' || key === 'observe' ? 'watch' : 'avoid';
    const reasonLabels = payload.reason_labels || {{}};
    const humanizeKey = (value) => text(value).replace(/_/g, ' ');
    const reasonText = (value) => reasonLabels[value] || humanizeKey(value);
    const winRateText = (value) => value === null || value === undefined ? '暂无' : `${{(Number(value) * 100).toFixed(1)}}%`;
    const reasonPills = (reasons, labels, limit = 3) => {{
      const box = document.createElement('div');
      box.className = 'reason-pills';
      const items = (reasons || []).slice(0, limit);
      const visibleLabels = (labels || []).slice(0, limit);
      if (!items.length) {{ box.appendChild(chip('暂无关键障碍', '')); return box; }}
      items.forEach((reason, index) => {{ const span = document.createElement('span'); span.className = 'reason-pill'; span.title = text(reason); span.textContent = visibleLabels[index] || reasonText(reason); box.appendChild(span); }});
      return box;
    }};
    const cell = (label, value) => {{ const td = document.createElement('td'); td.dataset.label = label; if (value instanceof Node) td.appendChild(value); else td.textContent = text(value); return td; }};
    const chip = (label, kind) => {{ const span = document.createElement('span'); span.className = 'chip ' + (kind || ''); span.textContent = label; return span; }};
    let activeFilter = 'all';
    document.getElementById('totalCount').textContent = text(payload.symbols.length);
    const researchCounts = payload.research_action_counts || {{}};
    document.getElementById('considerCount').textContent = text(researchCounts.consider || 0);
    document.getElementById('confirmCount').textContent = text(researchCounts.confirm || 0);
    document.getElementById('observeCount').textContent = text(researchCounts.observe || 0);
    document.getElementById('avoidCount').textContent = text(researchCounts.avoid || 0);
    document.getElementById('winRate').textContent = winRateText(payload.evidence.forward_win_rate);
    document.getElementById('winRateNote').textContent = `前向样本=${{text(payload.evidence.forward_samples)}}；样本不足时胜率不显示。`;
    document.getElementById('evidenceMetrics').textContent = `前向记录=${{text(payload.evidence.forward_logs)}}；成熟天数=${{text(payload.evidence.matured_days)}}；前向样本=${{text(payload.evidence.forward_samples)}}；人工/正式证据=${{text(payload.evidence.curated_available)}}；正式资料未接入=${{text(payload.evidence.proxy_only)}}；缺失=${{text(payload.evidence.missing)}}`;
    const topCards = document.getElementById('topCards');
    const renderTopCards = () => {{
      topCards.textContent = '';
      const rows = payload.symbols.filter(row => activeFilter === 'all' || researchAction(row).key === activeFilter).slice(0, 8);
      if (!rows.length) {{ const empty = document.createElement('div'); empty.className = 'empty'; empty.textContent = '当前筛选下暂无标的。'; topCards.appendChild(empty); return; }}
      for (const row of rows) {{
      const card = document.createElement('article');
      card.className = 'card symbol-card';
      const heading = document.createElement('h3');
      heading.textContent = text(row.symbol);
      const name = document.createElement('div');
      name.className = 'name';
      name.textContent = text(row.display_name || row.name);
      const action = researchAction(row);
      const status = document.createElement('div');
      status.appendChild(chip(action.label, researchKind(action.key)));
      status.appendChild(chip(categoryText(row.category), row.category));
      const metric = document.createElement('div');
      metric.className = 'metric';
      metric.textContent = `研究优先级：${{text(row.score)}} / 100`;
      const gates = document.createElement('div');
      gates.className = 'small';
      gates.textContent = `正式可行动=${{boolText(row.qualified_for_action)}}；观察=${{boolText(row.qualified_for_watch)}}；置信度=${{text(row.confidence)}}`;
      const why = document.createElement('div');
      why.className = 'small';
      why.textContent = `为什么：${{text(action.reason)}}`;
      const blockers = document.createElement('div');
      blockers.className = 'blockers';
      blockers.textContent = '主要障碍：';
      blockers.appendChild(reasonPills(row.blockers, row.blocker_labels, 3));
      const next = document.createElement('div');
      next.className = 'small';
      next.textContent = `升级条件：${{text(action.upgrade)}}｜失效条件：${{text(action.invalidation)}}`;
      card.append(heading, name, status, metric, gates, why, blockers, next);
      topCards.appendChild(card);
      }}
    }};
    const tbody = document.getElementById('symbolRows');
    for (const row of payload.symbols) {{
      const tr = document.createElement('tr');
      const action = researchAction(row);
      tr.dataset.search = [row.symbol, row.display_name, row.name, row.judgment, row.category, action.label, action.reason, action.upgrade, action.invalidation, ...(row.blockers || []), ...(row.blocker_labels || []), row.nontechnical_evidence && row.nontechnical_evidence.status].map(text).join(' ').toLowerCase();
      tr.dataset.researchAction = action.key;
      const title = document.createElement('div');
      const symbolStrong = document.createElement('strong');
      symbolStrong.textContent = text(row.symbol);
      const nameSmall = document.createElement('div');
      nameSmall.className = 'small';
      nameSmall.textContent = text(row.display_name || row.name);
      title.appendChild(symbolStrong);
      title.appendChild(nameSmall);
      tr.appendChild(cell('代码/名称', title));
      const judgment = document.createElement('div');
      judgment.appendChild(chip(action.label, researchKind(action.key)));
      judgment.appendChild(chip(judgmentText(row.judgment), row.category));
      judgment.appendChild(chip(categoryText(row.category), row.category));
      if (row.risk_cap) judgment.appendChild(chip('风险上限 ' + judgmentText(row.risk_cap), ''));
      tr.appendChild(cell('系统建议', judgment));
      tr.appendChild(cell('正式关卡', `可行动=${{boolText(row.qualified_for_action)}}；观察=${{boolText(row.qualified_for_watch)}}`));
      const priority = document.createElement('div');
      priority.textContent = text(row.score);
      const why = document.createElement('div');
      why.className = 'small';
      why.textContent = `为什么：${{text(action.reason)}}`;
      priority.appendChild(why);
      tr.appendChild(cell('研究优先级', priority));
      tr.appendChild(cell('置信度', row.confidence));
      tr.appendChild(cell('主要障碍', reasonPills(row.blockers, row.blocker_labels, 8)));
      const conditions = document.createElement('div');
      const upgrade = document.createElement('div');
      upgrade.textContent = `升级：${{text(action.upgrade)}}`;
      const invalidation = document.createElement('div');
      invalidation.className = 'small';
      invalidation.textContent = `失效：${{text(action.invalidation)}}`;
      conditions.append(upgrade, invalidation);
      tr.appendChild(cell('升级/失效', conditions));
      const evidence = row.nontechnical_evidence || {{}};
      const evidenceNode = document.createElement('div');
      evidenceNode.appendChild(chip(evidenceText(evidence.status), evidence.proxy_only ? 'proxy' : ''));
      const detail = document.createElement('div');
      detail.className = 'small';
      detail.textContent = `正式资料未接入=${{boolText(evidence.proxy_only)}}；总分=${{text(evidence.total_score)}}；事件风险=${{text(evidence.event_risk)}}`;
      evidenceNode.appendChild(detail);
      if (evidence.proxy_only) {{ const warn = document.createElement('div'); warn.className = 'small'; warn.textContent = payload.proxy_only_warning; evidenceNode.appendChild(warn); }}
      tr.appendChild(cell('非技术面证据', evidenceNode));
      tbody.appendChild(tr);
    }}
    const search = document.getElementById('symbolSearch');
    const empty = document.getElementById('emptyState');
    const applyFilters = () => {{
      const needle = search.value.trim().toLowerCase();
      let visible = 0;
      for (const tr of tbody.querySelectorAll('tr')) {{
        const categoryMatch = activeFilter === 'all' || tr.dataset.researchAction === activeFilter;
        const textMatch = !needle || tr.dataset.search.includes(needle);
        const show = categoryMatch && textMatch;
        tr.hidden = !show;
        if (show) visible += 1;
      }}
      empty.hidden = visible !== 0;
      renderTopCards();
    }};
    for (const button of document.querySelectorAll('.filter-pill')) {{
      button.addEventListener('click', () => {{
        activeFilter = button.dataset.filter || 'all';
        document.querySelectorAll('.filter-pill').forEach(item => item.classList.toggle('active', item === button));
        applyFilters();
      }});
    }}
    search.addEventListener('input', () => {{
      applyFilters();
    }});
    applyFilters();
  </script>
</body>
</html>
"""


def build_dashboard(
    date: str,
    session: str,
    close_report_json_path: pathlib.Path | None,
    close_report_md_path: pathlib.Path | None,
    ranking_path: pathlib.Path | None,
    nontechnical_evidence_path: pathlib.Path | None,
    forward_evaluation_path: pathlib.Path | None,
    evidence_ledger_path: pathlib.Path | None,
    output_path: pathlib.Path = DEFAULT_OUTPUT,
) -> dict[str, Any]:
    close_report = load_json(close_report_json_path)
    close_markdown = load_close_markdown(close_report_md_path)
    ranking = load_json(ranking_path)
    nontechnical = load_json(nontechnical_evidence_path)
    forward_eval = load_json(forward_evaluation_path)
    evidence_ledger = load_json(evidence_ledger_path)
    payload = build_payload(
        date,
        session,
        close_report,
        close_markdown,
        ranking,
        nontechnical,
        forward_eval,
        evidence_ledger,
        {
            "close_report_json": close_report_json_path,
            "close_report_markdown": close_report_md_path,
            "ranking": ranking_path,
            "nontechnical_evidence": nontechnical_evidence_path,
            "forward_evaluation": forward_evaluation_path,
            "evidence_ledger": evidence_ledger_path,
        },
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(payload), encoding="utf-8")
    return {"output": str(output_path), "payload": payload}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a standalone local HTML dashboard for investment research artifacts.")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--session", default="close")
    parser.add_argument("--close-report-json", default=None)
    parser.add_argument("--close-report-md", default=None)
    parser.add_argument("--ranking", default=None)
    parser.add_argument("--nontechnical-evidence", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.json"))
    parser.add_argument("--forward-evaluation", default=str(ROOT / "research" / "shadow" / "latest_forward_evaluation.json"))
    parser.add_argument("--evidence-ledger", default=str(ROOT / "research" / "shadow" / "latest_evidence_ledger.json"))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    stem = output_stem(args.date, args.session)
    close_json = resolve_path(args.close_report_json) or ROOT / "research" / "products" / "daily_close" / f"{stem}-close-report.json"
    close_md = resolve_path(args.close_report_md) or ROOT / "research" / "products" / "daily_close" / f"{stem}-close-report.md"
    ranking = resolve_path(args.ranking) or ROOT / "research" / "rankings" / f"{args.date if args.session == 'historical' else f'{args.date}-{args.session}'}-ranking.json"
    result = build_dashboard(
        args.date,
        args.session,
        close_json,
        close_md,
        ranking,
        resolve_path(args.nontechnical_evidence),
        resolve_path(args.forward_evaluation),
        resolve_path(args.evidence_ledger),
        resolve_path(args.output) or DEFAULT_OUTPUT,
    )
    print(json.dumps({"output": result["output"], "symbol_count": len(result["payload"].get("symbols", []))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

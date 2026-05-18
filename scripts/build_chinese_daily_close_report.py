#!/usr/bin/env python3

import argparse
import json
import pathlib
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT_DIR = ROOT / "research" / "products" / "daily_close"
ALLOWED_FINAL_STATES_BY_CAP = {
    "avoid": {"avoid"},
    "watch_only": {"watch_only", "avoid"},
    "buy_candidate": {"buy_candidate", "watch_only", "avoid"},
    "accumulate": {"accumulate", "buy_candidate", "watch_only", "avoid"},
    "hold": {"hold", "watch_only", "avoid"},
    "trim": {"trim", "watch_only", "avoid"},
    "sell_candidate": {"sell_candidate", "trim", "watch_only", "avoid"},
}
ACTION_LIKE_STATES = {"buy_candidate", "accumulate", "hold", "trim", "sell_candidate"}
WATCH_LIKE_STATES = {"watch", "watch_only"}
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
    "quote_trade_date_mismatch": "行情日期不匹配",
    "range_pos_60_below_0_12": "区间位置过低",
    "same_theme_best_peer_evidence_missing_or_failed": "同主题证据不足",
    "symbol_recent_adverse_breach": "近期逆向风险",
    "symbol_risk_veto": "个股风险否决",
    "volume_ratio_20_below_1_0": "量能不足",
}
HARD_RESEARCH_BLOCKERS = {
    "symbol_risk_veto",
    "symbol_recent_adverse_breach",
    "downtrend_regime",
    "price_below_ma20_and_ma60",
    "range_pos_60_below_0_12",
}


def load_json(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def file_metadata(path: pathlib.Path | None) -> dict[str, Any]:
    return {"path": str(path) if path else None, "exists": bool(path and path.exists())}


def clean_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if value:
        return [str(value)]
    return []


def unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def reason_label(reason: str) -> str:
    return REASON_LABELS.get(reason, reason)


def ranking_rows_by_symbol(ranking: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "top_candidates", "actionable_candidates", "diagnostic_candidates"):
        values = (ranking or {}).get(key, [])
        if not isinstance(values, list):
            continue
        for row in values:
            if isinstance(row, dict) and row.get("symbol") and str(row["symbol"]) not in rows:
                rows[str(row["symbol"])] = row
    return rows


def nontechnical_symbols_by_symbol(nontechnical_evidence: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    symbols = (nontechnical_evidence or {}).get("symbols", {})
    if not isinstance(symbols, dict):
        return {}
    return {str(symbol): row for symbol, row in symbols.items() if isinstance(row, dict)}


def nontechnical_profile(symbol: str, ranking_row: dict[str, Any], nontechnical_symbols: dict[str, dict[str, Any]]) -> dict[str, Any]:
    profile = ranking_row.get("nontechnical_evidence") if isinstance(ranking_row.get("nontechnical_evidence"), dict) else {}
    raw = nontechnical_symbols.get(symbol, {})
    status = profile.get("status") or raw.get("status")
    evidence_mode = raw.get("evidence_mode") or profile.get("evidence_mode")
    proxy_only = bool(
        profile.get("proxy_only") is True
        or raw.get("proxy_only") is True
        or status == "proxy_only"
        or evidence_mode in {"automatic_local_proxy", "proxy_only"}
    )
    if proxy_only:
        status = "proxy_only"
    elif evidence_mode == "missing_fail_closed":
        status = "missing"
    return {
        "status": status,
        "evidence_mode": evidence_mode,
        "proxy_only": proxy_only,
        "event_risk": profile.get("event_risk") or raw.get("event_risk"),
        "total_score": profile.get("total_score") if profile.get("total_score") is not None else raw.get("total_score"),
        "source_count": profile.get("source_count") if profile.get("source_count") is not None else raw.get("source_count"),
        "proxy_source_count": profile.get("proxy_source_count") if profile.get("proxy_source_count") is not None else raw.get("proxy_source_count"),
    }


def evidence_text_implies_proxy_only(text: str | None) -> bool:
    if not text:
        return False
    return "status=proxy_only" in text or "nontechnical_proxy_only" in text or "proxy_only=True" in text


def output_stem(date: str, session: str) -> str:
    return date if session in {"close", "historical"} else f"{date}-{session}"


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def require_close_session(calls: dict[str, Any] | None, session: str) -> None:
    actual = str((calls or {}).get("session") or session)
    if actual != "close":
        raise ValueError("Chinese daily close product requires session=close")


def date_value(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    return None


def assert_not_future(label: str, value: Any, report_date: str) -> None:
    parsed = date_value(value)
    if parsed and parsed > report_date:
        raise ValueError(f"{label} date {parsed} is after report date {report_date}")


def validate_source_dates(
    date: str,
    calls: dict[str, Any],
    ranking: dict[str, Any] | None,
    risk_review: dict[str, Any] | None,
    evidence_ledger: dict[str, Any] | None,
    calibration: dict[str, Any] | None,
    forward_eval: dict[str, Any] | None,
    variant_competition: dict[str, Any] | None,
    nontechnical_evidence: dict[str, Any] | None,
    nontechnical_attribution: dict[str, Any] | None,
) -> None:
    if date_value(calls.get("date")) != date:
        raise ValueError("calls date must match report date")
    if ranking is not None:
        assert_not_future("ranking as_of_date", ranking.get("as_of_date"), date)
    if risk_review is None:
        raise ValueError("Chinese daily close product requires risk review verdict caps")
    assert_not_future("risk review date", risk_review.get("date"), date)
    risk_review_date = date_value(risk_review.get("date"))
    if risk_review_date is None:
        raise ValueError("risk review date must match report date")
    if risk_review_date != date:
        raise ValueError("risk review date must match report date")
    if str(risk_review.get("session") or "") != "close":
        raise ValueError("risk review session must be close")
    if evidence_ledger is not None:
        assert_not_future("evidence ledger as_of_date", evidence_ledger.get("as_of_date"), date)
    if calibration is not None:
        assert_not_future("calibration as_of_date", calibration.get("as_of_date"), date)
    if forward_eval is not None:
        thresholds = forward_eval.get("thresholds", {}) if isinstance(forward_eval.get("thresholds"), dict) else {}
        assert_not_future("forward evaluation as_of_date", thresholds.get("as_of_date"), date)
    if variant_competition is not None:
        assert_not_future("variant competition as_of_date", variant_competition.get("as_of_date") or variant_competition.get("date"), date)
    if nontechnical_evidence is not None:
        assert_not_future("nontechnical evidence as_of_date", nontechnical_evidence.get("as_of_date"), date)
    if nontechnical_attribution is not None:
        assert_not_future("nontechnical attribution as_of_date", nontechnical_attribution.get("as_of_date"), date)


def verdicts_by_symbol(risk_review: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    rows = {}
    for verdict in (risk_review or {}).get("verdicts", []):
        if isinstance(verdict, dict) and verdict.get("symbol"):
            rows[str(verdict["symbol"])] = verdict
    return rows


def summarize_recommendations(calls: dict[str, Any], risk_review: dict[str, Any] | None) -> list[dict[str, Any]]:
    if risk_review is None:
        raise ValueError("missing risk review verdict caps")
    verdicts = verdicts_by_symbol(risk_review)
    rows = []
    for rec in calls.get("recommendations", []):
        if not isinstance(rec, dict):
            continue
        symbol = str(rec.get("symbol") or "")
        verdict = verdicts.get(symbol, {})
        state = str(rec.get("state") or "avoid")
        cap = str(verdict.get("final_state_cap") or state)
        if risk_review is not None and not verdict:
            raise ValueError(f"missing risk review verdict for {symbol}")
        allowed = ALLOWED_FINAL_STATES_BY_CAP.get(cap, set())
        if state not in allowed:
            raise ValueError(f"call state {state} exceeds risk review cap {cap} for {symbol}")
        nontechnical = None
        for item in rec.get("evidence", []):
            if isinstance(item, str) and item.startswith("nontechnical_evidence "):
                nontechnical = item
                break
        rows.append(
            {
                "symbol": symbol,
                "state": state,
                "effective_state": state,
                "theme": rec.get("theme"),
                "confidence": rec.get("confidence"),
                "risk_cap": cap,
                "risk_decision": verdict.get("risk_decision"),
                "rationale": rec.get("rationale"),
                "risks": rec.get("risks", [])[:3] if isinstance(rec.get("risks"), list) else [],
                "invalidation": rec.get("invalidation"),
                "nontechnical_evidence": nontechnical,
            }
        )
    return rows


def research_action_for(row: dict[str, Any]) -> dict[str, Any]:
    state = str(row.get("state") or "").lower()
    score = as_float(row.get("score")) or 0.0
    qualified_for_action = row.get("qualified_for_action") is True
    qualified_for_watch = row.get("qualified_for_watch") is True
    blockers = unique(clean_list(row.get("gate_blockers")) + [item for item in clean_list(row.get("blockers")) if item in REASON_LABELS])
    blocker_set = set(blockers)
    nontechnical = row.get("nontechnical_profile") if isinstance(row.get("nontechnical_profile"), dict) else {}
    event_risk = str(nontechnical.get("event_risk") or "").lower()
    proxy_only = nontechnical.get("proxy_only") is True or "nontechnical_proxy_only" in blocker_set or evidence_text_implies_proxy_only(str(row.get("nontechnical_evidence") or ""))
    hard_blocked = state == "avoid" or bool(blocker_set & HARD_RESEARCH_BLOCKERS)

    if state in ACTION_LIKE_STATES and qualified_for_action and not blockers and not proxy_only and event_risk not in {"unknown", "policy", "high"}:
        return {
            "key": "consider",
            "label": "可考虑研究",
            "why": "正式行动门槛、风险上限与非技术面约束均未显示阻断；仍只进入人工研究队列。",
            "upgrade": "不自动升级为交易；需人工复核资金、组合和最新盘中证据后另行判断。",
            "invalidation": row.get("invalidation") or "若风险上限下调、行动门槛失效、事件风险升高或非技术面证据转差，立即降级。",
            "formal_actionable": True,
        }
    if hard_blocked or (state == "avoid" and not qualified_for_watch):
        return {
            "key": "avoid",
            "label": "暂不碰",
            "why": "状态或硬阻断不支持投入研究时间。",
            "upgrade": "硬阻断解除并重新通过观察门槛后，才恢复观察。",
            "invalidation": "硬性阻断未解除前不升级；若更多风险暴露，继续维持回避。",
            "formal_actionable": False,
        }
    if state in ACTION_LIKE_STATES or qualified_for_action or (qualified_for_watch and (score >= 70 or proxy_only or event_risk in {"unknown", "policy", "high"})):
        why = "接近候选，但仍有关键确认项未满足。"
        if proxy_only:
            why = "正式资料未接入或存在资料阻断，不能视为正式行动候选。"
        return {
            "key": "confirm",
            "label": "等确认",
            "why": why,
            "upgrade": "阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。",
            "invalidation": row.get("invalidation") or "若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。",
            "formal_actionable": False,
        }
    if state in WATCH_LIKE_STATES or qualified_for_watch or score >= 45:
        return {
            "key": "observe",
            "label": "继续观察",
            "why": "有跟踪价值，但当前强度、证据或关卡状态不足。",
            "upgrade": "分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。",
            "invalidation": row.get("invalidation") or "若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。",
            "formal_actionable": False,
        }
    return {
        "key": "avoid",
        "label": "暂不碰",
        "why": "信号不足或约束不通过，暂不投入研究时间。",
        "upgrade": "重新通过观察门槛且无硬阻断后，可恢复观察。",
        "invalidation": "硬性阻断未解除前不升级。",
        "formal_actionable": False,
    }


def summarize_research_actions(recommendations: list[dict[str, Any]], ranking: dict[str, Any] | None, nontechnical_evidence: dict[str, Any] | None) -> list[dict[str, Any]]:
    ranked = ranking_rows_by_symbol(ranking)
    nontechnical_symbols = nontechnical_symbols_by_symbol(nontechnical_evidence)
    rows: list[dict[str, Any]] = []
    seen: set[str] = set()

    for rec in recommendations:
        symbol = str(rec.get("symbol") or "")
        if not symbol:
            continue
        ranked_row = ranked.get(symbol, {})
        gate_blockers = unique(clean_list(ranked_row.get("action_disqualifiers")) + clean_list(ranked_row.get("disqualifiers")))
        blockers = unique(gate_blockers + clean_list(rec.get("risks")))
        row = {
            "symbol": symbol,
            "state": rec.get("state"),
            "confidence": rec.get("confidence"),
            "score": ranked_row.get("score"),
            "qualified_for_action": ranked_row.get("qualified_for_action") is True,
            "qualified_for_watch": ranked_row.get("qualified_for_watch") is True,
            "gate_blockers": gate_blockers,
            "blockers": blockers,
            "why_source": rec.get("rationale"),
            "invalidation": rec.get("invalidation"),
            "nontechnical_evidence": rec.get("nontechnical_evidence"),
            "nontechnical_profile": nontechnical_profile(symbol, ranked_row, nontechnical_symbols),
        }
        row["research_action"] = research_action_for(row)
        rows.append(row)
        seen.add(symbol)

    for ranked_row in ranked.values():
        symbol = str(ranked_row.get("symbol") or "")
        if not symbol or symbol in seen:
            continue
        blockers = unique(clean_list(ranked_row.get("action_disqualifiers")) + clean_list(ranked_row.get("disqualifiers")))
        row = {
            "symbol": symbol,
            "state": "ranking_only",
            "confidence": ranked_row.get("confidence"),
            "score": ranked_row.get("score"),
            "qualified_for_action": ranked_row.get("qualified_for_action") is True,
            "qualified_for_watch": ranked_row.get("qualified_for_watch") is True,
            "gate_blockers": blockers,
            "blockers": blockers,
            "why_source": None,
            "invalidation": None,
            "nontechnical_evidence": None,
            "nontechnical_profile": nontechnical_profile(symbol, ranked_row, nontechnical_symbols),
        }
        row["research_action"] = research_action_for(row)
        rows.append(row)

    order = {"consider": 0, "confirm": 1, "observe": 2, "avoid": 3}
    rows.sort(key=lambda row: (order.get(row["research_action"]["key"], 9), -(as_float(row.get("score")) or 0.0), str(row.get("symbol") or "")))
    return rows


def top_rows(ranking: dict[str, Any] | None, key: str, limit: int = 5) -> list[dict[str, Any]]:
    rows = (ranking or {}).get(key, [])
    return rows[:limit] if isinstance(rows, list) else []


def summary_get(data: dict[str, Any] | None, path: list[str], default: Any = None) -> Any:
    node: Any = data
    for key in path:
        if not isinstance(node, dict):
            return default
        node = node.get(key)
    return node if node is not None else default


def build_payload(
    date: str,
    session: str,
    calls: dict[str, Any],
    ranking: dict[str, Any] | None,
    risk_review: dict[str, Any] | None,
    evidence_ledger: dict[str, Any] | None,
    calibration: dict[str, Any] | None,
    forward_eval: dict[str, Any] | None,
    variant_competition: dict[str, Any] | None,
    nontechnical_evidence: dict[str, Any] | None,
    nontechnical_attribution: dict[str, Any] | None,
    sources: dict[str, pathlib.Path | None],
) -> dict[str, Any]:
    require_close_session(calls, session)
    validate_source_dates(date, calls, ranking, risk_review, evidence_ledger, calibration, forward_eval, variant_competition, nontechnical_evidence, nontechnical_attribution)
    recommendations = summarize_recommendations(calls, risk_review)
    research_actions = summarize_research_actions(recommendations, ranking, nontechnical_evidence)
    return {
        "date": date,
        "session": "close",
        "source_of_truth": "calls_json_with_risk_review_caps",
        "research_only": True,
        "no_execution": True,
        "recommendations": recommendations,
        "research_actions": research_actions,
        "ranking": {
            "actionable_count": len((ranking or {}).get("actionable_candidates", [])) if isinstance((ranking or {}).get("actionable_candidates", []), list) else 0,
            "diagnostic_count": len((ranking or {}).get("diagnostic_candidates", [])) if isinstance((ranking or {}).get("diagnostic_candidates", []), list) else 0,
            "top_watch": top_rows(ranking, "top_candidates", 5),
        },
        "evidence": {
            "forward_shadow_logs": summary_get(evidence_ledger, ["summary", "forward_shadow_log_count"], summary_get(forward_eval, ["summary", "forward_shadow_log_count"])),
            "matured_forward_days": summary_get(evidence_ledger, ["shadow_evaluation_summary", "matured_forward_shadow_days"], summary_get(forward_eval, ["summary", "matured_forward_shadow_days"])),
            "forward_sample_count": summary_get(forward_eval, ["summary", "sample_count"], 0),
            "audit_passed": summary_get(evidence_ledger, ["audit_passed"]),
        },
        "calibration": {
            "sample_count": summary_get(calibration, ["summary", "combined_record_count"]),
            "scored_sample_count": summary_get(calibration, ["scorecard", "scored_sample_count"]),
            "hit_rate": summary_get(calibration, ["scorecard", "hit_rate"]),
            "brier_score": summary_get(calibration, ["scorecard", "brier_score"]),
            "calibration_error": summary_get(calibration, ["scorecard", "calibration_error"]),
        },
        "variants": {
            "competition_id": (variant_competition or {}).get("competition_id"),
            "scoreboard": (variant_competition or {}).get("scoreboard", [])[:3] if isinstance((variant_competition or {}).get("scoreboard", []), list) else [],
        },
        "nontechnical": {
            "evidence_summary": (nontechnical_evidence or {}).get("summary", {}),
            "attribution_summary": (nontechnical_attribution or {}).get("summary", {}),
            "score_buckets": summary_get(nontechnical_attribution, ["buckets", "total_score"], [])[:5]
            if isinstance(summary_get(nontechnical_attribution, ["buckets", "total_score"], []), list)
            else [],
        },
        "sources": {name: file_metadata(path) for name, path in sources.items()},
    }


def render_markdown(payload: dict[str, Any]) -> str:
    recs = payload["recommendations"]
    buy_like = [row for row in recs if row.get("state") == "buy_candidate"]
    watch = [row for row in recs if row.get("state") == "watch_only"]
    avoid = [row for row in recs if row.get("state") == "avoid"]
    nontechnical_summary = payload["nontechnical"]["evidence_summary"]
    curated_available = nontechnical_summary.get("curated_available_count", nontechnical_summary.get("available_count"))
    proxy_only_count = nontechnical_summary.get("proxy_only_count", nontechnical_summary.get("automatic_proxy_count", 0)) or 0
    final_result = "今日无行动候选；仅保留观察名单。" if not buy_like else "今日行动候选：" + "、".join(f"{row['symbol']}({row.get('confidence')})" for row in buy_like[:3])
    lines = [
        f"# {payload['date']} 收盘研究报告",
        "",
        "## 最终结果",
        f"- {final_result}",
        f"- 首要观察：{ '、'.join(row['symbol'] for row in watch[:3]) if watch else '无' }。",
        "- 执行状态：research-only，不下单、不改组合。",
        "",
        "## 今日结论",
        f"- 研究模式：仅推荐研究；不执行交易、不修改组合。",
        f"- 行动候选：{len(buy_like)} 个；观察名单：{len(watch)} 个；回避/不行动：{len(avoid)} 个。",
        f"- 证据进度：forward logs={payload['evidence']['forward_shadow_logs']}，matured days={payload['evidence']['matured_forward_days']}，forward samples={payload['evidence']['forward_sample_count']}。",
        "",
        "## 重点标的表",
    ]
    if not recs:
        lines.append("- 今日没有结构化推荐。")
    for row in recs[:8]:
        lines.append(f"- `{row['symbol']}`：状态={row.get('state')}，主题={row.get('theme')}，置信度={row.get('confidence')}，风险上限={row.get('risk_cap') or 'n/a'}。")
        if row.get("rationale"):
            lines.append(f"  - 理由：{row['rationale']}")
        if row.get("risks"):
            lines.append(f"  - 风险：{'；'.join(str(item) for item in row['risks'])}")
        if row.get("nontechnical_evidence"):
            lines.append(f"  - 非技术面：{row['nontechnical_evidence']}")
        if row.get("invalidation"):
            lines.append(f"  - 失效条件：{row['invalidation']}")
    lines.extend(["", "## 研究型行动建议", "- 声明：本节仅用于安排后续研究优先级；research-only、非交易、不下单、不改组合；不得把正式资料未接入的结果或 shadow 结果描述为正式可行动。"])
    research_actions = payload.get("research_actions") or []
    if not research_actions:
        lines.append("- 今日没有可排序的研究对象。")
    for row in research_actions[:8]:
        action = row.get("research_action") or {}
        profile = row.get("nontechnical_profile") if isinstance(row.get("nontechnical_profile"), dict) else {}
        blockers = clean_list(row.get("blockers"))
        blocker_text = "、".join(reason_label(item) for item in blockers[:4]) if blockers else "暂无主要障碍"
        score = row.get("score") if row.get("score") is not None else "n/a"
        proxy_note = "；正式资料未接入，不清除正式行动门槛" if profile.get("proxy_only") else ""
        formal_note = "正式门槛通过但仍非交易指令" if action.get("formal_actionable") else "非正式行动候选"
        lines.append(f"- `{row.get('symbol')}`：{action.get('label')}；状态={row.get('state')}；score={score}；{formal_note}{proxy_note}。")
        lines.append(f"  - why：{row.get('why_source') or action.get('why')}")
        lines.append(f"  - 主要障碍：{blocker_text}。")
        lines.append(f"  - 升级条件：{action.get('upgrade')}")
        lines.append(f"  - 失效条件：{action.get('invalidation')}")
    lines.extend(["", "## Gate 拒绝与观察重点"])
    for row in payload["ranking"]["top_watch"][:5]:
        disq = row.get("action_disqualifiers") or row.get("disqualifiers") or []
        lines.append(f"- `{row.get('symbol')}` score={row.get('score')} action={row.get('qualified_for_action')} watch={row.get('qualified_for_watch')} gates={disq[:3]}")
    lines.extend(
        [
            "",
            "## 影子证据与校准",
            f"- Evidence audit passed：{payload['evidence']['audit_passed']}。",
            f"- Calibration samples（historical/posterior diagnostics，不计入 forward readiness）：{payload['calibration']['sample_count']}；hit_rate={payload['calibration']['hit_rate']}；Brier={payload['calibration']['brier_score']}；calibration_error={payload['calibration']['calibration_error']}。",
            "",
            "## 非技术面证据与归因",
            f"- 非技术面证据覆盖：正式证据={curated_available} / 标的数={nontechnical_summary.get('symbol_count')}；正式资料未接入={proxy_only_count}；缺失={nontechnical_summary.get('missing_count')}；阻断项={nontechnical_summary.get('blocking_finding_count')}；严重项={nontechnical_summary.get('critical_finding_count')}。",
            f"- Attribution samples：{payload['nontechnical']['attribution_summary'].get('attributed_sample_count')}；hit_rate={payload['nontechnical']['attribution_summary'].get('hit_rate')}；avg_return={payload['nontechnical']['attribution_summary'].get('avg_return_pct')}。",
        ]
    )
    if proxy_only_count:
        lines.append("- 正式资料未接入的行尚未取得正式基本面、估值或事件资料；这些行只作观察和排序，不清除行动门槛。")
    for row in payload["nontechnical"].get("score_buckets") or []:
        lines.append(f"- 非技术面分桶 `{row.get('score_bucket')}` samples={row.get('scored_sample_count')} hit_rate={row.get('hit_rate')} avg_return={row.get('avg_return_pct')}")
    lines.extend(["", "## Shadow 变体竞赛"])
    variants = payload["variants"].get("scoreboard") or []
    if not variants:
        lines.append("- 暂无可排名的 shadow-only 变体样本；继续累计 forward evidence。")
    for row in variants:
        lines.append(f"- #{row.get('diagnostic_rank')} `{row.get('variant_id')}` samples={row.get('sample_count')} avg_net={row.get('avg_net_return_pct')} alpha={row.get('avg_alpha_pct')} audit={row.get('no_execution_audit_passed')}")
    lines.extend(
        [
            "",
            "## 数据与限制",
            "- 本报告只整理 deterministic ranking、calls、risk review、shadow evidence、calibration scorecard 和非技术面 evidence/attribution。",
            "- 不把 historical replay 当作 forward evidence；不因 shadow 变体结果自动晋升 active strategy。",
            "- forward 样本不足时，所有结论只能作为研究观察。",
            "",
            "## 研究声明",
            "- 这不是投资建议或交易指令；系统不会自动下单，也不会假设真实持仓。",
        ]
    )
    return "\n".join(lines) + "\n"


def build_report(
    date: str,
    session: str,
    calls_path: pathlib.Path,
    ranking_path: pathlib.Path | None,
    risk_review_path: pathlib.Path | None,
    evidence_ledger_path: pathlib.Path | None,
    calibration_path: pathlib.Path | None,
    forward_eval_path: pathlib.Path | None,
    variant_competition_path: pathlib.Path | None,
    output_dir: pathlib.Path,
    nontechnical_evidence_path: pathlib.Path | None = None,
    nontechnical_attribution_path: pathlib.Path | None = None,
) -> dict[str, Any]:
    calls = load_json(calls_path)
    if calls is None:
        raise ValueError(f"missing calls file: {calls_path}")
    payload = build_payload(
        date,
        session,
        calls,
        load_json(ranking_path),
        load_json(risk_review_path),
        load_json(evidence_ledger_path),
        load_json(calibration_path),
        load_json(forward_eval_path),
        load_json(variant_competition_path),
        load_json(nontechnical_evidence_path),
        load_json(nontechnical_attribution_path),
        {
            "calls": calls_path,
            "ranking": ranking_path,
            "risk_review": risk_review_path,
            "evidence_ledger": evidence_ledger_path,
            "calibration_scorecard": calibration_path,
            "forward_evaluation": forward_eval_path,
            "variant_competition": variant_competition_path,
            "nontechnical_evidence": nontechnical_evidence_path,
            "nontechnical_attribution": nontechnical_attribution_path,
        },
    )
    stem = output_stem(date, session)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{stem}-close-report.json"
    md_path = output_dir / f"{stem}-close-report.md"
    latest_md = output_dir / "latest.md"
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    markdown = render_markdown(payload)
    md_path.write_text(markdown, encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path), "latest": str(latest_md), "payload": payload}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic Chinese daily close research product report.")
    parser.add_argument("--date", required=True)
    parser.add_argument("--session", default="close")
    parser.add_argument("--calls", required=True)
    parser.add_argument("--ranking", default=None)
    parser.add_argument("--risk-review", default=None)
    parser.add_argument("--evidence-ledger", default=str(ROOT / "research" / "shadow" / "latest_evidence_ledger.json"))
    parser.add_argument("--calibration-scorecard", default=str(ROOT / "research" / "evaluations" / "latest_calibration_scorecard.json"))
    parser.add_argument("--forward-evaluation", default=str(ROOT / "research" / "shadow" / "latest_forward_evaluation.json"))
    parser.add_argument("--variant-competition", default=None)
    parser.add_argument("--nontechnical-evidence", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.json"))
    parser.add_argument("--nontechnical-attribution", default=str(ROOT / "research" / "evaluations" / "latest_nontechnical_attribution.json"))
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    args = parser.parse_args()

    result = build_report(
        args.date,
        args.session,
        resolve_path(args.calls) or pathlib.Path(args.calls),
        resolve_path(args.ranking),
        resolve_path(args.risk_review),
        resolve_path(args.evidence_ledger),
        resolve_path(args.calibration_scorecard),
        resolve_path(args.forward_evaluation),
        resolve_path(args.variant_competition),
        resolve_path(args.output_dir) or DEFAULT_OUTPUT_DIR,
        resolve_path(args.nontechnical_evidence),
        resolve_path(args.nontechnical_attribution),
    )
    print(json.dumps({key: result[key] for key in ["json", "markdown", "latest"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3

import argparse
import copy
import datetime as dt
import hashlib
import json
import pathlib
import sys
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from backtest_investment_strategy import EXPERIMENTAL_EXIT_RULES, EXPERIMENTAL_RISK_FILTERS, apply_experimental_risk_filter  # noqa: E402
from rank_investment_universe import DEFAULT_CN_MARKET_PROXY_SYMBOL, DEFAULT_MARKET_PROXY_SYMBOL, candidate_layers, market_family_for_symbol  # noqa: E402


DEFAULT_SHADOW_RISK_FILTER = "combined_heat_mid_range_market_stall"
DEFAULT_SHADOW_EXIT_RULE = "daily_close_stop"
DEFAULT_SHADOW_STOP_LOSS_PCT = -4.0
DEFAULT_SHADOW_HORIZON_DAYS = 14
EVIDENCE_MODES = {"forward_shadow", "historical_replay"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_path(path: str | pathlib.Path | None) -> pathlib.Path | None:
    if path is None or str(path) == "":
        return None
    candidate = pathlib.Path(path)
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def file_metadata(path: pathlib.Path | None) -> dict[str, Any] | None:
    if path is None:
        return None
    exists = path.exists()
    metadata: dict[str, Any] = {
        "path": str(path),
        "exists": exists,
        "sha256": None,
        "size_bytes": None,
    }
    if exists and path.is_file():
        content = path.read_bytes()
        metadata["sha256"] = hashlib.sha256(content).hexdigest()
        metadata["size_bytes"] = len(content)
    return metadata


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def benchmark_symbol(symbol: str) -> str:
    return DEFAULT_CN_MARKET_PROXY_SYMBOL if market_family_for_symbol(symbol) == "cn" else DEFAULT_MARKET_PROXY_SYMBOL


def stop_close_price(row: dict[str, Any], stop_loss_pct: float) -> float | None:
    price = as_float(row.get("latest_close"))
    if price is None:
        return None
    return round(price * (1.0 + stop_loss_pct / 100.0), 4)


def compact_candidate(row: dict[str, Any], stop_loss_pct: float, horizon_days: int) -> dict[str, Any]:
    symbol = str(row.get("symbol") or "")
    return {
        "symbol": symbol,
        "name": row.get("name"),
        "market_family": market_family_for_symbol(symbol),
        "theme": row.get("theme"),
        "kind": row.get("kind"),
        "source_layer": row.get("source_layer"),
        "score": row.get("score"),
        "qualified_for_action": bool(row.get("qualified_for_action")),
        "qualified_for_watch": bool(row.get("qualified_for_watch")),
        "diagnostic_only": bool(row.get("diagnostic_only")),
        "latest_close": row.get("latest_close"),
        "stop_loss_pct": stop_loss_pct,
        "daily_close_stop_price": stop_close_price(row, stop_loss_pct),
        "planned_horizon_days": horizon_days,
        "benchmark_symbol": benchmark_symbol(symbol),
        "expected_edge_bps": row.get("expected_edge_bps"),
        "net_expected_edge_bps": row.get("net_expected_edge_bps"),
        "cost_gate_passed": row.get("cost_gate_passed"),
        "range_pos_60": row.get("range_pos_60"),
        "pct_change_1d": row.get("pct_change_1d"),
        "volume_ratio_20": row.get("volume_ratio_20"),
        "market_proxy_symbol": row.get("market_proxy_symbol"),
        "market_range_pos_60": row.get("market_range_pos_60"),
        "same_theme_best_symbol": row.get("same_theme_best_symbol"),
        "same_theme_peer_evidence_passed": row.get("same_theme_peer_evidence_passed"),
        "qualification_flags": row.get("qualification_flags", []),
        "disqualifiers": row.get("disqualifiers", []),
        "action_disqualifiers": row.get("action_disqualifiers", []),
        "shadow_filter_profile": row.get("experimental_risk_filter_profile"),
        "shadow_filter_reasons": row.get("experimental_risk_filter_reasons", []),
        "monitoring_rules": [
            "Record only; do not change portfolio state from this shadow log.",
            f"Flag if daily close return is <= {stop_loss_pct}% from shadow entry close.",
            f"Evaluate {horizon_days}-day return and benchmark alpha after the planned horizon.",
        ],
    }


def build_shadow_log(
    ranking: dict[str, Any],
    ranking_path: pathlib.Path | None = None,
    snapshot_path: pathlib.Path | None = None,
    date: str | None = None,
    session: str | None = None,
    risk_filter: str = DEFAULT_SHADOW_RISK_FILTER,
    exit_rule: str = DEFAULT_SHADOW_EXIT_RULE,
    stop_loss_pct: float = DEFAULT_SHADOW_STOP_LOSS_PCT,
    horizon_days: int = DEFAULT_SHADOW_HORIZON_DAYS,
    evidence_mode: str = "forward_shadow",
) -> dict[str, Any]:
    if risk_filter not in EXPERIMENTAL_RISK_FILTERS:
        raise ValueError(f"risk_filter must be one of {sorted(EXPERIMENTAL_RISK_FILTERS)}")
    if exit_rule not in EXPERIMENTAL_EXIT_RULES:
        raise ValueError(f"exit_rule must be one of {sorted(EXPERIMENTAL_EXIT_RULES)}")
    if evidence_mode not in EVIDENCE_MODES:
        raise ValueError(f"evidence_mode must be one of {sorted(EVIDENCE_MODES)}")
    if exit_rule != "off" and stop_loss_pct >= 0:
        raise ValueError("stop_loss_pct must be negative for shadow exit rules")

    thresholds = ranking.get("thresholds", {}) if isinstance(ranking.get("thresholds"), dict) else {}
    actionable_top_n = int(thresholds.get("actionable_top_n") or len(ranking.get("actionable_candidates", [])) or 1)
    diagnostic_top_n = int(thresholds.get("diagnostic_top_n") or len(ranking.get("diagnostic_candidates", [])) or 3)
    shadow_ranked = copy.deepcopy(ranking.get("all_ranked") or ranking.get("top_candidates") or [])
    apply_experimental_risk_filter(shadow_ranked, risk_filter)
    shadow_actionable, shadow_diagnostics, shadow_top = candidate_layers(shadow_ranked, actionable_top_n, diagnostic_top_n)

    production_actionable = ranking.get("actionable_candidates", []) if isinstance(ranking.get("actionable_candidates"), list) else []
    downgraded = [row for row in shadow_ranked if row.get("experimental_risk_filter_profile")]
    snapshot_meta_path = snapshot_path or resolve_path(str(ranking.get("snapshot") or ""))

    return {
        "date": date or ranking.get("as_of_date"),
        "session": session or ranking.get("as_of_session") or ranking.get("session") or "unknown",
        "generated_at": utc_now(),
        "mode": "shadow_logging",
        "evidence_mode": evidence_mode,
        "counts_toward_forward_evidence": evidence_mode == "forward_shadow",
        "shadow_policy": {
            "status": "experimental_shadow_only",
            "production_ranking_unchanged": True,
            "no_execution": True,
            "no_portfolio_mutation": True,
            "risk_filter": risk_filter,
            "exit_rule": exit_rule,
            "stop_loss_pct": stop_loss_pct if exit_rule != "off" else None,
            "horizon_days": horizon_days,
            "evidence_mode": evidence_mode,
            "counts_toward_forward_evidence": evidence_mode == "forward_shadow",
        },
        "source": {
            "ranking": file_metadata(ranking_path),
            "snapshot": file_metadata(snapshot_meta_path),
            "as_of_date": ranking.get("as_of_date"),
            "ranking_generated_at": ranking.get("generated_at"),
            "strategy_id": ranking.get("strategy_id"),
            "strategy_version": ranking.get("strategy_version"),
            "strategy_status": ranking.get("strategy_status"),
        },
        "summary": {
            "production_actionable_count": len(production_actionable),
            "shadow_actionable_count": len(shadow_actionable),
            "shadow_diagnostic_count": len(shadow_diagnostics),
            "downgraded_by_shadow_filter_count": len(downgraded),
        },
        "production_actionable_symbols": [row.get("symbol") for row in production_actionable],
        "shadow_actionable_symbols": [row.get("symbol") for row in shadow_actionable],
        "shadow_actionable_candidates": [compact_candidate(row, stop_loss_pct, horizon_days) for row in shadow_actionable],
        "shadow_diagnostic_candidates": [compact_candidate(row, stop_loss_pct, horizon_days) for row in shadow_diagnostics],
        "downgraded_by_shadow_filter": [compact_candidate(row, stop_loss_pct, horizon_days) for row in downgraded],
    }


def default_output_path(date: str | None, session: str | None) -> pathlib.Path:
    date_part = date or dt.date.today().isoformat()
    session_part = session or "unknown"
    return ROOT / "research" / "shadow" / f"{date_part}-{session_part}-shadow.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a shadow-only investment decision log from a ranking JSON.")
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--date", default=None)
    parser.add_argument("--session", default=None)
    parser.add_argument("--risk-filter", choices=sorted(EXPERIMENTAL_RISK_FILTERS), default=DEFAULT_SHADOW_RISK_FILTER)
    parser.add_argument("--exit-rule", choices=sorted(EXPERIMENTAL_EXIT_RULES), default=DEFAULT_SHADOW_EXIT_RULE)
    parser.add_argument("--stop-loss-pct", type=float, default=DEFAULT_SHADOW_STOP_LOSS_PCT)
    parser.add_argument("--horizon-days", type=int, default=DEFAULT_SHADOW_HORIZON_DAYS)
    parser.add_argument("--evidence-mode", choices=sorted(EVIDENCE_MODES), default="forward_shadow")
    args = parser.parse_args()

    ranking_path = resolve_path(args.ranking)
    if ranking_path is None:
        raise SystemExit("--ranking is required")
    ranking = load_json(ranking_path)
    snapshot_path = resolve_path(args.snapshot) if args.snapshot else None
    date = args.date or ranking.get("as_of_date")
    session = args.session or ranking.get("as_of_session") or ranking.get("session") or "unknown"
    shadow = build_shadow_log(ranking, ranking_path, snapshot_path, date, session, args.risk_filter, args.exit_rule, args.stop_loss_pct, args.horizon_days, args.evidence_mode)

    output_path = resolve_path(args.output) if args.output else default_output_path(date, session)
    if output_path is None:
        raise SystemExit("could not resolve output path")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(shadow, indent=2), encoding="utf-8")
    print(f"Wrote shadow log: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

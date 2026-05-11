#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import pathlib
import statistics
import tomllib
from collections import defaultdict
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent

DEFAULT_THRESHOLDS = {
    "shadow_logging": {
        "min_sample_count": 60,
        "min_avg_net_return_pct": 0.05,
        "max_adverse_breach_rate": 0.0,
        "required_sample_quality": "sufficient",
    },
    "paper_trading": {
        "min_sample_count": 70,
        "min_win_rate": 0.50,
        "min_avg_net_return_pct": 0.15,
        "min_median_net_return_pct": 0.0,
        "min_avg_alpha_pct": 0.50,
        "min_max_adverse_pct": -6.0,
        "max_adverse_breach_rate": 0.0,
        "required_sample_quality": "sufficient",
        "min_mature_months": 4,
        "min_month_sample_count": 5,
        "min_mature_month_win_rate": 0.40,
        "min_mature_month_avg_net_return_pct": -0.30,
    },
    "small_live_observation": {
        "min_sample_count": 100,
        "min_win_rate": 0.56,
        "min_avg_net_return_pct": 0.30,
        "min_median_net_return_pct": 0.10,
        "min_avg_alpha_pct": 0.75,
        "min_max_adverse_pct": -4.0,
        "max_adverse_breach_rate": 0.0,
        "required_sample_quality": "sufficient",
        "min_forward_paper_days": 20,
        "max_forward_adverse_breach_rate": 0.0,
    },
}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def load_toml(path: pathlib.Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def as_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, bool):
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def as_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def merge_thresholds(profile: dict[str, Any]) -> dict[str, dict[str, Any]]:
    thresholds = {key: dict(value) for key, value in DEFAULT_THRESHOLDS.items()}
    profile_readiness = profile.get("readiness", {}) if isinstance(profile.get("readiness"), dict) else {}
    for tier, values in profile_readiness.items():
        if tier in thresholds and isinstance(values, dict):
            thresholds[tier].update(values)
    return thresholds


def selected_optimization_summary(optimization: dict[str, Any]) -> dict[str, Any]:
    if optimization.get("updated_active_strategy") is True:
        active = optimization.get("champion", {}) or {}
    else:
        active = optimization.get("baseline", {}) or {}
    return active.get("summary", {}) if isinstance(active.get("summary"), dict) else {}


def production_summary(backtest: dict[str, Any], optimization: dict[str, Any]) -> dict[str, Any]:
    summary = backtest.get("summary", {}) if isinstance(backtest.get("summary"), dict) else {}
    if summary:
        return summary
    return selected_optimization_summary(optimization)


def return_stats(records: list[dict[str, Any]]) -> dict[str, Any]:
    returns = [as_float(record.get("net_return_pct")) for record in records if record.get("net_return_pct") is not None]
    if not returns:
        return {"sample_count": 0, "win_rate": None, "avg_net_return_pct": None, "median_net_return_pct": None}
    return {
        "sample_count": len(returns),
        "win_rate": round(sum(1 for value in returns if value > 0) / len(returns), 3),
        "avg_net_return_pct": round(statistics.fmean(returns), 3),
        "median_net_return_pct": round(statistics.median(returns), 3),
    }


def month_stats(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        base_date = str(record.get("base_date") or "")
        if len(base_date) >= 7:
            buckets[base_date[:7]].append(record)
    return [{"month": month, **return_stats(rows)} for month, rows in sorted(buckets.items())]


def market_stats(backtest: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostics = backtest.get("risk_diagnostics") if isinstance(backtest.get("risk_diagnostics"), dict) else {}
    rows = diagnostics.get("by_market_family") if isinstance(diagnostics.get("by_market_family"), list) else []
    return [row for row in rows if isinstance(row, dict)]


def metric(summary: dict[str, Any], key: str) -> Any:
    if key == "sample_count":
        return summary.get("production_sample_count", summary.get("sample_count"))
    return summary.get(key)


def add_min_check(findings: list[dict[str, Any]], summary: dict[str, Any], metric_key: str, threshold_key: str, thresholds: dict[str, Any]) -> None:
    if threshold_key not in thresholds:
        return
    value = as_float(metric(summary, metric_key), default=-999.0)
    expected = as_float(thresholds[threshold_key])
    if value < expected:
        findings.append({"metric": metric_key, "actual": value, "expected": f">= {expected}"})


def add_max_check(findings: list[dict[str, Any]], summary: dict[str, Any], metric_key: str, threshold_key: str, thresholds: dict[str, Any]) -> None:
    if threshold_key not in thresholds:
        return
    value = as_float(metric(summary, metric_key), default=999.0)
    expected = as_float(thresholds[threshold_key])
    if value > expected:
        findings.append({"metric": metric_key, "actual": value, "expected": f"<= {expected}"})


def month_balance_findings(months: list[dict[str, Any]], thresholds: dict[str, Any]) -> list[dict[str, Any]]:
    if "min_mature_months" not in thresholds:
        return []
    min_month_sample_count = as_int(thresholds.get("min_month_sample_count"), 1)
    mature = [row for row in months if as_int(row.get("sample_count")) >= min_month_sample_count]
    findings: list[dict[str, Any]] = []
    if len(mature) < as_int(thresholds.get("min_mature_months")):
        findings.append({"metric": "mature_months", "actual": len(mature), "expected": f">= {thresholds['min_mature_months']}"})
    min_win = as_float(thresholds.get("min_mature_month_win_rate"), default=-999.0)
    weak_win = [row for row in mature if as_float(row.get("win_rate"), default=-999.0) < min_win]
    for row in weak_win:
        findings.append({"metric": f"month[{row['month']}].win_rate", "actual": row.get("win_rate"), "expected": f">= {min_win}"})
    min_avg = as_float(thresholds.get("min_mature_month_avg_net_return_pct"), default=-999.0)
    weak_avg = [row for row in mature if as_float(row.get("avg_net_return_pct"), default=-999.0) < min_avg]
    for row in weak_avg:
        findings.append({"metric": f"month[{row['month']}].avg_net_return_pct", "actual": row.get("avg_net_return_pct"), "expected": f">= {min_avg}"})
    return findings


def market_segment_findings(markets: list[dict[str, Any]], thresholds: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for row in markets:
        family = str(row.get("market_family") or "unknown")
        if "min_sample_count" in thresholds and as_int(row.get("sample_count")) < as_int(thresholds.get("min_sample_count")):
            findings.append({"metric": f"market[{family}].sample_count", "actual": row.get("sample_count"), "expected": f">= {thresholds['min_sample_count']}"})
        for metric_key, threshold_key in [
            ("win_rate", "min_win_rate"),
            ("avg_net_return_pct", "min_avg_net_return_pct"),
            ("median_net_return_pct", "min_median_net_return_pct"),
            ("avg_alpha_pct", "min_avg_alpha_pct"),
            ("max_adverse_pct", "min_max_adverse_pct"),
        ]:
            if threshold_key not in thresholds:
                continue
            value = as_float(row.get(metric_key), default=-999.0)
            expected = as_float(thresholds[threshold_key])
            if value < expected:
                findings.append({"metric": f"market[{family}].{metric_key}", "actual": row.get(metric_key), "expected": f">= {expected}"})
        if "max_adverse_breach_rate" in thresholds:
            value = as_float(row.get("adverse_breach_rate"), default=999.0)
            expected = as_float(thresholds["max_adverse_breach_rate"])
            if value > expected:
                findings.append({"metric": f"market[{family}].adverse_breach_rate", "actual": row.get("adverse_breach_rate"), "expected": f"<= {expected}"})
    return findings


def data_quality_findings(summary: dict[str, Any]) -> list[dict[str, Any]]:
    blocker_keys = [
        "skipped_registry_entry_count",
        "skipped_date_mismatch_count",
        "skipped_as_of_date_mismatch_count",
        "skipped_quote_date_mismatch_count",
        "skipped_future_quote_date_count",
        "skipped_invalid_quote_date_count",
        "skipped_invalid_entry_date_count",
        "quote_date_mismatch_item_count",
        "future_quote_date_item_count",
        "invalid_quote_date_item_count",
    ]
    findings = []
    for key in blocker_keys:
        value = as_int(summary.get(key), 0)
        if value > 0:
            findings.append({"metric": f"data_quality.{key}", "actual": value, "expected": "0"})
    if summary.get("symbol_risk_mode") != "point_in_time" or summary.get("symbol_risk_point_in_time") is not True:
        findings.append(
            {
                "metric": "data_quality.symbol_risk_point_in_time",
                "actual": summary.get("symbol_risk_mode"),
                "expected": "point_in_time",
            }
        )
    return findings


def tier_result(
    summary: dict[str, Any],
    months: list[dict[str, Any]],
    markets: list[dict[str, Any]],
    thresholds: dict[str, Any],
    paper_days: int,
    forward_adverse_breach_rate: float,
    quality_findings: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = list(quality_findings or [])
    add_min_check(findings, summary, "sample_count", "min_sample_count", thresholds)
    add_min_check(findings, summary, "win_rate", "min_win_rate", thresholds)
    add_min_check(findings, summary, "avg_net_return_pct", "min_avg_net_return_pct", thresholds)
    add_min_check(findings, summary, "median_net_return_pct", "min_median_net_return_pct", thresholds)
    add_min_check(findings, summary, "avg_alpha_pct", "min_avg_alpha_pct", thresholds)
    add_min_check(findings, summary, "max_adverse_pct", "min_max_adverse_pct", thresholds)
    add_max_check(findings, summary, "adverse_breach_rate", "max_adverse_breach_rate", thresholds)
    required_quality = thresholds.get("required_sample_quality")
    if required_quality and summary.get("sample_quality") != required_quality:
        findings.append({"metric": "sample_quality", "actual": summary.get("sample_quality"), "expected": str(required_quality)})
    if "min_forward_paper_days" in thresholds and paper_days < as_int(thresholds.get("min_forward_paper_days")):
        findings.append({"metric": "forward_paper_days", "actual": paper_days, "expected": f">= {thresholds['min_forward_paper_days']}"})
    if "max_forward_adverse_breach_rate" in thresholds and forward_adverse_breach_rate > as_float(thresholds.get("max_forward_adverse_breach_rate")):
        findings.append({"metric": "forward_adverse_breach_rate", "actual": forward_adverse_breach_rate, "expected": f"<= {thresholds['max_forward_adverse_breach_rate']}"})
    findings.extend(month_balance_findings(months, thresholds))
    findings.extend(market_segment_findings(markets, thresholds))
    return {"passed": not findings, "thresholds": thresholds, "findings": findings}


def highest_allowed_stage(tiers: dict[str, dict[str, Any]]) -> str:
    if tiers["small_live_observation"]["passed"]:
        return "small_live_observation"
    if tiers["paper_trading"]["passed"]:
        return "paper_trading"
    if tiers["shadow_logging"]["passed"]:
        return "shadow_logging"
    return "research_only"


def build_readiness(
    backtest: dict[str, Any],
    optimization: dict[str, Any],
    profile: dict[str, Any],
    paper_days: int = 0,
    forward_adverse_breach_rate: float = 0.0,
) -> dict[str, Any]:
    thresholds = merge_thresholds(profile)
    summary = production_summary(backtest, optimization)
    months = month_stats(backtest.get("records", []) if isinstance(backtest.get("records"), list) else [])
    markets = market_stats(backtest)
    quality_findings = data_quality_findings(summary)
    tiers = {
        tier: tier_result(summary, months, markets, tier_thresholds, paper_days, forward_adverse_breach_rate, quality_findings)
        for tier, tier_thresholds in thresholds.items()
    }
    return {
        "generated_at": utc_now(),
        "production_summary": summary,
        "optimization_current_summary": selected_optimization_summary(optimization),
        "data_quality_findings": quality_findings,
        "month_stats": months,
        "market_stats": markets,
        "risk_diagnostics": backtest.get("risk_diagnostics", {}) if isinstance(backtest.get("risk_diagnostics"), dict) else {},
        "paper_days": paper_days,
        "forward_adverse_breach_rate": forward_adverse_breach_rate,
        "tiers": tiers,
        "current_allowed_stage": highest_allowed_stage(tiers),
    }


def write_markdown(path: pathlib.Path, result: dict[str, Any]) -> None:
    summary = result["production_summary"]
    lines = [
        "# Investment Readiness",
        "",
        f"Generated: `{result['generated_at']}`",
        f"Current allowed stage: `{result['current_allowed_stage']}`",
        "",
        "## Production Summary",
        f"- samples: `{summary.get('sample_count')}`",
        f"- production samples: `{summary.get('production_sample_count', summary.get('sample_count'))}`",
        f"- win_rate: `{summary.get('win_rate')}`",
        f"- avg_net_return_pct: `{summary.get('avg_net_return_pct')}`",
        f"- median_net_return_pct: `{summary.get('median_net_return_pct')}`",
        f"- adverse_breach_rate: `{summary.get('adverse_breach_rate')}`",
        f"- sample_quality: `{summary.get('sample_quality')}`",
        "",
        "## Data Quality",
    ]
    if result.get("data_quality_findings"):
        for finding in result["data_quality_findings"]:
            lines.append(f"- blocked by `{finding['metric']}`: actual `{finding['actual']}`, expected `{finding['expected']}`")
    else:
        lines.append("- no registry quality blockers detected")
    lines.extend(["", "## Market Stats"])
    if result.get("market_stats"):
        for row in result["market_stats"]:
            lines.append(
                f"- `{row.get('market_family')}`: samples={row.get('sample_count')}, win={row.get('win_rate')}, "
                f"avg={row.get('avg_net_return_pct')}%, alpha={row.get('avg_alpha_pct')}%, "
                f"max_adverse={row.get('max_adverse_pct')}%, breach_rate={row.get('adverse_breach_rate')}"
            )
    else:
        lines.append("- no market-family diagnostics available")
    diagnostics = result.get("risk_diagnostics", {}) if isinstance(result.get("risk_diagnostics"), dict) else {}
    lines.extend(["", "## Worst Adverse Records"])
    for record in diagnostics.get("worst_adverse_records", [])[:10]:
        lines.append(
            f"- `{record.get('base_date')}` `{record.get('symbol')}` ({record.get('market_family')}): "
            f"net={record.get('net_return_pct')}%, adverse={record.get('max_adverse_pct')}%"
        )
    lines.extend([
        "",
        "## Tiers",
    ])
    for tier, data in result["tiers"].items():
        lines.append(f"- `{tier}`: passed=`{data['passed']}`")
        for finding in data["findings"]:
            lines.append(f"- `{tier}` blocked by `{finding['metric']}`: actual `{finding['actual']}`, expected `{finding['expected']}`")
    lines.extend(["", "## Month Stats"])
    for row in result["month_stats"]:
        lines.append(f"- `{row['month']}`: samples={row['sample_count']}, win={row['win_rate']}, avg={row['avg_net_return_pct']}%, median={row['median_net_return_pct']}%")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check investment research readiness for shadow, paper, and small-live observation stages.")
    parser.add_argument("--backtest", default=str(ROOT / "research" / "experiments" / "latest_backtest.json"))
    parser.add_argument("--optimization", default=str(ROOT / "research" / "experiments" / "latest_optimization.json"))
    parser.add_argument("--profile", default=str(ROOT / "config" / "investment_profile.toml"))
    parser.add_argument("--output-json", default=str(ROOT / "research" / "readiness" / "latest_readiness.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "readiness" / "latest_readiness.md"))
    parser.add_argument("--paper-days", type=int, default=0)
    parser.add_argument("--forward-adverse-breach-rate", type=float, default=0.0)
    args = parser.parse_args()

    result = build_readiness(
        load_json(pathlib.Path(args.backtest)),
        load_json(pathlib.Path(args.optimization)),
        load_toml(pathlib.Path(args.profile)),
        args.paper_days,
        args.forward_adverse_breach_rate,
    )
    output_json = pathlib.Path(args.output_json)
    output_md = pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_markdown(output_md, result)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

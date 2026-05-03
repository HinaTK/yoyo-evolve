#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys
import tomllib
from typing import Any


REQUIRED_TOP_LEVEL = ["date", "session", "recommendations"]
REQUIRED_RECOMMENDATION_FIELDS = [
    "symbol",
    "state",
    "theme",
    "kind",
    "horizon_days_min",
    "horizon_days_max",
    "confidence",
    "rationale",
    "evidence",
    "risks",
    "invalidation",
    "selection_source_theme",
    "selection_reason",
]
VALID_STATES = {"watch_only", "buy_candidate", "accumulate", "hold", "trim", "sell_candidate", "avoid"}
ACTIONABLE_STATES = {"buy_candidate", "accumulate", "hold"}
NON_DIAGNOSTIC_STATES = ACTIONABLE_STATES | {"trim", "sell_candidate"}


def load_json(path: pathlib.Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def trade_universe_symbols(path: pathlib.Path) -> set[str]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return {str(item.get("symbol")) for item in data.get("symbols", []) if item.get("symbol")}


def ranking_rows(ranking: dict[str, Any]) -> tuple[set[str], dict[str, dict[str, Any]]]:
    actionable_symbols = {str(row.get("symbol")) for row in ranking.get("actionable_candidates", []) if row.get("symbol")}
    rows: dict[str, dict[str, Any]] = {}
    for key in ("all_ranked", "top_candidates", "diagnostic_candidates", "actionable_candidates"):
        for row in ranking.get(key, []):
            symbol = row.get("symbol")
            if symbol:
                rows[str(symbol)] = row
    return actionable_symbols, rows


def validate(calls: dict[str, Any], ranking: dict[str, Any], symbols: set[str]) -> list[str]:
    errors: list[str] = []
    for field in REQUIRED_TOP_LEVEL:
        if field not in calls:
            errors.append(f"missing top-level field: {field}")

    recommendations = calls.get("recommendations")
    if not isinstance(recommendations, list):
        errors.append("top-level recommendations must be a list")
        return errors

    actionable_symbols, rows = ranking_rows(ranking)
    for index, rec in enumerate(recommendations):
        prefix = f"recommendations[{index}]"
        if not isinstance(rec, dict):
            errors.append(f"{prefix} must be an object")
            continue

        for field in REQUIRED_RECOMMENDATION_FIELDS:
            if field not in rec:
                errors.append(f"{prefix} missing field: {field}")

        symbol = rec.get("symbol")
        state = rec.get("state")
        if symbol not in symbols:
            errors.append(f"{prefix}.symbol {symbol!r} is not in trade universe")
        if state not in VALID_STATES:
            errors.append(f"{prefix}.state {state!r} is not valid")

        confidence = rec.get("confidence")
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            errors.append(f"{prefix}.confidence must be a number between 0 and 1")
        if not isinstance(rec.get("evidence"), list):
            errors.append(f"{prefix}.evidence must be a list")
        if not isinstance(rec.get("risks"), list):
            errors.append(f"{prefix}.risks must be a list")

        row = rows.get(str(symbol))
        if state in NON_DIAGNOSTIC_STATES:
            if row is None:
                errors.append(f"{prefix}.{state} state requires a ranking row")
            elif bool(row.get("diagnostic_only")) or not bool(row.get("qualified_for_watch")):
                errors.append(f"{prefix}.{state} state is forbidden for diagnostic or non-watch ranking row")

        if state in ACTIONABLE_STATES:
            if symbol not in actionable_symbols:
                errors.append(f"{prefix} actionable state requires symbol in ranking actionable_candidates")
            if row is None:
                errors.append(f"{prefix} actionable state requires a ranking row")
                continue
            if not bool(row.get("qualified_for_action")):
                errors.append(f"{prefix} actionable state requires qualified_for_action=true")
            if bool(row.get("diagnostic_only")):
                errors.append(f"{prefix} actionable state is forbidden for diagnostic_only ranking row")
            if not bool(row.get("qualified_for_watch")):
                errors.append(f"{prefix} actionable state is forbidden when qualified_for_watch=false")
            if row.get("cost_gate_passed") is False:
                errors.append(f"{prefix} actionable state is forbidden when cost_gate_passed=false")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate structured investment calls against ranking and trade universe constraints.")
    parser.add_argument("--calls", required=True)
    parser.add_argument("--ranking", required=True)
    parser.add_argument("--trade-universe", required=True)
    args = parser.parse_args()

    errors = validate(load_json(pathlib.Path(args.calls)), load_json(pathlib.Path(args.ranking)), trade_universe_symbols(pathlib.Path(args.trade_universe)))
    if errors:
        print("Investment calls validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Investment calls validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

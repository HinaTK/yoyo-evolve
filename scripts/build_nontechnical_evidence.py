#!/usr/bin/env python3

import argparse
import datetime as dt
import glob
import json
import pathlib
import re
import tomllib
import urllib.parse
import urllib.request
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_POLICY = {
    "require_for_action": True,
    "max_staleness_days": 30,
    "min_total_score_for_action": 0.55,
    "block_unknown_event_risk": True,
}
DEFAULT_WEIGHTS = {
    "fundamental_score": 0.30,
    "valuation_score": 0.20,
    "catalyst_score": 0.25,
    "flow_score": 0.15,
    "macro_score": 0.10,
}
DEFAULT_COMPONENT_MAX_STALENESS_DAYS = {
    "fundamental_score": 120,
    "valuation_score": 45,
    "catalyst_score": 30,
    "flow_score": 5,
    "macro_score": 14,
    "event_risk": 7,
}
COMPONENT_KEYS = tuple(DEFAULT_WEIGHTS.keys())
FORMAL_EVIDENCE_MODES = {
    "curated_point_in_time",
    "manual_point_in_time",
    "formal_provider_point_in_time",
}
SESSION_ORDER = {"morning": 0, "midday": 1, "close": 2, "historical": 2}
DEFENSIVE_THEMES = {"dividend", "utilities", "defensive", "broad-market", "consumer-staples"}
POLICY_HEAVY_THEMES = {"biotech", "semiconductor", "semiconductors", "hard-tech", "renewable", "platform"}
HARD_EVENT_RISKS = {"elevated", "earnings_gap", "regulatory", "policy", "suspension", "accounting", "quote_stale"}
EASTMONEY_CN_FINANCE_URL = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew"
EASTMONEY_HK_DATA_URL = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
EASTMONEY_FUND_JS_URL = "https://fund.eastmoney.com/pingzhongdata/{code}.js"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_toml(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def load_json(path: pathlib.Path | None) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_json(url: str, params: dict[str, Any], timeout: float) -> dict[str, Any]:
    full_url = f"{url}?{urllib.parse.urlencode(params)}" if params else url
    req = urllib.request.Request(
        full_url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json,text/plain,*/*"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return json.loads(resp.read().decode(charset, errors="ignore"))


def fetch_text(url: str, timeout: float) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "text/javascript,text/plain,*/*"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="ignore")


def resolve_path(value: str | pathlib.Path | None) -> pathlib.Path | None:
    if value is None or str(value) == "":
        return None
    path = pathlib.Path(value)
    return path if path.is_absolute() else ROOT / path


def configured_source_count(row: dict[str, Any]) -> int:
    if row.get("source_count") is not None:
        try:
            return int(row.get("source_count") or 0)
        except (TypeError, ValueError):
            return 0
    return len(normalize_sources(row.get("sources")))


def evidence_rows_from_payload(payload: Any) -> list[dict[str, Any]]:
    raw_rows: list[Any] = []
    if isinstance(payload, list):
        raw_rows.extend(payload)
    elif isinstance(payload, dict):
        defaults = {key: payload[key] for key in ("as_of_date", "as_of_session", "evidence_mode") if payload.get(key) is not None}
        raw_symbols = payload.get("symbols", {})
        if isinstance(raw_symbols, dict):
            for symbol, row in raw_symbols.items():
                if isinstance(row, dict):
                    raw_rows.append({**defaults, "symbol": str(symbol), **row})
        if isinstance(payload.get("evidence"), list):
            raw_rows.extend({**defaults, **row} if isinstance(row, dict) else row for row in payload["evidence"])

    rows = []
    for row in raw_rows:
        if isinstance(row, dict) and row.get("symbol"):
            rows.append(dict(row))
    return rows


def placeholder_evidence(row: dict[str, Any]) -> bool:
    return explicit_true(row.get("manual_review_required"))


def read_curated_evidence_file(path: pathlib.Path) -> list[dict[str, Any]]:
    try:
        if path.suffix.lower() == ".json":
            payload = json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix.lower() == ".toml":
            with path.open("rb") as fh:
                payload = tomllib.load(fh)
        else:
            return []
    except (OSError, json.JSONDecodeError, tomllib.TOMLDecodeError):
        return []

    rows = [row for row in evidence_rows_from_payload(payload) if not placeholder_evidence(row)]
    for row in rows:
        row.setdefault("evidence_mode", "manual_point_in_time")
        row.setdefault("source_count", configured_source_count(row))
    return rows


def curated_source_paths(config: dict[str, Any]) -> list[pathlib.Path]:
    source_config = config.get("curated_sources", {}) if isinstance(config.get("curated_sources"), dict) else {}
    if not source_config.get("enabled", False):
        return []

    raw_paths: list[Any] = []
    if source_config.get("path"):
        raw_paths.append(source_config["path"])
    if isinstance(source_config.get("paths"), list):
        raw_paths.extend(source_config["paths"])

    paths: list[pathlib.Path] = []
    seen: set[str] = set()
    for raw_path in raw_paths:
        resolved = resolve_path(str(raw_path).strip())
        if resolved is None:
            continue
        pattern = str(resolved)
        if any(token in pattern for token in "*?["):
            matches = [pathlib.Path(match) for match in glob.glob(pattern)]
        else:
            matches = [resolved]
        for path in sorted(matches):
            key = str(path)
            if key not in seen and path.is_file():
                paths.append(path)
                seen.add(key)
    return paths


def curated_source_rows(config: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in curated_source_paths(config):
        for row in read_curated_evidence_file(path):
            row["loaded_from"] = str(path)
            rows.append(row)
    return rows


def evidence_session_rank(value: Any) -> int:
    text = str(value or "").strip().lower()
    return SESSION_ORDER.get(text, -1)


def evidence_row_after(row: dict[str, Any], as_of_date: str | None, as_of_session: str | None) -> bool:
    report_date = parse_date(as_of_date)
    evidence_date = parse_date(row.get("as_of_date"))
    if report_date is None or evidence_date is None:
        return False
    if evidence_date > report_date:
        return True
    if evidence_date < report_date:
        return False
    evidence_session = str(row.get("as_of_session") or "").strip().lower()
    report_session = str(as_of_session or "").strip().lower()
    if not evidence_session or not report_session:
        return False
    return SESSION_ORDER.get(evidence_session, 99) > SESSION_ORDER.get(report_session, 99)


def evidence_selection_key(row: dict[str, Any], index: int) -> tuple[dt.date, int, int, int]:
    evidence_date = parse_date(row.get("as_of_date")) or dt.date.min
    return (evidence_date, evidence_session_rank(row.get("as_of_session")), configured_source_count(row), index)


def parse_policy(config: dict[str, Any]) -> tuple[dict[str, Any], dict[str, float]]:
    policy = DEFAULT_POLICY.copy()
    policy.update(config.get("policy", {}) if isinstance(config.get("policy"), dict) else {})
    freshness = config.get("freshness", {}) if isinstance(config.get("freshness"), dict) else {}
    component_days = DEFAULT_COMPONENT_MAX_STALENESS_DAYS.copy()
    for key in DEFAULT_COMPONENT_MAX_STALENESS_DAYS:
        config_key = f"{key}_days"
        if freshness.get(config_key) is not None:
            component_days[key] = int(freshness[config_key])
    policy["component_max_staleness_days"] = component_days
    weights = DEFAULT_WEIGHTS.copy()
    raw_weights = config.get("weights", {}) if isinstance(config.get("weights"), dict) else {}
    for key, value in raw_weights.items():
        if key in weights:
            weights[key] = float(value)
    return policy, weights


def configured_symbols(
    config: dict[str, Any],
    as_of_date: str | None = None,
    as_of_session: str | None = None,
) -> dict[str, dict[str, Any]]:
    candidates: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    configured_rows = curated_source_rows(config)
    inline_rows = config.get("evidence", []) if isinstance(config.get("evidence"), list) else []
    configured_rows.extend(row for row in inline_rows if isinstance(row, dict))
    for index, row in enumerate(configured_rows):
        if not row.get("symbol"):
            continue
        candidate = dict(row)
        sources = normalize_sources(candidate.get("sources"))
        if candidate.get("source_count") is None and sources:
            candidate["source_count"] = len(sources)
        candidates.setdefault(str(candidate["symbol"]), []).append((index, candidate))

    selected: dict[str, dict[str, Any]] = {}
    for symbol, rows in candidates.items():
        point_in_time_rows = [(index, row) for index, row in rows if not evidence_row_after(row, as_of_date, as_of_session)]
        choices = point_in_time_rows or rows
        selected[symbol] = max(choices, key=lambda item: evidence_selection_key(item[1], item[0]))[1]
    return selected


def universe_symbols(universe: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in universe.get("symbols", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = row
    return rows


def snapshot_symbols(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in snapshot.get("items", []):
        if isinstance(row, dict) and row.get("symbol"):
            rows[str(row["symbol"])] = row
    return rows


def ranking_symbols(ranking: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for key in ("top_candidates", "actionable_candidates", "diagnostic_candidates", "all_ranked"):
        for row in ranking.get(key, []):
            if isinstance(row, dict) and row.get("symbol") and str(row["symbol"]) not in rows:
                rows[str(row["symbol"])] = row
    return rows


def date_token(value: Any) -> str | None:
    text = str(value or "").strip()
    if len(text) >= 10 and text[4] == "-" and text[7] == "-":
        return text[:10]
    if len(text) >= 8 and text[:8].isdigit():
        return f"{text[:4]}-{text[4:6]}-{text[6:8]}"
    return None


def parse_date(value: Any) -> dt.date | None:
    token = date_token(value)
    if token is None:
        return None
    try:
        return dt.date.fromisoformat(token)
    except ValueError:
        return None


def as_float(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def explicit_true(value: Any) -> bool:
    return value is True or (isinstance(value, str) and value.strip().lower() == "true")


def total_score(row: dict[str, Any], weights: dict[str, float]) -> float | None:
    score_sum = 0.0
    weight_sum = 0.0
    for key, weight in weights.items():
        value = as_float(row.get(key))
        if value is None:
            continue
        score_sum += max(0.0, min(1.0, value)) * float(weight)
        weight_sum += float(weight)
    return round(score_sum / weight_sum, 3) if weight_sum else None


def component_dates_from_configured(configured: dict[str, Any], fallback_date: Any) -> dict[str, str | None]:
    raw_dates = configured.get("component_as_of_dates", {}) if isinstance(configured.get("component_as_of_dates"), dict) else {}
    dates: dict[str, str | None] = {}
    for key in COMPONENT_KEYS:
        dates[key] = date_token(raw_dates.get(key) or configured.get(f"{key}_as_of_date") or fallback_date)
    return dates


def component_staleness_findings(symbol: str, component_dates: dict[str, Any], report_date: dt.date | None, policy: dict[str, Any]) -> tuple[dict[str, int], list[dict[str, Any]]]:
    ages: dict[str, int] = {}
    findings: list[dict[str, Any]] = []
    if report_date is None:
        return ages, findings
    max_days = policy.get("component_max_staleness_days", DEFAULT_COMPONENT_MAX_STALENESS_DAYS)
    max_days = max_days if isinstance(max_days, dict) else DEFAULT_COMPONENT_MAX_STALENESS_DAYS
    for key, raw_date in component_dates.items():
        component_date = parse_date(raw_date)
        if component_date is None:
            findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_component_date_missing", "component": key})
            continue
        age_days = (report_date - component_date).days
        ages[key] = age_days
        if age_days < 0:
            findings.append({"symbol": symbol, "severity": "critical", "reason": "nontechnical_component_from_future", "component": key, "age_days": age_days})
        elif age_days > int(max_days.get(key, policy.get("max_staleness_days", 30))):
            findings.append({"symbol": symbol, "severity": "info", "reason": "nontechnical_component_stale", "component": key, "age_days": age_days})
    return ages, findings


def normalize_sources(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list):
        return []
    sources = []
    for item in raw:
        if isinstance(item, dict):
            sources.append(dict(item))
        elif item:
            sources.append({"label": str(item)})
    return sources


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def theme_contains(theme: str, tokens: set[str]) -> bool:
    return any(token in theme for token in tokens)


def automatic_proxy_enabled(config: dict[str, Any]) -> bool:
    proxy = config.get("automatic_proxy", {}) if isinstance(config.get("automatic_proxy"), dict) else {}
    return bool(proxy.get("enabled", False))


def market_summary(snapshot: dict[str, Any], symbol: str) -> dict[str, Any]:
    family = "cn" if symbol.upper().endswith((".SH", ".SZ", ".BJ")) else "hk" if symbol.upper().endswith(".HK") else "unknown"
    summary = snapshot.get("market_summary", {}) if isinstance(snapshot.get("market_summary"), dict) else {}
    exchange = "HKEX" if family == "hk" else "SSE" if symbol.upper().endswith(".SH") else "SZSE" if symbol.upper().endswith(".SZ") else None
    by_exchange = summary.get("by_exchange", {}) if isinstance(summary.get("by_exchange"), dict) else {}
    exchange_summary = by_exchange.get(exchange, {}) if exchange else {}
    return exchange_summary if isinstance(exchange_summary, dict) and exchange_summary else summary


def formal_provider_config(config: dict[str, Any]) -> dict[str, Any]:
    provider = config.get("formal_provider", {}) if isinstance(config.get("formal_provider"), dict) else {}
    return provider


def formal_provider_fetch_allowed(config: dict[str, Any], as_of_date: str) -> bool:
    provider = formal_provider_config(config)
    if not provider.get("enabled", False):
        return False
    if bool(provider.get("current_date_only", True)) and as_of_date != dt.date.today().isoformat():
        return False
    return True


def formal_provider_timeout(config: dict[str, Any]) -> float:
    return float(formal_provider_config(config).get("timeout_secs", 5.0))


def first_data_row(payload: dict[str, Any]) -> dict[str, Any] | None:
    direct = payload.get("data")
    if isinstance(direct, list) and direct and isinstance(direct[0], dict):
        return direct[0]
    result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
    nested = result.get("data") if isinstance(result, dict) else None
    if isinstance(nested, list) and nested and isinstance(nested[0], dict):
        return nested[0]
    return None


def average_present(values: list[float | None], default: float = 0.5) -> float:
    present = [value for value in values if value is not None]
    return round(clamp(sum(present) / len(present) if present else default), 3)


def score_growth_pct(value: Any) -> float | None:
    pct = as_float(value)
    if pct is None:
        return None
    return clamp(0.50 + pct / 100.0, 0.25, 0.80)


def score_roe_pct(value: Any) -> float | None:
    pct = as_float(value)
    if pct is None:
        return None
    return clamp(0.40 + pct / 50.0, 0.25, 0.85)


def score_margin_pct(value: Any) -> float | None:
    pct = as_float(value)
    if pct is None:
        return None
    return clamp(0.45 + pct / 120.0, 0.25, 0.85)


def score_cash_ratio(value: Any) -> float | None:
    ratio = as_float(value)
    if ratio is None:
        return None
    return clamp(0.50 + ratio * 0.30, 0.25, 0.80)


def score_debt_pct(value: Any) -> float | None:
    pct = as_float(value)
    if pct is None:
        return None
    return clamp(0.75 - pct / 250.0, 0.25, 0.75)


def score_pe(value: Any) -> float | None:
    pe = as_float(value)
    if pe is None:
        return None
    if pe <= 0:
        return 0.35
    if pe <= 12:
        return 0.72
    if pe <= 25:
        return 0.60
    if pe <= 45:
        return 0.48
    return 0.35


def score_pb(value: Any) -> float | None:
    pb = as_float(value)
    if pb is None:
        return None
    if pb <= 0:
        return 0.35
    if pb <= 1.0:
        return 0.68
    if pb <= 3.0:
        return 0.58
    if pb <= 6.0:
        return 0.48
    return 0.35


def score_dividend_pct(value: Any) -> float | None:
    pct = as_float(value)
    if pct is None:
        return None
    return clamp(0.45 + pct / 20.0, 0.35, 0.75)


def flow_score_from_metadata(metadata: dict[str, Any]) -> float:
    score = 0.50
    turnover = as_float(metadata.get("turnover"))
    latest_volume = as_float(metadata.get("latest_volume") or metadata.get("quote_volume"))
    volume_ratio = as_float(metadata.get("volume_ratio_20"))
    if turnover is not None and turnover > 1_000_000_000:
        score += 0.06
    elif latest_volume is not None and latest_volume > 10_000_000:
        score += 0.04
    if volume_ratio is not None:
        if volume_ratio >= 1.2:
            score += 0.04
        elif volume_ratio < 0.7:
            score -= 0.06
    return round(clamp(score), 3)


def macro_score_from_context(symbol: str, metadata: dict[str, Any], snapshot: dict[str, Any]) -> float:
    score = 0.50
    theme = str(metadata.get("theme") or "").lower()
    if theme_contains(theme, DEFENSIVE_THEMES):
        score += 0.04
    if theme_contains(theme, POLICY_HEAVY_THEMES):
        score -= 0.04
    risk_state = str(market_summary(snapshot, symbol).get("risk_state") or "neutral")
    if risk_state == "risk_on":
        score += 0.05
    elif risk_state == "risk_off":
        score -= 0.08
    return round(clamp(score), 3)


def formal_event_risk(metadata: dict[str, Any], growth_values: list[Any], debt_ratio: Any = None) -> str:
    theme = str(metadata.get("theme") or "").lower()
    if theme_contains(theme, POLICY_HEAVY_THEMES):
        return "policy"
    if any((value := as_float(raw)) is not None and value <= -30.0 for raw in growth_values):
        return "earnings_gap"
    debt = as_float(debt_ratio)
    if debt is not None and debt >= 85.0:
        return "elevated"
    return "low"


def eastmoney_cn_code(symbol: str) -> str | None:
    code, _, suffix = symbol.upper().partition(".")
    if len(code) != 6 or suffix not in {"SH", "SZ", "BJ"}:
        return None
    return f"{suffix}{code}"


def eastmoney_hk_secucode(symbol: str) -> str | None:
    code, _, suffix = symbol.upper().partition(".")
    if suffix != "HK" or not code.isdigit():
        return None
    return f"{code.zfill(5)}.HK"


def formal_cn_stock_evidence(symbol: str, metadata: dict[str, Any], snapshot: dict[str, Any], timeout: float, decision_date: str, as_of_session: str | None) -> dict[str, Any] | None:
    code = eastmoney_cn_code(symbol)
    if code is None:
        return None
    payload = fetch_json(EASTMONEY_CN_FINANCE_URL, {"type": "0", "code": code}, timeout)
    row = first_data_row(payload)
    if row is None:
        return None
    as_of_date = date_token(row.get("NOTICE_DATE") or row.get("UPDATE_DATE") or row.get("REPORT_DATE"))
    if as_of_date is None:
        return None
    revenue_growth = row.get("TOTALOPERATEREVETZ")
    profit_growth = row.get("PARENTNETPROFITTZ")
    debt_ratio = row.get("ZCFZL")
    scores = {
        "fundamental_score": average_present([score_roe_pct(row.get("ROEJQ")), score_growth_pct(profit_growth), score_growth_pct(revenue_growth), score_cash_ratio(row.get("JYXJLYYSR"))]),
        "valuation_score": average_present([score_roe_pct(row.get("ROEJQ")), score_debt_pct(debt_ratio), score_margin_pct(row.get("XSJLL"))]),
        "catalyst_score": average_present([score_growth_pct(revenue_growth), score_growth_pct(profit_growth)]),
        "flow_score": flow_score_from_metadata(metadata),
        "macro_score": macro_score_from_context(symbol, metadata, snapshot),
    }
    return {
        "symbol": symbol,
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "component_as_of_dates": {
            "fundamental_score": as_of_date,
            "valuation_score": as_of_date,
            "catalyst_score": as_of_date,
            "flow_score": decision_date,
            "macro_score": decision_date,
        },
        "event_risk_as_of_date": as_of_date,
        **scores,
        "event_risk": formal_event_risk(metadata, [revenue_growth, profit_growth], debt_ratio),
        "source_count": 1,
        "sources": [{"label": "Eastmoney A-share F10 financial indicators", "kind": "formal_public_f10", "url": EASTMONEY_CN_FINANCE_URL}],
        "notes": [
            f"formal provider report_date={date_token(row.get('REPORT_DATE'))}, notice_date={date_token(row.get('NOTICE_DATE'))}",
            "scores derived from public F10 revenue, profit, ROE, margin, cash-flow and balance-sheet fields",
        ],
        "evidence_mode": "formal_provider_point_in_time",
        "proxy_only": False,
    }


def formal_hk_stock_evidence(symbol: str, metadata: dict[str, Any], snapshot: dict[str, Any], timeout: float, decision_date: str, as_of_session: str | None) -> dict[str, Any] | None:
    secucode = eastmoney_hk_secucode(symbol)
    if secucode is None:
        return None
    params = {
        "reportName": "RPT_CUSTOM_HKF10_FN_MAININDICATORMAX",
        "columns": "ALL",
        "filter": f'(SECUCODE="{secucode}")',
        "pageNumber": "1",
        "pageSize": "1",
        "sortColumns": "REPORT_DATE",
        "sortTypes": "-1",
        "source": "HKF10",
        "client": "PC",
    }
    row = first_data_row(fetch_json(EASTMONEY_HK_DATA_URL, params, timeout))
    if row is None:
        return None
    as_of_date = date_token(row.get("UPDATE_DATE") or row.get("NOTICE_DATE") or row.get("REPORT_DATE"))
    if as_of_date is None:
        return None
    revenue_growth = row.get("OPERATE_INCOME_QOQ")
    profit_growth = row.get("HOLDER_PROFIT_QOQ")
    scores = {
        "fundamental_score": average_present([score_roe_pct(row.get("ROE_AVG")), score_growth_pct(profit_growth), score_growth_pct(revenue_growth), score_margin_pct(row.get("NET_PROFIT_RATIO"))]),
        "valuation_score": average_present([score_pe(row.get("PE_TTM")), score_pb(row.get("PB_TTM")), score_dividend_pct(row.get("DIVIDEND_RATE"))]),
        "catalyst_score": average_present([score_growth_pct(revenue_growth), score_growth_pct(profit_growth)]),
        "flow_score": flow_score_from_metadata(metadata),
        "macro_score": macro_score_from_context(symbol, metadata, snapshot),
    }
    return {
        "symbol": symbol,
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "component_as_of_dates": {
            "fundamental_score": as_of_date,
            "valuation_score": as_of_date,
            "catalyst_score": as_of_date,
            "flow_score": decision_date,
            "macro_score": decision_date,
        },
        "event_risk_as_of_date": as_of_date,
        **scores,
        "event_risk": formal_event_risk(metadata, [revenue_growth, profit_growth]),
        "source_count": 1,
        "sources": [{"label": "Eastmoney HK F10 financial indicators", "kind": "formal_public_f10", "url": EASTMONEY_HK_DATA_URL}],
        "notes": [
            f"formal provider report_date={date_token(row.get('REPORT_DATE'))}",
            "scores derived from public HK F10 revenue, profit, ROE, valuation and dividend fields",
        ],
        "evidence_mode": "formal_provider_point_in_time",
        "proxy_only": False,
    }


def js_var(text: str, name: str) -> str | None:
    match = re.search(rf"var\s+{re.escape(name)}\s*=\s*\"([^\"]*)\"", text)
    return match.group(1) if match else None


def formal_cn_fund_evidence(symbol: str, metadata: dict[str, Any], snapshot: dict[str, Any], timeout: float, decision_date: str, as_of_session: str | None) -> dict[str, Any] | None:
    code, _, suffix = symbol.upper().partition(".")
    if suffix not in {"SH", "SZ"} or len(code) != 6:
        return None
    text = fetch_text(EASTMONEY_FUND_JS_URL.format(code=code), timeout).lstrip("\ufeff")
    if "var fS_code" not in text:
        return None
    date_match = re.search(r"/\*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}:\d{2}\*/var", text)
    as_of_date = date_match.group(1) if date_match else None
    if as_of_date is None:
        return None
    one_year = as_float(js_var(text, "syl_1n"))
    six_month = as_float(js_var(text, "syl_6y"))
    three_month = as_float(js_var(text, "syl_3y"))
    month = as_float(js_var(text, "syl_1y"))
    theme = str(metadata.get("theme") or "").lower()
    baseline = 0.58 if theme_contains(theme, DEFENSIVE_THEMES | {"broad-market"}) else 0.52
    if theme_contains(theme, POLICY_HEAVY_THEMES):
        baseline -= 0.04
    scores = {
        "fundamental_score": round(clamp(baseline), 3),
        "valuation_score": average_present([score_growth_pct(one_year), score_growth_pct(six_month)], default=0.52),
        "catalyst_score": average_present([score_growth_pct(month), score_growth_pct(three_month), score_growth_pct(six_month)], default=0.50),
        "flow_score": flow_score_from_metadata(metadata),
        "macro_score": macro_score_from_context(symbol, metadata, snapshot),
    }
    return {
        "symbol": symbol,
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "component_as_of_dates": {
            "fundamental_score": as_of_date,
            "valuation_score": as_of_date,
            "catalyst_score": as_of_date,
            "flow_score": decision_date,
            "macro_score": decision_date,
        },
        "event_risk_as_of_date": as_of_date,
        **scores,
        "event_risk": formal_event_risk(metadata, [one_year, six_month, three_month]),
        "source_count": 1,
        "sources": [{"label": "Eastmoney fund public data", "kind": "formal_public_fund", "url": EASTMONEY_FUND_JS_URL.format(code=code)}],
        "notes": [
            f"formal provider fund_name={js_var(text, 'fS_name') or ''}, source_date={as_of_date}",
            "scores derived from public fund return fields plus local liquidity context",
        ],
        "evidence_mode": "formal_provider_point_in_time",
        "proxy_only": False,
    }


def formal_provider_evidence(
    symbol: str,
    metadata: dict[str, Any],
    snapshot: dict[str, Any],
    config: dict[str, Any],
    as_of_date: str,
    as_of_session: str | None,
) -> dict[str, Any] | None:
    if not formal_provider_fetch_allowed(config, as_of_date):
        return None
    timeout = formal_provider_timeout(config)
    kind = str(metadata.get("kind") or "").lower()
    try:
        if symbol.upper().endswith((".SH", ".SZ", ".BJ")):
            if kind == "etf":
                return formal_cn_fund_evidence(symbol, metadata, snapshot, timeout, as_of_date, as_of_session)
            return formal_cn_stock_evidence(symbol, metadata, snapshot, timeout, as_of_date, as_of_session)
        if symbol.upper().endswith(".HK") and kind != "etf":
            return formal_hk_stock_evidence(symbol, metadata, snapshot, timeout, as_of_date, as_of_session)
    except Exception:
        return None
    return None


def proxy_event_risk(symbol: str, metadata: dict[str, Any], quote_fresh: bool, config: dict[str, Any]) -> str:
    proxy = config.get("automatic_proxy", {}) if isinstance(config.get("automatic_proxy"), dict) else {}
    kind = str(metadata.get("kind") or "").lower()
    theme = str(metadata.get("theme") or "").lower()
    if not quote_fresh:
        return "quote_stale"
    if kind == "etf" and bool(proxy.get("allow_action_for_etfs", True)):
        return "none"
    if theme_contains(theme, POLICY_HEAVY_THEMES):
        return "policy"
    if theme_contains(theme, DEFENSIVE_THEMES) and bool(proxy.get("allow_action_for_defensive_liquid_stocks", True)):
        return "none"
    return "unknown"


def automatic_proxy_evidence(
    symbol: str,
    metadata: dict[str, Any],
    snapshot: dict[str, Any],
    config: dict[str, Any],
    as_of_date: str,
    as_of_session: str | None,
) -> dict[str, Any] | None:
    if not automatic_proxy_enabled(config) or not metadata:
        return None
    proxy = config.get("automatic_proxy", {}) if isinstance(config.get("automatic_proxy"), dict) else {}
    kind = str(metadata.get("kind") or "").lower()
    theme = str(metadata.get("theme") or "").lower()
    max_score = float(proxy.get("max_total_score", 0.62))
    quote_date = date_token(metadata.get("quote_trade_date") or metadata.get("as_of"))
    quote_fresh = quote_date == as_of_date
    range_pos = as_float(metadata.get("range_pos_60"))
    volume_ratio = as_float(metadata.get("volume_ratio_20"))
    turnover = as_float(metadata.get("turnover"))
    latest_volume = as_float(metadata.get("latest_volume"))
    m_summary = market_summary(snapshot, symbol)
    risk_state = str(m_summary.get("risk_state") or "neutral")
    avg_stock_move = as_float(m_summary.get("avg_stock_move_1d")) or 0.0
    avg_etf_move = as_float(m_summary.get("avg_etf_move_1d")) or 0.0

    fundamental = 0.50
    if kind == "etf":
        fundamental += 0.08
    if theme_contains(theme, DEFENSIVE_THEMES):
        fundamental += 0.06
    if theme_contains(theme, POLICY_HEAVY_THEMES):
        fundamental -= 0.08

    valuation = 0.50
    if range_pos is not None:
        if range_pos <= 0.15:
            valuation += 0.03
        elif range_pos <= 0.65:
            valuation += 0.08
        elif range_pos <= 0.85:
            valuation += 0.01
        else:
            valuation -= 0.12

    catalyst = 0.50
    if risk_state == "risk_on":
        catalyst += 0.04
    elif risk_state == "risk_off":
        catalyst -= 0.06
    if kind == "etf" and avg_etf_move > avg_stock_move:
        catalyst += 0.03

    flow = 0.48
    if quote_fresh:
        flow += 0.05
    if turnover is not None and turnover > 1_000_000_000:
        flow += 0.05
    elif latest_volume is not None and latest_volume > 10_000_000:
        flow += 0.03
    if volume_ratio is not None:
        if volume_ratio >= 1.2:
            flow += 0.04
        elif volume_ratio < 0.7:
            flow -= 0.06

    macro = 0.50
    if risk_state == "risk_on":
        macro += 0.05
    elif risk_state == "risk_off":
        macro -= 0.08
    if kind == "etf":
        macro += 0.03

    row = {
        "symbol": symbol,
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "component_as_of_dates": {key: as_of_date for key in COMPONENT_KEYS},
        "event_risk_as_of_date": as_of_date,
        "fundamental_score": round(clamp(min(fundamental, max_score)), 3),
        "valuation_score": round(clamp(min(valuation, max_score)), 3),
        "catalyst_score": round(clamp(min(catalyst, max_score)), 3),
        "flow_score": round(clamp(min(flow, max_score)), 3),
        "macro_score": round(clamp(min(macro, max_score)), 3),
        "event_risk": proxy_event_risk(symbol, metadata, quote_fresh, config),
        "source_count": 0,
        "proxy_source_count": 3,
        "sources": [
            {"label": str(proxy.get("provider_id") or "automatic_local_proxy_v1"), "kind": "automatic_proxy"},
            {"label": "trade_universe.toml", "kind": "static_metadata"},
            {"label": "snapshot_quote_and_market_summary", "kind": "local_snapshot"},
        ],
        "notes": [
            "automatic proxy evidence from local metadata, quote liquidity, and market summary; not a substitute for audited fundamentals",
            f"kind={kind}, theme={theme}, quote_fresh={quote_fresh}, risk_state={risk_state}",
        ],
        "proxy_only": True,
    }
    return row


def build_symbol_evidence(
    symbol: str,
    metadata: dict[str, Any],
    configured: dict[str, Any] | None,
    as_of_date: str,
    as_of_session: str | None,
    policy: dict[str, Any],
    weights: dict[str, float],
    proxy_generated: bool = False,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    findings: list[dict[str, Any]] = []
    configured = configured or {}
    sources = normalize_sources(configured.get("sources"))
    configured_mode = str(configured.get("evidence_mode") or "").strip()
    proxy_only = proxy_generated or configured_mode == "automatic_local_proxy" or explicit_true(configured.get("proxy_only"))
    raw_source_count = int(configured.get("source_count")) if configured.get("source_count") is not None else len(sources)
    proxy_source_count = int(configured.get("proxy_source_count") or len(sources) or raw_source_count or 0) if proxy_only else 0
    source_count = 0 if proxy_only else raw_source_count
    raw_as_of = configured.get("as_of_date")
    evidence_date = parse_date(raw_as_of)
    report_date = parse_date(as_of_date)
    evidence_mode = configured_mode or ("automatic_local_proxy" if proxy_generated else "proxy_only" if proxy_only else "curated_point_in_time" if configured else "missing_fail_closed")
    component_as_of_dates = component_dates_from_configured(configured, raw_as_of)
    event_risk_as_of_date = date_token(configured.get("event_risk_as_of_date") or configured.get("event_as_of_date") or raw_as_of)
    row: dict[str, Any] = {
        "symbol": symbol,
        "name": metadata.get("name"),
        "kind": metadata.get("kind"),
        "theme": metadata.get("theme"),
        "as_of_date": date_token(raw_as_of),
        "as_of_session": configured.get("as_of_session") or as_of_session,
        "component_as_of_dates": component_as_of_dates,
        "event_risk_as_of_date": event_risk_as_of_date,
        "event_risk": str(configured.get("event_risk") or "unknown").lower(),
        "source_count": source_count,
        "proxy_source_count": proxy_source_count if proxy_only else 0,
        "sources": sources,
        "notes": configured.get("notes", []) if isinstance(configured.get("notes", []), list) else [],
        "evidence_mode": evidence_mode,
        "proxy_only": proxy_only,
    }
    for key in COMPONENT_KEYS:
        row[key] = as_float(configured.get(key))
    row["total_score"] = total_score(row, weights)

    missing_components = [key for key in COMPONENT_KEYS if row.get(key) is None]
    if not configured:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_evidence_missing"})
    elif proxy_generated:
        findings.append({"symbol": symbol, "severity": "info", "reason": "automatic_proxy_evidence", "provider": "automatic_local_proxy_v1"})
    if proxy_only:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_proxy_only", "proxy_source_count": proxy_source_count})
    if evidence_date is None:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_evidence_date_missing"})
    elif report_date is not None:
        age_days = (report_date - evidence_date).days
        row["age_days"] = age_days
        if age_days < 0:
            findings.append({"symbol": symbol, "severity": "critical", "reason": "nontechnical_evidence_from_future"})
        elif not any(component_as_of_dates.values()) and age_days > int(policy.get("max_staleness_days", 30)):
            findings.append({"symbol": symbol, "severity": "info", "reason": "nontechnical_evidence_stale", "age_days": age_days})
    component_age_days, component_findings = component_staleness_findings(symbol, component_as_of_dates, report_date, policy)
    if component_age_days:
        row["component_age_days"] = component_age_days
    findings.extend(component_findings)
    if report_date is not None and event_risk_as_of_date is not None:
        event_risk_date = parse_date(event_risk_as_of_date)
        max_days = policy.get("component_max_staleness_days", DEFAULT_COMPONENT_MAX_STALENESS_DAYS)
        max_days = max_days if isinstance(max_days, dict) else DEFAULT_COMPONENT_MAX_STALENESS_DAYS
        if event_risk_date is not None:
            event_age_days = (report_date - event_risk_date).days
            row["event_risk_age_days"] = event_age_days
            if event_age_days < 0:
                findings.append({"symbol": symbol, "severity": "critical", "reason": "event_risk_from_future", "age_days": event_age_days})
            elif event_age_days > int(max_days.get("event_risk", policy.get("max_staleness_days", 30))):
                findings.append({"symbol": symbol, "severity": "warning", "reason": "event_risk_stale", "age_days": event_age_days})
    if missing_components:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_component_missing", "components": missing_components})
    if row["total_score"] is None:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_score_missing"})
    elif row["total_score"] < float(policy.get("min_total_score_for_action", 0.55)):
        findings.append({"symbol": symbol, "severity": "info", "reason": "nontechnical_score_below_action_min", "total_score": row["total_score"]})
    if row["event_risk"] == "unknown" and policy.get("block_unknown_event_risk", True):
        findings.append({"symbol": symbol, "severity": "warning", "reason": "event_risk_unknown"})
    elif row["event_risk"] in HARD_EVENT_RISKS:
        findings.append({"symbol": symbol, "severity": "warning", "reason": f"event_risk_{row['event_risk']}"})
    if source_count <= 0:
        findings.append({"symbol": symbol, "severity": "warning", "reason": "nontechnical_source_missing"})
    return row, findings


def build_evidence(
    config_path: pathlib.Path,
    as_of_date: str,
    trade_universe_path: pathlib.Path | None = None,
    snapshot_path: pathlib.Path | None = None,
    ranking_path: pathlib.Path | None = None,
    as_of_session: str | None = None,
) -> dict[str, Any]:
    config = read_toml(config_path)
    policy, weights = parse_policy(config)
    configured = configured_symbols(config, as_of_date, as_of_session)
    universe = universe_symbols(read_toml(trade_universe_path))
    snapshot = snapshot_symbols(load_json(snapshot_path))
    snapshot_payload = load_json(snapshot_path)
    ranking = ranking_symbols(load_json(ranking_path))
    symbols: dict[str, dict[str, Any]] = {}
    for source in (universe, snapshot, ranking, {symbol: {"symbol": symbol} for symbol in configured}):
        for symbol, row in source.items():
            symbols.setdefault(symbol, {}).update(row)

    rows: dict[str, dict[str, Any]] = {}
    findings: list[dict[str, Any]] = []
    for symbol in sorted(symbols):
        raw_configured = configured.get(symbol)
        proxy_generated = False
        if raw_configured is None:
            raw_configured = formal_provider_evidence(symbol, symbols[symbol], snapshot_payload, config, as_of_date, as_of_session)
        if raw_configured is None:
            raw_configured = automatic_proxy_evidence(symbol, symbols[symbol], snapshot_payload, config, as_of_date, as_of_session)
            proxy_generated = raw_configured is not None
        row, row_findings = build_symbol_evidence(symbol, symbols[symbol], raw_configured, as_of_date, as_of_session, policy, weights, proxy_generated)
        rows[symbol] = row
        findings.extend(row_findings)

    missing_count = sum(1 for row in rows.values() if row.get("evidence_mode") == "missing_fail_closed")
    proxy_count = sum(1 for row in rows.values() if row.get("evidence_mode") == "automatic_local_proxy")
    proxy_only_count = sum(1 for row in rows.values() if row.get("evidence_mode") == "automatic_local_proxy" or row.get("proxy_only") is True)
    formal_available_count = sum(1 for row in rows.values() if row.get("evidence_mode") in FORMAL_EVIDENCE_MODES and row.get("proxy_only") is not True)
    formal_provider_count = sum(1 for row in rows.values() if row.get("evidence_mode") == "formal_provider_point_in_time" and row.get("proxy_only") is not True)
    hard_event_risks = {"unknown", *HARD_EVENT_RISKS}
    return {
        "generated_at": utc_now(),
        "as_of_date": as_of_date,
        "as_of_session": as_of_session,
        "research_only": True,
        "no_execution": True,
        "evidence_mode": "point_in_time_curated_proxy_or_missing_fail_closed",
        "policy": policy,
        "weights": weights,
        "summary": {
            "symbol_count": len(rows),
            "available_count": formal_available_count,
            "curated_available_count": formal_available_count,
            "formal_provider_count": formal_provider_count,
            "automatic_proxy_count": proxy_count,
            "proxy_only_count": proxy_only_count,
            "proxy_coverage_ratio": round(proxy_only_count / len(rows), 3) if rows else None,
            "missing_count": missing_count,
            "coverage_ratio": round(formal_available_count / len(rows), 3) if rows else None,
            "actionable_evidence_count": sum(
                1
                for row in rows.values()
                if row.get("evidence_mode") in FORMAL_EVIDENCE_MODES
                and row.get("proxy_only") is not True
                and row.get("total_score") is not None
                and row.get("total_score") >= float(policy.get("min_total_score_for_action", 0.55))
                and row.get("source_count", 0) > 0
                and row.get("event_risk") not in hard_event_risks
            ),
            "finding_count": len(findings),
            "critical_finding_count": sum(1 for finding in findings if finding.get("severity") == "critical"),
            "blocking_finding_count": sum(1 for finding in findings if finding.get("severity") in {"critical", "warning"}),
        },
        "symbols": rows,
        "findings": findings,
        "sources": {
            "config": str(config_path),
            "trade_universe": str(trade_universe_path) if trade_universe_path else None,
            "snapshot": str(snapshot_path) if snapshot_path else None,
            "ranking": str(ranking_path) if ranking_path else None,
        },
    }


def write_markdown(path: pathlib.Path, payload: dict[str, Any]) -> None:
    summary = payload["summary"]
    lines = [
        "# Nontechnical Evidence Ledger",
        "",
        f"Generated: `{payload['generated_at']}`",
        f"As-of: `{payload['as_of_date']}`",
        f"Research only: `{payload['research_only']}`; no execution: `{payload['no_execution']}`",
        "",
        "## Summary",
        f"- symbols: `{summary['symbol_count']}`",
        f"- curated_available: `{summary['available_count']}`",
        f"- proxy_only: `{summary.get('proxy_only_count')}` automatic=`{summary.get('automatic_proxy_count')}`",
        f"- missing: `{summary['missing_count']}`",
        f"- coverage_ratio: `{summary['coverage_ratio']}`",
        f"- actionable_evidence_count: `{summary['actionable_evidence_count']}`",
        f"- findings: `{summary['finding_count']}` critical=`{summary['critical_finding_count']}`",
        "",
        "## Findings",
    ]
    for finding in payload.get("findings", [])[:20]:
        lines.append(f"- `{finding.get('symbol')}` {finding.get('reason')} severity={finding.get('severity')}")
    if not payload.get("findings"):
        lines.append("- No evidence integrity findings.")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build point-in-time nontechnical evidence used as an action gate.")
    parser.add_argument("--config", default=str(ROOT / "config" / "nontechnical_evidence.toml"))
    parser.add_argument("--trade-universe", default=str(ROOT / "config" / "trade_universe.toml"))
    parser.add_argument("--snapshot", default=None)
    parser.add_argument("--ranking", default=None)
    parser.add_argument("--as-of-date", required=True)
    parser.add_argument("--as-of-session", default=None)
    parser.add_argument("--output-json", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.json"))
    parser.add_argument("--output-md", default=str(ROOT / "research" / "evidence" / "nontechnical" / "latest.md"))
    args = parser.parse_args()

    payload = build_evidence(
        resolve_path(args.config) or pathlib.Path(args.config),
        args.as_of_date,
        resolve_path(args.trade_universe),
        resolve_path(args.snapshot),
        resolve_path(args.ranking),
        args.as_of_session,
    )
    output_json = resolve_path(args.output_json) or pathlib.Path(args.output_json)
    output_md = resolve_path(args.output_md) or pathlib.Path(args.output_md)
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(output_md, payload)
    print(f"Wrote nontechnical evidence: {output_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

import json
import pathlib
import sys
import tempfile
import unittest
from unittest import mock


ROOT = pathlib.Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import evaluate_investment_system_change as change_eval  # noqa: E402
import evaluate_investment_calls as call_eval  # noqa: E402
import attribute_investment_outcomes as attribution  # noqa: E402
import optimize_investment_params as optimizer  # noqa: E402
import plan_investment_system_improvements as planner  # noqa: E402
import rank_investment_universe as ranker  # noqa: E402
import backtest_investment_strategy as backtester  # noqa: E402
import backfill_investment_snapshots as backfill_snapshots  # noqa: E402
import build_snapshot_registry as snapshot_registry  # noqa: E402
import build_symbol_risk_memory as symbol_risk  # noqa: E402
import create_investment_run_manifest as run_manifest  # noqa: E402
import generate_investment_draft_calls as draft_calls  # noqa: E402
import generate_investment_risk_review as risk_review  # noqa: E402
import validate_investment_calls as calls_validator  # noqa: E402
import check_investment_readiness as readiness  # noqa: E402
import fetch_investment_data as fetch_data  # noqa: E402
import log_investment_shadow as shadow_log  # noqa: E402
import backfill_investment_shadow as shadow_backfill  # noqa: E402
import evaluate_investment_shadow as shadow_eval  # noqa: E402
import run_investment_daily_shadow as daily_shadow  # noqa: E402
import run_investment_shadow_variants as shadow_variants  # noqa: E402
import build_chinese_daily_close_report as close_report  # noqa: E402
import build_investment_dashboard as investment_dashboard  # noqa: E402
import build_investment_evidence_ledger as evidence_ledger  # noqa: E402
import build_investment_calibration_scorecard as calibration_scorecard  # noqa: E402
import build_nontechnical_evidence as nontechnical_builder  # noqa: E402
import evaluate_nontechnical_evidence as nontechnical_eval  # noqa: E402
import generate_investment_focus_pool as focus_pool  # noqa: E402


class InvestmentLevel5Level6Tests(unittest.TestCase):
    def write_trade_snapshot(self, path, date, a_price, b_price):
        path.write_text(
            json.dumps(
                {
                    "as_of_date": date,
                    "generated_at": f"{date}T00:00:00Z",
                    "items": [
                        {
                            "symbol": "AAA.HK",
                            "name": "AAA",
                            "kind": "stock",
                            "theme": "growth",
                            "latest_close": a_price,
                            "ma20": 10.0,
                            "ma60": 10.0,
                            "range_pos_60": 0.2,
                            "pct_change_1d": 0.0,
                            "volume_ratio_20": 1.0,
                            "regime_flags": [],
                        },
                        {
                            "symbol": "BBB.HK",
                            "name": "BBB",
                            "kind": "stock",
                            "theme": "defensive",
                            "latest_close": b_price,
                            "ma20": 10.0,
                            "ma60": 10.0,
                            "range_pos_60": 0.1,
                            "pct_change_1d": -1.0,
                            "volume_ratio_20": 0.8,
                            "regime_flags": [],
                        },
                        {
                            "symbol": "2800.HK",
                            "name": "Tracker Fund",
                            "kind": "etf",
                            "theme": "broad",
                            "latest_close": 25.0,
                            "ma20": 25.0,
                            "ma60": 25.0,
                            "range_pos_60": 0.1,
                            "pct_change_1d": 0.0,
                            "volume_ratio_20": 1.0,
                            "regime_flags": [],
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )

    def write_trade_registry(self, tmp_path, dates):
        entries = []
        for date in dates:
            entries.append(
                {
                    "path": str(tmp_path / f"trade-{date}.json"),
                    "date": date,
                    "session": "close",
                    "snapshot_type": "trade",
                    "as_of_date": date,
                    "quality": {"missing_latest_close": 0, "date_mismatch": False},
                }
            )
        registry = tmp_path / "registry.json"
        registry.write_text(json.dumps({"entries": entries}), encoding="utf-8")
        return registry

    def write_daily_shadow_configs(self, tmp_path):
        config_dir = tmp_path / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        (config_dir / "investment_profile.toml").write_text(
            """
[costs]
estimated_round_trip_bps = 35
minimum_edge_bps = 100

[ranking]
min_action_score = 65
min_watch_score = 45
max_candidates = 8
""".lstrip(),
            encoding="utf-8",
        )
        (config_dir / "optimization.toml").write_text(
            """
actionable_top_n = 2
diagnostic_top_n = 3
round_trip_bps = 35
minimum_edge_bps = 100
symbol_risk_memory = "research/experiments/symbol_risk_memory.json"

[safety_invariants]
forbid_cost_gate_reduction = true
forbid_edge_gate_reduction = true
""".lstrip(),
            encoding="utf-8",
        )
        (config_dir / "active_strategy.toml").write_text(
            """
strategy_id = "test_strategy"
strategy_version = "test_strategy"
status = "active"

[weights]
trend_weight = 0.45
momentum_weight = 0.30
range_weight = 0.15
risk_penalty_weight = 1.15

[cost_gate]
estimated_round_trip_bps = 35
minimum_edge_bps = 100

[safety_invariants]
forbid_cost_gate_reduction = true
forbid_edge_gate_reduction = true
""".lstrip(),
            encoding="utf-8",
        )
        (config_dir / "nontechnical_evidence.toml").write_text(
            """
[policy]
require_for_action = true
max_staleness_days = 30
min_total_score_for_action = 0.55
block_unknown_event_risk = true

[weights]
fundamental_score = 0.30
valuation_score = 0.20
catalyst_score = 0.25
flow_score = 0.15
macro_score = 0.10
""".lstrip(),
            encoding="utf-8",
        )
        (config_dir / "focus_industries.toml").write_text(
            """
[policy]
max_active_industries = 2
max_active_symbols_per_industry = 2
min_active_industry_score = 40
min_watch_industry_score = 20
min_focus_symbol_score = 0

[[industries]]
id = "growth_focus"
name = "成长"
strategic_weight = 1.0
themes = ["growth"]
leader_symbols = ["AAA.HK"]
high_beta_symbols = []
confirming_symbols = []
""".lstrip(),
            encoding="utf-8",
        )

    def valid_call(self, symbol="AAA.HK", state="buy_candidate"):
        return {
            "symbol": symbol,
            "state": state,
            "theme": "growth",
            "kind": "stock",
            "horizon_days_min": 3,
            "horizon_days_max": 10,
            "confidence": 0.7,
            "rationale": "test rationale",
            "evidence": ["test evidence"],
            "risks": ["test risk"],
            "invalidation": "test invalidation",
            "selection_source_theme": "growth",
            "selection_reason": "test selection reason",
        }

    def shadow_variant_ranking(self, date="2026-04-01", session="close"):
        row = {
            "symbol": "AAA.HK",
            "name": "AAA",
            "kind": "stock",
            "theme": "growth",
            "score": 80.0,
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "latest_close": 10.0,
            "range_pos_60": 0.5,
            "pct_change_1d": 1.0,
            "volume_ratio_20": 1.2,
            "same_theme_peer_evidence_passed": True,
            "qualification_flags": [],
            "disqualifiers": [],
            "action_disqualifiers": [],
            "expected_edge_bps": 160.0,
            "net_expected_edge_bps": 125.0,
        }
        return {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": date,
            "as_of_session": session,
            "session": session,
            "thresholds": {"actionable_top_n": 1, "diagnostic_top_n": 1},
            "actionable_candidates": [dict(row)],
            "diagnostic_candidates": [dict(row)],
            "top_candidates": [dict(row)],
            "all_ranked": [dict(row)],
        }

    def write_close_report_fixture(
        self,
        tmp_path,
        date="2026-04-27",
        calls_update=None,
        risk=None,
        ranking=None,
        evidence=None,
        calibration=None,
        forward=None,
        variants=None,
        nontechnical=None,
        attribution_data=None,
    ):
        paths = {
            "calls": tmp_path / "calls.json",
            "ranking": tmp_path / "ranking.json",
            "risk": tmp_path / "risk.json",
            "evidence": tmp_path / "evidence.json",
            "calibration": tmp_path / "calibration.json",
            "forward": tmp_path / "forward.json",
            "variants": tmp_path / "variants.json",
            "nontechnical": tmp_path / "nontechnical.json",
            "attribution": tmp_path / "nontechnical-attribution.json",
            "output": tmp_path / "reports",
        }
        calls = {"date": date, "session": "close", "recommendations": [self.valid_call("AAA.HK", "buy_candidate")]}
        if calls_update:
            calls.update(calls_update)
        fixtures = {
            paths["calls"]: calls,
            paths["ranking"]: ranking if ranking is not None else {"as_of_date": date, "actionable_candidates": [], "diagnostic_candidates": [], "top_candidates": []},
            paths["risk"]: risk if risk is not None else {"date": date, "session": "close", "verdicts": [{"symbol": "AAA.HK", "final_state_cap": "buy_candidate", "risk_decision": "pass"}]},
            paths["evidence"]: evidence if evidence is not None else {"as_of_date": date, "summary": {"forward_shadow_log_count": 1}},
            paths["calibration"]: calibration if calibration is not None else {"as_of_date": date, "summary": {"combined_record_count": 1}, "scorecard": {}},
            paths["forward"]: forward if forward is not None else {"thresholds": {"as_of_date": date}, "summary": {"sample_count": 1}},
            paths["variants"]: variants if variants is not None else {"as_of_date": date, "competition_id": "test_competition", "scoreboard": []},
            paths["nontechnical"]: nontechnical if nontechnical is not None else {"as_of_date": date, "summary": {}},
            paths["attribution"]: attribution_data if attribution_data is not None else {"as_of_date": date, "summary": {}, "buckets": {"total_score": []}},
        }
        for path, payload in fixtures.items():
            path.write_text(json.dumps(payload), encoding="utf-8")
        return paths

    def build_close_report_from_fixture(self, paths, date="2026-04-27"):
        return close_report.build_report(
            date,
            "close",
            paths["calls"],
            paths["ranking"],
            paths["risk"],
            paths["evidence"],
            paths["calibration"],
            paths["forward"],
            paths["variants"],
            paths["output"],
            paths["nontechnical"],
            paths["attribution"],
        )

    def test_tencent_symbol_mapping_supports_hk_and_a_shares(self):
        self.assertEqual(fetch_data.to_tencent_symbol("0700.HK"), "hk00700")
        self.assertEqual(fetch_data.to_tencent_symbol("600519.SH"), "sh600519")
        self.assertEqual(fetch_data.to_tencent_symbol("000333.SZ"), "sz000333")
        self.assertEqual(fetch_data.exchange_for_symbol("510300.SH"), "SSE")
        self.assertEqual(fetch_data.currency_for_symbol("159915.SZ"), "CNY")

    def test_backfill_metric_uses_symbol_market_metadata(self):
        series = []
        for index in range(20):
            price = 10.0 + index
            series.append([f"2026-01-{index + 1:02d}", price, price + 0.5, price + 1.0, price - 1.0, 1000 + index])

        metric = backfill_snapshots.build_historical_metric("600519.SH", "Kweichow Moutai", "stock", "consumer-staples", series, 19)

        self.assertEqual(metric["exchange"], "SSE")
        self.assertEqual(metric["currency"], "CNY")

    def ranking_with_row(self, row):
        defaults = {
            "expected_edge_bps": 160.0,
            "net_expected_edge_bps": 125.0,
            "cost_gate_passed": True,
            "edge_method": "technical_snapshot_score_v1",
            "evidence_window": "1d_momentum_20d_volume_20d_60d_trend_60d_range",
            "theme_rank": 1,
            "theme_leader": row.get("symbol"),
            "theme_leader_score": row.get("score", 80),
            "theme_score_gap_to_leader": 0.0,
            "is_theme_leader": True,
            "same_theme_peer_evidence_passed": True,
            "same_theme_best_symbol": row.get("symbol"),
            "same_theme_best_score": row.get("score", 80),
            "same_theme_selected_vs_best_score_gap": 0.0,
            "peer_relative_decision": "theme_leader",
        }
        row = {**defaults, **row}
        return {
            "actionable_candidates": [row] if row.get("qualified_for_action") else [],
            "diagnostic_candidates": [row],
            "top_candidates": [row],
            "all_ranked": [row],
        }

    def test_optimizer_fail_closed_when_execution_is_enabled(self):
        active = {"safety_invariants": {"automatic_trading_enabled": True}}
        opt = {"safety_invariants": {key: True for key in optimizer.IMMUTABLE_TRUE_INVARIANTS}}
        with self.assertRaises(SystemExit):
            optimizer.invariant_block(active, opt)

    def test_change_evaluator_detects_mode_false_and_execution_terms(self):
        false_line = "+" + "recommendation_only" + " = " + "false"
        exec_word = "br" + "oker"
        diff = "\n".join(
            [
                "diff --git a/config/portfolio.toml b/config/portfolio.toml",
                "+++ b/config/portfolio.toml",
                false_line,
                "diff --git a/scripts/example.py b/scripts/example.py",
                "+++ b/scripts/example.py",
                "+" + exec_word + " = True",
            ]
        )
        result = change_eval.evaluate_change(pathlib.Path(tempfile.gettempdir()), ["config/portfolio.toml", "scripts/example.py"], diff, [])
        rules = {finding["rule"] for finding in result["findings"]}
        self.assertFalse(result["passed"])
        self.assertIn("research_only_mode", rules)
        self.assertIn("no_execution_terms", rules)

    def test_change_evaluator_blocks_risk_limit_increases_and_gate_reductions(self):
        diff = "\n".join(
            [
                "diff --git a/config/investment_profile.toml b/config/investment_profile.toml",
                "+++ b/config/investment_profile.toml",
                "-minimum_edge_bps = 100",
                "+minimum_edge_bps = 50",
                "-max_single_position_pct = 10",
                "+max_single_position_pct = 20",
                "-max_theme_exposure_pct = 30",
                "+max_theme_exposure_pct = 50",
            ]
        )
        result = change_eval.evaluate_change(pathlib.Path(tempfile.gettempdir()), ["config/investment_profile.toml"], diff, [])
        rules = {finding["rule"] for finding in result["findings"]}
        self.assertFalse(result["passed"])
        self.assertIn("risk_gate_not_lowered", rules)
        self.assertIn("risk_limit_not_increased", rules)

    def test_change_evaluator_blocks_execution_enable_aliases(self):
        diff = "\n".join(
            [
                "diff --git a/scripts/execution.py b/scripts/execution.py",
                "+++ b/scripts/execution.py",
                "+execution_enabled = true",
                "+def execute_buy(): pass",
            ]
        )
        result = change_eval.evaluate_change(pathlib.Path(tempfile.gettempdir()), ["scripts/execution.py"], diff, [])
        rules = {finding["rule"] for finding in result["findings"]}
        self.assertFalse(result["passed"])
        self.assertIn("automatic_execution_disabled", rules)
        self.assertIn("no_execution_terms", rules)

    def test_change_evaluator_checks_final_repo_state_invariants(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config_dir = tmp_path / "config"
            config_dir.mkdir()
            (config_dir / "portfolio.toml").write_text('[portfolio]\nmode = "live"\n', encoding="utf-8")
            (config_dir / "active_strategy.toml").write_text(
                "[safety_invariants]\nautomatic_trading_enabled = false\nresearch_only = false\n",
                encoding="utf-8",
            )

            result = change_eval.evaluate_change(tmp_path, [], "", [])

            final_findings = [finding for finding in result["findings"] if finding["rule"] == "final_state_invariant"]
            self.assertFalse(result["passed"])
            self.assertGreaterEqual(len(final_findings), 2)
            self.assertTrue(any(finding["path"] == "config/portfolio.toml" for finding in final_findings))
            self.assertTrue(any(finding["path"] == "config/active_strategy.toml" for finding in final_findings))

    def test_change_evaluator_allows_safe_final_repo_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config_dir = tmp_path / "config"
            config_dir.mkdir()
            (config_dir / "portfolio.toml").write_text('[portfolio]\nmode = "recommendation_only"\n', encoding="utf-8")
            safety = (
                "[safety_invariants]\n"
                "automatic_trading_enabled = false\n"
                "forbid_automatic_trading = true\n"
                "forbid_cost_gate_reduction = true\n"
                "forbid_edge_gate_reduction = true\n"
                "forbid_history_tampering = true\n"
                "forbid_snapshot_mutation = true\n"
                "research_only = true\n"
            )
            (config_dir / "active_strategy.toml").write_text(safety, encoding="utf-8")
            (config_dir / "optimization.toml").write_text(safety, encoding="utf-8")

            result = change_eval.evaluate_change(tmp_path, [], "", [])

            self.assertTrue(result["passed"])

    def test_change_evaluator_fails_when_required_config_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            (tmp_path / "config").mkdir()

            result = change_eval.evaluate_change(tmp_path, [], "", [])

            rules = {finding["rule"] for finding in result["findings"]}
            self.assertFalse(result["passed"])
            self.assertIn("final_state_invariant", rules)

    def test_evaluate_calls_as_of_skips_future_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            calls_dir = tmp_path / "calls"
            snapshot_dir = tmp_path / "snapshots"
            calls_dir.mkdir()
            snapshot_dir.mkdir()
            self.write_trade_snapshot(snapshot_dir / "2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(snapshot_dir / "2026-04-02.json", "2026-04-02", 11.0, 10.0)
            (calls_dir / "2026-04-01-calls.json").write_text(
                json.dumps({"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}),
                encoding="utf-8",
            )

            evaluations, _summary = call_eval.evaluate_calls(
                calls_dir,
                snapshot_dir,
                close_windows=[1],
                intraday_windows=[0],
                as_of_date=call_eval.parse_date("2026-04-01"),
                as_of_session="close",
            )

            self.assertEqual(evaluations, [])

    def test_evaluate_calls_morning_as_of_skips_same_day_close_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            calls_dir = tmp_path / "calls"
            snapshot_dir = tmp_path / "snapshots"
            calls_dir.mkdir()
            snapshot_dir.mkdir()
            self.write_trade_snapshot(snapshot_dir / "2026-04-01.json", "2026-04-01", 10.0, 10.0)
            (calls_dir / "2026-04-01-morning-calls.json").write_text(
                json.dumps({"date": "2026-04-01", "session": "morning", "recommendations": [self.valid_call()]}),
                encoding="utf-8",
            )

            evaluations, summary = call_eval.evaluate_calls(
                calls_dir,
                snapshot_dir,
                close_windows=[1],
                intraday_windows=[0],
                as_of_date=call_eval.parse_date("2026-04-01"),
                as_of_session="morning",
            )

            self.assertEqual(evaluations, [])
            self.assertEqual(summary["as_of_date"], "2026-04-01")
            self.assertEqual(summary["as_of_session"], "morning")

    def test_calls_validator_rejects_diagnostic_actionable(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": False,
            "qualified_for_watch": True,
            "diagnostic_only": True,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})

        self.assertTrue(any("diagnostic_only" in error for error in errors))
        self.assertTrue(any("actionable_candidates" in error for error in errors))

    def test_calls_validator_rejects_diagnostic_sell_states(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": False,
            "qualified_for_watch": False,
            "diagnostic_only": True,
        }

        for state in ("trim", "sell_candidate"):
            calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state=state)]}
            errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})
            self.assertTrue(any("diagnostic or non-watch" in error for error in errors))

    def test_calls_validator_allows_diagnostic_watch_and_avoid(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": False,
            "qualified_for_watch": False,
            "diagnostic_only": True,
        }

        for state in ("watch_only", "avoid"):
            calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state=state)]}
            errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})
            self.assertEqual(errors, [])

    def test_calls_validator_accepts_legal_actionable(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})

        self.assertEqual(errors, [])

    def test_calls_validator_rejects_actionable_without_edge_fields(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        ranking = {
            "actionable_candidates": [row],
            "diagnostic_candidates": [row],
            "top_candidates": [row],
            "all_ranked": [row],
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, ranking, {"AAA.HK"})

        self.assertTrue(any("expected_edge_bps" in error for error in errors))
        self.assertTrue(any("net_expected_edge_bps" in error for error in errors))

    def test_snapshot_registry_flags_quote_date_leakage(self):
        quality = snapshot_registry.quality_for(
            {
                "as_of_date": "2026-01-07",
                "items": [
                    {"symbol": "AAA.HK", "latest_close": 10.0, "quote_trade_date": "2026-04-29"},
                    {"symbol": "BBB.HK", "latest_close": 11.0, "quote_trade_date": "2026-01-07"},
                    {"symbol": "CCC.HK", "latest_close": 12.0, "quote_trade_date": "bad-date"},
                ],
            },
            "2026-01-07",
        )

        self.assertEqual(quality["quote_date_mismatch_count"], 2)
        self.assertEqual(quality["future_quote_date_count"], 1)
        self.assertEqual(quality["invalid_quote_date_count"], 1)
        self.assertEqual(quality["max_quote_trade_date"], "2026-04-29")

    def test_backfill_selects_requested_date_range(self):
        selected = backfill_snapshots.selected_dates_for_backfill(
            {"2026-01-02", "2026-01-03", "2026-01-06", "2026-02-01"},
            days=2,
            start_date="2026-01-03",
            end_date="2026-01-31",
        )

        self.assertEqual(selected, ["2026-01-03", "2026-01-06"])

    def test_backfill_defaults_to_last_n_dates(self):
        selected = backfill_snapshots.selected_dates_for_backfill(
            {"2026-01-02", "2026-01-03", "2026-01-06"},
            days=2,
        )

        self.assertEqual(selected, ["2026-01-03", "2026-01-06"])

    def test_backtest_skips_registry_entries_with_payload_date_mismatch(self):
        registry = {
            "entries": [
                {
                    "path": "a.json",
                    "date": "2026-04-01",
                    "session": "close",
                    "snapshot_type": "trade",
                    "as_of_date": "2026-04-27",
                    "quality": {"missing_latest_close": 0, "date_mismatch": True},
                },
                {
                    "path": "b.json",
                    "date": "2026-04-02",
                    "session": "close",
                    "snapshot_type": "trade",
                    "as_of_date": "2026-04-02",
                    "quality": {"missing_latest_close": 0, "date_mismatch": False},
                },
            ]
        }
        entries = backtester.registry_entries(registry, "trade")
        self.assertEqual([entry["date"] for entry in entries], ["2026-04-02"])

    def test_backtest_skips_registry_entries_with_quote_date_leakage(self):
        registry = {
            "entries": [
                {
                    "path": "a.json",
                    "date": "2026-04-01",
                    "session": "close",
                    "snapshot_type": "trade",
                    "as_of_date": "2026-04-01",
                    "quality": {"missing_latest_close": 0, "date_mismatch": False, "quote_date_mismatch_count": 1, "future_quote_date_count": 1},
                },
                {
                    "path": "b.json",
                    "date": "2026-04-02",
                    "session": "close",
                    "snapshot_type": "trade",
                    "as_of_date": "2026-04-02",
                    "quality": {"missing_latest_close": 0, "date_mismatch": False, "quote_date_mismatch_count": 0, "future_quote_date_count": 0},
                },
            ]
        }

        entries = backtester.registry_entries(registry, "trade")
        quality = backtester.registry_quality_summary(registry, "trade")

        self.assertEqual([entry["date"] for entry in entries], ["2026-04-02"])
        self.assertEqual(quality["skipped_quote_date_mismatch_count"], 1)
        self.assertEqual(quality["skipped_future_quote_date_count"], 1)
        self.assertEqual(quality["quote_date_mismatch_item_count"], 1)
        self.assertEqual(quality["future_quote_date_item_count"], 1)

    def test_backtest_summary_includes_registry_quality_skips(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 10.5, 10.2)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-03.json", "2026-04-03", 11.0, 10.4)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02", "2026-04-03"])
            registry_payload = json.loads(registry.read_text(encoding="utf-8"))
            registry_payload["entries"][1]["quality"]["quote_date_mismatch_count"] = 1
            registry_payload["entries"][1]["quality"]["future_quote_date_count"] = 1
            registry.write_text(json.dumps(registry_payload), encoding="utf-8")

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_samples=1,
                minimum_edge_bps=0,
            )

            self.assertEqual(result["summary"]["registry_entry_count"], 3)
            self.assertEqual(result["summary"]["usable_registry_entry_count"], 2)
            self.assertEqual(result["summary"]["skipped_registry_entry_count"], 1)
            self.assertEqual(result["summary"]["skipped_quote_date_mismatch_count"], 1)
            self.assertEqual(result["summary"]["skipped_future_quote_date_count"], 1)

    def test_backtest_relaxed_fallback_marks_below_watch_score_and_quality(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 9.0, 10.2)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-03.json", "2026-04-03", 11.0, 10.4)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02", "2026-04-03"])

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=95,
                candidate_policy="relaxed",
                min_samples=2,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
            )

            self.assertEqual(result["summary"]["sample_quality"], "relaxed_fallback")
            self.assertEqual(result["summary"]["strict_sample_count"], 0)
            self.assertGreater(result["summary"]["relaxed_sample_count"], 0)
            self.assertEqual(result["summary"]["production_sample_count"], result["summary"]["sample_count"])
            self.assertIn("diagnostic_layer_sample_count", result["summary"])
            self.assertGreater(result["summary"]["diagnostic_only_sample_count"], 0)
            self.assertTrue(any(record["below_watch_score"] for record in result["records"]))

    def test_backtest_summary_includes_adverse_breach_rate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 9.0, 10.2)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-03.json", "2026-04-03", 11.0, 10.4)
            day2 = json.loads((tmp_path / "trade-2026-04-02.json").read_text(encoding="utf-8"))
            day2["items"][0]["ma20"] = 8.0
            day2["items"][0]["ma60"] = 8.0
            (tmp_path / "trade-2026-04-02.json").write_text(json.dumps(day2), encoding="utf-8")
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02", "2026-04-03"])

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                min_action_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
            )

            self.assertIn("adverse_breach_rate", result["summary"])
            self.assertEqual(result["summary"]["adverse_breach_rate"], 0.5)

    def test_backtest_daily_close_stop_uses_first_stop_close_as_outcome(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 9.3, 10.2)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-15.json", "2026-04-15", 8.0, 10.4)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02", "2026-04-15"])

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=14,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                min_action_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
                experimental_exit_rule="daily_close_stop",
                stop_loss_pct=-6.0,
            )

            self.assertEqual(result["summary"]["experimental_exit_rule"], "daily_close_stop")
            self.assertEqual(result["summary"]["exit_triggered_count"], 1)
            self.assertEqual(result["summary"]["exit_triggered_rate"], 1.0)
            record = result["records"][0]
            self.assertTrue(record["exit_triggered"])
            self.assertEqual(record["exit_reason"], "daily_close_stop_loss")
            self.assertEqual(record["future_date"], "2026-04-02")
            self.assertEqual(record["planned_future_date"], "2026-04-15")
            self.assertEqual(record["net_return_pct"], -7.0)
            self.assertEqual(record["unmanaged_net_return_pct"], -20.0)
            self.assertEqual(record["max_adverse_pct"], -7.0)
            self.assertEqual(record["unmanaged_max_adverse_pct"], -20.0)

    def test_backtest_risk_diagnostics_group_market_and_adverse_drivers(self):
        records = [
            {
                "base_date": "2026-01-02",
                "future_date": "2026-01-16",
                "symbol": "0700.HK",
                "market_family": "hk",
                "theme": "internet",
                "net_return_pct": 1.2,
                "alpha_pct": 0.4,
                "max_adverse_pct": -2.0,
                "adverse_breach": False,
                "score": 70,
                "range_pos_60": 0.5,
                "volume_ratio_20": 1.1,
                "pct_change_1d": 1.0,
                "market_range_pos_60": 0.4,
            },
            {
                "base_date": "2026-01-03",
                "future_date": "2026-01-17",
                "symbol": "600519.SH",
                "market_family": "cn",
                "theme": "consumer",
                "net_return_pct": -3.5,
                "alpha_pct": -1.0,
                "max_adverse_pct": -9.2,
                "adverse_breach": True,
                "score": 82,
                "range_pos_60": 0.92,
                "volume_ratio_20": 2.8,
                "pct_change_1d": 5.2,
                "market_range_pos_60": 0.68,
            },
        ]

        diagnostics = backtester.build_risk_diagnostics(records, -8.0)

        market_rows = {row["market_family"]: row for row in diagnostics["by_market_family"]}
        self.assertEqual(market_rows["hk"]["sample_count"], 1)
        self.assertEqual(market_rows["cn"]["adverse_breach_rate"], 1.0)
        self.assertEqual(diagnostics["worst_adverse_records"][0]["symbol"], "600519.SH")
        volume_buckets = {row["bucket"]: row for row in diagnostics["driver_buckets"]["volume_ratio_20"]}
        self.assertEqual(volume_buckets["gte_2_50"]["adverse_breach_count"], 1)

    def test_backtest_strict_excludes_disqualified_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 10.5, 10.2)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02"])
            first = json.loads((tmp_path / "trade-2026-04-01.json").read_text(encoding="utf-8"))
            first["items"][0].update(
                {
                    "latest_close": 8.0,
                    "ma20": 10.0,
                    "ma60": 11.0,
                    "range_pos_60": 0.05,
                    "volume_ratio_20": 0.4,
                    "regime_flags": ["downtrend"],
                }
            )
            first["items"][1]["range_pos_60"] = 0.2
            first["items"][2]["range_pos_60"] = 0.2
            (tmp_path / "trade-2026-04-01.json").write_text(json.dumps(first), encoding="utf-8")

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=2,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
            )

            symbols = {record["symbol"] for record in result["records"]}
            self.assertNotIn("AAA.HK", symbols)
            self.assertTrue(all(record["qualified_for_watch"] for record in result["records"]))

    def test_backtest_applies_symbol_risk_veto(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 11.0, 10.2)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02"])
            first = json.loads((tmp_path / "trade-2026-04-01.json").read_text(encoding="utf-8"))
            first["items"][0].update({"latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8})
            (tmp_path / "trade-2026-04-01.json").write_text(json.dumps(first), encoding="utf-8")

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=2,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                min_action_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
                symbol_risk={"AAA.HK": {"action_veto": True, "reasons": ["test veto"], "tags": ["backtest_adverse_breach"]}},
            )

            self.assertNotIn("AAA.HK", {record["symbol"] for record in result["records"]})

    def test_backtest_point_in_time_symbol_risk_ignores_future_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 11.0, 10.2)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02"])
            first = json.loads((tmp_path / "trade-2026-04-01.json").read_text(encoding="utf-8"))
            first["items"][0].update({"latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8})
            (tmp_path / "trade-2026-04-01.json").write_text(json.dumps(first), encoding="utf-8")

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                min_action_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
                symbol_risk={"AAA.HK": {"action_veto": True, "reasons": ["future full-memory veto"], "tags": ["recent_symbol_adverse_breach"]}},
                symbol_risk_mode="point_in_time",
                symbol_risk_records=[{"call_date": "2026-04-02", "symbol": "AAA.HK", "return_pct": -9.0, "verdict": "fail"}],
            )

            self.assertIn("AAA.HK", {record["symbol"] for record in result["records"]})
            self.assertTrue(result["summary"]["symbol_risk_point_in_time"])

    def test_backtest_point_in_time_symbol_risk_blocks_past_adverse_records(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 11.0, 10.2)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02"])
            first = json.loads((tmp_path / "trade-2026-04-01.json").read_text(encoding="utf-8"))
            first["items"][0].update({"latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8})
            (tmp_path / "trade-2026-04-01.json").write_text(json.dumps(first), encoding="utf-8")

            result = backtester.backtest(
                registry,
                "test_strategy",
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                top_n=1,
                horizon_days=1,
                round_trip_bps=0,
                benchmark_symbol="2800.HK",
                min_watch_score=0,
                min_action_score=0,
                candidate_policy="strict",
                min_samples=1,
                max_adverse_limit_pct=-8.0,
                minimum_edge_bps=0,
                symbol_risk_mode="point_in_time",
                symbol_risk_records=[{"call_date": "2026-03-31", "symbol": "AAA.HK", "return_pct": -9.0, "verdict": "fail"}],
            )

            self.assertNotIn("AAA.HK", {record["symbol"] for record in result["records"]})

    def test_optimizer_does_not_promote_relaxed_fallback_champion(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config_dir = tmp_path / "config"
            output_dir = tmp_path / "research" / "experiments"
            config_dir.mkdir(parents=True)
            active_path = config_dir / "active_strategy.toml"
            active_text = (
                'strategy_id = "active"\nstrategy_version = "active"\nstatus = "active"\n'
                '[weights]\ntrend_weight = 0.45\nmomentum_weight = 0.30\nrange_weight = 0.15\nrisk_penalty_weight = 1.15\n'
                '[safety_invariants]\nautomatic_trading_enabled = false\nforbid_automatic_trading = true\nforbid_cost_gate_reduction = true\n'
                'forbid_edge_gate_reduction = true\nforbid_history_tampering = true\nforbid_snapshot_mutation = true\nauto_select_active_research_strategy = true\nresearch_only = true\n'
            )
            active_path.write_text(active_text, encoding="utf-8")
            registry_path = tmp_path / "registry.json"
            registry_path.write_text(json.dumps({"entries": [{"snapshot_type": "trade", "session": "close"}]}), encoding="utf-8")
            opt_path = config_dir / "optimization.toml"
            opt_path.write_text(
                '\n'.join(
                    [
                        'active_strategy = "config/active_strategy.toml"',
                        'snapshot_registry = "registry.json"',
                        'output_dir = "research/experiments"',
                        'enabled = true',
                        'top_n = 1',
                        'horizon_days = 1',
                        'round_trip_bps = 0',
                        'benchmark_symbol = "2800.HK"',
                        'min_watch_score = 95',
                        'candidate_policy = "relaxed"',
                        'min_samples = 2',
                        'min_improvement_bps = 1',
                        'min_win_rate = 0.1',
                        'max_adverse_limit_pct = -8.0',
                        'max_adverse_breach_rate = 0.5',
                        'walk_forward_windows = 1',
                        '[promotion]',
                        'enabled = true',
                        'sessions = ["close"]',
                        '[search]',
                        'trend_weight = [0.40]',
                        'momentum_weight = [0.40]',
                        'range_weight = [0.20]',
                        'risk_penalty_weight = [1.00]',
                        '[safety_invariants]',
                        'automatic_trading_enabled = false',
                        'forbid_automatic_trading = true',
                        'forbid_cost_gate_reduction = true',
                        'forbid_edge_gate_reduction = true',
                        'forbid_history_tampering = true',
                        'forbid_snapshot_mutation = true',
                        'auto_select_active_research_strategy = true',
                        'research_only = true',
                    ]
                )
                + '\n',
                encoding="utf-8",
            )
            baseline = {
                "summary": {"sample_count": 2, "sample_quality": "sufficient", "avg_net_return_pct": 0.0, "win_rate": 0.5, "avg_alpha_pct": 0.0, "max_adverse_pct": -1.0, "avg_max_adverse_pct": -0.5, "adverse_breach_rate": 0.0},
                "records": [{"base_date": "2026-04-01", "net_return_pct": 0.0}, {"base_date": "2026-04-02", "net_return_pct": 0.0}],
            }
            challenger = {
                "summary": {"sample_count": 2, "sample_quality": "relaxed_fallback", "avg_net_return_pct": 10.0, "win_rate": 1.0, "avg_alpha_pct": 5.0, "max_adverse_pct": -1.0, "avg_max_adverse_pct": -0.5, "adverse_breach_rate": 0.0},
                "records": [{"base_date": "2026-04-01", "net_return_pct": 10.0}, {"base_date": "2026-04-02", "net_return_pct": 10.0}],
            }

            argv = ["opt", "--config", str(opt_path), "--session", "close"]
            with mock.patch.object(optimizer, "ROOT", tmp_path), mock.patch.object(optimizer, "backtest", side_effect=[baseline, challenger]), mock.patch.object(sys, "argv", argv):
                self.assertEqual(optimizer.main(), 0)

            result = json.loads((output_dir / "latest_optimization.json").read_text(encoding="utf-8"))
            self.assertFalse(result["updated_active_strategy"])
            self.assertIn("sample_quality=False", result["decision_reason"])
            self.assertEqual(active_path.read_text(encoding="utf-8"), active_text)

    def test_planner_creates_task_for_low_samples_and_win_rate(self):
        evaluation = {"evaluations": 10, "verdict_counts": {"pass": 2, "fail": 8}, "learning_counts": {}}
        backtest = {"summary": {"sample_count": 8, "win_rate": 0.2, "avg_net_return_pct": -1.0, "max_adverse_pct": -3.0}}
        optimization = {"decision_reason": "samples=False win_rate=False", "champion": {"summary": {"sample_count": 8, "win_rate": 0.2}}}
        tasks = planner.plan_tasks(evaluation, backtest, optimization, "")
        titles = [task["title"] for task in tasks]
        self.assertTrue(any("sample" in title.lower() for title in titles))
        self.assertTrue(any("win-rate" in title.lower() for title in titles))

    def test_planner_does_not_repeat_diagnostic_alignment_when_reporting_explicit(self):
        evaluation = {"evaluations": 10, "verdict_counts": {"pass": 8, "fail": 2}, "learning_counts": {}}
        backtest = {
            "summary": {
                "sample_count": 59,
                "production_sample_count": 59,
                "promotable_sample_count": 59,
                "qualified_sample_count": 59,
                "diagnostic_sample_count": 270,
                "diagnostic_layer_sample_count": 270,
                "diagnostic_only_sample_count": 270,
                "sample_quality": "sufficient",
                "win_rate": 0.5,
                "avg_net_return_pct": 0.1,
                "max_adverse_pct": -3.0,
            }
        }

        tasks = planner.plan_tasks(evaluation, backtest, {}, "")

        self.assertFalse(any(task["title"] == "Align diagnostic and qualified candidate reporting" for task in tasks))

    def test_ranking_weights_change_score_and_emit_strategy_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            snapshot = tmp_path / "snapshot.json"
            snapshot.write_text(
                json.dumps(
                    {
                        "as_of_date": "2026-04-27",
                        "generated_at": "2026-04-27T00:00:00Z",
                        "items": [
                            {
                                "symbol": "2800.HK",
                                "name": "Tracker Fund",
                                "kind": "etf",
                                "theme": "broad",
                                "latest_close": 25.0,
                                "ma20": 24.0,
                                "ma60": 23.0,
                                "range_pos_60": 0.8,
                                "pct_change_1d": 0.2,
                                "volume_ratio_20": 1.2,
                                "regime_flags": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            strategy_a = tmp_path / "strategy_a.toml"
            strategy_b = tmp_path / "strategy_b.toml"
            strategy_a.write_text('strategy_id = "a"\nstrategy_version = "a1"\nstatus = "active"\n[weights]\ntrend_weight = 0.60\nmomentum_weight = 0.20\nrange_weight = 0.20\nrisk_penalty_weight = 1.00\n', encoding="utf-8")
            strategy_b.write_text('strategy_id = "b"\nstrategy_version = "b1"\nstatus = "candidate"\n[weights]\ntrend_weight = 0.20\nmomentum_weight = 0.60\nrange_weight = 0.20\nrisk_penalty_weight = 1.00\n', encoding="utf-8")
            out_a = tmp_path / "out_a.json"
            out_b = tmp_path / "out_b.json"

            for strategy, output in ((strategy_a, out_a), (strategy_b, out_b)):
                argv = ["rank", "--snapshot", str(snapshot), "--output", str(output), "--strategy-config", str(strategy)]
                with mock.patch.object(sys, "argv", argv):
                    self.assertEqual(ranker.main(), 0)

            data_a = json.loads(out_a.read_text(encoding="utf-8"))
            data_b = json.loads(out_b.read_text(encoding="utf-8"))
            self.assertNotEqual(data_a["all_ranked"][0]["score"], data_b["all_ranked"][0]["score"])
            self.assertEqual(data_a["strategy_id"], "a")
            self.assertEqual(data_b["strategy_version"], "b1")
            self.assertIn("strategy_weights", data_a)

    def test_ranker_disqualifies_downtrend_low_volume_candidate(self):
        item = {
            "symbol": "WEAK.HK",
            "name": "Weak",
            "kind": "stock",
            "theme": "growth",
            "latest_close": 8.0,
            "ma20": 10.0,
            "ma60": 11.0,
            "range_pos_60": 0.05,
            "pct_change_1d": -1.0,
            "volume_ratio_20": 0.4,
            "regime_flags": ["downtrend"],
        }

        scored = ranker.item_score(item, ranker.DEFAULT_STRATEGY_WEIGHTS, min_watch_score=0)

        self.assertFalse(scored["qualified_for_watch"])
        self.assertIn("low_volume_ratio_20_below_0_6", scored["disqualifiers"])
        self.assertIn("downtrend_regime", scored["disqualifiers"])
        self.assertIn("range_pos_60_below_0_12", scored["disqualifiers"])
        self.assertIn("price_below_ma20_and_ma60", scored["disqualifiers"])

    def test_ranker_marks_same_theme_non_leaders_diagnostic_only(self):
        leader = ranker.item_score(
            {"symbol": "AAA.HK", "theme": "ai", "latest_close": 12.0, "ma20": 10.0, "ma60": 10.0, "range_pos_60": 0.8, "pct_change_1d": 1.0, "volume_ratio_20": 1.2, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        laggard = ranker.item_score(
            {"symbol": "BBB.HK", "theme": "ai", "latest_close": 11.0, "ma20": 10.0, "ma60": 10.0, "range_pos_60": 0.3, "pct_change_1d": 0.0, "volume_ratio_20": 1.0, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )

        annotated = sorted(ranker.annotate_theme_positions([leader, laggard]), key=lambda row: row["theme_rank"])

        self.assertTrue(annotated[0]["is_theme_leader"])
        self.assertTrue(annotated[0]["same_theme_peer_evidence_passed"])
        self.assertEqual(annotated[0]["same_theme_best_symbol"], "AAA.HK")
        self.assertEqual(annotated[0]["peer_relative_decision"], "theme_leader")
        self.assertFalse(annotated[1]["qualified_for_watch"])
        self.assertTrue(annotated[1]["diagnostic_only"])
        self.assertFalse(annotated[1]["same_theme_peer_evidence_passed"])
        self.assertEqual(annotated[1]["peer_relative_decision"], "blocked_by_same_theme_leader")
        self.assertIn("not_theme_score_leader", annotated[1]["disqualifiers"])

    def test_symbol_risk_veto_blocks_action_qualification(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 12.0, "ma20": 10.0, "ma60": 10.0, "range_pos_60": 0.9, "pct_change_1d": 2.0, "volume_ratio_20": 1.5, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_action_qualification(ranked, 0, {"0700.HK": {"action_veto": True, "reasons": ["test veto"], "tags": ["low_symbol_pass_rate"]}})

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("symbol_risk_veto", ranked[0]["disqualifiers"])
        self.assertTrue(ranked[0]["diagnostic_only"])

    def test_recent_symbol_adverse_breach_blocks_action_but_not_watch(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, 0, {"0700.HK": {"action_veto": False, "reasons": ["test adverse"], "tags": ["recent_symbol_adverse_breach"]}})

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("symbol_recent_adverse_breach", ranked[0]["action_disqualifiers"])
        self.assertNotIn("symbol_recent_adverse_breach", ranked[0]["disqualifiers"])
        self.assertTrue(ranked[0]["diagnostic_only"])

    def test_ranker_adds_edge_fields_and_cost_gate_blocks_action(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 12.0, "ma20": 10.0, "ma60": 10.0, "range_pos_60": 0.9, "pct_change_1d": 2.0, "volume_ratio_20": 1.5, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=35, minimum_edge_bps=500)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        row = ranked[0]
        self.assertIn("expected_edge_bps", row)
        self.assertIn("net_expected_edge_bps", row)
        self.assertEqual(row["edge_method"], "technical_snapshot_score_v1")
        self.assertEqual(row["evidence_window"], "1d_momentum_20d_volume_20d_60d_trend_60d_range")
        self.assertFalse(row["cost_gate_passed"])
        self.assertFalse(row["qualified_for_action"])
        self.assertIn("cost_gate_failed", row["disqualifiers"])

    def test_ranker_cost_gate_can_pass_for_strong_candidate(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["cost_gate_passed"])
        self.assertTrue(ranked[0]["qualified_for_action"])
        self.assertIn("same_theme_best_peer_evidence_passed", ranked[0]["qualification_flags"])

    def test_focus_pool_prioritizes_configured_industries_and_symbols(self):
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-05-20",
            "as_of_session": "close",
            "all_ranked": [
                {
                    "symbol": "AAA.HK",
                    "name": "AAA",
                    "theme": "internet-platform",
                    "kind": "stock",
                    "score": 82.0,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": True,
                    "volume_ratio_20": 1.6,
                    "disqualifiers": [],
                    "action_disqualifiers": [],
                },
                {
                    "symbol": "BBB.HK",
                    "name": "BBB",
                    "theme": "healthcare-biotech",
                    "kind": "stock",
                    "score": 58.0,
                    "qualified_for_action": False,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": False,
                    "volume_ratio_20": 1.1,
                    "disqualifiers": [],
                    "action_disqualifiers": ["cost_gate_failed"],
                },
                {"symbol": "CCC.HK", "theme": "energy", "kind": "stock", "score": 90.0, "qualified_for_action": True, "qualified_for_watch": True, "diagnostic_only": False, "volume_ratio_20": 2.0},
            ],
        }
        config = {
            "policy": {"max_active_industries": 2, "max_active_symbols_per_industry": 2, "min_active_industry_score": 40, "min_watch_industry_score": 20, "min_focus_symbol_score": 0},
            "industries": [
                {"id": "technology", "name": "科技", "strategic_weight": 1.1, "themes": ["internet-platform"], "leader_symbols": ["AAA.HK"], "high_beta_symbols": [], "confirming_symbols": []},
                {"id": "healthcare", "name": "医疗", "strategic_weight": 1.0, "themes": ["healthcare-biotech"], "leader_symbols": ["BBB.HK"], "high_beta_symbols": [], "confirming_symbols": []},
            ],
        }

        result = focus_pool.rank_industries(ranking, config)

        self.assertEqual(result["active_focus_industries"][0], "technology")
        self.assertEqual(result["active_focus_symbols"][0]["symbol"], "AAA.HK")
        self.assertEqual(result["active_focus_symbols"][0]["focus_role"], "leader")
        self.assertEqual(result["active_focus_symbols"][0]["focus_state"], "actionable")
        self.assertNotIn("CCC.HK", {row["symbol"] for row in result["active_focus_symbols"]})

    def test_focus_pool_keeps_watch_industry_leaders_observable(self):
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-05-20",
            "as_of_session": "close",
            "all_ranked": [
                {"symbol": "300750.SZ", "name": "CATL", "theme": "china-a-battery-ev", "kind": "stock", "score": 56.0, "qualified_for_action": False, "qualified_for_watch": True, "diagnostic_only": True, "cost_gate_passed": False, "volume_ratio_20": 0.92, "disqualifiers": ["cost_gate_failed"], "action_disqualifiers": ["volume_ratio_20_below_1_0"]},
                {"symbol": "515790.SH", "name": "PV ETF", "theme": "china-a-renewable-energy", "kind": "etf", "score": 2.0, "qualified_for_action": False, "qualified_for_watch": False, "diagnostic_only": True, "cost_gate_passed": False, "volume_ratio_20": 1.4, "disqualifiers": ["downtrend_regime"], "action_disqualifiers": []},
            ],
        }
        config = {
            "policy": {"max_active_industries": 2, "max_active_symbols_per_industry": 2, "max_watch_symbols_per_industry": 2, "min_active_industry_score": 90, "min_watch_industry_score": 20, "min_focus_symbol_score": 0},
            "industries": [
                {"id": "new_energy", "name": "新能源", "strategic_weight": 1.0, "themes": ["china-a-battery-ev", "china-a-renewable-energy"], "leader_symbols": ["300750.SZ"], "high_beta_symbols": [], "confirming_symbols": ["515790.SH"]},
            ],
        }

        result = focus_pool.rank_industries(ranking, config)

        self.assertEqual(result["watch_focus_industries"], ["new_energy"])
        self.assertEqual(result["watch_focus_symbols"][0]["symbol"], "300750.SZ")
        self.assertEqual(result["watch_focus_symbols"][0]["focus_state"], "watch_only")

    def test_draft_calls_include_focus_pool_fields_when_available(self):
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-05-20",
            "as_of_session": "close",
            "all_ranked": [
                {
                    "symbol": "300750.SZ",
                    "theme": "china-a-battery-ev",
                    "kind": "stock",
                    "score": 56.0,
                    "qualified_for_action": False,
                    "qualified_for_watch": True,
                    "diagnostic_only": True,
                    "cost_gate_passed": False,
                    "same_theme_peer_evidence_passed": True,
                    "action_disqualifiers": ["volume_ratio_20_below_1_0"],
                    "disqualifiers": ["cost_gate_failed"],
                }
            ],
            "actionable_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "internet-platform",
                    "kind": "stock",
                    "score": 82.0,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": True,
                    "same_theme_peer_evidence_passed": True,
                    "action_disqualifiers": [],
                    "disqualifiers": [],
                }
            ],
            "diagnostic_candidates": [],
        }
        focus = {
            "active_focus_industries": ["technology"],
            "watch_focus_industries": ["new_energy"],
            "active_focus_symbols": [
                {
                    "symbol": "AAA.HK",
                    "focus_industry": "technology",
                    "focus_industry_name": "科技",
                    "focus_industry_score": 76.5,
                    "focus_industry_rank": 1,
                    "focus_role": "leader",
                    "focus_state": "actionable",
                }
            ],
            "watch_focus_symbols": [
                {
                    "symbol": "300750.SZ",
                    "focus_industry": "new_energy",
                    "focus_industry_name": "新能源",
                    "focus_industry_score": 48.0,
                    "focus_industry_rank": 3,
                    "focus_role": "leader",
                    "focus_state": "watch_only",
                }
            ],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=True, focus_pool=focus)
        rec = calls["recommendations"][0]
        by_symbol = {item["symbol"]: item for item in calls["recommendations"]}

        self.assertEqual(rec["focus_industry"], "technology")
        self.assertEqual(rec["focus_industry_rank"], 1)
        self.assertIn("focus_industry=technology", rec["selection_reason"])
        self.assertTrue(any("focus_industry=technology" in item for item in rec["evidence"]))
        self.assertEqual(by_symbol["300750.SZ"]["focus_industry"], "new_energy")
        self.assertEqual(by_symbol["300750.SZ"]["state"], "watch_only")

    def test_nontechnical_evidence_required_blocks_action_when_missing(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        evidence = {"policy": {"require_for_action": True, "max_staleness_days": 30, "min_total_score_for_action": 0.55}, "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS, "symbols": {}}

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertEqual(ranked[0]["nontechnical_evidence"]["status"], "missing")
        self.assertIn("nontechnical_evidence_missing", ranked[0]["action_disqualifiers"])

    def test_nontechnical_evidence_allows_action_when_fresh_and_positive(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        evidence = {
            "policy": {"require_for_action": True, "max_staleness_days": 30, "min_total_score_for_action": 0.55, "block_unknown_event_risk": True},
            "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS,
            "symbols": {
                "0700.HK": {
                    "as_of_date": "2026-05-13",
                    "fundamental_score": 0.7,
                    "valuation_score": 0.6,
                    "catalyst_score": 0.65,
                    "flow_score": 0.6,
                    "macro_score": 0.55,
                    "event_risk": "none",
                    "source_count": 3,
                }
            },
        }

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertTrue(ranked[0]["qualified_for_action"])
        self.assertIn("nontechnical_evidence_gate_clear", ranked[0]["qualification_flags"])
        self.assertGreaterEqual(ranked[0]["nontechnical_evidence"]["total_score"], 0.55)

    def test_nontechnical_evidence_blocks_stale_or_event_risk(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        evidence = {
            "policy": {"require_for_action": True, "max_staleness_days": 10, "min_total_score_for_action": 0.55},
            "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS,
            "symbols": {"0700.HK": {"as_of_date": "2026-04-01", "fundamental_score": 0.9, "valuation_score": 0.9, "catalyst_score": 0.9, "flow_score": 0.9, "macro_score": 0.9, "event_risk": "regulatory", "source_count": 2}},
        }

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("nontechnical_evidence_stale", ranked[0]["action_disqualifiers"])
        self.assertIn("event_risk_regulatory", ranked[0]["action_disqualifiers"])

    def test_nontechnical_evidence_blocks_missing_component_and_future_session(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        ranked[0]["snapshot_as_of_session"] = "morning"
        evidence = {
            "policy": {"require_for_action": True, "max_staleness_days": 30, "min_total_score_for_action": 0.55, "block_unknown_event_risk": True},
            "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS,
            "symbols": {
                "0700.HK": {
                    "as_of_date": "2026-05-13",
                    "as_of_session": "close",
                    "fundamental_score": 0.7,
                    "valuation_score": 0.6,
                    "catalyst_score": 0.65,
                    "flow_score": 0.6,
                    "event_risk": "none",
                    "source_count": 3,
                }
            },
        }

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("nontechnical_component_missing", ranked[0]["action_disqualifiers"])
        self.assertIn("nontechnical_evidence_from_future_session", ranked[0]["action_disqualifiers"])

    def test_nontechnical_evidence_builder_outputs_missing_fail_closed_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "nontechnical.toml"
            config.write_text(
                """
[policy]
require_for_action = true
max_staleness_days = 30
min_total_score_for_action = 0.55
block_unknown_event_risk = true

[weights]
fundamental_score = 0.30
valuation_score = 0.20
catalyst_score = 0.25
flow_score = 0.15
macro_score = 0.10

[[evidence]]
symbol = "AAA.HK"
as_of_date = "2026-04-27"
fundamental_score = 0.70
valuation_score = 0.60
catalyst_score = 0.65
flow_score = 0.60
macro_score = 0.55
event_risk = "none"
source_count = 2
""".lstrip(),
                encoding="utf-8",
            )
            universe = tmp_path / "universe.toml"
            universe.write_text(
                """
[[symbols]]
symbol = "AAA.HK"
name = "AAA"
kind = "stock"
theme = "growth"

[[symbols]]
symbol = "BBB.HK"
name = "BBB"
kind = "stock"
theme = "defensive"
""".lstrip(),
                encoding="utf-8",
            )

            payload = nontechnical_builder.build_evidence(config, "2026-04-27", universe)

            self.assertTrue(payload["research_only"])
            self.assertTrue(payload["no_execution"])
            self.assertEqual(payload["symbols"]["AAA.HK"]["evidence_mode"], "curated_point_in_time")
            self.assertEqual(payload["symbols"]["BBB.HK"]["evidence_mode"], "missing_fail_closed")
            self.assertEqual(payload["summary"]["available_count"], 1)
            self.assertEqual(payload["summary"]["missing_count"], 1)
            self.assertGreater(payload["summary"]["blocking_finding_count"], 0)

    def test_nontechnical_evidence_builder_can_auto_generate_proxy_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "nontechnical.toml"
            config.write_text(
                """
[policy]
require_for_action = true
max_staleness_days = 30
min_total_score_for_action = 0.55
block_unknown_event_risk = true

[automatic_proxy]
enabled = true
max_total_score = 0.62
min_source_count = 3
allow_action_for_etfs = true
allow_action_for_defensive_liquid_stocks = true
""".lstrip(),
                encoding="utf-8",
            )
            universe = tmp_path / "universe.toml"
            universe.write_text(
                """
[[symbols]]
symbol = "2800.HK"
name = "ETF"
kind = "etf"
theme = "hong-kong-broad-market"
""".lstrip(),
                encoding="utf-8",
            )
            snapshot = tmp_path / "snapshot.json"
            snapshot.write_text(
                json.dumps(
                    {
                        "as_of_date": "2026-04-27",
                        "market_summary": {"risk_state": "neutral", "avg_stock_move_1d": 0.1, "avg_etf_move_1d": 0.2},
                        "items": [
                            {
                                "symbol": "2800.HK",
                                "name": "ETF",
                                "kind": "etf",
                                "theme": "hong-kong-broad-market",
                                "quote_trade_date": "2026-04-27",
                                "range_pos_60": 0.5,
                                "volume_ratio_20": 1.3,
                                "turnover": 2_000_000_000,
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            payload = nontechnical_builder.build_evidence(config, "2026-04-27", universe, snapshot, as_of_session="close")

            row = payload["symbols"]["2800.HK"]
            self.assertEqual(row["evidence_mode"], "automatic_local_proxy")
            self.assertTrue(row["proxy_only"])
            self.assertEqual(row["event_risk"], "none")
            self.assertEqual(row["source_count"], 0)
            self.assertGreaterEqual(row["proxy_source_count"], 3)
            self.assertGreaterEqual(row["total_score"], 0.55)
            self.assertEqual(payload["summary"]["automatic_proxy_count"], 1)
            self.assertEqual(payload["summary"]["proxy_only_count"], 1)
            self.assertEqual(payload["summary"]["available_count"], 0)
            self.assertEqual(payload["summary"]["curated_available_count"], 0)
            self.assertEqual(payload["summary"]["actionable_evidence_count"], 0)
            self.assertEqual(payload["summary"]["coverage_ratio"], 0.0)
            self.assertEqual(payload["summary"]["proxy_coverage_ratio"], 1.0)
            reasons = {finding["reason"] for finding in payload["findings"]}
            self.assertIn("nontechnical_proxy_only", reasons)

    def test_nontechnical_evidence_builder_can_generate_formal_provider_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "nontechnical.toml"
            config.write_text(
                """
[policy]
require_for_action = true
max_staleness_days = 30
min_total_score_for_action = 0.55
block_unknown_event_risk = true

[formal_provider]
enabled = true
current_date_only = false
""".lstrip(),
                encoding="utf-8",
            )
            universe = tmp_path / "universe.toml"
            universe.write_text(
                """
[[symbols]]
symbol = "600519.SH"
name = "Kweichow Moutai / 贵州茅台"
kind = "stock"
theme = "china-a-consumer-staples"
""".lstrip(),
                encoding="utf-8",
            )
            snapshot = tmp_path / "snapshot.json"
            snapshot.write_text(
                json.dumps(
                    {
                        "as_of_date": "2026-05-16",
                        "market_summary": {"risk_state": "neutral"},
                        "items": [{"symbol": "600519.SH", "turnover": 2_000_000_000, "volume_ratio_20": 1.3}],
                    }
                ),
                encoding="utf-8",
            )
            finance_row = {
                "REPORT_DATE": "2026-03-31 00:00:00",
                "NOTICE_DATE": "2026-04-25 00:00:00",
                "TOTALOPERATEREVETZ": 10.0,
                "PARENTNETPROFITTZ": 12.0,
                "ROEJQ": 15.0,
                "ZCFZL": 30.0,
                "JYXJLYYSR": 0.4,
                "XSJLL": 30.0,
            }

            with mock.patch.object(nontechnical_builder, "fetch_json", return_value={"data": [finance_row]}):
                payload = nontechnical_builder.build_evidence(config, "2026-05-16", universe, snapshot, as_of_session="close")

            row = payload["symbols"]["600519.SH"]
            self.assertEqual(row["evidence_mode"], "formal_provider_point_in_time")
            self.assertFalse(row["proxy_only"])
            self.assertEqual(row["as_of_date"], "2026-04-25")
            self.assertEqual(row["source_count"], 1)
            self.assertGreaterEqual(row["total_score"], 0.55)
            self.assertEqual(payload["summary"]["formal_provider_count"], 1)
            self.assertEqual(payload["summary"]["available_count"], 1)
            self.assertEqual(payload["summary"]["proxy_only_count"], 0)
            reasons = {finding["reason"] for finding in payload["findings"]}
            self.assertNotIn("nontechnical_proxy_only", reasons)

    def test_nontechnical_evidence_builder_pads_hk_codes_for_formal_provider(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "nontechnical.toml"
            config.write_text(
                """
[formal_provider]
enabled = true
current_date_only = false
""".lstrip(),
                encoding="utf-8",
            )
            universe = tmp_path / "universe.toml"
            universe.write_text(
                """
[[symbols]]
symbol = "0700.HK"
name = "Tencent / 腾讯控股"
kind = "stock"
theme = "consumer-tech"
""".lstrip(),
                encoding="utf-8",
            )
            finance_row = {
                "REPORT_DATE": "2026-03-31 00:00:00",
                "OPERATE_INCOME_QOQ": 6.0,
                "HOLDER_PROFIT_QOQ": 8.0,
                "ROE_AVG": 10.0,
                "NET_PROFIT_RATIO": 25.0,
                "PE_TTM": 18.0,
                "PB_TTM": 3.2,
                "DIVIDEND_RATE": 2.1,
            }

            with mock.patch.object(nontechnical_builder, "fetch_json", return_value={"result": {"data": [finance_row]}}) as fetch_json:
                payload = nontechnical_builder.build_evidence(config, "2026-05-16", universe, as_of_session="close")

            row = payload["symbols"]["0700.HK"]
            self.assertEqual(row["evidence_mode"], "formal_provider_point_in_time")
            self.assertFalse(row["proxy_only"])
            self.assertEqual(row["source_count"], 1)
            self.assertIn('SECUCODE="00700.HK"', fetch_json.call_args.args[1]["filter"])

    def test_nontechnical_evidence_builder_does_not_live_fetch_historical_dates(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "nontechnical.toml"
            config.write_text(
                """
[formal_provider]
enabled = true
current_date_only = true
""".lstrip(),
                encoding="utf-8",
            )
            universe = tmp_path / "universe.toml"
            universe.write_text(
                """
[[symbols]]
symbol = "600519.SH"
name = "Kweichow Moutai / 贵州茅台"
kind = "stock"
theme = "china-a-consumer-staples"
""".lstrip(),
                encoding="utf-8",
            )

            with mock.patch.object(nontechnical_builder, "fetch_json") as fetch_json:
                payload = nontechnical_builder.build_evidence(config, "2026-04-27", universe)

            fetch_json.assert_not_called()
            self.assertEqual(payload["symbols"]["600519.SH"]["evidence_mode"], "missing_fail_closed")
            self.assertEqual(payload["summary"].get("formal_provider_count"), 0)

    def test_ranker_blocks_action_for_proxy_only_nontechnical_evidence(self):
        item = ranker.item_score(
            {"symbol": "2800.HK", "theme": "broad-market", "kind": "etf", "latest_close": 28.0, "ma20": 25.0, "ma60": 24.0, "range_pos_60": 0.6, "pct_change_1d": 1.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        evidence = {
            "policy": {"require_for_action": True, "max_staleness_days": 30, "min_total_score_for_action": 0.55, "block_unknown_event_risk": True},
            "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS,
            "symbols": {
                "2800.HK": {
                    "evidence_mode": "automatic_local_proxy",
                    "proxy_only": True,
                    "as_of_date": "2026-05-13",
                    "fundamental_score": 0.9,
                    "valuation_score": 0.9,
                    "catalyst_score": 0.9,
                    "flow_score": 0.9,
                    "macro_score": 0.9,
                    "event_risk": "none",
                    "source_count": 3,
                    "sources": [{"label": "proxy"}, {"label": "metadata"}, {"label": "snapshot"}],
                }
            },
        }

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertEqual(ranked[0]["nontechnical_evidence"]["status"], "proxy_only")
        self.assertEqual(ranked[0]["nontechnical_evidence"]["source_count"], 0)
        self.assertIn("nontechnical_proxy_only", ranked[0]["action_disqualifiers"])
        self.assertIn("nontechnical_evidence_gate_blocked", ranked[0]["qualification_flags"])

    def test_ranker_treats_generated_missing_nontechnical_row_as_missing(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-13"
        evidence = {
            "policy": {"require_for_action": True, "max_staleness_days": 30, "min_total_score_for_action": 0.55},
            "weights": ranker.DEFAULT_NONTECHNICAL_WEIGHTS,
            "symbols": {"0700.HK": {"evidence_mode": "missing_fail_closed", "as_of_date": None}},
        }

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={}, nontechnical_evidence=evidence)

        self.assertEqual(ranked[0]["nontechnical_evidence"]["status"], "missing")
        self.assertIn("nontechnical_evidence_missing", ranked[0]["action_disqualifiers"])

    def test_nontechnical_attribution_uses_only_point_in_time_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            calls_dir = tmp_path / "calls"
            snapshot_dir = tmp_path / "snapshots"
            shadow_dir = tmp_path / "shadow"
            calls_dir.mkdir()
            snapshot_dir.mkdir()
            shadow_dir.mkdir()
            self.write_trade_snapshot(snapshot_dir / "2026-04-01.json", "2026-04-01", 10.0, 10.0)
            self.write_trade_snapshot(snapshot_dir / "2026-04-04.json", "2026-04-04", 11.0, 9.0)
            (calls_dir / "2026-04-01-calls.json").write_text(
                json.dumps(
                    {
                        "date": "2026-04-01",
                        "session": "close",
                        "recommendations": [self.valid_call("AAA.HK", "buy_candidate"), self.valid_call("BBB.HK", "buy_candidate")],
                    }
                ),
                encoding="utf-8",
            )
            evidence_path = tmp_path / "nontechnical.json"
            evidence_path.write_text(
                json.dumps(
                    {
                        "as_of_date": "2026-04-01",
                        "symbols": {
                            "AAA.HK": {"as_of_date": "2026-04-01", "total_score": 0.7, "fundamental_score": 0.7, "valuation_score": 0.7, "catalyst_score": 0.7, "flow_score": 0.7, "macro_score": 0.7, "event_risk": "none", "source_count": 2},
                            "BBB.HK": {"as_of_date": "2026-04-02", "total_score": 0.7, "fundamental_score": 0.7, "valuation_score": 0.7, "catalyst_score": 0.7, "flow_score": 0.7, "macro_score": 0.7, "event_risk": "none", "source_count": 2},
                        },
                    }
                ),
                encoding="utf-8",
            )

            result = nontechnical_eval.build_attribution(
                evidence_path,
                calls_dir,
                snapshot_dir,
                shadow_dir,
                tmp_path / "missing-registry.json",
                nontechnical_eval.dt.date(2026, 4, 4),
                "close",
                min_bucket_samples=1,
            )

            self.assertEqual(result["summary"]["outcome_count"], 2)
            self.assertEqual(result["summary"]["attributed_sample_count"], 1)
            self.assertEqual(result["records"][0]["symbol"], "AAA.HK")
            self.assertEqual(result["skipped_records"][0]["symbol"], "BBB.HK")

    def test_nontechnical_attribution_rejects_same_day_future_session_evidence(self):
        evidence = {
            "as_of_date": "2026-04-01",
            "as_of_session": "close",
            "symbols": {
                "AAA.HK": {"total_score": 0.7, "event_risk": "none", "source_count": 2, "fundamental_score": 0.7, "valuation_score": 0.7, "catalyst_score": 0.7, "flow_score": 0.7, "macro_score": 0.7}
            },
        }

        row = nontechnical_eval.evidence_for_symbol(evidence, "AAA.HK", nontechnical_eval.dt.date(2026, 4, 1), "morning")

        self.assertIsNone(row)

    def test_ranker_requires_volume_confirmation_for_action_not_watch(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 0.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("volume_ratio_20_below_1_0", ranked[0]["action_disqualifiers"])
        self.assertNotIn("volume_ratio_20_below_1_0", ranked[0]["disqualifiers"])

    def test_ranker_blocks_action_when_market_proxy_is_overextended(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        snapshot = {"items": [{"symbol": "2800.HK", "range_pos_60": 0.85, "pct_change_1d": 1.0, "volume_ratio_20": 1.2}]}
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_market_context(ranked, snapshot, max_market_range_for_action=0.7)
        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertEqual(ranked[0]["market_proxy_symbol"], "2800.HK")
        self.assertIn("market_range_pos_60_above_action_limit", ranked[0]["action_disqualifiers"])

    def test_ranker_uses_cn_market_proxy_for_a_share_candidates(self):
        item = ranker.item_score(
            {"symbol": "600519.SH", "theme": "consumer-staples", "latest_close": 1400.0, "ma20": 1300.0, "ma60": 1250.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        snapshot = {
            "items": [
                {"symbol": "2800.HK", "range_pos_60": 0.2, "pct_change_1d": 0.0, "volume_ratio_20": 1.0},
                {"symbol": "510300.SH", "range_pos_60": 0.85, "pct_change_1d": 1.0, "volume_ratio_20": 1.2},
            ]
        }
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_market_context(ranked, snapshot, max_market_range_for_action=0.7)
        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertEqual(ranked[0]["market_proxy_symbol"], "510300.SH")
        self.assertIn("market_range_pos_60_above_action_limit", ranked[0]["action_disqualifiers"])

    def test_hk_quote_trade_date_mismatch_blocks_action_not_watch(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "kind": "stock", "latest_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 2.0, "volume_ratio_20": 1.8, "regime_flags": [], "price_source": "quote", "quote_trade_date": "2026-05-13"},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranked[0]["snapshot_as_of_date"] = "2026-05-14"

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("quote_trade_date_mismatch", ranked[0]["action_disqualifiers"])
        self.assertNotIn("quote_trade_date_mismatch", ranked[0]["disqualifiers"])

    def test_hk_zero_volume_unchanged_quote_blocks_action(self):
        item = ranker.item_score(
            {"symbol": "0700.HK", "theme": "internet", "kind": "stock", "latest_close": 14.0, "prev_close": 14.0, "ma20": 10.0, "ma60": 9.0, "range_pos_60": 0.7, "pct_change_1d": 0.0, "volume_ratio_20": 1.8, "regime_flags": [], "price_source": "quote", "quote_volume": 0, "latest_volume": 0},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_watch"])
        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertIn("hk_halt_or_no_turnover_suspected", ranked[0]["action_disqualifiers"])

    def test_cn_limit_board_moves_block_action(self):
        cases = [
            (9.5, "cn_limit_up_chase_block"),
            (-9.5, "cn_limit_down_liquidity_block"),
        ]
        for pct_change, expected_disqualifier in cases:
            item = ranker.item_score(
                {"symbol": "600519.SH", "theme": "consumer-staples", "kind": "stock", "latest_close": 1400.0, "ma20": 1300.0, "ma60": 1250.0, "range_pos_60": 0.7, "pct_change_1d": pct_change, "volume_ratio_20": 1.8, "regime_flags": []},
                ranker.DEFAULT_STRATEGY_WEIGHTS,
                min_watch_score=0,
            )
            ranked = ranker.annotate_theme_positions([item])

            ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
            ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

            self.assertTrue(ranked[0]["qualified_for_watch"])
            self.assertFalse(ranked[0]["qualified_for_action"])
            self.assertIn(expected_disqualifier, ranked[0]["action_disqualifiers"])

    def test_cn_limit_board_gate_does_not_block_etfs(self):
        item = ranker.item_score(
            {"symbol": "510300.SH", "theme": "broad", "kind": "etf", "latest_close": 5.0, "ma20": 4.7, "ma60": 4.5, "range_pos_60": 0.7, "pct_change_1d": 9.5, "volume_ratio_20": 1.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])

        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_action"])
        self.assertNotIn("cn_limit_up_chase_block", ranked[0]["action_disqualifiers"])

    def test_backtest_experimental_risk_filter_downgrades_overheated_action_row(self):
        item = ranker.item_score(
            {"symbol": "600519.SH", "theme": "consumer-staples", "latest_close": 1400.0, "ma20": 1300.0, "ma60": 1250.0, "range_pos_60": 0.9, "pct_change_1d": 6.0, "volume_ratio_20": 2.8, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranker.apply_market_context(ranked, {"items": [{"symbol": "510300.SH", "range_pos_60": 0.6, "pct_change_1d": 0.5, "volume_ratio_20": 1.2}]})
        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_action"])

        backtester.apply_experimental_risk_filter(ranked, "combined_heat")

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertTrue(ranked[0]["diagnostic_only"])
        self.assertEqual(ranked[0]["experimental_risk_filter_profile"], "combined_heat")
        self.assertIn("experimental_pct_change_1d_gte_5", ranked[0]["action_disqualifiers"])
        self.assertIn("experimental_volume_ratio_20_gte_2_5_and_range_pos_60_gte_0_85", ranked[0]["action_disqualifiers"])

    def test_backtest_experimental_risk_filter_downgrades_high_range_market_stall(self):
        item = ranker.item_score(
            {"symbol": "600519.SH", "theme": "consumer-staples", "latest_close": 1400.0, "ma20": 1300.0, "ma60": 1250.0, "range_pos_60": 0.95, "pct_change_1d": 1.0, "volume_ratio_20": 1.4, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = ranker.annotate_theme_positions([item])
        ranker.apply_market_context(ranked, {"items": [{"symbol": "510300.SH", "range_pos_60": 0.6, "pct_change_1d": 0.5, "volume_ratio_20": 1.2}]})
        ranker.apply_edge_cost_fields(ranked, round_trip_bps=10, minimum_edge_bps=20)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        self.assertTrue(ranked[0]["qualified_for_action"])

        backtester.apply_experimental_risk_filter(ranked, "market_stall")

        self.assertFalse(ranked[0]["qualified_for_action"])
        self.assertTrue(ranked[0]["diagnostic_only"])
        self.assertIn("experimental_range_pos_60_gte_0_88_market_range_pos_60_gte_0_55_pct_change_1d_lte_1_5", ranked[0]["action_disqualifiers"])

    def test_shadow_log_downgrades_candidate_without_mutating_production_ranking(self):
        row = {
            "symbol": "600519.SH",
            "name": "Kweichow Moutai",
            "kind": "stock",
            "theme": "consumer-staples",
            "score": 80.0,
            "qualified_for_watch": True,
            "qualified_for_action": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "latest_close": 100.0,
            "range_pos_60": 0.95,
            "pct_change_1d": 1.0,
            "volume_ratio_20": 1.4,
            "market_proxy_symbol": "510300.SH",
            "market_range_pos_60": 0.6,
            "max_market_range_for_action": 0.7,
            "same_theme_peer_evidence_passed": True,
            "qualification_flags": [],
            "disqualifiers": [],
            "action_disqualifiers": [],
        }
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-04-01",
            "session": "close",
            "strategy_id": "test_strategy",
            "strategy_version": "test_strategy",
            "strategy_status": "active",
            "thresholds": {"actionable_top_n": 1, "diagnostic_top_n": 1},
            "actionable_candidates": [row],
            "diagnostic_candidates": [row],
            "all_ranked": [row],
        }

        result = shadow_log.build_shadow_log(ranking, risk_filter="market_stall", stop_loss_pct=-4.0, horizon_days=14)

        self.assertTrue(result["shadow_policy"]["no_execution"])
        self.assertTrue(result["shadow_policy"]["production_ranking_unchanged"])
        self.assertEqual(result["summary"]["production_actionable_count"], 1)
        self.assertEqual(result["summary"]["shadow_actionable_count"], 0)
        self.assertEqual(result["summary"]["downgraded_by_shadow_filter_count"], 1)
        self.assertTrue(ranking["all_ranked"][0]["qualified_for_action"])
        self.assertIn("experimental_range_pos_60_gte_0_88_market_range_pos_60_gte_0_55_pct_change_1d_lte_1_5", result["downgraded_by_shadow_filter"][0]["action_disqualifiers"])

    def test_shadow_log_keeps_monitoring_fields_for_actionable_candidate(self):
        row = {
            "symbol": "0700.HK",
            "name": "Tencent",
            "kind": "stock",
            "theme": "internet-platform",
            "score": 82.0,
            "qualified_for_watch": True,
            "qualified_for_action": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "latest_close": 10.0,
            "range_pos_60": 0.72,
            "pct_change_1d": 1.2,
            "volume_ratio_20": 1.6,
            "market_proxy_symbol": "2800.HK",
            "market_range_pos_60": 0.3,
            "same_theme_peer_evidence_passed": True,
            "qualification_flags": [],
            "disqualifiers": [],
            "action_disqualifiers": [],
        }
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-04-01",
            "session": "close",
            "thresholds": {"actionable_top_n": 1, "diagnostic_top_n": 1},
            "actionable_candidates": [row],
            "diagnostic_candidates": [row],
            "all_ranked": [row],
        }

        result = shadow_log.build_shadow_log(ranking, risk_filter="off", stop_loss_pct=-4.0, horizon_days=14)

        self.assertEqual(result["summary"]["shadow_actionable_count"], 1)
        candidate = result["shadow_actionable_candidates"][0]
        self.assertEqual(candidate["symbol"], "0700.HK")
        self.assertEqual(candidate["daily_close_stop_price"], 9.6)
        self.assertEqual(candidate["benchmark_symbol"], "2800.HK")
        self.assertEqual(candidate["planned_horizon_days"], 14)

    def test_shadow_log_marks_historical_replay_as_not_forward_evidence(self):
        ranking = {
            "snapshot": "data/snapshots/test.json",
            "as_of_date": "2026-04-01",
            "session": "historical",
            "thresholds": {"actionable_top_n": 1, "diagnostic_top_n": 1},
            "actionable_candidates": [],
            "diagnostic_candidates": [],
            "all_ranked": [],
        }

        result = shadow_log.build_shadow_log(ranking, evidence_mode="historical_replay")

        self.assertEqual(result["evidence_mode"], "historical_replay")
        self.assertFalse(result["counts_toward_forward_evidence"])
        self.assertFalse(result["shadow_policy"]["counts_toward_forward_evidence"])

    def test_shadow_backfill_writes_historical_replay_logs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            rankings_dir = tmp_path / "rankings"
            output_dir = tmp_path / "shadow"
            rankings_dir.mkdir()
            ranking = {
                "snapshot": str(tmp_path / "snapshot.json"),
                "as_of_date": "2026-04-01",
                "session": "close",
                "thresholds": {"actionable_top_n": 1, "diagnostic_top_n": 1},
                "actionable_candidates": [],
                "diagnostic_candidates": [],
                "all_ranked": [],
            }
            (rankings_dir / "2026-04-01-close-ranking.json").write_text(json.dumps(ranking), encoding="utf-8")
            (rankings_dir / "2026-04-02-close-ranking.json").write_text(json.dumps({**ranking, "as_of_date": "2026-04-02"}), encoding="utf-8")

            rows = shadow_backfill.discover_rankings(rankings_dir, limit=1)
            result = shadow_backfill.build_replay_logs(rows, output_dir, "off", "daily_close_stop", -4.0, 14, overwrite=False)

            self.assertEqual(result["written_count"], 1)
            payload = json.loads(pathlib.Path(result["written"][0]).read_text(encoding="utf-8"))
            self.assertEqual(payload["evidence_mode"], "historical_replay")
            self.assertFalse(payload["counts_toward_forward_evidence"])
            self.assertEqual(payload["date"], "2026-04-02")

    def test_shadow_forward_evaluator_ignores_replay_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-02.json", "2026-04-02", 9.5, 25.2)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-15.json", "2026-04-15", 12.0, 26.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-02", "2026-04-15"])
            candidate = {
                "symbol": "AAA.HK",
                "market_family": "hk",
                "theme": "growth",
                "latest_close": 10.0,
                "stop_loss_pct": -4.0,
                "benchmark_symbol": "2800.HK",
            }
            base_log = {
                "date": "2026-04-01",
                "session": "close",
                "mode": "shadow_logging",
                "shadow_policy": {"horizon_days": 14},
                "shadow_actionable_candidates": [candidate],
            }
            (shadow_dir / "2026-04-01-close-shadow.json").write_text(
                json.dumps({**base_log, "evidence_mode": "forward_shadow", "counts_toward_forward_evidence": True}),
                encoding="utf-8",
            )
            (shadow_dir / "2026-04-01-historical-shadow.json").write_text(
                json.dumps({**base_log, "evidence_mode": "historical_replay", "counts_toward_forward_evidence": False}),
                encoding="utf-8",
            )

            result = shadow_eval.build_evaluation(shadow_dir, registry, include_replay=False, round_trip_bps=0, min_forward_shadow_days=1)

            self.assertEqual(result["summary"]["forward_shadow_log_count"], 1)
            self.assertEqual(result["summary"]["historical_replay_log_count"], 1)
            self.assertEqual(result["summary"]["sample_count"], 1)
            self.assertEqual(result["records"][0]["future_date"], "2026-04-02")
            self.assertTrue(result["records"][0]["exit_triggered"])
            self.assertEqual(result["records"][0]["net_return_pct"], -5.0)
            self.assertTrue(result["records"][0]["counts_toward_forward_evidence"])

    def test_shadow_forward_evaluator_blocks_until_twenty_forward_days(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-15.json", "2026-04-15", 11.0, 26.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-15"])
            log = {
                "date": "2026-04-01",
                "session": "close",
                "mode": "shadow_logging",
                "evidence_mode": "forward_shadow",
                "counts_toward_forward_evidence": True,
                "shadow_policy": {"horizon_days": 14},
                "shadow_actionable_candidates": [{"symbol": "AAA.HK", "market_family": "hk", "theme": "growth", "latest_close": 10.0, "stop_loss_pct": -4.0}],
            }
            (shadow_dir / "2026-04-01-close-shadow.json").write_text(json.dumps(log), encoding="utf-8")

            result = shadow_eval.build_evaluation(shadow_dir, registry, include_replay=False, round_trip_bps=0, min_forward_shadow_days=20)

            metrics = {finding["metric"] for finding in result["gate"]["findings"]}
            self.assertFalse(result["gate"]["passed"])
            self.assertIn("forward_shadow_days", metrics)
            self.assertIn("matured_forward_shadow_days", metrics)

    def test_shadow_forward_evaluator_respects_as_of_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-15.json", "2026-04-15", 11.0, 26.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-15"])
            log = {
                "date": "2026-04-01",
                "session": "close",
                "mode": "shadow_logging",
                "evidence_mode": "forward_shadow",
                "counts_toward_forward_evidence": True,
                "shadow_policy": {"horizon_days": 14},
                "shadow_actionable_candidates": [{"symbol": "AAA.HK", "market_family": "hk", "theme": "growth", "latest_close": 10.0, "stop_loss_pct": -4.0}],
            }
            (shadow_dir / "2026-04-01-close-shadow.json").write_text(json.dumps(log), encoding="utf-8")

            result = shadow_eval.build_evaluation(shadow_dir, registry, include_replay=False, round_trip_bps=0, min_forward_shadow_days=1, as_of_date=call_eval.parse_date("2026-04-10"))

            self.assertEqual(result["summary"]["sample_count"], 0)
            self.assertEqual(result["summary"]["pending_sample_count"], 1)
            self.assertEqual(result["pending_records"][0]["reason"], "future_horizon_not_available")

    def test_shadow_forward_evaluator_skips_shadow_logs_after_as_of_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(tmp_path / "trade-2026-04-15.json", "2026-04-15", 11.0, 26.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-15"])
            future_log = {
                "date": "2026-04-15",
                "session": "close",
                "mode": "shadow_logging",
                "evidence_mode": "forward_shadow",
                "counts_toward_forward_evidence": True,
                "shadow_policy": {"horizon_days": 14},
                "shadow_actionable_candidates": [{"symbol": "AAA.HK", "market_family": "hk", "theme": "growth", "latest_close": 11.0, "stop_loss_pct": -4.0}],
            }
            (shadow_dir / "2026-04-15-close-shadow.json").write_text(json.dumps(future_log), encoding="utf-8")

            result = shadow_eval.build_evaluation(shadow_dir, registry, include_replay=False, round_trip_bps=0, min_forward_shadow_days=1, as_of_date=call_eval.parse_date("2026-04-10"))

            self.assertEqual(result["summary"]["forward_shadow_log_count"], 0)
            self.assertEqual(result["summary"]["evaluated_log_count"], 0)
            self.assertEqual(result["summary"]["sample_count"], 0)
            self.assertEqual(result["skipped_logs"][0]["reason"], "shadow_date_after_as_of")

    def test_shadow_variant_config_validates_default_and_rejects_bad_variants(self):
        default = shadow_variants.load_variant_config(ROOT / "config" / "shadow_variants.toml")
        self.assertEqual(default["competition_id"], "shadow_gate_variants_v1")
        self.assertGreaterEqual(len(default["variants"]), 1)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            duplicate = tmp_path / "duplicate.toml"
            duplicate.write_text(
                """
competition_id = "test_competition"

[[variant]]
id = "dup"
risk_filter = "off"
exit_rule = "daily_close_stop"
stop_loss_pct = -4.0

[[variant]]
id = "dup"
risk_filter = "market_stall"
exit_rule = "daily_close_stop"
stop_loss_pct = -4.0
""".lstrip(),
                encoding="utf-8",
            )
            invalid_risk = tmp_path / "invalid-risk.toml"
            invalid_risk.write_text(
                """
[[variant]]
id = "bad_risk"
risk_filter = "not_a_filter"
exit_rule = "daily_close_stop"
stop_loss_pct = -4.0
""".lstrip(),
                encoding="utf-8",
            )
            positive_stop = tmp_path / "positive-stop.toml"
            positive_stop.write_text(
                """
[[variant]]
id = "bad_stop"
risk_filter = "off"
exit_rule = "daily_close_stop"
stop_loss_pct = 1.0
""".lstrip(),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "duplicate variant ids"):
                shadow_variants.load_variant_config(duplicate)
            with self.assertRaisesRegex(ValueError, "invalid risk_filter"):
                shadow_variants.load_variant_config(invalid_risk)
            with self.assertRaisesRegex(ValueError, "stop_loss_pct must be negative"):
                shadow_variants.load_variant_config(positive_stop)

    def test_shadow_variant_competition_writes_logs_without_mutating_ranking(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            config = tmp_path / "shadow_variants.toml"
            config.write_text(
                """
enabled = true
competition_id = "test_competition"

[[variant]]
id = "baseline"
label = "Baseline"
risk_filter = "off"
exit_rule = "daily_close_stop"
stop_loss_pct = -4.0
horizon_days = 14

[[variant]]
id = "market_stall"
label = "Market stall"
risk_filter = "market_stall"
exit_rule = "daily_close_stop"
stop_loss_pct = -4.0
horizon_days = 14
""".lstrip(),
                encoding="utf-8",
            )
            ranking_path = tmp_path / "ranking.json"
            ranking_path.write_text(json.dumps(self.shadow_variant_ranking()), encoding="utf-8")
            before = ranking_path.read_bytes()
            snapshot_path = tmp_path / "snapshot.json"
            snapshot_path.write_text(json.dumps({"as_of_date": "2026-04-01", "items": []}), encoding="utf-8")
            registry = tmp_path / "registry.json"
            registry.write_text(json.dumps({"entries": []}), encoding="utf-8")
            output_dir = tmp_path / "research" / "shadow_variants"

            result = shadow_variants.run_competition(
                config,
                ranking_path,
                snapshot_path,
                registry,
                output_dir,
                None,
                None,
                "forward_shadow",
                call_eval.parse_date("2026-04-01"),
                0,
            )

            logs_dir = output_dir / "test_competition" / "logs"
            log_files = sorted(logs_dir.glob("*-shadow.json"))
            self.assertEqual(len(log_files), 2)
            self.assertEqual(len(result["written_logs"]), 2)
            self.assertEqual(result["policy"]["mode"], "shadow_variant_competition")
            self.assertTrue(result["policy"]["no_execution"])
            self.assertTrue(result["policy"]["no_portfolio_mutation"])
            self.assertTrue(result["policy"]["production_ranking_unchanged"])
            self.assertFalse(result["policy"]["counts_toward_forward_evidence"])
            self.assertEqual(ranking_path.read_bytes(), before)
            for path in log_files:
                self.assertEqual(path.parent, logs_dir)
                payload = json.loads(path.read_text(encoding="utf-8"))
                policy = payload["shadow_policy"]
                self.assertEqual(payload["mode"], "shadow_variant_competition")
                self.assertTrue(policy["no_execution"])
                self.assertTrue(policy["no_portfolio_mutation"])
                self.assertTrue(policy["production_ranking_unchanged"])
                self.assertFalse(payload["counts_toward_forward_evidence"])
                self.assertFalse(policy["counts_toward_forward_evidence"])

    def test_shadow_evaluator_normal_directory_ignores_variant_logs_elsewhere(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "research" / "shadow"
            shadow_dir.mkdir(parents=True)
            variant_dir = tmp_path / "research" / "shadow_variants" / "competition" / "logs"
            variant_dir.mkdir(parents=True)
            normal_log = {"date": "2026-04-01", "session": "close", "mode": "shadow_logging", "shadow_actionable_candidates": []}
            variant_log = {"date": "2026-04-01", "session": "close", "mode": "shadow_variant_competition", "shadow_actionable_candidates": []}
            (shadow_dir / "2026-04-01-close-shadow.json").write_text(json.dumps(normal_log), encoding="utf-8")
            (variant_dir / "2026-04-01-close-v1-shadow.json").write_text(json.dumps(variant_log), encoding="utf-8")

            logs = shadow_eval.load_shadow_logs(shadow_dir)

            self.assertEqual(len(logs), 1)
            self.assertEqual(logs[0][0].parent, shadow_dir)
            self.assertEqual(logs[0][1]["mode"], "shadow_logging")

    def test_shadow_variant_scoreboard_respects_as_of_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            registry = tmp_path / "registry.json"
            registry.write_text(json.dumps({"entries": []}), encoding="utf-8")

            def variant_log(date):
                return {
                    "date": date,
                    "session": "close",
                    "mode": "shadow_variant_competition",
                    "evidence_mode": "forward_shadow",
                    "shadow_policy": {
                        "variant_id": "v1",
                        "variant_label": "Variant 1",
                        "competition_id": "test_competition",
                        "risk_filter": "off",
                        "exit_rule": "daily_close_stop",
                        "stop_loss_pct": -4.0,
                        "horizon_days": 14,
                        "no_execution": True,
                        "no_portfolio_mutation": True,
                        "production_ranking_unchanged": True,
                    },
                    "shadow_actionable_candidates": [],
                }

            logs = [
                (tmp_path / "2026-04-01-close-v1-shadow.json", variant_log("2026-04-01")),
                (tmp_path / "2026-05-01-close-v1-shadow.json", variant_log("2026-05-01")),
            ]

            scoreboard, skipped = shadow_variants.summarize_variant_logs(logs, registry, call_eval.parse_date("2026-04-10"), 0)

            self.assertEqual(len(scoreboard), 1)
            self.assertEqual(scoreboard[0]["variant_id"], "v1")
            self.assertEqual(scoreboard[0]["log_count"], 1)
            self.assertEqual(scoreboard[0]["forward_like_log_count"], 1)
            self.assertTrue(any(item["reason"] == "shadow_date_after_as_of" for item in skipped))

    def test_evidence_ledger_audits_forward_shadow_sources_and_excludes_replay_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            snapshot_path = tmp_path / "trade-2026-04-01.json"
            future_path = tmp_path / "trade-2026-04-15.json"
            self.write_trade_snapshot(snapshot_path, "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(future_path, "2026-04-15", 11.0, 26.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-15"])
            ranking_path = tmp_path / "ranking.json"
            ranking_path.write_text("{}", encoding="utf-8")
            candidate = {"symbol": "AAA.HK", "market_family": "hk", "theme": "growth", "latest_close": 10.0, "stop_loss_pct": -4.0, "benchmark_symbol": "2800.HK", "score": 70.0, "planned_horizon_days": 14}
            source = {
                "ranking": {"path": str(ranking_path), "exists": True, "sha256": "rankhash", "size_bytes": 2},
                "snapshot": {"path": str(snapshot_path), "exists": True, "sha256": "snaphash", "size_bytes": 2},
            }
            base_log = {
                "date": "2026-04-01",
                "session": "close",
                "generated_at": "2026-04-01T00:00:00Z",
                "mode": "shadow_logging",
                "shadow_policy": {"no_execution": True, "no_portfolio_mutation": True, "production_ranking_unchanged": True, "horizon_days": 14},
                "source": source,
                "shadow_actionable_candidates": [candidate],
            }
            (shadow_dir / "2026-04-01-close-shadow.json").write_text(json.dumps({**base_log, "evidence_mode": "forward_shadow", "counts_toward_forward_evidence": True}), encoding="utf-8")
            (shadow_dir / "2026-04-01-historical-shadow.json").write_text(json.dumps({**base_log, "evidence_mode": "historical_replay", "counts_toward_forward_evidence": False}), encoding="utf-8")

            result = evidence_ledger.build_ledger(shadow_dir, registry, include_replay=False, round_trip_bps=0, min_forward_shadow_days=1)

            self.assertTrue(result["audit_passed"])
            self.assertEqual(result["summary"]["forward_shadow_log_count"], 1)
            self.assertEqual(result["summary"]["historical_replay_log_count"], 1)
            self.assertEqual(result["summary"]["candidate_entry_count"], 1)
            self.assertEqual(result["candidate_entries"][0]["symbol"], "AAA.HK")
            self.assertEqual(result["candidate_entries"][0]["outcome_status"], "matured")

    def test_evidence_ledger_flags_replay_counting_as_forward(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01"])
            log = {
                "date": "2026-04-01",
                "session": "historical",
                "generated_at": "2026-04-01T00:00:00Z",
                "mode": "shadow_logging",
                "evidence_mode": "historical_replay",
                "counts_toward_forward_evidence": True,
                "shadow_policy": {"no_execution": True, "no_portfolio_mutation": True, "production_ranking_unchanged": True},
                "source": {},
                "shadow_actionable_candidates": [],
            }
            (shadow_dir / "2026-04-01-historical-shadow.json").write_text(json.dumps(log), encoding="utf-8")

            result = evidence_ledger.build_ledger(shadow_dir, registry)

            self.assertFalse(result["audit_passed"])
            fields = {finding["field"] for finding in result["audit_findings"]}
            self.assertIn("counts_toward_forward_evidence", fields)

    def test_evidence_ledger_flags_historical_session_marked_forward(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            shadow_dir = tmp_path / "shadow"
            shadow_dir.mkdir()
            self.write_trade_snapshot(tmp_path / "trade-2026-04-01.json", "2026-04-01", 10.0, 25.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01"])
            log = {
                "date": "2026-04-01",
                "session": "historical",
                "generated_at": "2026-04-01T00:00:00Z",
                "mode": "shadow_logging",
                "evidence_mode": "forward_shadow",
                "counts_toward_forward_evidence": True,
                "shadow_policy": {"no_execution": True, "no_portfolio_mutation": True, "production_ranking_unchanged": True},
                "source": {
                    "as_of_date": "2026-04-01",
                    "ranking": {"exists": True, "sha256": "rankhash"},
                    "snapshot": {"exists": True, "sha256": "snaphash"},
                },
                "shadow_actionable_candidates": [],
            }
            (shadow_dir / "2026-04-01-historical-shadow.json").write_text(json.dumps(log), encoding="utf-8")

            result = evidence_ledger.build_ledger(shadow_dir, registry)

            self.assertFalse(result["audit_passed"])
            fields = {finding["field"] for finding in result["audit_findings"]}
            self.assertIn("session", fields)

    def test_calibration_scorecard_reports_confidence_buckets_and_low_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            calls_dir = tmp_path / "calls"
            snapshot_dir = tmp_path / "snapshots"
            shadow_dir = tmp_path / "shadow"
            calls_dir.mkdir()
            snapshot_dir.mkdir()
            shadow_dir.mkdir()
            self.write_trade_snapshot(snapshot_dir / "2026-04-01.json", "2026-04-01", 10.0, 25.0)
            self.write_trade_snapshot(snapshot_dir / "2026-04-04.json", "2026-04-04", 11.0, 25.0)
            registry = self.write_trade_registry(tmp_path, ["2026-04-01", "2026-04-04"])
            call = self.valid_call("AAA.HK", "buy_candidate")
            call["confidence"] = 0.75
            (calls_dir / "2026-04-01-close-calls.json").write_text(json.dumps({"date": "2026-04-01", "session": "close", "recommendations": [call]}), encoding="utf-8")

            result = calibration_scorecard.build_scorecard(
                calls_dir,
                snapshot_dir,
                shadow_dir,
                registry,
                close_windows=[3],
                intraday_windows=[0],
                min_total_samples=2,
                min_bucket_samples=2,
            )

            self.assertEqual(result["overall"]["scored_sample_count"], 1)
            self.assertTrue(result["overall"]["low_sample"])
            bucket = next(item for item in result["confidence_buckets"] if item["bucket"] == "0.70-0.85")
            self.assertEqual(bucket["scored_sample_count"], 1)
            self.assertEqual(bucket["hit_rate"], 1.0)
            self.assertTrue(bucket["low_sample"])
            self.assertTrue(any(finding["metric"] == "scored_sample_count" for finding in result["findings"]))

    def test_calibration_scorecard_ignores_success_without_confidence_for_scored_samples(self):
        rows = [{"success": 1.0, "confidence": None, "return_pct": 2.0}]

        result = calibration_scorecard.overall_stats(rows, min_total_samples=1)

        self.assertEqual(result["sample_count"], 1)
        self.assertEqual(result["scored_sample_count"], 0)
        self.assertIsNone(result["hit_rate"])
        self.assertTrue(result["low_sample"])

    def test_daily_shadow_runner_plans_forward_pipeline_without_bash(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            snapshot = tmp_path / "data" / "snapshots" / "2026-04-27.json"
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(json.dumps({"as_of_date": "2026-04-27", "items": []}), encoding="utf-8")
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            summary = daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="close",
                    skip_fetch=True,
                    skip_radar_fetch=True,
                ),
                runner=fake_runner,
            )

            self.assertEqual([name for name, *_ in calls], ["build_snapshot_registry", "build_nontechnical_evidence", "rank_universe", "generate_focus_pool", "build_draft_calls", "build_risk_review", "validate_draft_calls", "log_shadow", "evaluate_shadow", "build_evidence_ledger", "build_calibration_scorecard", "evaluate_nontechnical_attribution", "run_shadow_variants", "build_investment_dashboard"])
            self.assertTrue(all(command[0] == "python" for _, command, *_ in calls))
            self.assertFalse(any("bash" in part.lower() for _, command, *_ in calls for part in command))
            shadow_command = next(command for name, command, *_ in calls if name == "log_shadow")
            self.assertEqual(shadow_command[shadow_command.index("--evidence-mode") + 1], "forward_shadow")
            eval_command = next(command for name, command, *_ in calls if name == "evaluate_shadow")
            self.assertEqual(eval_command[eval_command.index("--as-of-date") + 1], "2026-04-27")
            ledger_command = next(command for name, command, *_ in calls if name == "build_evidence_ledger")
            self.assertEqual(ledger_command[ledger_command.index("--as-of-date") + 1], "2026-04-27")
            scorecard_command = next(command for name, command, *_ in calls if name == "build_calibration_scorecard")
            self.assertEqual(scorecard_command[scorecard_command.index("--as-of-date") + 1], "2026-04-27")
            self.assertEqual(scorecard_command[scorecard_command.index("--as-of-session") + 1], "close")
            rank_command = next(command for name, command, *_ in calls if name == "rank_universe")
            self.assertEqual(rank_command[rank_command.index("--actionable-top-n") + 1], "2")
            self.assertEqual(rank_command[rank_command.index("--diagnostic-top-n") + 1], "3")
            self.assertIn("--nontechnical-evidence", rank_command)
            self.assertTrue(rank_command[rank_command.index("--nontechnical-evidence") + 1].endswith("research\\evidence\\nontechnical\\latest.json") or rank_command[rank_command.index("--nontechnical-evidence") + 1].endswith("research/evidence/nontechnical/latest.json"))
            nontechnical_command = next(command for name, command, *_ in calls if name == "build_nontechnical_evidence")
            self.assertEqual(nontechnical_command[nontechnical_command.index("--as-of-date") + 1], "2026-04-27")
            attribution_command = next(command for name, command, *_ in calls if name == "evaluate_nontechnical_attribution")
            self.assertEqual(attribution_command[attribution_command.index("--as-of-date") + 1], "2026-04-27")
            self.assertEqual(attribution_command[attribution_command.index("--as-of-session") + 1], "close")
            draft_command = next(command for name, command, *_ in calls if name == "build_draft_calls")
            self.assertIn("--focus-pool", draft_command)
            self.assertIn("--include-diagnostics", draft_command)
            risk_command = next(command for name, command, *_ in calls if name == "build_risk_review")
            self.assertTrue(risk_command[risk_command.index("--draft-calls") + 1].endswith("2026-04-27-close-draft-policy.json"))
            variant_command = next(command for name, command, *_ in calls if name == "run_shadow_variants")
            self.assertEqual(variant_command[variant_command.index("--evidence-mode") + 1], "forward_shadow")
            self.assertEqual(variant_command[variant_command.index("--as-of-date") + 1], "2026-04-27")
            dashboard_command = next(command for name, command, *_ in calls if name == "build_investment_dashboard")
            self.assertIn("--close-report-json", dashboard_command)
            self.assertIn("--ranking", dashboard_command)
            self.assertTrue(dashboard_command[dashboard_command.index("--output") + 1].endswith("research\\dashboard\\index.html") or dashboard_command[dashboard_command.index("--output") + 1].endswith("research/dashboard/index.html"))
            self.assertEqual(summary["paths"]["ranking"], str(tmp_path.resolve() / "research" / "rankings" / "2026-04-27-close-ranking.json"))
            self.assertEqual(summary["paths"]["dashboard"], str(tmp_path.resolve() / "research" / "dashboard" / "index.html"))

    def test_daily_shadow_runner_refreshes_live_snapshots_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            snapshot = tmp_path / "data" / "snapshots" / "2026-04-27.json"
            radar_snapshot = tmp_path / "data" / "snapshots" / "2026-04-27-radar.json"
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(json.dumps({"as_of_date": "2026-04-27", "items": []}), encoding="utf-8")
            radar_snapshot.write_text(json.dumps({"as_of_date": "2026-04-27", "items": []}), encoding="utf-8")
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="close",
                ),
                runner=fake_runner,
            )

            names = [name for name, *_ in calls]
            self.assertIn("fetch_trade_snapshot", names)
            self.assertIn("fetch_radar_snapshot", names)

    def test_daily_shadow_runner_reuses_historical_snapshot_by_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            snapshot = tmp_path / "data" / "snapshots" / "2026-04-27.json"
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(json.dumps({"as_of_date": "2026-04-27", "items": []}), encoding="utf-8")
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="historical",
                    evaluate_shadow=False,
                ),
                runner=fake_runner,
            )

            names = [name for name, *_ in calls]
            self.assertNotIn("fetch_trade_snapshot", names)

    def test_investment_evolve_refreshes_live_llm_outputs_by_default(self):
        text = (ROOT / "scripts" / "evolve_investment.sh").read_text(encoding="utf-8")

        self.assertIn('SKIP_EXISTING_OUTPUTS="${SKIP_EXISTING_OUTPUTS:-}"', text)
        self.assertIn('if [ "$SESSION" = "historical" ]; then\n        SKIP_EXISTING_OUTPUTS="true"\n    else\n        SKIP_EXISTING_OUTPUTS="false"', text)

    def test_investment_dashboard_builds_static_html_from_fixture_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            close_json = tmp_path / "close-report.json"
            close_md = tmp_path / "close-report.md"
            ranking_json = tmp_path / "ranking.json"
            nontechnical_json = tmp_path / "nontechnical.json"
            forward_json = tmp_path / "forward.json"
            ledger_json = tmp_path / "ledger.json"
            output = tmp_path / "dashboard" / "index.html"

            close_json.write_text(
                json.dumps(
                    {
                        "date": "2026-04-27",
                        "session": "close",
                        "recommendations": [
                            {"symbol": "AAA.HK", "state": "buy_candidate", "confidence": 0.71},
                            {"symbol": "BBB.HK", "state": "watch_only", "confidence": 0.43},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            close_md.write_text("# Report\n\n## Final Result\n- markdown fallback headline\n", encoding="utf-8")
            ranking_json.write_text(
                json.dumps(
                    {
                        "as_of_date": "2026-04-27",
                        "session": "close",
                        "all_ranked": [
                            {
                                "symbol": "AAA.HK",
                                "name": "Alpha Co / 阿尔法",
                                "score": 82.5,
                                "qualified_for_action": True,
                                "qualified_for_watch": True,
                                "action_disqualifiers": [],
                                "quote_trade_date": "2026-04-27",
                                "nontechnical_evidence": {"status": "available", "total_score": 0.74, "event_risk": "low", "source_count": 2},
                            },
                            {
                                "symbol": "BBB.HK",
                                "name": "Beta Co",
                                "score": 61.0,
                                "qualified_for_action": False,
                                "qualified_for_watch": True,
                                "action_disqualifiers": ["quote_trade_date_mismatch", "event_risk_quote_stale", "nontechnical_proxy_only"],
                                "quote_trade_date": "2026-04-26",
                                "nontechnical_evidence": {"status": "proxy_only", "proxy_only": True, "total_score": 0.58, "event_risk": "unknown", "proxy_source_count": 3},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            nontechnical_json.write_text(
                json.dumps(
                    {
                        "summary": {"curated_available_count": 1, "proxy_only_count": 1, "missing_count": 0},
                        "symbols": {
                            "AAA.HK": {"evidence_mode": "curated_point_in_time", "proxy_only": False, "total_score": 0.74, "event_risk": "low", "source_count": 2},
                            "BBB.HK": {"evidence_mode": "automatic_local_proxy", "proxy_only": True, "total_score": 0.58, "event_risk": "unknown", "proxy_source_count": 3},
                        },
                    }
                ),
                encoding="utf-8",
            )
            forward_json.write_text(json.dumps({"summary": {"forward_shadow_log_count": 5, "matured_forward_shadow_days": 3, "sample_count": 2}}), encoding="utf-8")
            ledger_json.write_text(json.dumps({"summary": {"forward_shadow_log_count": 6}, "shadow_evaluation_summary": {"matured_forward_shadow_days": 4, "sample_count": 3}}), encoding="utf-8")

            result = investment_dashboard.build_dashboard("2026-04-27", "close", close_json, close_md, ranking_json, nontechnical_json, forward_json, ledger_json, output)

            html_text = output.read_text(encoding="utf-8")
            self.assertEqual(result["payload"]["counts"], {"action": 1, "watch": 1, "avoid": 0})
            self.assertIn("仅供研究 · 非交易信号 · 不构成投资建议", html_text)
            self.assertIn("id=\"symbolSearch\"", html_text)
            self.assertIn("当前前向胜率", html_text)
            self.assertIn("最新执行时间", html_text)
            self.assertIn("generated_at_hkt", result["payload"])
            self.assertIn("行情快照日期", html_text)
            self.assertIn("行情实际交易日", html_text)
            self.assertIn("本次分析有 1 个标的使用非报告日行情", html_text)
            self.assertEqual(result["payload"]["snapshot"]["as_of_date"], "2026-04-27")
            self.assertEqual(result["payload"]["snapshot"]["latest_quote_trade_date"], "2026-04-27")
            self.assertEqual(result["payload"]["snapshot"]["quote_date_mismatch_count"], 1)
            self.assertIn("data-filter=\"consider\"", html_text)
            self.assertIn("data-filter=\"confirm\"", html_text)
            self.assertIn("data-filter=\"observe\"", html_text)
            self.assertIn("data-filter=\"avoid\"", html_text)
            self.assertIn("成本/边际不足", html_text)
            self.assertIn("正式资料未接入", html_text)
            self.assertIn("行情日期不匹配", html_text)
            self.assertIn("行情日期滞后", html_text)
            self.assertIn("搜索代码、名称、建议或障碍项", html_text)
            self.assertIn('"symbol": "AAA.HK"', html_text)
            self.assertIn('"symbol": "BBB.HK"', html_text)
            self.assertIn("正式资料未接入：尚未取得正式核验过", html_text)
            self.assertEqual(result["payload"]["symbols"][0]["research_action"]["label"], "可考虑研究")
            self.assertEqual(result["payload"]["symbols"][1]["research_action"]["label"], "等确认")
            self.assertEqual(result["payload"]["symbols"][0]["display_name"], "阿尔法")
            self.assertIn("行情日期不匹配", result["payload"]["symbols"][1]["blocker_labels"])
            self.assertIn("行情日期滞后", result["payload"]["symbols"][1]["blocker_labels"])
            self.assertIn('"category": "action"', html_text)
            self.assertIn('"category": "watch"', html_text)

    def test_dashboard_research_actions_do_not_promote_ranking_or_proxy_edges(self):
        rows = investment_dashboard.normalize_symbols(
            {
                "all_ranked": [
                    {
                        "symbol": "RANK.HK",
                        "name": "Ranking Only",
                        "score": 88,
                        "qualified_for_action": True,
                        "qualified_for_watch": True,
                        "action_disqualifiers": [],
                        "nontechnical_evidence": {"status": "available", "total_score": 0.8, "event_risk": "low", "source_count": 2},
                    },
                    {
                        "symbol": "PROXY.HK",
                        "name": "Proxy Text",
                        "score": 82,
                        "qualified_for_action": True,
                        "qualified_for_watch": True,
                        "action_disqualifiers": [],
                        "nontechnical_evidence": {"status": "available", "total_score": 0.8, "event_risk": "low", "source_count": 2},
                    },
                    {
                        "symbol": "CAPPED.HK",
                        "name": "Risk Capped",
                        "score": 83,
                        "qualified_for_action": True,
                        "qualified_for_watch": True,
                        "action_disqualifiers": [],
                        "nontechnical_evidence": {"status": "available", "total_score": 0.8, "event_risk": "low", "source_count": 2},
                    },
                ]
            },
            {
                "recommendations": [
                    {
                        "symbol": "PROXY.HK",
                        "state": "buy_candidate",
                        "confidence": 0.7,
                        "evidence": ["nontechnical_evidence status=proxy_only, flags=['nontechnical_proxy_only']"],
                    },
                    {"symbol": "CAPPED.HK", "state": "watch_only", "risk_cap": "watch_only", "confidence": 0.6},
                ]
            },
            {"symbols": {}},
        )

        labels = {row["symbol"]: row["research_action"]["label"] for row in rows}
        statuses = {row["symbol"]: row["nontechnical_evidence"]["status"] for row in rows}
        self.assertNotEqual(labels["RANK.HK"], "可考虑研究")
        self.assertNotEqual(labels["PROXY.HK"], "可考虑研究")
        self.assertNotEqual(labels["CAPPED.HK"], "可考虑研究")
        self.assertEqual(statuses["PROXY.HK"], "proxy_only")

    def test_close_report_research_action_treats_proxy_risk_as_formal_blocker(self):
        action = close_report.research_action_for(
            {
                "symbol": "AAA.HK",
                "state": "buy_candidate",
                "score": 86,
                "qualified_for_action": True,
                "qualified_for_watch": True,
                "gate_blockers": [],
                "blockers": ["nontechnical_proxy_only"],
                "nontechnical_profile": {"status": "available", "proxy_only": False, "event_risk": "low"},
            }
        )

        self.assertEqual(action["label"], "等确认")
        self.assertFalse(action["formal_actionable"])

    def test_daily_shadow_runner_plans_close_report_for_close_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            (tmp_path / "config" / "shadow_variants.toml").write_text('competition_id = "custom_competition"\n', encoding="utf-8")
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            summary = daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="close",
                    dry_run=True,
                ),
                runner=fake_runner,
            )

            names = [step["name"] for step in summary["steps"]]
            self.assertIn("run_shadow_variants", names)
            self.assertIn("build_chinese_close_report", names)
            self.assertIn("build_investment_dashboard", names)
            report_command = next(step["command"] for step in summary["steps"] if step["name"] == "build_chinese_close_report")
            self.assertEqual(report_command[report_command.index("--session") + 1], "close")
            self.assertIn("--nontechnical-evidence", report_command)
            self.assertIn("--nontechnical-attribution", report_command)
            variant_path = report_command[report_command.index("--variant-competition") + 1]
            self.assertEqual(variant_path, str(tmp_path.resolve() / "research" / "shadow_variants" / "custom_competition" / "latest_variant_competition.json"))
            self.assertNotIn("shadow_gate_variants_v1", variant_path)
            dashboard_command = next(step["command"] for step in summary["steps"] if step["name"] == "build_investment_dashboard")
            self.assertEqual(dashboard_command[dashboard_command.index("--session") + 1], "close")
            self.assertEqual(dashboard_command[dashboard_command.index("--close-report-json") + 1], str(tmp_path.resolve() / "research" / "products" / "daily_close" / "2026-04-27-close-report.json"))
            self.assertEqual(calls, [])

    def test_daily_shadow_runner_skip_dashboard_omits_dashboard_step(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)

            summary = daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="close",
                    build_dashboard=False,
                    dry_run=True,
                ),
                runner=lambda name, command, cwd, check=True: 0,
            )

            names = [step["name"] for step in summary["steps"]]
            self.assertNotIn("build_investment_dashboard", names)

    def test_daily_shadow_runner_skip_options_omit_variants_and_close_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            summary = daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="close",
                    run_variant_competition=False,
                    build_close_report=False,
                    build_dashboard=False,
                    dry_run=True,
                ),
                runner=fake_runner,
            )

            names = [step["name"] for step in summary["steps"]]
            self.assertNotIn("run_shadow_variants", names)
            self.assertNotIn("build_chinese_close_report", names)
            self.assertNotIn("build_investment_dashboard", names)
            self.assertEqual(calls, [])

    def test_daily_shadow_runner_uses_replay_mode_for_historical_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)
            snapshot = tmp_path / "data" / "snapshots" / "2026-04-27.json"
            snapshot.parent.mkdir(parents=True, exist_ok=True)
            snapshot.write_text(json.dumps({"as_of_date": "2026-04-27", "items": []}), encoding="utf-8")
            calls = []

            def fake_runner(name, command, cwd, check=True):
                calls.append((name, [str(part) for part in command], cwd, check))
                return 0

            summary = daily_shadow.run_pipeline(
                daily_shadow.DailyShadowOptions(
                    root=tmp_path,
                    python_bin="python",
                    date="2026-04-27",
                    session="historical",
                    skip_fetch=True,
                    evaluate_shadow=False,
                ),
                runner=fake_runner,
            )

            shadow_command = next(command for name, command, *_ in calls if name == "log_shadow")
            self.assertEqual(shadow_command[shadow_command.index("--evidence-mode") + 1], "historical_replay")
            self.assertEqual(summary["evidence_mode"], "historical_replay")
            self.assertEqual(summary["paths"]["shadow"], str(tmp_path.resolve() / "research" / "shadow" / "2026-04-27-shadow.json"))

    def test_daily_shadow_runner_requires_existing_snapshot_when_fetch_is_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            self.write_daily_shadow_configs(tmp_path)

            with self.assertRaises(SystemExit) as raised:
                daily_shadow.run_pipeline(
                    daily_shadow.DailyShadowOptions(
                        root=tmp_path,
                        python_bin="python",
                        date="2026-04-27",
                        session="close",
                        skip_fetch=True,
                    )
                )

            self.assertIn("Missing snapshot file", str(raised.exception))

    def test_ranker_emits_actionable_and_diagnostic_layers(self):
        strong = ranker.item_score(
            {"symbol": "AAA.HK", "theme": "ai", "latest_close": 14.0, "ma20": 10.0, "ma60": 10.0, "range_pos_60": 0.9, "pct_change_1d": 2.0, "volume_ratio_20": 1.5, "regime_flags": []},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        weak = ranker.item_score(
            {"symbol": "BBB.HK", "theme": "banks", "latest_close": 8.0, "ma20": 10.0, "ma60": 11.0, "range_pos_60": 0.05, "pct_change_1d": -1.0, "volume_ratio_20": 0.4, "regime_flags": ["downtrend"]},
            ranker.DEFAULT_STRATEGY_WEIGHTS,
            min_watch_score=0,
        )
        ranked = sorted(ranker.annotate_theme_positions([strong, weak]), key=lambda row: row["score"], reverse=True)
        ranker.apply_edge_cost_fields(ranked, round_trip_bps=0, minimum_edge_bps=0)
        ranker.apply_action_qualification(ranked, min_action_score=0, symbol_risk={})

        actionable, diagnostics, top = ranker.candidate_layers(ranked, actionable_top_n=1, diagnostic_top_n=2)

        self.assertEqual([row["symbol"] for row in actionable], ["AAA.HK"])
        self.assertEqual(len(diagnostics), 2)
        self.assertEqual(actionable[0]["source_layer"], "actionable_candidates")
        self.assertTrue(actionable[0]["eligible_for_action_from_layer"])
        self.assertEqual(diagnostics[0]["source_layer"], "diagnostic_candidates")
        self.assertFalse(diagnostics[0]["eligible_for_action_from_layer"])
        self.assertEqual(diagnostics[0]["layer_action_cap"], "watch_only")
        self.assertTrue(any(row["diagnostic_only"] for row in diagnostics))
        self.assertEqual(top[0]["symbol"], "AAA.HK")

    def test_run_manifest_hashes_existing_files_and_allows_missing_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            existing = tmp_path / "input.json"
            missing = tmp_path / "future.json"
            runs_root = tmp_path / "runs"
            existing.write_text("alpha", encoding="utf-8")
            args = mock.Mock(
                date="2026-04-27",
                session="morning",
                as_of_date=None,
                as_of_session=None,
                model="test-model",
                provider="test-provider",
                file=[("input", str(existing)), ("future_output", str(missing))],
            )

            manifest = run_manifest.build_manifest(args)
            argv = ["manifest", "--date", "2026-04-27", "--session", "morning", "--model", "test-model", "--provider", "test-provider", "--runs-root", str(runs_root), "--file", "input", str(existing), "--file", "future_output", str(missing)]
            with mock.patch.object(sys, "argv", argv):
                self.assertEqual(run_manifest.main(), 0)

            written = json.loads((runs_root / "2026-04-27-morning" / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["run_id"], "2026-04-27-morning")
            self.assertTrue(written["files"]["input"]["exists"])
            self.assertEqual(written["files"]["input"]["sha256"], "8ed3f6ad685b959ead7022518e1af76cd816f8e8ec7ccdda1ed4018e8f2223f8")
            self.assertFalse(written["files"]["future_output"]["exists"])
            self.assertIsNone(written["files"]["future_output"]["sha256"])

    def test_draft_calls_only_buy_when_qualified_and_cost_gate_passed(self):
        ranking = {
            "as_of_date": "2026-04-27",
            "as_of_session": "close",
            "actionable_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "growth",
                    "kind": "stock",
                    "score": 80,
                    "trend_score": 90,
                    "momentum_score": 70,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": True,
                    "expected_edge_bps": 160,
                    "net_expected_edge_bps": 125,
                    "theme_rank": 1,
                    "theme_leader": "AAA.HK",
                    "is_theme_leader": True,
                    "theme_peer_count": 2,
                    "same_theme_peer_evidence_passed": True,
                    "same_theme_best_symbol": "AAA.HK",
                    "same_theme_best_score": 80,
                    "same_theme_selected_vs_best_score_gap": 0.0,
                    "same_theme_next_best_symbol": "BBB.HK",
                    "same_theme_selected_vs_next_best_score_gap": 10.0,
                    "peer_relative_decision": "theme_leader",
                    "edge_method": "technical_snapshot_score_v1",
                    "evidence_window": "1d_momentum_20d_volume_20d_60d_trend_60d_range",
                }
            ],
            "diagnostic_candidates": [
                {
                    "symbol": "BBB.HK",
                    "theme": "defensive",
                    "kind": "stock",
                    "score": 50,
                    "trend_score": 55,
                    "momentum_score": 45,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": False,
                    "expected_edge_bps": 40,
                    "net_expected_edge_bps": 5,
                },
                {
                    "symbol": "CCC.HK",
                    "theme": "weak",
                    "kind": "stock",
                    "score": 10,
                    "trend_score": 5,
                    "momentum_score": 20,
                    "qualified_for_action": False,
                    "qualified_for_watch": False,
                    "diagnostic_only": True,
                    "cost_gate_passed": False,
                    "disqualifiers": ["downtrend_regime"],
                },
            ],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=True)
        states = {rec["symbol"]: rec["state"] for rec in calls["recommendations"]}

        self.assertEqual(states["AAA.HK"], "buy_candidate")
        self.assertEqual(states["BBB.HK"], "watch_only")
        self.assertEqual(states["CCC.HK"], "avoid")
        self.assertTrue(any("same_theme_peer_check" in item for item in calls["recommendations"][0]["evidence"]))
        self.assertTrue(any("same_theme_best_peer_evidence" in item for item in calls["recommendations"][0]["evidence"]))
        self.assertEqual(calls["recommendations"][0]["horizon_days_min"], 14)
        self.assertEqual(calls["recommendations"][0]["horizon_days_max"], 90)
        self.assertEqual(calls_validator.validate(calls, {**ranking, "all_ranked": ranking["actionable_candidates"] + ranking["diagnostic_candidates"]}, {"AAA.HK", "BBB.HK", "CCC.HK"}), [])

    def test_draft_calls_caps_diagnostics_at_watch_even_if_row_is_qualified(self):
        ranking = {
            "as_of_date": "2026-04-27",
            "actionable_candidates": [],
            "diagnostic_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "growth",
                    "kind": "stock",
                    "score": 80,
                    "trend_score": 90,
                    "momentum_score": 70,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": True,
                    "expected_edge_bps": 160,
                    "net_expected_edge_bps": 125,
                    "edge_method": "technical_snapshot_score_v1",
                    "evidence_window": "1d_momentum_20d_volume_20d_60d_trend_60d_range",
                }
            ],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=True)

        self.assertEqual(calls["recommendations"][0]["state"], "watch_only")
        self.assertIn("source_layer=diagnostic_candidates", calls["recommendations"][0]["selection_reason"])

    def test_draft_calls_require_same_theme_peer_evidence_for_buy_candidate(self):
        ranking = {
            "as_of_date": "2026-04-27",
            "actionable_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "growth",
                    "kind": "stock",
                    "score": 80,
                    "trend_score": 90,
                    "momentum_score": 70,
                    "qualified_for_action": True,
                    "qualified_for_watch": True,
                    "diagnostic_only": False,
                    "cost_gate_passed": True,
                    "expected_edge_bps": 160,
                    "net_expected_edge_bps": 125,
                    "same_theme_peer_evidence_passed": False,
                    "peer_relative_decision": "blocked_by_same_theme_leader",
                }
            ],
            "diagnostic_candidates": [],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=False)

        self.assertEqual(calls["recommendations"][0]["state"], "watch_only")
        self.assertIn("same_theme_best_peer_evidence_missing_or_failed", calls["recommendations"][0]["risks"])

    def test_draft_calls_surface_market_overextension_risk(self):
        ranking = {
            "as_of_date": "2026-04-27",
            "actionable_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "growth",
                    "kind": "stock",
                    "score": 80,
                    "trend_score": 90,
                    "momentum_score": 70,
                    "qualified_for_action": False,
                    "qualified_for_watch": True,
                    "diagnostic_only": True,
                    "cost_gate_passed": True,
                    "expected_edge_bps": 160,
                    "net_expected_edge_bps": 125,
                    "same_theme_peer_evidence_passed": True,
                    "market_proxy_symbol": "2800.HK",
                    "market_range_pos_60": 0.85,
                    "max_market_range_for_action": 0.7,
                }
            ],
            "diagnostic_candidates": [],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=False)

        self.assertEqual(calls["recommendations"][0]["state"], "watch_only")
        self.assertIn("market_range_pos_60_above_action_limit", calls["recommendations"][0]["risks"])
        self.assertTrue(any("market_context" in item for item in calls["recommendations"][0]["evidence"]))

    def test_draft_calls_surface_action_disqualifiers_in_risks(self):
        ranking = {
            "as_of_date": "2026-04-27",
            "actionable_candidates": [
                {
                    "symbol": "AAA.HK",
                    "theme": "growth",
                    "kind": "stock",
                    "score": 80,
                    "trend_score": 90,
                    "momentum_score": 70,
                    "qualified_for_action": False,
                    "qualified_for_watch": True,
                    "diagnostic_only": True,
                    "cost_gate_passed": True,
                    "expected_edge_bps": 160,
                    "net_expected_edge_bps": 125,
                    "same_theme_peer_evidence_passed": True,
                    "action_disqualifiers": ["hk_halt_or_no_turnover_suspected"],
                }
            ],
            "diagnostic_candidates": [],
        }

        calls = draft_calls.build_calls(ranking, include_diagnostics=False)

        self.assertEqual(calls["recommendations"][0]["state"], "watch_only")
        self.assertIn("hk_halt_or_no_turnover_suspected", calls["recommendations"][0]["risks"])

    def test_draft_calls_fail_closed_when_action_disqualifiers_conflict_with_actionable_row(self):
        row = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "kind": "stock",
            "score": 80,
            "trend_score": 90,
            "momentum_score": 70,
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "expected_edge_bps": 160,
            "net_expected_edge_bps": 125,
            "same_theme_peer_evidence_passed": True,
            "action_disqualifiers": ["quote_trade_date_mismatch"],
        }
        ranking = {"as_of_date": "2026-04-27", "actionable_candidates": [row], "diagnostic_candidates": []}

        calls = draft_calls.build_calls(ranking, include_diagnostics=False)

        self.assertEqual(calls["recommendations"][0]["state"], "watch_only")
        self.assertIn("quote_trade_date_mismatch", calls["recommendations"][0]["risks"])

    def test_draft_calls_calibrate_confidence_for_symbol_risk(self):
        clean = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "kind": "stock",
            "score": 80,
            "trend_score": 90,
            "momentum_score": 70,
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "expected_edge_bps": 160,
            "net_expected_edge_bps": 125,
            "same_theme_peer_evidence_passed": True,
            "same_theme_best_symbol": "AAA.HK",
            "same_theme_best_score": 80,
            "same_theme_selected_vs_best_score_gap": 0.0,
            "peer_relative_decision": "theme_leader",
        }
        risky = {
            **clean,
            "symbol": "BBB.HK",
            "same_theme_best_symbol": "BBB.HK",
            "symbol_risk": {"tags": ["low_symbol_pass_rate", "negative_symbol_avg_return", "repeated_symbol_selection_error"]},
        }
        ranking = {"as_of_date": "2026-04-27", "actionable_candidates": [clean, risky], "diagnostic_candidates": []}

        calls = draft_calls.build_calls(ranking, include_diagnostics=False)
        confidences = {rec["symbol"]: rec["confidence"] for rec in calls["recommendations"]}

        self.assertLess(confidences["BBB.HK"], confidences["AAA.HK"])
        self.assertTrue(any("confidence_calibration" in item for item in calls["recommendations"][1]["evidence"]))

    def test_calls_validator_rejects_final_state_upgrade_beyond_draft(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="accumulate")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft)

        self.assertTrue(any("upgrades beyond deterministic draft" in error for error in errors))

    def test_calls_validator_rejects_bullish_draft_flipped_to_trim(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft)

        self.assertTrue(any("upgrades beyond deterministic draft" in error for error in errors))

    def test_calls_validator_rejects_actionable_without_matching_draft(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": []}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft)

        self.assertTrue(any("matching deterministic draft call" in error for error in errors))

    def test_calls_validator_rejects_actionable_without_same_theme_peer_evidence(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "same_theme_peer_evidence_passed": False,
            "same_theme_best_symbol": "BBB.HK",
            "same_theme_selected_vs_best_score_gap": -5.0,
            "theme_rank": 2,
            "theme_leader": "BBB.HK",
            "is_theme_leader": False,
            "peer_relative_decision": "blocked_by_same_theme_leader",
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})

        self.assertTrue(any("same_theme_peer_evidence_passed=true" in error for error in errors))
        self.assertTrue(any("theme_rank=1" in error for error in errors))

    def test_calls_validator_rejects_actionable_when_market_proxy_is_overextended(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "market_range_pos_60": 0.85,
            "max_market_range_for_action": 0.7,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})

        self.assertTrue(any("market_range_pos_60 <= max_market_range_for_action" in error for error in errors))

    def test_calls_validator_rejects_actionable_with_action_disqualifiers(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "action_disqualifiers": ["quote_trade_date_mismatch"],
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call()]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"})

        self.assertTrue(any("actionable state requires empty action_disqualifiers" in error for error in errors))

    def test_calls_validator_rejects_confidence_above_draft_cap(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [{**self.valid_call(), "confidence": 0.72}]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [{**self.valid_call(), "confidence": 0.58}]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft)

        self.assertTrue(any("confidence exceeds deterministic draft confidence cap" in error for error in errors))

    def test_calls_validator_rejects_sell_state_without_matching_draft(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": []}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft)

        self.assertTrue(any("trim state requires matching deterministic draft call" in error for error in errors))

    def test_risk_review_passes_clean_buy_candidate(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "volume_ratio_20": 1.4,
            "regime_flags": [],
        }
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        review = risk_review.build_review(draft, self.ranking_with_row(row), {"risk": {"max_single_position_pct": 10}})
        verdict = review["verdicts"][0]

        self.assertFalse(review["policy"]["execution_allowed"])
        self.assertFalse(verdict["execution_allowed"])
        self.assertEqual(verdict["position_policy"], "recommendation_cap_only")
        self.assertEqual(verdict["risk_decision"], "pass")
        self.assertEqual(verdict["final_state_cap"], "buy_candidate")
        self.assertEqual(verdict["max_position_pct"], 10)

    def test_risk_review_downgrades_buy_candidate_on_weak_volume(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "volume_ratio_20": 0.8,
            "regime_flags": [],
        }
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        review = risk_review.build_review(draft, self.ranking_with_row(row), {"risk": {"max_single_position_pct": 10}})
        verdict = review["verdicts"][0]

        self.assertEqual(verdict["risk_decision"], "downgrade")
        self.assertEqual(verdict["final_state_cap"], "watch_only")
        self.assertLess(verdict["max_position_pct"], 10)
        self.assertIn("volume_ratio_20_below_1_0", verdict["risk_tags"])

    def test_risk_review_downgrades_buy_candidate_without_same_theme_peer_evidence(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "volume_ratio_20": 1.4,
            "regime_flags": [],
            "same_theme_peer_evidence_passed": False,
        }
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        review = risk_review.build_review(draft, self.ranking_with_row(row), {"risk": {"max_single_position_pct": 10}})
        verdict = review["verdicts"][0]

        self.assertEqual(verdict["risk_decision"], "downgrade")
        self.assertEqual(verdict["final_state_cap"], "watch_only")
        self.assertIn("same_theme_best_peer_evidence_missing_or_failed", verdict["risk_tags"])

    def test_risk_review_downgrades_buy_candidate_on_market_overextension(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "volume_ratio_20": 1.4,
            "regime_flags": [],
            "same_theme_peer_evidence_passed": True,
            "action_disqualifiers": ["market_range_pos_60_above_action_limit"],
        }
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}

        review = risk_review.build_review(draft, self.ranking_with_row(row), {"risk": {"max_single_position_pct": 10}})
        verdict = review["verdicts"][0]

        self.assertEqual(verdict["risk_decision"], "downgrade")
        self.assertEqual(verdict["final_state_cap"], "watch_only")
        self.assertIn("market_range_pos_60_above_action_limit", verdict["risk_tags"])

    def test_risk_review_vetoes_symbol_risk_memory(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
            "volume_ratio_20": 1.5,
            "regime_flags": [],
        }
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}
        memory = {"symbols": {"AAA.HK": {"action_veto": True, "tags": ["low_symbol_pass_rate"], "reasons": ["test veto"]}}}

        review = risk_review.build_review(draft, self.ranking_with_row(row), {"risk": {"max_single_position_pct": 10}}, memory)
        verdict = review["verdicts"][0]

        self.assertEqual(verdict["risk_decision"], "veto")
        self.assertEqual(verdict["final_state_cap"], "avoid")
        self.assertEqual(verdict["max_position_pct"], 0.0)
        self.assertIn("symbol_risk_veto", verdict["risk_tags"])

    def test_calls_validator_rejects_final_state_above_risk_cap(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="buy_candidate")]}
        review = {"verdicts": [{"symbol": "AAA.HK", "final_state_cap": "watch_only"}]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft, review)

        self.assertTrue(any("exceeds deterministic risk final_state_cap" in error for error in errors))

    def test_calls_validator_rejects_bullish_risk_cap_flipped_to_trim(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}
        review = {"verdicts": [{"symbol": "AAA.HK", "final_state_cap": "buy_candidate"}]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft, review)

        self.assertTrue(any("exceeds deterministic risk final_state_cap" in error for error in errors))

    def test_calls_validator_requires_risk_verdict_for_non_diagnostic_state(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": True,
            "qualified_for_watch": True,
            "diagnostic_only": False,
            "cost_gate_passed": True,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="trim")]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft, {"verdicts": []})

        self.assertTrue(any("requires matching deterministic risk verdict" in error for error in errors))

    def test_close_report_requires_close_session_and_renders_chinese_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            calls_path = tmp_path / "calls.json"
            ranking_path = tmp_path / "ranking.json"
            risk_path = tmp_path / "risk.json"
            evidence_path = tmp_path / "evidence.json"
            calibration_path = tmp_path / "calibration.json"
            forward_path = tmp_path / "forward.json"
            variants_path = tmp_path / "variants.json"
            nontechnical_path = tmp_path / "nontechnical.json"
            attribution_path = tmp_path / "nontechnical-attribution.json"
            output_dir = tmp_path / "reports"
            calls = {
                "date": "2026-04-27",
                "session": "close",
                "recommendations": [
                    {
                        **self.valid_call("AAA.HK", "buy_candidate"),
                        "confidence": 0.72,
                        "rationale": "量价结构改善",
                        "risks": ["成交不足", "大市转弱"],
                        "invalidation": "跌破关键位",
                    },
                    {
                        **self.valid_call("BBB.HK", "watch_only"),
                        "theme": "defensive",
                        "confidence": 0.41,
                        "evidence": ["nontechnical_evidence status=proxy_only, total_score=0.58, event_risk=unknown, flags=['nontechnical_proxy_only']"],
                        "risks": ["nontechnical_proxy_only"],
                    },
                    {**self.valid_call("CCC.HK", "avoid"), "theme": "weak", "confidence": 0.2},
                ],
            }
            ranking = {
                "actionable_candidates": [{"symbol": "ZZZ.HK"}],
                "diagnostic_candidates": [{"symbol": "AAA.HK"}],
                "top_candidates": [
                    {"symbol": "AAA.HK", "score": 80, "qualified_for_action": True, "qualified_for_watch": True, "disqualifiers": [], "action_disqualifiers": [], "nontechnical_evidence": {"status": "available", "total_score": 0.7, "event_risk": "none", "source_count": 2}},
                    {"symbol": "BBB.HK", "score": 74, "qualified_for_action": False, "qualified_for_watch": True, "disqualifiers": [], "action_disqualifiers": ["nontechnical_proxy_only"], "nontechnical_evidence": {"status": "proxy_only", "proxy_only": True, "total_score": 0.58, "event_risk": "unknown", "proxy_source_count": 3}},
                    {"symbol": "DDD.HK", "score": 50, "qualified_for_action": False, "qualified_for_watch": True, "disqualifiers": ["cost_gate_failed"], "action_disqualifiers": ["cost_gate_failed"]},
                    {"symbol": "CCC.HK", "score": 10, "qualified_for_action": False, "qualified_for_watch": False, "disqualifiers": ["downtrend_regime"], "action_disqualifiers": ["downtrend_regime"]},
                ],
                "all_ranked": [
                    {"symbol": "AAA.HK", "score": 80, "qualified_for_action": True, "qualified_for_watch": True, "disqualifiers": [], "action_disqualifiers": [], "nontechnical_evidence": {"status": "available", "total_score": 0.7, "event_risk": "none", "source_count": 2}},
                    {"symbol": "BBB.HK", "score": 74, "qualified_for_action": False, "qualified_for_watch": True, "disqualifiers": [], "action_disqualifiers": ["nontechnical_proxy_only"], "nontechnical_evidence": {"status": "proxy_only", "proxy_only": True, "total_score": 0.58, "event_risk": "unknown", "proxy_source_count": 3}},
                    {"symbol": "DDD.HK", "score": 50, "qualified_for_action": False, "qualified_for_watch": True, "disqualifiers": ["cost_gate_failed"], "action_disqualifiers": ["cost_gate_failed"]},
                    {"symbol": "CCC.HK", "score": 10, "qualified_for_action": False, "qualified_for_watch": False, "disqualifiers": ["downtrend_regime"], "action_disqualifiers": ["downtrend_regime"]},
                ],
            }
            risk = {
                "date": "2026-04-27",
                "session": "close",
                "verdicts": [
                    {"symbol": "AAA.HK", "final_state_cap": "buy_candidate", "risk_decision": "pass"},
                    {"symbol": "BBB.HK", "final_state_cap": "watch_only", "risk_decision": "pass"},
                    {"symbol": "CCC.HK", "final_state_cap": "avoid", "risk_decision": "pass"},
                ]
            }
            evidence = {"summary": {"forward_shadow_log_count": 3}, "shadow_evaluation_summary": {"matured_forward_shadow_days": 2}, "audit_passed": True}
            calibration = {"summary": {"combined_record_count": 5}, "scorecard": {"scored_sample_count": 4, "hit_rate": 0.5, "brier_score": 0.2, "calibration_error": 0.1}}
            forward = {"summary": {"sample_count": 4}}
            variants = {"competition_id": "test_competition", "scoreboard": [{"diagnostic_rank": 1, "variant_id": "baseline", "sample_count": 2, "avg_net_return_pct": 1.2, "avg_alpha_pct": 0.5, "no_execution_audit_passed": True}]}
            nontechnical = {
                "as_of_date": "2026-04-27",
                "summary": {"symbol_count": 3, "available_count": 1, "curated_available_count": 1, "automatic_proxy_count": 1, "proxy_only_count": 1, "missing_count": 1, "critical_finding_count": 0},
                "symbols": {
                    "AAA.HK": {"evidence_mode": "curated_point_in_time", "proxy_only": False, "total_score": 0.7, "event_risk": "none", "source_count": 2},
                    "BBB.HK": {"evidence_mode": "automatic_local_proxy", "proxy_only": True, "total_score": 0.58, "event_risk": "unknown", "proxy_source_count": 3},
                },
            }
            attribution_data = {"as_of_date": "2026-04-27", "summary": {"attributed_sample_count": 1, "hit_rate": 1.0, "avg_return_pct": 2.0}, "buckets": {"total_score": [{"score_bucket": "0.55-0.70", "scored_sample_count": 1, "hit_rate": 1.0, "avg_return_pct": 2.0}]}}
            fixtures = [
                (calls_path, calls),
                (ranking_path, ranking),
                (risk_path, risk),
                (evidence_path, evidence),
                (calibration_path, calibration),
                (forward_path, forward),
                (variants_path, variants),
                (nontechnical_path, nontechnical),
                (attribution_path, attribution_data),
            ]
            for path, payload in fixtures:
                path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")

            result = close_report.build_report(
                "2026-04-27",
                "close",
                calls_path,
                ranking_path,
                risk_path,
                evidence_path,
                calibration_path,
                forward_path,
                variants_path,
                output_dir,
                nontechnical_path,
                attribution_path,
            )

            payload = result["payload"]
            markdown = pathlib.Path(result["markdown"]).read_text(encoding="utf-8")
            for section in ["最终结果", "今日结论", "重点标的表", "研究型行动建议", "Gate 拒绝与观察重点", "影子证据与校准", "非技术面证据与归因", "Shadow 变体竞赛", "研究声明"]:
                self.assertIn(section, markdown)
            self.assertTrue(payload["research_only"])
            self.assertTrue(payload["no_execution"])
            self.assertEqual(payload["source_of_truth"], "calls_json_with_risk_review_caps")
            self.assertEqual([row["symbol"] for row in payload["recommendations"]], ["AAA.HK", "BBB.HK", "CCC.HK"])
            self.assertNotEqual([row["symbol"] for row in payload["recommendations"]], ["ZZZ.HK"])
            self.assertEqual(payload["variants"]["scoreboard"][0]["variant_id"], "baseline")
            self.assertEqual(payload["nontechnical"]["evidence_summary"]["available_count"], 1)
            self.assertIn("正式资料未接入", markdown)
            self.assertIn("正式基本面", markdown)
            self.assertIn("非技术面分桶", markdown)
            self.assertIn("research-only、非交易、不下单、不改组合", markdown)
            for label in ["可考虑研究", "等确认", "继续观察", "暂不碰"]:
                self.assertIn(label, markdown)
            for label in ["why", "主要障碍", "升级条件", "失效条件"]:
                self.assertIn(label, markdown)
            self.assertIn("`BBB.HK`：等确认", markdown)
            self.assertIn("正式资料未接入，不清除正式行动门槛", markdown)
            self.assertNotIn("`BBB.HK`：可考虑研究", markdown)
            action_labels = {row["symbol"]: row["research_action"]["label"] for row in payload["research_actions"]}
            self.assertEqual(action_labels["AAA.HK"], "可考虑研究")
            self.assertEqual(action_labels["BBB.HK"], "等确认")
            self.assertEqual(action_labels["DDD.HK"], "继续观察")
            self.assertEqual(action_labels["CCC.HK"], "暂不碰")

            morning_calls = tmp_path / "morning-calls.json"
            morning_calls.write_text(json.dumps({**calls, "session": "morning"}, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires session=close"):
                close_report.build_report(
                    "2026-04-27",
                    "morning",
                    morning_calls,
                    ranking_path,
                    risk_path,
                    evidence_path,
                    calibration_path,
                    forward_path,
                    variants_path,
                    output_dir,
                    nontechnical_path,
                    attribution_path,
                )

    def test_close_report_rejects_calls_date_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = self.write_close_report_fixture(pathlib.Path(tmp), calls_update={"date": "2026-04-28"})

            with self.assertRaisesRegex(ValueError, "calls date must match report date"):
                self.build_close_report_from_fixture(paths)

    def test_close_report_rejects_future_artifacts(self):
        cases = [
            {"evidence": {"as_of_date": "2026-04-28", "summary": {}}},
            {"calibration": {"as_of_date": "2026-04-28", "summary": {}, "scorecard": {}}},
            {"forward": {"thresholds": {"as_of_date": "2026-04-28"}, "summary": {}}},
            {"variants": {"as_of_date": "2026-04-28", "competition_id": "test_competition", "scoreboard": []}},
            {"variants": {"date": "2026-04-28", "competition_id": "test_competition", "scoreboard": []}},
            {"nontechnical": {"as_of_date": "2026-04-28", "summary": {}}},
            {"attribution_data": {"as_of_date": "2026-04-28", "summary": {}, "buckets": {"total_score": []}}},
            {"risk": {"date": "2026-04-28", "session": "close", "verdicts": [{"symbol": "AAA.HK", "final_state_cap": "buy_candidate"}]}},
        ]

        for overrides in cases:
            with self.subTest(overrides=overrides):
                with tempfile.TemporaryDirectory() as tmp:
                    paths = self.write_close_report_fixture(pathlib.Path(tmp), **overrides)

                    with self.assertRaisesRegex(ValueError, "after report date"):
                        self.build_close_report_from_fixture(paths)

    def test_close_report_enforces_risk_review_verdict_caps(self):
        cases = [
            ({"date": "2026-04-27", "session": "close", "verdicts": [{"symbol": "AAA.HK", "final_state_cap": "watch_only", "risk_decision": "cap"}]}, "exceeds risk review cap"),
            ({"date": "2026-04-27", "session": "close", "verdicts": []}, "missing risk review verdict"),
            ({"date": "2026-04-27", "session": "morning", "verdicts": [{"symbol": "AAA.HK", "final_state_cap": "buy_candidate"}]}, "risk review session must be close"),
        ]

        for risk, message in cases:
            with self.subTest(message=message):
                with tempfile.TemporaryDirectory() as tmp:
                    paths = self.write_close_report_fixture(pathlib.Path(tmp), risk=risk)

                    with self.assertRaisesRegex(ValueError, message):
                        self.build_close_report_from_fixture(paths)

    def test_calls_validator_rejects_watch_state_above_avoid_risk_cap(self):
        row = {
            "symbol": "AAA.HK",
            "qualified_for_action": False,
            "qualified_for_watch": False,
            "diagnostic_only": True,
            "cost_gate_passed": False,
        }
        calls = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="watch_only")]}
        draft = {"date": "2026-04-01", "session": "close", "recommendations": [self.valid_call(state="watch_only")]}
        review = {"verdicts": [{"symbol": "AAA.HK", "final_state_cap": "avoid"}]}

        errors = calls_validator.validate(calls, self.ranking_with_row(row), {"AAA.HK"}, draft, review)

        self.assertTrue(any("exceeds deterministic risk final_state_cap" in error for error in errors))

    def test_build_symbol_risk_memory_from_summary_fields(self):
        data = {
            "symbol_stats": {"0700.HK": {"samples": 5, "avg_return_pct": -1.2, "pass_rate": 0.1}},
            "recent_misfires": [{"symbol": "0700.HK", "call_date": "2026-04-20", "return_pct": -2.0}],
            "recent_selection_errors": [{"symbol": "0700.HK"}],
        }

        result = symbol_risk.build_memory([data], "2026-04-27")

        row = result["symbols"]["0700.HK"]
        self.assertIn("low_symbol_pass_rate", row["tags"])
        self.assertIn("negative_symbol_avg_return", row["tags"])
        self.assertIn("recent_symbol_adverse_breach", row["tags"])
        self.assertIn("repeated_symbol_selection_error", row["tags"])
        self.assertFalse(row["action_veto"])
        self.assertTrue(result["metadata"]["as_of_limited"])

    def test_build_symbol_risk_memory_from_backtest_adverse_records(self):
        backtest = {
            "summary": {"max_adverse_limit_pct": -8.0},
            "records": [
                {"symbol": "9992.HK", "eligible_for_action_from_layer": True, "max_adverse_pct": -8.4},
                {"symbol": "9992.HK", "eligible_for_action_from_layer": True, "max_adverse_pct": -2.0},
                {"symbol": "9992.HK", "eligible_for_action_from_layer": True, "max_adverse_pct": -1.0},
                {"symbol": "0883.HK", "eligible_for_action_from_layer": True, "max_adverse_pct": -8.2},
            ],
        }

        result = symbol_risk.build_memory([], "2026-05-06", backtest)

        row = result["symbols"]["9992.HK"]
        self.assertTrue(row["action_veto"])
        self.assertIn("backtest_adverse_breach", row["tags"])
        self.assertNotIn("0883.HK", result["symbols"])

    def test_peer_return_stats_marks_same_theme_best_missed(self):
        base = {
            "items": [
                {"symbol": "AAA.HK", "theme": "ai", "latest_close": 10.0},
                {"symbol": "BBB.HK", "theme": "ai", "latest_close": 10.0},
                {"symbol": "CCC.HK", "theme": "ai", "latest_close": 10.0},
            ]
        }
        future = {
            "items": [
                {"symbol": "AAA.HK", "theme": "ai", "latest_close": 10.5},
                {"symbol": "BBB.HK", "theme": "ai", "latest_close": 12.0},
                {"symbol": "CCC.HK", "theme": "ai", "latest_close": 10.0},
            ]
        }

        stats = call_eval.peer_return_stats(base, future, "ai", "AAA.HK")

        self.assertTrue(stats["same_theme_best_missed"])
        self.assertEqual(stats["peer_best_symbol"], "BBB.HK")
        self.assertLess(stats["selected_vs_best_bps"], 0)
        learning = call_eval.classify_learning(
            {"confidence": 0.5, "state": "hold"},
            5.0,
            "pass",
            stats["peer_median_return_pct"],
            stats["peer_count"],
            stats["same_theme_best_missed"],
        )
        self.assertEqual(learning, "symbol_selection_error")

    def test_attribution_tags_cost_and_risk_evidence(self):
        record = {
            "call_date": "2026-04-01",
            "session": "close",
            "symbol": "AAA.HK",
            "theme": "growth",
            "window_days": 3,
            "state": "buy_candidate",
            "verdict": "fail",
            "return_pct": -2.5,
            "learning_tag": "symbol_selection_error",
            "same_theme_best_missed": True,
            "selected_vs_best_bps": -250,
            "peer_best_symbol": "BBB.HK",
        }
        final_call = self.valid_call("AAA.HK", "buy_candidate")
        draft_call = self.valid_call("AAA.HK", "buy_candidate")
        risk_verdict = {"risk_decision": "pass", "final_state_cap": "buy_candidate", "risk_tags": []}
        ranking_row = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "score": 70,
            "cost_gate_passed": True,
            "qualified_for_action": True,
            "net_expected_edge_bps": 120,
        }
        ranking = {"all_ranked": [ranking_row, {"symbol": "BBB.HK", "theme": "growth", "score": 90}]}

        tags, evidence = attribution.classify_attribution(record, final_call, draft_call, risk_verdict, ranking_row, ranking)

        self.assertIn("ranking_selection_error", tags)
        self.assertIn("same_theme_best_missed", tags)
        self.assertIn("cost_gate_too_loose", tags)
        self.assertIn("risk_veto_missed", tags)
        self.assertNotIn("llm_final_deviation", tags)
        self.assertTrue(any("theme_leader=BBB.HK" in item for item in evidence))

    def test_attribution_tags_llm_final_deviation_for_draft_upgrade(self):
        record = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "state": "buy_candidate",
            "verdict": "mixed",
            "return_pct": 0.1,
            "learning_tag": None,
        }
        final_call = self.valid_call("AAA.HK", "buy_candidate")
        draft_call = self.valid_call("AAA.HK", "watch_only")

        tags, _evidence = attribution.classify_attribution(record, final_call, draft_call, None, None, {})

        self.assertIn("llm_final_deviation", tags)

    def test_attribution_tags_focus_industry_errors_separately(self):
        record = {
            "symbol": "AAA.HK",
            "theme": "internet-platform",
            "state": "buy_candidate",
            "verdict": "fail",
            "return_pct": -1.8,
            "learning_tag": "theme_error",
            "peer_median_return_pct": 0.9,
        }
        final_call = self.valid_call("AAA.HK", "buy_candidate")
        draft_call = self.valid_call("AAA.HK", "buy_candidate")
        focus_row = {"focus_industry": "technology", "focus_industry_rank": 1, "focus_industry_score": 77.0, "focus_role": "leader", "focus_state": "actionable"}

        tags, evidence = attribution.classify_attribution(record, final_call, draft_call, None, None, {}, focus_row=focus_row)

        self.assertIn("theme_error", tags)
        self.assertIn("focus_industry_error", tags)
        self.assertTrue(any("focus_industry=technology" in item for item in evidence))

    def test_attribution_does_not_blame_risk_when_final_exceeds_risk_cap(self):
        record = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "state": "buy_candidate",
            "verdict": "fail",
            "return_pct": -2.0,
            "learning_tag": None,
        }
        final_call = self.valid_call("AAA.HK", "buy_candidate")
        draft_call = self.valid_call("AAA.HK", "buy_candidate")
        risk_verdict = {"risk_decision": "pass", "final_state_cap": "watch_only", "risk_tags": []}

        tags, _evidence = attribution.classify_attribution(record, final_call, draft_call, risk_verdict, None, {})

        self.assertIn("llm_final_deviation", tags)
        self.assertNotIn("risk_veto_missed", tags)

    def test_attribution_does_not_call_bearish_win_cost_gate_too_strict(self):
        record = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "state": "trim",
            "verdict": "fail",
            "return_pct": 2.0,
            "learning_tag": "defensive_misread",
        }
        final_call = self.valid_call("AAA.HK", "trim")
        draft_call = self.valid_call("AAA.HK", "trim")
        ranking_row = {"symbol": "AAA.HK", "cost_gate_passed": False, "qualified_for_action": False, "net_expected_edge_bps": 50}

        tags, _evidence = attribution.classify_attribution(record, final_call, draft_call, None, ranking_row, {"all_ranked": [ranking_row]})

        self.assertNotIn("cost_gate_too_strict", tags)

    def test_attribution_build_is_fail_soft_without_artifacts(self):
        payload = {
            "records": [
                {
                    "call_date": "2026-04-01",
                    "session": "close",
                    "symbol": "AAA.HK",
                    "window_days": 3,
                    "state": "buy_candidate",
                    "verdict": "fail",
                    "return_pct": -1.5,
                    "learning_tag": None,
                }
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            result = attribution.build_attribution(payload, tmp_path / "calls", tmp_path / "rankings", tmp_path / "risk")

        self.assertEqual(result["record_count"], 1)
        entry = result["entries"][0]
        self.assertNotIn("risk_veto_missed", entry["attribution_tags"])
        self.assertIn("missing ranking artifact or row", entry["evidence"])

    def test_attribution_does_not_call_pass_watch_cap_too_strict(self):
        record = {
            "symbol": "AAA.HK",
            "theme": "growth",
            "state": "watch_only",
            "verdict": "informational",
            "return_pct": 2.0,
            "learning_tag": None,
        }
        final_call = self.valid_call("AAA.HK", "watch_only")
        draft_call = self.valid_call("AAA.HK", "watch_only")
        risk_verdict = {"risk_decision": "pass", "final_state_cap": "watch_only", "risk_tags": []}

        tags, _evidence = attribution.classify_attribution(record, final_call, draft_call, risk_verdict, None, {})

        self.assertNotIn("risk_veto_too_strict", tags)

    def test_attribution_counts_unique_calls_for_planner_thresholds(self):
        payload = {
            "records": [
                {"call_date": "2026-04-01", "session": "close", "symbol": "AAA.HK", "window_days": 3, "state": "buy_candidate", "verdict": "fail", "return_pct": -1.2, "learning_tag": None},
                {"call_date": "2026-04-01", "session": "close", "symbol": "AAA.HK", "window_days": 5, "state": "buy_candidate", "verdict": "fail", "return_pct": -1.5, "learning_tag": None},
            ]
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = pathlib.Path(tmp)
            result = attribution.build_attribution(payload, tmp_path / "calls", tmp_path / "rankings", tmp_path / "risk")

        self.assertEqual(result["attribution_counts"].get("risk_veto_missed"), None)
        self.assertEqual(result["attribution_call_counts"].get("risk_veto_missed"), None)

    def test_planner_generates_tasks_from_repeated_attribution(self):
        tasks = planner.plan_tasks(
            {},
            {"summary": {"sample_count": 20, "sample_quality": "sufficient"}},
            {},
            "",
            {"record_count": 6, "attribution_call_counts": {"risk_veto_too_strict": 2, "cost_gate_too_loose": 3, "focus_industry_error": 2}},
        )

        titles = [task["title"] for task in tasks]
        self.assertIn("Calibrate risk veto strictness after saved-opportunity evidence", titles)
        self.assertIn("Tighten loose cost gate diagnostics", titles)
        self.assertIn("Improve four-industry focus priority scoring", titles)
        self.assertTrue(any("scripts/attribute_investment_outcomes.py" in command for task in tasks for command in task["validation"]))

    def test_planner_ignores_window_counts_without_call_counts(self):
        tasks = planner.plan_tasks(
            {},
            {},
            {},
            "",
            {"record_count": 6, "attribution_counts": {"risk_veto_too_strict": 6}},
        )

        self.assertFalse(any(task["title"] == "Calibrate risk veto strictness after saved-opportunity evidence" for task in tasks))

    def test_planner_uses_baseline_when_optimizer_does_not_promote_champion(self):
        optimization = {
            "updated_active_strategy": False,
            "baseline": {"summary": {"sample_count": 61, "sample_quality": "sufficient", "win_rate": 0.459, "avg_net_return_pct": 0.129, "max_adverse_pct": -6.5, "adverse_breach_rate": 0.0}},
            "champion": {"summary": {"sample_count": 52, "sample_quality": "sufficient", "win_rate": 0.404, "avg_net_return_pct": 0.179, "max_adverse_pct": -5.1, "adverse_breach_rate": 0.0}},
        }
        tasks = planner.plan_tasks({}, {}, optimization, "", {})

        self.assertFalse(any(task["title"] == "Reduce low win-rate candidate selection" for task in tasks))

    def test_readiness_allows_shadow_but_blocks_paper_on_weak_median_and_win_rate(self):
        backtest = {
            "summary": {
                "sample_count": 61,
                "production_sample_count": 61,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.129,
                "avg_alpha_pct": 0.747,
                "median_net_return_pct": -0.178,
                "win_rate": 0.459,
                "max_adverse_pct": -6.557,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
            },
            "records": [
                {"base_date": "2026-01-02", "net_return_pct": -0.2},
                {"base_date": "2026-01-03", "net_return_pct": -0.1},
                {"base_date": "2026-01-04", "net_return_pct": -0.3},
                {"base_date": "2026-01-05", "net_return_pct": -0.4},
                {"base_date": "2026-01-06", "net_return_pct": 0.1},
                {"base_date": "2026-02-02", "net_return_pct": 0.2},
                {"base_date": "2026-02-03", "net_return_pct": 0.1},
                {"base_date": "2026-02-04", "net_return_pct": 0.3},
                {"base_date": "2026-02-05", "net_return_pct": -0.1},
                {"base_date": "2026-02-06", "net_return_pct": 0.2},
                {"base_date": "2026-03-02", "net_return_pct": 0.2},
                {"base_date": "2026-03-03", "net_return_pct": 0.1},
                {"base_date": "2026-03-04", "net_return_pct": 0.3},
                {"base_date": "2026-03-05", "net_return_pct": -0.1},
                {"base_date": "2026-03-06", "net_return_pct": 0.2},
            ],
        }

        result = readiness.build_readiness(backtest, {}, {})

        self.assertTrue(result["tiers"]["shadow_logging"]["passed"])
        self.assertFalse(result["tiers"]["paper_trading"]["passed"])
        self.assertEqual(result["current_allowed_stage"], "shadow_logging")
        paper_findings = {finding["metric"] for finding in result["tiers"]["paper_trading"]["findings"]}
        self.assertIn("sample_count", paper_findings)
        self.assertIn("win_rate", paper_findings)
        self.assertIn("median_net_return_pct", paper_findings)
        self.assertIn("max_adverse_pct", paper_findings)

    def test_readiness_blocks_all_stages_on_registry_quote_date_leakage(self):
        backtest = {
            "summary": {
                "sample_count": 100,
                "production_sample_count": 100,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.5,
                "avg_alpha_pct": 1.0,
                "median_net_return_pct": 0.2,
                "win_rate": 0.6,
                "max_adverse_pct": -3.0,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
                "skipped_quote_date_mismatch_count": 1,
                "skipped_future_quote_date_count": 1,
            },
            "records": [],
        }

        result = readiness.build_readiness(backtest, {}, {})

        self.assertEqual(result["current_allowed_stage"], "research_only")
        self.assertFalse(result["tiers"]["shadow_logging"]["passed"])
        finding_metrics = {finding["metric"] for finding in result["data_quality_findings"]}
        self.assertIn("data_quality.skipped_quote_date_mismatch_count", finding_metrics)
        self.assertIn("data_quality.skipped_future_quote_date_count", finding_metrics)

    def test_readiness_blocks_non_point_in_time_symbol_risk(self):
        backtest = {
            "summary": {
                "sample_count": 100,
                "production_sample_count": 100,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.5,
                "avg_alpha_pct": 1.0,
                "median_net_return_pct": 0.2,
                "win_rate": 0.6,
                "max_adverse_pct": -3.0,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "full",
                "symbol_risk_point_in_time": False,
            },
            "records": [],
        }

        result = readiness.build_readiness(backtest, {}, {})

        self.assertEqual(result["current_allowed_stage"], "research_only")
        finding_metrics = {finding["metric"] for finding in result["data_quality_findings"]}
        self.assertIn("data_quality.symbol_risk_point_in_time", finding_metrics)

    def test_readiness_allows_paper_when_metrics_and_month_balance_pass(self):
        records = []
        for month in ("2026-01", "2026-02", "2026-03", "2026-04"):
            records.extend(
                [
                    {"base_date": f"{month}-02", "net_return_pct": 0.2},
                    {"base_date": f"{month}-03", "net_return_pct": 0.1},
                    {"base_date": f"{month}-04", "net_return_pct": 0.3},
                    {"base_date": f"{month}-05", "net_return_pct": -0.1},
                    {"base_date": f"{month}-06", "net_return_pct": 0.0},
                ]
            )
        backtest = {
            "summary": {
                "sample_count": 75,
                "production_sample_count": 75,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.16,
                "avg_alpha_pct": 0.60,
                "median_net_return_pct": 0.02,
                "win_rate": 0.50,
                "max_adverse_pct": -5.5,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
            },
            "records": records,
        }

        result = readiness.build_readiness(backtest, {}, {})

        self.assertTrue(result["tiers"]["paper_trading"]["passed"])
        self.assertEqual(result["current_allowed_stage"], "paper_trading")

    def test_readiness_blocks_stage_when_market_segment_risk_fails(self):
        records = []
        for month in ("2026-01", "2026-02", "2026-03", "2026-04"):
            records.extend(
                [
                    {"base_date": f"{month}-02", "net_return_pct": 0.2},
                    {"base_date": f"{month}-03", "net_return_pct": 0.1},
                    {"base_date": f"{month}-04", "net_return_pct": 0.3},
                    {"base_date": f"{month}-05", "net_return_pct": -0.1},
                    {"base_date": f"{month}-06", "net_return_pct": 0.0},
                ]
            )
        backtest = {
            "summary": {
                "sample_count": 160,
                "production_sample_count": 160,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.3,
                "avg_alpha_pct": 0.70,
                "median_net_return_pct": 0.08,
                "win_rate": 0.56,
                "max_adverse_pct": -5.5,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
            },
            "records": records,
            "risk_diagnostics": {
                "by_market_family": [
                    {"market_family": "hk", "sample_count": 80, "win_rate": 0.6, "avg_net_return_pct": 0.4, "median_net_return_pct": 0.1, "avg_alpha_pct": 0.8, "max_adverse_pct": -4.0, "adverse_breach_rate": 0.0},
                    {"market_family": "cn", "sample_count": 80, "win_rate": 0.52, "avg_net_return_pct": 0.2, "median_net_return_pct": 0.05, "avg_alpha_pct": 0.6, "max_adverse_pct": -9.0, "adverse_breach_rate": 0.1},
                ]
            },
        }

        result = readiness.build_readiness(backtest, {}, {})

        self.assertEqual(result["current_allowed_stage"], "research_only")
        self.assertEqual(result["market_stats"][1]["market_family"], "cn")
        paper_findings = {finding["metric"] for finding in result["tiers"]["paper_trading"]["findings"]}
        self.assertIn("market[cn].max_adverse_pct", paper_findings)
        self.assertIn("market[cn].adverse_breach_rate", paper_findings)

    def test_readiness_small_live_requires_forward_paper_days(self):
        backtest = {
            "summary": {
                "sample_count": 90,
                "production_sample_count": 90,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.25,
                "avg_alpha_pct": 0.80,
                "median_net_return_pct": 0.05,
                "win_rate": 0.55,
                "max_adverse_pct": -3.5,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
            },
            "records": [],
        }

        result = readiness.build_readiness(backtest, {}, {}, paper_days=0)

        self.assertFalse(result["tiers"]["small_live_observation"]["passed"])
        findings = {finding["metric"] for finding in result["tiers"]["small_live_observation"]["findings"]}
        self.assertIn("forward_paper_days", findings)

    def test_readiness_exit_rule_still_requires_forward_paper_for_small_live(self):
        records = []
        for month in ("2026-01", "2026-02", "2026-03", "2026-04"):
            records.extend(
                [
                    {"base_date": f"{month}-02", "net_return_pct": 0.5},
                    {"base_date": f"{month}-03", "net_return_pct": 0.4},
                    {"base_date": f"{month}-04", "net_return_pct": 0.3},
                    {"base_date": f"{month}-05", "net_return_pct": -0.1},
                    {"base_date": f"{month}-06", "net_return_pct": 0.2},
                ]
            )
        backtest = {
            "summary": {
                "sample_count": 120,
                "production_sample_count": 120,
                "sample_quality": "sufficient",
                "avg_net_return_pct": 0.35,
                "avg_alpha_pct": 0.80,
                "median_net_return_pct": 0.15,
                "win_rate": 0.57,
                "max_adverse_pct": -3.5,
                "adverse_breach_rate": 0.0,
                "symbol_risk_mode": "point_in_time",
                "symbol_risk_point_in_time": True,
                "experimental_exit_rule": "daily_close_stop",
            },
            "records": records,
        }

        result = readiness.build_readiness(backtest, {}, {}, paper_days=0)

        self.assertTrue(result["tiers"]["paper_trading"]["passed"])
        self.assertFalse(result["tiers"]["small_live_observation"]["passed"])
        self.assertEqual(result["current_allowed_stage"], "paper_trading")
        findings = {finding["metric"] for finding in result["tiers"]["small_live_observation"]["findings"]}
        self.assertIn("forward_paper_days", findings)


if __name__ == "__main__":
    unittest.main()

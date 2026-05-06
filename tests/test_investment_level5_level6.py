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
import build_symbol_risk_memory as symbol_risk  # noqa: E402
import create_investment_run_manifest as run_manifest  # noqa: E402
import generate_investment_draft_calls as draft_calls  # noqa: E402
import generate_investment_risk_review as risk_review  # noqa: E402
import validate_investment_calls as calls_validator  # noqa: E402


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

    def ranking_with_row(self, row):
        defaults = {
            "expected_edge_bps": 160.0,
            "net_expected_edge_bps": 125.0,
            "cost_gate_passed": True,
            "edge_method": "technical_snapshot_score_v1",
            "evidence_window": "1d_momentum_20d_volume_20d_60d_trend_60d_range",
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
        self.assertFalse(annotated[1]["qualified_for_watch"])
        self.assertTrue(annotated[1]["diagnostic_only"])
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
        self.assertTrue(row["action_veto"])
        self.assertIn("low_symbol_pass_rate", row["tags"])
        self.assertIn("negative_symbol_avg_return", row["tags"])
        self.assertIn("recent_symbol_adverse_breach", row["tags"])
        self.assertIn("repeated_symbol_selection_error", row["tags"])
        self.assertTrue(result["metadata"]["as_of_limited"])

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
            {},
            {},
            "",
            {"record_count": 6, "attribution_call_counts": {"risk_veto_too_strict": 2, "cost_gate_too_loose": 3}},
        )

        titles = [task["title"] for task in tasks]
        self.assertIn("Calibrate risk veto strictness after saved-opportunity evidence", titles)
        self.assertIn("Tighten loose cost gate diagnostics", titles)
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


if __name__ == "__main__":
    unittest.main()

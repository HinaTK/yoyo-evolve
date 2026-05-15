# 2026-05-14 收盘研究报告

## 今日结论
- 研究模式：仅推荐研究；不执行交易、不修改组合。
- 行动候选：0 个；观察名单：2 个；回避/不行动：1 个。
- 证据进度：forward logs=4，matured days=1，forward samples=0。

## 重点标的表
- `9618.HK`：状态=watch_only，主题=internet-platform，置信度=0.36，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 9618.HK.
  - 风险：nontechnical_evidence_missing；market_range_pos_60_above_action_limit；diagnostic_layer_action_cap_watch_only
  - 非技术面：nontechnical_evidence status=missing, total_score=None, event_risk=None, flags=['nontechnical_evidence_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0002.HK`：状态=watch_only，主题=utilities-defensive，置信度=0.36，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 0002.HK.
  - 风险：nontechnical_evidence_missing；market_range_pos_60_above_action_limit；diagnostic_layer_action_cap_watch_only
  - 非技术面：nontechnical_evidence status=missing, total_score=None, event_risk=None, flags=['nontechnical_evidence_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0728.HK`：状态=avoid，主题=telecom-dividend，置信度=0.27，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 0728.HK.
  - 风险：symbol_risk_veto；nontechnical_evidence_missing；market_range_pos_60_above_action_limit
  - 非技术面：nontechnical_evidence status=missing, total_score=None, event_risk=None, flags=['nontechnical_evidence_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.

## Gate 拒绝与观察重点
- `9618.HK` score=85.31 action=False watch=True gates=['nontechnical_evidence_missing', 'market_range_pos_60_above_action_limit']
- `0002.HK` score=83.29 action=False watch=True gates=['nontechnical_evidence_missing', 'market_range_pos_60_above_action_limit']
- `0728.HK` score=82.87 action=False watch=True gates=['nontechnical_evidence_missing', 'market_range_pos_60_above_action_limit']

## 影子证据与校准
- Evidence audit passed：True。
- Calibration samples：854；hit_rate=None；Brier=None；calibration_error=None。

## 非技术面证据与归因
- Evidence coverage：available=0 / symbols=46；missing=46；blocking_findings=276；critical_findings=0。
- Attribution samples：0；hit_rate=None；avg_return=None。

## Shadow 变体竞赛
- #1 `baseline_shadow` samples=0 avg_net=None alpha=None audit=True
- #2 `no_heat_filter` samples=0 avg_net=None alpha=None audit=True
- #3 `tighter_stop` samples=0 avg_net=None alpha=None audit=True

## 数据与限制
- 本报告只整理 deterministic ranking、calls、risk review、shadow evidence、calibration scorecard 和非技术面 evidence/attribution。
- 不把 historical replay 当作 forward evidence；不因 shadow 变体结果自动晋升 active strategy。
- forward 样本不足时，所有结论只能作为研究观察。

## 研究声明
- 这不是投资建议或交易指令；系统不会自动下单，也不会假设真实持仓。

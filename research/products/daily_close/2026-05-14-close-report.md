# 2026-05-14 收盘研究报告

## 最终结果
- 今日无行动候选；仅保留观察名单。
- 首要观察：9618.HK、0002.HK。
- 执行状态：research-only，不下单、不改组合。

## 今日结论
- 研究模式：仅推荐研究；不执行交易、不修改组合。
- 行动候选：0 个；观察名单：2 个；回避/不行动：1 个。
- 证据进度：forward logs=4，matured days=1，forward samples=0。

## 重点标的表
- `9618.HK`：状态=watch_only，主题=internet-platform，置信度=0.36，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 9618.HK.
  - 风险：nontechnical_proxy_only；nontechnical_score_below_action_min；event_risk_policy
  - 非技术面：nontechnical_evidence status=proxy_only, total_score=0.47, event_risk=policy, flags=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'event_risk_policy', 'nontechnical_source_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0002.HK`：状态=watch_only，主题=utilities-defensive，置信度=0.36，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 0002.HK.
  - 风险：nontechnical_proxy_only；nontechnical_score_below_action_min；nontechnical_source_missing
  - 非技术面：nontechnical_evidence status=proxy_only, total_score=0.505, event_risk=none, flags=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'nontechnical_source_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0728.HK`：状态=avoid，主题=telecom-dividend，置信度=0.27，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 0728.HK.
  - 风险：symbol_risk_veto；nontechnical_proxy_only；nontechnical_score_below_action_min
  - 非技术面：nontechnical_evidence status=proxy_only, total_score=0.509, event_risk=none, flags=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'nontechnical_source_missing']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.

## Gate 拒绝与观察重点
- `9618.HK` score=85.31 action=False watch=True gates=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'event_risk_policy']
- `0002.HK` score=83.29 action=False watch=True gates=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'nontechnical_source_missing']
- `0728.HK` score=82.87 action=False watch=True gates=['nontechnical_proxy_only', 'nontechnical_score_below_action_min', 'nontechnical_source_missing']

## 影子证据与校准
- Evidence audit passed：True。
- Calibration samples（historical/posterior diagnostics，不计入 forward readiness）：854；hit_rate=None；Brier=None；calibration_error=None。

## 非技术面证据与归因
- Evidence coverage：curated_available=0 / symbols=46；proxy_only=46；missing=0；blocking_findings=120；critical_findings=0。
- Attribution samples：0；hit_rate=None；avg_return=None。
- proxy-only 覆盖仅来自本地元数据/行情代理，不是 audited fundamentals；这些行只作观察和诊断，不清除行动门槛。

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

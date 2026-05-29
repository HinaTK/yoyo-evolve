# 2026-05-21 收盘研究报告

## 最终结果
- 今日无行动候选；仅保留观察名单。
- 首要观察：0002.HK。
- 执行状态：research-only，不下单、不改组合。

## 今日结论
- 研究模式：仅推荐研究；不执行交易、不修改组合。
- 行动候选：0 个；观察名单：1 个；回避/不行动：2 个。
- 证据进度：forward logs=11，matured days=1，forward samples=0。

## 重点标的表
- `0005.HK`：状态=avoid，主题=financials-bank，置信度=0.26，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 0005.HK.
  - 风险：symbol_risk_veto；nontechnical_evidence_stale；nontechnical_score_below_action_min
  - 非技术面：nontechnical_evidence status=available, total_score=0.548, event_risk=low, flags=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `000333.SZ`：状态=avoid，主题=china-a-home-appliances，置信度=0.24，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 000333.SZ.
  - 风险：symbol_risk_veto；nontechnical_score_below_action_min；volume_ratio_20_below_1_0
  - 非技术面：nontechnical_evidence status=available, total_score=0.508, event_risk=low, flags=['nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0002.HK`：状态=watch_only，主题=utilities-defensive，置信度=0.33，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 0002.HK.
  - 风险：nontechnical_evidence_stale；nontechnical_score_below_action_min；diagnostic_layer_action_cap_watch_only
  - 非技术面：nontechnical_evidence status=available, total_score=0.501, event_risk=low, flags=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.

## 研究型行动建议
- 声明：本节仅用于安排后续研究优先级；research-only、非交易、不下单、不改组合；不得把正式资料未接入的结果或 shadow 结果描述为正式可行动。
- `0002.HK`：等确认；状态=watch_only；score=70.25；非正式行动候选。
  - why：Draft watch_only generated from deterministic ranking and edge gate fields for 0002.HK.
  - 主要障碍：非技术面证据过期、非技术分不足、diagnostic_layer_action_cap_watch_only。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0941.HK`：等确认；状态=ranking_only；score=70.15；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：非技术面证据过期、非技术分不足、量能不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `588000.SH`：等确认；状态=ranking_only；score=64.99；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：政策风险、成本/边际不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `9618.HK`：等确认；状态=ranking_only；score=61.91；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：非技术面证据过期、非技术分不足、政策风险、成本/边际不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `0006.HK`：继续观察；状态=ranking_only；score=65.54；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：非技术面证据过期、非技术分不足、量能不足、同主题证据不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `159915.SZ`：继续观察；状态=ranking_only；score=65.5；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：成本/边际不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `510300.SH`：继续观察；状态=ranking_only；score=60.86；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：成本/边际不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `0857.HK`：继续观察；状态=ranking_only；score=56.87；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：非技术面证据过期、非技术分不足、成本/边际不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。

## Gate 拒绝与观察重点
- `0005.HK` score=80.5 action=False watch=True gates=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']
- `000333.SZ` score=71.27 action=False watch=True gates=['nontechnical_score_below_action_min', 'volume_ratio_20_below_1_0']
- `0002.HK` score=70.25 action=False watch=True gates=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']

## 影子证据与校准
- Evidence audit passed：True。
- Calibration samples（historical/posterior diagnostics，不计入 forward readiness）：854；hit_rate=None；Brier=None；calibration_error=None。

## 非技术面证据与归因
- 非技术面证据覆盖：正式证据=43 / 标的数=46；正式资料未接入=3；缺失=0；阻断项=20；严重项=0。
- Attribution samples：270；hit_rate=0.511；avg_return=-0.594。
- 正式资料未接入的行尚未取得正式基本面、估值或事件资料；这些行只作观察和排序，不清除行动门槛。
- 非技术面分桶 `0.40-0.55` samples=170 hit_rate=0.524 avg_return=-0.838
- 非技术面分桶 `0.55-0.70` samples=4 hit_rate=0.0 avg_return=10.151

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

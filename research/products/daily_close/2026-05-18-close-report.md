# 2026-05-18 收盘研究报告

## 最终结果
- 今日无行动候选；仅保留观察名单。
- 首要观察：无。
- 执行状态：research-only，不下单、不改组合。

## 今日结论
- 研究模式：仅推荐研究；不执行交易、不修改组合。
- 行动候选：0 个；观察名单：0 个；回避/不行动：3 个。
- 证据进度：forward logs=8，matured days=1，forward samples=0。

## 重点标的表
- `0728.HK`：状态=avoid，主题=telecom-dividend，置信度=0.29，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 0728.HK.
  - 风险：symbol_risk_veto；nontechnical_evidence_stale；nontechnical_score_below_action_min
  - 非技术面：nontechnical_evidence status=available, total_score=0.528, event_risk=low, flags=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `000333.SZ`：状态=avoid，主题=china-a-home-appliances，置信度=0.25，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 000333.SZ.
  - 风险：symbol_risk_veto；nontechnical_score_below_action_min；market_range_pos_60_above_action_limit
  - 非技术面：nontechnical_evidence status=available, total_score=0.514, event_risk=low, flags=['nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `512480.SH`：状态=avoid，主题=china-a-semiconductors，置信度=0.25，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 512480.SH.
  - 风险：symbol_risk_veto；event_risk_policy；volume_ratio_20_below_1_0
  - 非技术面：nontechnical_evidence status=available, total_score=0.617, event_risk=policy, flags=['event_risk_policy']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.

## 研究型行动建议
- 声明：本节仅用于安排后续研究优先级；research-only、非交易、不下单、不改组合；不得把正式资料未接入的结果或 shadow 结果描述为正式可行动。
- `588000.SH`：等确认；状态=ranking_only；score=74.45；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：政策风险、市场位置偏高。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `9618.HK`：等确认；状态=ranking_only；score=69.11；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：非技术面证据过期、非技术分不足、政策风险、量能不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `515790.SH`：等确认；状态=ranking_only；score=51.57；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：非技术分不足、政策风险、量能不足、市场位置偏高。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `0941.HK`：继续观察；状态=ranking_only；score=74.15；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：非技术面证据过期、非技术分不足、量能不足、同主题证据不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `0002.HK`：继续观察；状态=ranking_only；score=69.8；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：非技术面证据过期、非技术分不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `159915.SZ`：继续观察；状态=ranking_only；score=68.32；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：市场位置偏高、成本/边际不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `0006.HK`：继续观察；状态=ranking_only；score=67.08；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：非技术面证据过期、非技术分不足、量能不足、同主题证据不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。
- `510500.SH`：继续观察；状态=ranking_only；score=66.26；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：量能不足、市场位置偏高、成本/边际不足。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。

## Gate 拒绝与观察重点
- `0728.HK` score=92.67 action=False watch=True gates=['nontechnical_evidence_stale', 'nontechnical_score_below_action_min']
- `000333.SZ` score=77.34 action=False watch=True gates=['nontechnical_score_below_action_min', 'market_range_pos_60_above_action_limit']
- `512480.SH` score=76.17 action=False watch=True gates=['event_risk_policy', 'volume_ratio_20_below_1_0', 'market_range_pos_60_above_action_limit']

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

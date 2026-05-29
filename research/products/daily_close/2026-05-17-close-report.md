# 2026-05-17 收盘研究报告

## 最终结果
- 今日无行动候选；仅保留观察名单。
- 首要观察：159915.SZ。
- 执行状态：research-only，不下单、不改组合。

## 今日结论
- 研究模式：仅推荐研究；不执行交易、不修改组合。
- 行动候选：0 个；观察名单：1 个；回避/不行动：2 个。
- 证据进度：forward logs=7，matured days=1，forward samples=0。

## 重点标的表
- `000333.SZ`：状态=avoid，主题=china-a-home-appliances，置信度=0.26，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 000333.SZ.
  - 风险：symbol_risk_veto；quote_trade_date_mismatch；nontechnical_score_below_action_min
  - 非技术面：nontechnical_evidence status=available, total_score=0.522, event_risk=low, flags=['nontechnical_score_below_action_min']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `688981.SH`：状态=avoid，主题=china-a-semiconductors，置信度=0.25，风险上限=avoid。
  - 理由：Draft avoid generated from deterministic ranking and edge gate fields for 688981.SH.
  - 风险：symbol_risk_veto；quote_trade_date_mismatch；nontechnical_score_below_action_min
  - 非技术面：nontechnical_evidence status=available, total_score=0.521, event_risk=policy, flags=['nontechnical_score_below_action_min', 'event_risk_policy']
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `159915.SZ`：状态=watch_only，主题=china-a-growth-tech，置信度=0.43，风险上限=watch_only。
  - 理由：Draft watch_only generated from deterministic ranking and edge gate fields for 159915.SZ.
  - 风险：quote_trade_date_mismatch；market_range_pos_60_above_action_limit；diagnostic_layer_action_cap_watch_only
  - 非技术面：nontechnical_evidence status=available, total_score=0.626, event_risk=low, flags=[]
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.

## 研究型行动建议
- 声明：本节仅用于安排后续研究优先级；research-only、非交易、不下单、不改组合；不得把正式资料未接入的结果或 shadow 结果描述为正式可行动。
- `159915.SZ`：等确认；状态=watch_only；score=75.71；非正式行动候选。
  - why：Draft watch_only generated from deterministic ranking and edge gate fields for 159915.SZ.
  - 主要障碍：行情日期不匹配、市场位置偏高、diagnostic_layer_action_cap_watch_only。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：Invalidate if price loses MA20 support, volume confirmation fades, or the edge/cost gate is no longer met.
- `0941.HK`：等确认；状态=ranking_only；score=72.51；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：行情日期不匹配、非技术面证据过期、非技术分不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `0002.HK`：等确认；状态=ranking_only；score=70.48；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：行情日期不匹配、非技术面证据过期、非技术分不足、量能不足。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `588000.SH`：等确认；状态=ranking_only；score=70.2；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：行情日期不匹配、政策风险、市场位置偏高。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `9618.HK`：等确认；状态=ranking_only；score=70.04；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：行情日期不匹配、非技术面证据过期、非技术分不足、政策风险。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `2800.HK`：等确认；状态=ranking_only；score=65.72；非正式行动候选；正式资料未接入，不清除正式行动门槛。
  - why：正式资料未接入或存在资料阻断，不能视为正式行动候选。
  - 主要障碍：行情日期不匹配、正式资料未接入、非技术分不足、行情日期滞后。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `515790.SH`：等确认；状态=ranking_only；score=58.62；非正式行动候选。
  - why：接近候选，但仍有关键确认项未满足。
  - 主要障碍：行情日期不匹配、非技术分不足、政策风险、市场位置偏高。
  - 升级条件：阻断项清零、正式门槛通过、事件风险回落且正式资料接入后，可升级为「可考虑研究」。
  - 失效条件：若观察分数跌破门槛、状态转弱或新增硬阻断，移出重点跟踪。
- `600900.SH`：继续观察；状态=ranking_only；score=68.61；非正式行动候选。
  - why：有跟踪价值，但当前强度、证据或关卡状态不足。
  - 主要障碍：行情日期不匹配、市场位置偏高。
  - 升级条件：分数进入观察线、状态改善且主要障碍减少后，可升级为「等确认」。
  - 失效条件：若出现硬阻断、状态失败或分数持续偏低，则降为「暂不碰」。

## Gate 拒绝与观察重点
- `000333.SZ` score=80.88 action=False watch=True gates=['quote_trade_date_mismatch', 'nontechnical_score_below_action_min', 'market_range_pos_60_above_action_limit']
- `688981.SH` score=77.32 action=False watch=True gates=['quote_trade_date_mismatch', 'nontechnical_score_below_action_min', 'event_risk_policy']
- `159915.SZ` score=75.71 action=False watch=True gates=['quote_trade_date_mismatch', 'market_range_pos_60_above_action_limit']

## 影子证据与校准
- Evidence audit passed：True。
- Calibration samples（historical/posterior diagnostics，不计入 forward readiness）：854；hit_rate=None；Brier=None；calibration_error=None。

## 非技术面证据与归因
- 非技术面证据覆盖：正式证据=43 / 标的数=46；正式资料未接入=3；缺失=0；阻断项=23；严重项=0。
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

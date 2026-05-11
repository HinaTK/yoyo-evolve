# Investment Strategy Backtest

Generated: `2026-05-09T05:04:49Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `510`
Production samples: `510`
Promotable samples: `510`
Sample quality: `sufficient`
Strict samples: `510`
Relaxed samples: `0`
Qualified samples: `510`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `market_stall`
Experimental exit rule: `daily_close_stop`
Stop loss pct: `-4.0`
Exit triggered rate: `0.324`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.936`%
Win rate: `0.502`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.604`%
Average max adverse return: `-2.04`%
Max adverse-ish return: `-10.865`%
Adverse breach rate: `0.01`
Registry entries: `591`
Usable registry entries: `591`
Skipped registry entries: `0`
Skipped quote-date mismatch entries: `0`
Skipped future quote-date entries: `0`

## Weights
- `trend_weight`: 0.45
- `momentum_weight`: 0.3
- `range_weight`: 0.15
- `risk_penalty_weight`: 1.15

## Market Family Risk
- `hk`: samples=300, win=0.527, avg=0.994%, alpha=0.507%, max_adverse=-10.865%, breach_rate=0.013
- `cn`: samples=210, win=0.467, avg=0.854%, alpha=0.741%, max_adverse=-10.573%, breach_rate=0.005

## Worst Adverse Records
- `2024-11-13` `1024.HK` (hk): net=-11.215%, adverse=-10.865%, range=0.5996, volume=1.1614, pct_1d=3.932
- `2024-10-09` `688981.SH` (cn): net=-10.923%, adverse=-10.573%, range=1.0, volume=8.4163, pct_1d=16.53
- `2024-07-19` `9992.HK` (hk): net=-10.666%, adverse=-10.316%, range=1.0, volume=3.0811, pct_1d=10.745
- `2025-04-03` `0728.HK` (hk): net=-8.467%, adverse=-8.117%, range=0.6942, volume=1.2339, pct_1d=2.66
- `2026-02-27` `2269.HK` (hk): net=-8.356%, adverse=-8.006%, range=0.8663, volume=1.2804, pct_1d=5.068
- `2024-04-12` `601899.SH` (cn): net=-8.025%, adverse=-7.675%, range=1.0, volume=1.1289, pct_1d=2.327
- `2024-08-01` `512480.SH` (cn): net=-7.94%, adverse=-7.59%, range=0.8304, volume=1.0552, pct_1d=0.535
- `2025-01-02` `9992.HK` (hk): net=-7.662%, adverse=-7.312%, range=0.897, volume=1.1304, pct_1d=1.69
- `2026-04-09` `2331.HK` (hk): net=-7.587%, adverse=-7.237%, range=0.957, volume=1.0752, pct_1d=3.66
- `2024-12-24` `688981.SH` (cn): net=-7.474%, adverse=-7.124%, range=0.8648, volume=1.2962, pct_1d=1.765

## Adverse Driver Buckets
### `range_pos_60`
- `0_35_to_0_70`: samples=60, breaches=2, breach_rate=0.033, max_adverse=-10.865%
- `0_85_to_1_00`: samples=367, breaches=3, breach_rate=0.008, max_adverse=-10.573%
- `0_70_to_0_85`: samples=83, breaches=0, breach_rate=0.0, max_adverse=-7.59%
### `volume_ratio_20`
- `gte_2_50`: samples=37, breaches=2, breach_rate=0.054, max_adverse=-10.573%
- `1_00_to_1_50`: samples=318, breaches=3, breach_rate=0.009, max_adverse=-10.865%
- `1_50_to_2_50`: samples=155, breaches=0, breach_rate=0.0, max_adverse=-6.706%
### `pct_change_1d`
- `gte_5`: samples=69, breaches=3, breach_rate=0.043, max_adverse=-10.573%
- `2_to_5`: samples=213, breaches=2, breach_rate=0.009, max_adverse=-10.865%
- `0_to_2`: samples=169, breaches=0, breach_rate=0.0, max_adverse=-7.59%
- `neg_2_to_0`: samples=59, breaches=0, breach_rate=0.0, max_adverse=-6.232%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=215, breaches=3, breach_rate=0.014, max_adverse=-10.573%
- `0_30_to_0_50`: samples=139, breaches=2, breach_rate=0.014, max_adverse=-10.865%
- `lt_0_30`: samples=156, breaches=0, breach_rate=0.0, max_adverse=-7.59%

## Recent Records
- `2026-03-19` rank 2 `0883.HK`: net=-5.691%, alpha=-2.702%, adverse=-5.341%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `002594.SZ`: net=-4.522%, alpha=-5.481%, adverse=-4.172%, qualified=True, diagnostic=False
- `2026-03-23` rank 2 `601088.SH`: net=-4.895%, alpha=-7.119%, adverse=-4.545%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-5.029%, alpha=-4.903%, adverse=-4.679%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `9618.HK`: net=2.792%, alpha=1.038%, adverse=-0.461%, qualified=True, diagnostic=False
- `2026-03-25` rank 2 `2331.HK`: net=-4.722%, alpha=-1.8%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-01` rank 2 `1093.HK`: net=-5.651%, alpha=-7.183%, adverse=-5.301%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-7.587%, alpha=-8.081%, adverse=-7.237%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `300750.SZ`: net=8.403%, alpha=5.737%, adverse=2.721%, qualified=True, diagnostic=False
- `2026-04-10` rank 2 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-4.824%, alpha=-3.483%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-4.47%, alpha=-2.244%, adverse=-4.12%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

# Investment Strategy Backtest

Generated: `2026-05-09T04:18:50Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `551`
Production samples: `551`
Promotable samples: `551`
Sample quality: `sufficient`
Strict samples: `551`
Relaxed samples: `0`
Qualified samples: `551`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `off`
Experimental exit rule: `daily_close_stop`
Stop loss pct: `-4.0`
Exit triggered rate: `0.319`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.849`%
Win rate: `0.494`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.513`%
Average max adverse return: `-2.143`%
Max adverse-ish return: `-14.934`%
Adverse breach rate: `0.016`
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
- `hk`: samples=327, win=0.526, avg=0.941%, alpha=0.38%, max_adverse=-14.934%, breach_rate=0.015
- `cn`: samples=224, win=0.446, avg=0.715%, alpha=0.707%, max_adverse=-10.641%, breach_rate=0.018

## Worst Adverse Records
- `2025-04-03` `1093.HK` (hk): net=-15.284%, adverse=-14.934%, range=1.0, volume=1.395, pct_1d=0.0
- `2024-11-13` `1024.HK` (hk): net=-11.215%, adverse=-10.865%, range=0.5996, volume=1.1614, pct_1d=3.932
- `2024-10-22` `688981.SH` (cn): net=-10.991%, adverse=-10.641%, range=0.9739, volume=1.7071, pct_1d=-1.477
- `2024-10-09` `688981.SH` (cn): net=-10.923%, adverse=-10.573%, range=1.0, volume=8.4163, pct_1d=16.53
- `2024-07-19` `9992.HK` (hk): net=-10.666%, adverse=-10.316%, range=1.0, volume=3.0811, pct_1d=10.745
- `2024-10-09` `600030.SH` (cn): net=-9.152%, adverse=-8.802%, range=1.0, volume=7.0313, pct_1d=1.477
- `2024-12-25` `688981.SH` (cn): net=-8.545%, adverse=-8.195%, range=0.8808, volume=1.3796, pct_1d=1.167
- `2025-04-03` `0728.HK` (hk): net=-8.467%, adverse=-8.117%, range=0.6942, volume=1.2339, pct_1d=2.66
- `2026-02-27` `2269.HK` (hk): net=-8.356%, adverse=-8.006%, range=0.8663, volume=1.2804, pct_1d=5.068
- `2026-02-04` `1299.HK` (hk): net=-8.288%, adverse=-7.938%, range=0.9823, volume=1.0013, pct_1d=1.397

## Adverse Driver Buckets
### `range_pos_60`
- `0_35_to_0_70`: samples=53, breaches=2, breach_rate=0.038, max_adverse=-10.865%
- `0_85_to_1_00`: samples=426, breaches=7, breach_rate=0.016, max_adverse=-14.934%
- `0_70_to_0_85`: samples=72, breaches=0, breach_rate=0.0, max_adverse=-7.59%
### `volume_ratio_20`
- `gte_2_50`: samples=37, breaches=3, breach_rate=0.081, max_adverse=-10.573%
- `1_00_to_1_50`: samples=341, breaches=5, breach_rate=0.015, max_adverse=-14.934%
- `1_50_to_2_50`: samples=173, breaches=1, breach_rate=0.006, max_adverse=-10.641%
### `pct_change_1d`
- `gte_5`: samples=67, breaches=3, breach_rate=0.045, max_adverse=-10.573%
- `0_to_2`: samples=202, breaches=3, breach_rate=0.015, max_adverse=-14.934%
- `neg_2_to_0`: samples=75, breaches=1, breach_rate=0.013, max_adverse=-10.641%
- `2_to_5`: samples=207, breaches=2, breach_rate=0.01, max_adverse=-10.865%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=258, breaches=7, breach_rate=0.027, max_adverse=-14.934%
- `0_30_to_0_50`: samples=138, breaches=2, breach_rate=0.014, max_adverse=-10.865%
- `lt_0_30`: samples=155, breaches=0, breach_rate=0.0, max_adverse=-7.59%

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

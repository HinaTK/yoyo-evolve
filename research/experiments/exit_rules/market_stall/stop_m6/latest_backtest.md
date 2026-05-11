# Investment Strategy Backtest

Generated: `2026-05-09T05:05:18Z`
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
Stop loss pct: `-6.0`
Exit triggered rate: `0.176`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `1.019`%
Win rate: `0.527`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.635`%
Average max adverse return: `-2.429`%
Max adverse-ish return: `-13.116`%
Adverse breach rate: `0.051`
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
- `hk`: samples=300, win=0.563, avg=1.129%, alpha=0.565%, max_adverse=-13.116%, breach_rate=0.07
- `cn`: samples=210, win=0.476, avg=0.861%, alpha=0.736%, max_adverse=-10.573%, breach_rate=0.024

## Worst Adverse Records
- `2025-10-16` `9992.HK` (hk): net=-13.466%, adverse=-13.116%, range=0.4925, volume=1.6699, pct_1d=5.568
- `2024-11-13` `1024.HK` (hk): net=-11.215%, adverse=-10.865%, range=0.5996, volume=1.1614, pct_1d=3.932
- `2024-10-09` `688981.SH` (cn): net=-10.923%, adverse=-10.573%, range=1.0, volume=8.4163, pct_1d=16.53
- `2024-07-31` `9992.HK` (hk): net=-10.705%, adverse=-10.355%, range=0.9789, volume=1.3931, pct_1d=6.99
- `2024-07-19` `9992.HK` (hk): net=-10.666%, adverse=-10.316%, range=1.0, volume=3.0811, pct_1d=10.745
- `2024-11-07` `6862.HK` (hk): net=-10.657%, adverse=-10.307%, range=0.8251, volume=1.8403, pct_1d=9.772
- `2024-09-02` `0386.HK` (hk): net=-10.57%, adverse=-10.22%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2025-01-06` `1810.HK` (hk): net=-9.992%, adverse=-9.642%, range=1.0, volume=1.0516, pct_1d=0.138
- `2025-01-03` `1810.HK` (hk): net=-9.867%, adverse=-9.517%, range=1.0, volume=2.181, pct_1d=6.618
- `2025-04-28` `1093.HK` (hk): net=-9.66%, adverse=-9.31%, range=0.9349, volume=1.0091, pct_1d=-1.193

## Adverse Driver Buckets
### `range_pos_60`
- `0_35_to_0_70`: samples=60, breaches=8, breach_rate=0.133, max_adverse=-13.116%
- `0_85_to_1_00`: samples=367, breaches=17, breach_rate=0.046, max_adverse=-10.573%
- `0_70_to_0_85`: samples=83, breaches=1, breach_rate=0.012, max_adverse=-10.307%
### `volume_ratio_20`
- `gte_2_50`: samples=37, breaches=6, breach_rate=0.162, max_adverse=-10.573%
- `1_00_to_1_50`: samples=318, breaches=14, breach_rate=0.044, max_adverse=-10.865%
- `1_50_to_2_50`: samples=155, breaches=6, breach_rate=0.039, max_adverse=-13.116%
### `pct_change_1d`
- `gte_5`: samples=69, breaches=11, breach_rate=0.159, max_adverse=-13.116%
- `0_to_2`: samples=169, breaches=6, breach_rate=0.036, max_adverse=-10.22%
- `neg_2_to_0`: samples=59, breaches=2, breach_rate=0.034, max_adverse=-9.31%
- `2_to_5`: samples=213, breaches=7, breach_rate=0.033, max_adverse=-10.865%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=215, breaches=13, breach_rate=0.06, max_adverse=-13.116%
- `lt_0_30`: samples=156, breaches=8, breach_rate=0.051, max_adverse=-10.355%
- `0_30_to_0_50`: samples=139, breaches=5, breach_rate=0.036, max_adverse=-10.865%

## Recent Records
- `2026-03-19` rank 2 `0883.HK`: net=-9.207%, alpha=-8.001%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `002594.SZ`: net=-8.359%, alpha=-8.551%, adverse=-8.009%, qualified=True, diagnostic=False
- `2026-03-23` rank 2 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-7.505%, alpha=-6.597%, adverse=-7.155%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `9618.HK`: net=2.792%, alpha=1.038%, adverse=-0.461%, qualified=True, diagnostic=False
- `2026-03-25` rank 2 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-01` rank 2 `1093.HK`: net=-6.795%, alpha=-8.09%, adverse=-6.445%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-7.587%, alpha=-8.081%, adverse=-7.237%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `300750.SZ`: net=8.403%, alpha=5.737%, adverse=2.721%, qualified=True, diagnostic=False
- `2026-04-10` rank 2 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.001%, alpha=-3.388%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-7.216%, alpha=-4.168%, adverse=-6.866%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

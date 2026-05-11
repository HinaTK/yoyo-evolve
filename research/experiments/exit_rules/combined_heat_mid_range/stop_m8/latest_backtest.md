# Investment Strategy Backtest

Generated: `2026-05-09T04:21:00Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `473`
Production samples: `473`
Promotable samples: `473`
Sample quality: `sufficient`
Strict samples: `473`
Relaxed samples: `0`
Qualified samples: `473`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `combined_heat_mid_range`
Experimental exit rule: `daily_close_stop`
Stop loss pct: `-8.0`
Exit triggered rate: `0.074`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.95`%
Win rate: `0.533`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.561`%
Average max adverse return: `-2.401`%
Max adverse-ish return: `-15.763`%
Adverse breach rate: `0.074`
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
- `hk`: samples=277, win=0.588, avg=1.32%, alpha=0.58%, max_adverse=-14.934%, breach_rate=0.072
- `cn`: samples=196, win=0.454, avg=0.426%, alpha=0.536%, max_adverse=-15.763%, breach_rate=0.077

## Worst Adverse Records
- `2025-03-26` `601899.SH` (cn): net=-16.113%, adverse=-15.763%, range=0.939, volume=1.5719, pct_1d=-1.117
- `2025-03-31` `000333.SZ` (cn): net=-15.538%, adverse=-15.188%, range=0.9763, volume=1.6993, pct_1d=2.236
- `2025-04-03` `1093.HK` (hk): net=-15.284%, adverse=-14.934%, range=1.0, volume=1.395, pct_1d=0.0
- `2024-07-11` `601899.SH` (cn): net=-13.213%, adverse=-12.863%, range=0.8374, volume=1.0912, pct_1d=2.756
- `2024-01-04` `1093.HK` (hk): net=-13.016%, adverse=-12.666%, range=1.0, volume=1.2, pct_1d=3.349
- `2024-07-22` `3690.HK` (hk): net=-12.057%, adverse=-11.707%, range=0.7902, volume=1.1421, pct_1d=3.234
- `2026-02-27` `0005.HK` (hk): net=-11.826%, adverse=-11.476%, range=1.0, volume=1.1048, pct_1d=1.626
- `2026-02-04` `1299.HK` (hk): net=-11.816%, adverse=-11.466%, range=0.9823, volume=1.0013, pct_1d=1.397
- `2024-08-28` `0386.HK` (hk): net=-11.477%, adverse=-11.127%, range=0.9293, volume=1.0791, pct_1d=-1.394
- `2024-10-22` `688981.SH` (cn): net=-10.991%, adverse=-10.641%, range=0.9739, volume=1.7071, pct_1d=-1.477

## Adverse Driver Buckets
### `range_pos_60`
- `0_70_to_0_85`: samples=80, breaches=6, breach_rate=0.075, max_adverse=-12.863%
- `0_85_to_1_00`: samples=393, breaches=29, breach_rate=0.074, max_adverse=-15.763%
### `volume_ratio_20`
- `1_00_to_1_50`: samples=323, breaches=28, breach_rate=0.087, max_adverse=-14.934%
- `1_50_to_2_50`: samples=149, breaches=7, breach_rate=0.047, max_adverse=-15.763%
- `gte_2_50`: samples=1, breaches=0, breach_rate=0.0, max_adverse=-1.09%
### `pct_change_1d`
- `0_to_2`: samples=206, breaches=19, breach_rate=0.092, max_adverse=-14.934%
- `neg_2_to_0`: samples=83, breaches=6, breach_rate=0.072, max_adverse=-15.763%
- `2_to_5`: samples=184, breaches=10, breach_rate=0.054, max_adverse=-15.188%
### `market_range_pos_60`
- `0_30_to_0_50`: samples=120, breaches=10, breach_rate=0.083, max_adverse=-12.863%
- `0_50_to_0_70`: samples=219, breaches=16, breach_rate=0.073, max_adverse=-15.763%
- `lt_0_30`: samples=134, breaches=9, breach_rate=0.067, max_adverse=-12.666%

## Recent Records
- `2026-03-16` rank 2 `002594.SZ`: net=1.017%, alpha=5.213%, adverse=-2.801%, qualified=True, diagnostic=False
- `2026-03-17` rank 1 `300750.SZ`: net=-1.179%, alpha=3.11%, adverse=-2.012%, qualified=True, diagnostic=False
- `2026-03-17` rank 2 `002594.SZ`: net=1.964%, alpha=6.252%, adverse=-1.147%, qualified=True, diagnostic=False
- `2026-03-19` rank 1 `601088.SH`: net=-3.948%, alpha=-1.206%, adverse=-5.761%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-9.207%, alpha=-8.001%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-8.471%, alpha=-7.384%, adverse=-8.121%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-9.441%, alpha=-10.783%, adverse=-9.091%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.001%, alpha=-3.388%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-6.408%, alpha=-3.776%, adverse=-6.866%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

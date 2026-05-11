# Investment Strategy Backtest

Generated: `2026-05-09T04:19:49Z`
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
Stop loss pct: `-8.0`
Exit triggered rate: `0.109`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.874`%
Win rate: `0.521`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.462`%
Average max adverse return: `-2.707`%
Max adverse-ish return: `-15.763`%
Adverse breach rate: `0.109`
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
- `hk`: samples=327, win=0.563, avg=0.994%, alpha=0.332%, max_adverse=-14.934%, breach_rate=0.122
- `cn`: samples=224, win=0.46, avg=0.697%, alpha=0.653%, max_adverse=-15.763%, breach_rate=0.089

## Worst Adverse Records
- `2025-03-26` `601899.SH` (cn): net=-16.113%, adverse=-15.763%, range=0.939, volume=1.5719, pct_1d=-1.117
- `2025-03-31` `000333.SZ` (cn): net=-15.538%, adverse=-15.188%, range=0.9763, volume=1.6993, pct_1d=2.236
- `2025-04-03` `1093.HK` (hk): net=-15.284%, adverse=-14.934%, range=1.0, volume=1.395, pct_1d=0.0
- `2025-10-16` `9992.HK` (hk): net=-13.466%, adverse=-13.116%, range=0.4925, volume=1.6699, pct_1d=5.568
- `2024-07-11` `601899.SH` (cn): net=-13.213%, adverse=-12.863%, range=0.8374, volume=1.0912, pct_1d=2.756
- `2024-01-04` `1093.HK` (hk): net=-13.016%, adverse=-12.666%, range=1.0, volume=1.2, pct_1d=3.349
- `2024-11-07` `3690.HK` (hk): net=-12.456%, adverse=-12.106%, range=0.8787, volume=1.143, pct_1d=5.6
- `2024-10-08` `1093.HK` (hk): net=-12.097%, adverse=-11.747%, range=0.9689, volume=3.927, pct_1d=-1.19
- `2026-02-27` `0005.HK` (hk): net=-11.826%, adverse=-11.476%, range=1.0, volume=1.1048, pct_1d=1.626
- `2026-02-04` `1299.HK` (hk): net=-11.816%, adverse=-11.466%, range=0.9823, volume=1.0013, pct_1d=1.397

## Adverse Driver Buckets
### `range_pos_60`
- `0_35_to_0_70`: samples=53, breaches=14, breach_rate=0.264, max_adverse=-13.116%
- `0_85_to_1_00`: samples=426, breaches=40, breach_rate=0.094, max_adverse=-15.763%
- `0_70_to_0_85`: samples=72, breaches=6, breach_rate=0.083, max_adverse=-12.863%
### `volume_ratio_20`
- `gte_2_50`: samples=37, breaches=8, breach_rate=0.216, max_adverse=-11.747%
- `1_00_to_1_50`: samples=341, breaches=40, breach_rate=0.117, max_adverse=-14.934%
- `1_50_to_2_50`: samples=173, breaches=12, breach_rate=0.069, max_adverse=-15.763%
### `pct_change_1d`
- `gte_5`: samples=67, breaches=14, breach_rate=0.209, max_adverse=-13.116%
- `neg_2_to_0`: samples=75, breaches=8, breach_rate=0.107, max_adverse=-15.763%
- `0_to_2`: samples=202, breaches=21, breach_rate=0.104, max_adverse=-14.934%
- `2_to_5`: samples=207, breaches=17, breach_rate=0.082, max_adverse=-15.188%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=258, breaches=33, breach_rate=0.128, max_adverse=-15.763%
- `0_30_to_0_50`: samples=138, breaches=13, breach_rate=0.094, max_adverse=-12.863%
- `lt_0_30`: samples=155, breaches=14, breach_rate=0.09, max_adverse=-12.666%

## Recent Records
- `2026-03-19` rank 2 `0883.HK`: net=-9.207%, alpha=-8.001%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `002594.SZ`: net=-8.359%, alpha=-8.551%, adverse=-8.009%, qualified=True, diagnostic=False
- `2026-03-23` rank 2 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-8.471%, alpha=-7.384%, adverse=-8.121%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `9618.HK`: net=2.792%, alpha=1.038%, adverse=-0.461%, qualified=True, diagnostic=False
- `2026-03-25` rank 2 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-01` rank 2 `1093.HK`: net=-2.221%, alpha=-4.612%, adverse=-6.445%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-9.441%, alpha=-10.783%, adverse=-9.091%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `300750.SZ`: net=8.403%, alpha=5.737%, adverse=2.721%, qualified=True, diagnostic=False
- `2026-04-10` rank 2 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.001%, alpha=-3.388%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-6.408%, alpha=-3.776%, adverse=-6.866%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

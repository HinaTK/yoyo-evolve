# Investment Strategy Backtest

Generated: `2026-05-08T16:56:25Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `506`
Production samples: `506`
Promotable samples: `506`
Sample quality: `sufficient`
Strict samples: `506`
Relaxed samples: `0`
Qualified samples: `506`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `mid_range`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `1.052`%
Win rate: `0.528`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.595`%
Average max adverse return: `-2.793`%
Max adverse-ish return: `-19.735`%
Adverse breach rate: `0.091`
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
- `hk`: samples=298, win=0.581, avg=1.212%, alpha=0.414%, max_adverse=-19.735%, breach_rate=0.094
- `cn`: samples=208, win=0.452, avg=0.823%, alpha=0.854%, max_adverse=-18.829%, breach_rate=0.087

## Worst Adverse Records
- `2024-01-04` `1093.HK` (hk): net=-18.612%, adverse=-19.735%, range=1.0, volume=1.2, pct_1d=3.349
- `2024-07-11` `601899.SH` (cn): net=-19.179%, adverse=-18.829%, range=0.8374, volume=1.0912, pct_1d=2.756
- `2024-08-28` `0386.HK` (hk): net=-18.949%, adverse=-18.599%, range=0.9293, volume=1.0791, pct_1d=-1.394
- `2024-09-02` `0386.HK` (hk): net=-15.874%, adverse=-18.176%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2024-10-09` `688981.SH` (cn): net=9.687%, adverse=-17.177%, range=1.0, volume=8.4163, pct_1d=16.53
- `2025-03-26` `601899.SH` (cn): net=-13.231%, adverse=-15.763%, range=0.939, volume=1.5719, pct_1d=-1.117
- `2024-11-07` `6862.HK` (hk): net=-14.523%, adverse=-15.461%, range=0.8251, volume=1.8403, pct_1d=9.772
- `2024-11-07` `3690.HK` (hk): net=-13.957%, adverse=-15.458%, range=0.8787, volume=1.143, pct_1d=5.6
- `2025-03-31` `000333.SZ` (cn): net=-11.862%, adverse=-15.188%, range=0.9763, volume=1.6993, pct_1d=2.236
- `2025-04-03` `1093.HK` (hk): net=0.217%, adverse=-14.934%, range=1.0, volume=1.395, pct_1d=0.0

## Adverse Driver Buckets
### `range_pos_60`
- `0_85_to_1_00`: samples=430, breaches=40, breach_rate=0.093, max_adverse=-19.735%
- `0_70_to_0_85`: samples=76, breaches=6, breach_rate=0.079, max_adverse=-18.829%
### `volume_ratio_20`
- `gte_2_50`: samples=35, breaches=7, breach_rate=0.2, max_adverse=-17.177%
- `1_00_to_1_50`: samples=314, breaches=29, breach_rate=0.092, max_adverse=-19.735%
- `1_50_to_2_50`: samples=157, breaches=10, breach_rate=0.064, max_adverse=-15.763%
### `pct_change_1d`
- `gte_5`: samples=55, breaches=10, breach_rate=0.182, max_adverse=-17.177%
- `0_to_2`: samples=189, breaches=19, breach_rate=0.101, max_adverse=-18.176%
- `neg_2_to_0`: samples=78, breaches=7, breach_rate=0.09, max_adverse=-18.599%
- `2_to_5`: samples=184, breaches=10, breach_rate=0.054, max_adverse=-19.735%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=238, breaches=24, breach_rate=0.101, max_adverse=-18.599%
- `0_30_to_0_50`: samples=127, breaches=11, breach_rate=0.087, max_adverse=-18.829%
- `lt_0_30`: samples=141, breaches=11, breach_rate=0.078, max_adverse=-19.735%

## Recent Records
- `2026-03-19` rank 1 `601088.SH`: net=-3.948%, alpha=-1.206%, adverse=-5.761%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-9.004%, alpha=-7.255%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `002594.SZ`: net=-9.316%, alpha=-9.327%, adverse=-8.966%, qualified=True, diagnostic=False
- `2026-03-23` rank 2 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-8.471%, alpha=-7.384%, adverse=-8.121%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `9618.HK`: net=2.792%, alpha=1.038%, adverse=-0.461%, qualified=True, diagnostic=False
- `2026-03-25` rank 2 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-12.795%, alpha=-13.134%, adverse=-12.445%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `300750.SZ`: net=8.403%, alpha=5.737%, adverse=2.721%, qualified=True, diagnostic=False
- `2026-04-10` rank 2 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.001%, alpha=-3.388%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-6.408%, alpha=-3.776%, adverse=-6.866%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

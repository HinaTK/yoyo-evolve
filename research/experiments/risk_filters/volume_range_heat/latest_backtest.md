# Investment Strategy Backtest

Generated: `2026-05-08T16:55:44Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `538`
Production samples: `538`
Promotable samples: `538`
Sample quality: `sufficient`
Strict samples: `538`
Relaxed samples: `0`
Qualified samples: `538`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `volume_range_heat`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.963`%
Win rate: `0.53`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.464`%
Average max adverse return: `-2.851`%
Max adverse-ish return: `-35.257`%
Adverse breach rate: `0.1`
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
- `hk`: samples=317, win=0.571, avg=1.104%, alpha=0.31%, max_adverse=-35.257%, breach_rate=0.117
- `cn`: samples=221, win=0.471, avg=0.761%, alpha=0.685%, max_adverse=-18.829%, breach_rate=0.077

## Worst Adverse Records
- `2026-03-18` `9992.HK` (hk): net=-34.841%, adverse=-35.257%, range=0.4737, volume=1.39, pct_1d=2.971
- `2025-10-16` `9992.HK` (hk): net=-20.614%, adverse=-20.819%, range=0.4925, volume=1.6699, pct_1d=5.568
- `2024-01-04` `1093.HK` (hk): net=-18.612%, adverse=-19.735%, range=1.0, volume=1.2, pct_1d=3.349
- `2024-07-11` `601899.SH` (cn): net=-19.179%, adverse=-18.829%, range=0.8374, volume=1.0912, pct_1d=2.756
- `2024-08-28` `0386.HK` (hk): net=-18.949%, adverse=-18.599%, range=0.9293, volume=1.0791, pct_1d=-1.394
- `2024-09-02` `0386.HK` (hk): net=-15.874%, adverse=-18.176%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2024-11-08` `0388.HK` (hk): net=-16.997%, adverse=-16.647%, range=0.6855, volume=1.7846, pct_1d=1.642
- `2025-03-26` `601899.SH` (cn): net=-13.231%, adverse=-15.763%, range=0.939, volume=1.5719, pct_1d=-1.117
- `2024-11-07` `6862.HK` (hk): net=-14.523%, adverse=-15.461%, range=0.8251, volume=1.8403, pct_1d=9.772
- `2024-11-07` `3690.HK` (hk): net=-13.957%, adverse=-15.458%, range=0.8787, volume=1.143, pct_1d=5.6

## Adverse Driver Buckets
### `range_pos_60`
- `0_35_to_0_70`: samples=53, breaches=14, breach_rate=0.264, max_adverse=-35.257%
- `0_70_to_0_85`: samples=77, breaches=7, breach_rate=0.091, max_adverse=-18.829%
- `0_85_to_1_00`: samples=408, breaches=33, breach_rate=0.081, max_adverse=-19.735%
### `volume_ratio_20`
- `gte_2_50`: samples=6, breaches=1, breach_rate=0.167, max_adverse=-10.518%
- `1_00_to_1_50`: samples=355, breaches=41, breach_rate=0.115, max_adverse=-35.257%
- `1_50_to_2_50`: samples=177, breaches=12, breach_rate=0.068, max_adverse=-20.819%
### `pct_change_1d`
- `gte_5`: samples=52, breaches=10, breach_rate=0.192, max_adverse=-20.819%
- `0_to_2`: samples=210, breaches=20, breach_rate=0.095, max_adverse=-18.176%
- `neg_2_to_0`: samples=78, breaches=7, breach_rate=0.09, max_adverse=-18.599%
- `2_to_5`: samples=198, breaches=17, breach_rate=0.086, max_adverse=-35.257%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=252, breaches=28, breach_rate=0.111, max_adverse=-20.819%
- `0_30_to_0_50`: samples=136, breaches=13, breach_rate=0.096, max_adverse=-18.829%
- `lt_0_30`: samples=150, breaches=13, breach_rate=0.087, max_adverse=-35.257%

## Recent Records
- `2026-03-19` rank 1 `601088.SH`: net=-3.948%, alpha=-1.206%, adverse=-5.761%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-9.004%, alpha=-7.255%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-8.471%, alpha=-7.384%, adverse=-8.121%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `9618.HK`: net=2.792%, alpha=1.038%, adverse=-0.461%, qualified=True, diagnostic=False
- `2026-03-25` rank 2 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-01` rank 2 `1093.HK`: net=-2.221%, alpha=-4.612%, adverse=-6.445%, qualified=True, diagnostic=False
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

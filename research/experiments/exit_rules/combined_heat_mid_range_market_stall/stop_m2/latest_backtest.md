# Investment Strategy Backtest

Generated: `2026-05-09T05:33:15Z`
Strategy: `l5_mvp_conservative_v1`
Samples: `425`
Production samples: `425`
Promotable samples: `425`
Sample quality: `sufficient`
Strict samples: `425`
Relaxed samples: `0`
Qualified samples: `425`
Symbol risk mode: `point_in_time`
Symbol risk point-in-time: `True`
Experimental risk filter: `combined_heat_mid_range_market_stall`
Experimental exit rule: `daily_close_stop`
Stop loss pct: `-2.0`
Exit triggered rate: `0.482`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `0.71`%
Win rate: `0.442`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.524`%
Average max adverse return: `-1.4`%
Max adverse-ish return: `-7.375`%
Adverse breach rate: `0.0`
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
- `hk`: samples=243, win=0.473, avg=0.841%, alpha=0.563%, max_adverse=-7.375%, breach_rate=0.0
- `cn`: samples=182, win=0.401, avg=0.534%, alpha=0.473%, max_adverse=-6.641%, breach_rate=0.0

## Worst Adverse Records
- `2024-10-09` `3690.HK` (hk): net=-7.725%, adverse=-7.375%, range=0.7394, volume=1.6613, pct_1d=2.331
- `2024-06-04` `300750.SZ` (cn): net=-6.991%, adverse=-6.641%, range=0.9392, volume=1.0639, pct_1d=1.838
- `2026-02-02` `1299.HK` (hk): net=-6.582%, adverse=-6.232%, range=0.8657, volume=1.3807, pct_1d=-1.439
- `2025-01-03` `9992.HK` (hk): net=-6.512%, adverse=-6.162%, range=0.9736, volume=1.2004, pct_1d=3.379
- `2024-09-11` `600276.SH` (cn): net=-6.364%, adverse=-6.014%, range=1.0, volume=1.1872, pct_1d=2.145
- `2025-01-06` `1810.HK` (hk): net=-6.273%, adverse=-5.923%, range=1.0, volume=1.0516, pct_1d=0.138
- `2024-12-23` `688981.SH` (cn): net=-5.834%, adverse=-5.484%, range=0.8372, volume=2.1558, pct_1d=0.955
- `2024-06-18` `688981.SH` (cn): net=-5.731%, adverse=-5.381%, range=0.9059, volume=1.0055, pct_1d=0.754
- `2024-12-19` `512480.SH` (cn): net=-5.655%, adverse=-5.305%, range=0.7948, volume=1.2399, pct_1d=1.902
- `2026-02-27` `0005.HK` (hk): net=-5.636%, adverse=-5.286%, range=1.0, volume=1.1048, pct_1d=1.626

## Adverse Driver Buckets
### `range_pos_60`
- `0_85_to_1_00`: samples=332, breaches=0, breach_rate=0.0, max_adverse=-6.641%
- `0_70_to_0_85`: samples=93, breaches=0, breach_rate=0.0, max_adverse=-7.375%
### `volume_ratio_20`
- `1_00_to_1_50`: samples=293, breaches=0, breach_rate=0.0, max_adverse=-6.641%
- `1_50_to_2_50`: samples=131, breaches=0, breach_rate=0.0, max_adverse=-7.375%
- `gte_2_50`: samples=1, breaches=0, breach_rate=0.0, max_adverse=-1.09%
### `pct_change_1d`
- `2_to_5`: samples=188, breaches=0, breach_rate=0.0, max_adverse=-7.375%
- `0_to_2`: samples=166, breaches=0, breach_rate=0.0, max_adverse=-6.641%
- `neg_2_to_0`: samples=71, breaches=0, breach_rate=0.0, max_adverse=-6.232%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=169, breaches=0, breach_rate=0.0, max_adverse=-7.375%
- `lt_0_30`: samples=136, breaches=0, breach_rate=0.0, max_adverse=-6.014%
- `0_30_to_0_50`: samples=120, breaches=0, breach_rate=0.0, max_adverse=-6.162%

## Recent Records
- `2026-03-16` rank 2 `002594.SZ`: net=-3.151%, alpha=-2.416%, adverse=-2.801%, qualified=True, diagnostic=False
- `2026-03-17` rank 1 `300750.SZ`: net=-2.362%, alpha=1.582%, adverse=-2.012%, qualified=True, diagnostic=False
- `2026-03-17` rank 2 `002594.SZ`: net=1.964%, alpha=6.252%, adverse=-1.147%, qualified=True, diagnostic=False
- `2026-03-19` rank 1 `601088.SH`: net=-2.351%, alpha=0.608%, adverse=-2.001%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-4.001%, alpha=-3.26%, adverse=-3.651%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-3.061%, alpha=0.479%, adverse=-2.711%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `601088.SH`: net=-2.411%, alpha=-3.167%, adverse=-2.061%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-3.632%, alpha=-3.483%, adverse=-3.282%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `2331.HK`: net=-2.627%, alpha=-0.251%, adverse=-2.277%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-3.086%, alpha=-3.425%, adverse=-2.736%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.415%, alpha=-3.065%, adverse=-3.065%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-3.258%, alpha=-2.01%, adverse=-2.908%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

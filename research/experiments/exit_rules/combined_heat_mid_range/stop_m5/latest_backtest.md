# Investment Strategy Backtest

Generated: `2026-05-09T04:20:17Z`
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
Stop loss pct: `-5.0`
Exit triggered rate: `0.184`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `1.03`%
Win rate: `0.524`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.664`%
Average max adverse return: `-2.093`%
Max adverse-ish return: `-14.934`%
Adverse breach rate: `0.011`
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
- `hk`: samples=277, win=0.574, avg=1.398%, alpha=0.695%, max_adverse=-14.934%, breach_rate=0.011
- `cn`: samples=196, win=0.454, avg=0.51%, alpha=0.62%, max_adverse=-10.641%, breach_rate=0.01

## Worst Adverse Records
- `2025-04-03` `1093.HK` (hk): net=-15.284%, adverse=-14.934%, range=1.0, volume=1.395, pct_1d=0.0
- `2024-10-22` `688981.SH` (cn): net=-10.991%, adverse=-10.641%, range=0.9739, volume=1.7071, pct_1d=-1.477
- `2024-09-02` `0386.HK` (hk): net=-10.57%, adverse=-10.22%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2024-12-25` `688981.SH` (cn): net=-8.545%, adverse=-8.195%, range=0.8808, volume=1.3796, pct_1d=1.167
- `2024-06-20` `0883.HK` (hk): net=-8.539%, adverse=-8.189%, range=1.0, volume=1.1795, pct_1d=3.889
- `2026-02-04` `1299.HK` (hk): net=-8.288%, adverse=-7.938%, range=0.9823, volume=1.0013, pct_1d=1.397
- `2024-04-12` `601899.SH` (cn): net=-8.025%, adverse=-7.675%, range=1.0, volume=1.1289, pct_1d=2.327
- `2024-08-01` `512480.SH` (cn): net=-7.94%, adverse=-7.59%, range=0.8304, volume=1.0552, pct_1d=0.535
- `2024-11-01` `601899.SH` (cn): net=-7.932%, adverse=-7.582%, range=0.7617, volume=1.0205, pct_1d=2.635
- `2026-02-12` `2269.HK` (hk): net=-7.752%, adverse=-7.402%, range=0.9945, volume=1.7095, pct_1d=-0.145

## Adverse Driver Buckets
### `range_pos_60`
- `0_85_to_1_00`: samples=393, breaches=5, breach_rate=0.013, max_adverse=-14.934%
- `0_70_to_0_85`: samples=80, breaches=0, breach_rate=0.0, max_adverse=-7.59%
### `volume_ratio_20`
- `1_00_to_1_50`: samples=323, breaches=4, breach_rate=0.012, max_adverse=-14.934%
- `1_50_to_2_50`: samples=149, breaches=1, breach_rate=0.007, max_adverse=-10.641%
- `gte_2_50`: samples=1, breaches=0, breach_rate=0.0, max_adverse=-1.09%
### `pct_change_1d`
- `0_to_2`: samples=206, breaches=3, breach_rate=0.015, max_adverse=-14.934%
- `neg_2_to_0`: samples=83, breaches=1, breach_rate=0.012, max_adverse=-10.641%
- `2_to_5`: samples=184, breaches=1, breach_rate=0.005, max_adverse=-8.189%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=219, breaches=5, breach_rate=0.023, max_adverse=-14.934%
- `lt_0_30`: samples=134, breaches=0, breach_rate=0.0, max_adverse=-7.59%
- `0_30_to_0_50`: samples=120, breaches=0, breach_rate=0.0, max_adverse=-7.237%

## Recent Records
- `2026-03-16` rank 2 `002594.SZ`: net=1.017%, alpha=5.213%, adverse=-2.801%, qualified=True, diagnostic=False
- `2026-03-17` rank 1 `300750.SZ`: net=-1.179%, alpha=3.11%, adverse=-2.012%, qualified=True, diagnostic=False
- `2026-03-17` rank 2 `002594.SZ`: net=1.964%, alpha=6.252%, adverse=-1.147%, qualified=True, diagnostic=False
- `2026-03-19` rank 1 `601088.SH`: net=-5.848%, alpha=-2.541%, adverse=-5.498%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-5.691%, alpha=-2.702%, adverse=-5.341%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `601088.SH`: net=-5.906%, alpha=-6.3%, adverse=-5.556%, qualified=True, diagnostic=False
- `2026-03-24` rank 2 `002594.SZ`: net=-7.505%, alpha=-6.597%, adverse=-7.155%, qualified=True, diagnostic=False
- `2026-03-25` rank 1 `2331.HK`: net=-0.805%, alpha=-2.56%, adverse=-4.372%, qualified=True, diagnostic=False
- `2026-04-01` rank 1 `0006.HK`: net=2.641%, alpha=0.25%, adverse=1.374%, qualified=True, diagnostic=False
- `2026-04-08` rank 1 `9618.HK`: net=7.067%, alpha=6.421%, adverse=-0.447%, qualified=True, diagnostic=False
- `2026-04-08` rank 2 `0006.HK`: net=0.518%, alpha=-0.128%, adverse=-0.237%, qualified=True, diagnostic=False
- `2026-04-09` rank 1 `2331.HK`: net=-7.587%, alpha=-8.081%, adverse=-7.237%, qualified=True, diagnostic=False
- `2026-04-10` rank 1 `159915.SZ`: net=6.546%, alpha=3.88%, adverse=0.902%, qualified=True, diagnostic=False
- `2026-04-13` rank 1 `300750.SZ`: net=3.138%, alpha=0.693%, adverse=0.871%, qualified=True, diagnostic=False
- `2026-04-14` rank 1 `9618.HK`: net=-0.437%, alpha=0.752%, adverse=-0.087%, qualified=True, diagnostic=False
- `2026-04-14` rank 2 `0941.HK`: net=3.515%, alpha=4.703%, adverse=-0.184%, qualified=True, diagnostic=False
- `2026-04-15` rank 1 `9618.HK`: net=-3.001%, alpha=-3.388%, adverse=-4.474%, qualified=True, diagnostic=False
- `2026-04-16` rank 1 `9618.HK`: net=-5.843%, alpha=-3.769%, adverse=-5.493%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

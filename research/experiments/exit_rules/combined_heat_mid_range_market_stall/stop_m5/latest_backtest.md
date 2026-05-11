# Investment Strategy Backtest

Generated: `2026-05-09T05:05:46Z`
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
Stop loss pct: `-5.0`
Exit triggered rate: `0.179`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `1.025`%
Win rate: `0.529`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.667`%
Average max adverse return: `-1.994`%
Max adverse-ish return: `-10.22`%
Adverse breach rate: `0.005`
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
- `hk`: samples=243, win=0.576, avg=1.347%, alpha=0.714%, max_adverse=-10.22%, breach_rate=0.008
- `cn`: samples=182, win=0.467, avg=0.594%, alpha=0.605%, max_adverse=-7.675%, breach_rate=0.0

## Worst Adverse Records
- `2024-09-02` `0386.HK` (hk): net=-10.57%, adverse=-10.22%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2024-06-20` `0883.HK` (hk): net=-8.539%, adverse=-8.189%, range=1.0, volume=1.1795, pct_1d=3.889
- `2024-04-12` `601899.SH` (cn): net=-8.025%, adverse=-7.675%, range=1.0, volume=1.1289, pct_1d=2.327
- `2024-08-01` `512480.SH` (cn): net=-7.94%, adverse=-7.59%, range=0.8304, volume=1.0552, pct_1d=0.535
- `2024-11-01` `601899.SH` (cn): net=-7.932%, adverse=-7.582%, range=0.7617, volume=1.0205, pct_1d=2.635
- `2024-10-09` `3690.HK` (hk): net=-7.725%, adverse=-7.375%, range=0.7394, volume=1.6613, pct_1d=2.331
- `2025-01-02` `9992.HK` (hk): net=-7.662%, adverse=-7.312%, range=0.897, volume=1.1304, pct_1d=1.69
- `2024-06-13` `0002.HK` (hk): net=-7.619%, adverse=-7.269%, range=1.0, volume=1.5212, pct_1d=2.195
- `2026-04-09` `2331.HK` (hk): net=-7.587%, adverse=-7.237%, range=0.957, volume=1.0752, pct_1d=3.66
- `2026-03-24` `002594.SZ` (cn): net=-7.505%, adverse=-7.155%, range=0.9519, volume=1.2426, pct_1d=-0.92

## Adverse Driver Buckets
### `range_pos_60`
- `0_85_to_1_00`: samples=332, breaches=2, breach_rate=0.006, max_adverse=-10.22%
- `0_70_to_0_85`: samples=93, breaches=0, breach_rate=0.0, max_adverse=-7.59%
### `volume_ratio_20`
- `1_00_to_1_50`: samples=293, breaches=2, breach_rate=0.007, max_adverse=-10.22%
- `1_50_to_2_50`: samples=131, breaches=0, breach_rate=0.0, max_adverse=-7.375%
- `gte_2_50`: samples=1, breaches=0, breach_rate=0.0, max_adverse=-1.09%
### `pct_change_1d`
- `0_to_2`: samples=166, breaches=1, breach_rate=0.006, max_adverse=-10.22%
- `2_to_5`: samples=188, breaches=1, breach_rate=0.005, max_adverse=-8.189%
- `neg_2_to_0`: samples=71, breaches=0, breach_rate=0.0, max_adverse=-7.155%
### `market_range_pos_60`
- `0_50_to_0_70`: samples=169, breaches=2, breach_rate=0.012, max_adverse=-10.22%
- `lt_0_30`: samples=136, breaches=0, breach_rate=0.0, max_adverse=-7.59%
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

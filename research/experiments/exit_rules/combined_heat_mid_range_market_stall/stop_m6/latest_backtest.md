# Investment Strategy Backtest

Generated: `2026-05-09T05:06:00Z`
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
Stop loss pct: `-6.0`
Exit triggered rate: `0.129`
Default market proxy: `2800.HK`
CN market proxy: `510300.SH`
Diagnostic layer samples: `1669`
Diagnostic-only samples: `1669`
Diagnostic samples: `1669`
Average net return: `1.022`%
Win rate: `0.536`
Default benchmark: `2800.HK`
CN benchmark: `510300.SH`
Average benchmark alpha: `0.655`%
Average max adverse return: `-2.11`%
Max adverse-ish return: `-10.22`%
Adverse breach rate: `0.019`
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
- `hk`: samples=243, win=0.588, avg=1.338%, alpha=0.682%, max_adverse=-10.22%, breach_rate=0.029
- `cn`: samples=182, win=0.467, avg=0.599%, alpha=0.619%, max_adverse=-8.388%, breach_rate=0.005

## Worst Adverse Records
- `2024-09-02` `0386.HK` (hk): net=-10.57%, adverse=-10.22%, range=0.8788, volume=1.3243, pct_1d=0.204
- `2025-01-06` `1810.HK` (hk): net=-9.992%, adverse=-9.642%, range=1.0, volume=1.0516, pct_1d=0.138
- `2025-04-28` `1093.HK` (hk): net=-9.66%, adverse=-9.31%, range=0.9349, volume=1.0091, pct_1d=-1.193
- `2024-01-09` `0005.HK` (hk): net=-9.339%, adverse=-8.989%, range=1.0, volume=1.6057, pct_1d=1.681
- `2026-03-19` `0883.HK` (hk): net=-9.207%, adverse=-8.857%, range=0.9809, volume=1.0949, pct_1d=4.523
- `2026-03-02` `6862.HK` (hk): net=-8.812%, adverse=-8.462%, range=0.9534, volume=1.0699, pct_1d=-0.738
- `2024-08-26` `000333.SZ` (cn): net=-8.738%, adverse=-8.388%, range=1.0, volume=1.4694, pct_1d=1.399
- `2024-06-20` `0883.HK` (hk): net=-8.539%, adverse=-8.189%, range=1.0, volume=1.1795, pct_1d=3.889
- `2026-02-27` `0005.HK` (hk): net=-8.348%, adverse=-7.998%, range=1.0, volume=1.1048, pct_1d=1.626
- `2024-06-06` `1093.HK` (hk): net=-8.136%, adverse=-7.786%, range=1.0, volume=1.1781, pct_1d=1.55

## Adverse Driver Buckets
### `range_pos_60`
- `0_85_to_1_00`: samples=332, breaches=8, breach_rate=0.024, max_adverse=-10.22%
- `0_70_to_0_85`: samples=93, breaches=0, breach_rate=0.0, max_adverse=-7.59%
### `volume_ratio_20`
- `1_00_to_1_50`: samples=293, breaches=7, breach_rate=0.024, max_adverse=-10.22%
- `1_50_to_2_50`: samples=131, breaches=1, breach_rate=0.008, max_adverse=-8.989%
- `gte_2_50`: samples=1, breaches=0, breach_rate=0.0, max_adverse=-1.09%
### `pct_change_1d`
- `neg_2_to_0`: samples=71, breaches=2, breach_rate=0.028, max_adverse=-9.31%
- `0_to_2`: samples=166, breaches=4, breach_rate=0.024, max_adverse=-10.22%
- `2_to_5`: samples=188, breaches=2, breach_rate=0.011, max_adverse=-8.857%
### `market_range_pos_60`
- `lt_0_30`: samples=136, breaches=4, breach_rate=0.029, max_adverse=-9.642%
- `0_30_to_0_50`: samples=120, breaches=2, breach_rate=0.017, max_adverse=-9.31%
- `0_50_to_0_70`: samples=169, breaches=2, breach_rate=0.012, max_adverse=-10.22%

## Recent Records
- `2026-03-16` rank 2 `002594.SZ`: net=1.017%, alpha=5.213%, adverse=-2.801%, qualified=True, diagnostic=False
- `2026-03-17` rank 1 `300750.SZ`: net=-1.179%, alpha=3.11%, adverse=-2.012%, qualified=True, diagnostic=False
- `2026-03-17` rank 2 `002594.SZ`: net=1.964%, alpha=6.252%, adverse=-1.147%, qualified=True, diagnostic=False
- `2026-03-19` rank 1 `601088.SH`: net=-3.948%, alpha=-1.206%, adverse=-5.761%, qualified=True, diagnostic=False
- `2026-03-19` rank 2 `0883.HK`: net=-9.207%, alpha=-8.001%, adverse=-8.857%, qualified=True, diagnostic=False
- `2026-03-20` rank 1 `300750.SZ`: net=-6.885%, alpha=-3.869%, adverse=-6.535%, qualified=True, diagnostic=False
- `2026-03-23` rank 1 `601088.SH`: net=-2.532%, alpha=-2.543%, adverse=-5.818%, qualified=True, diagnostic=False
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
- `2026-04-16` rank 1 `9618.HK`: net=-7.216%, alpha=-4.168%, adverse=-6.866%, qualified=True, diagnostic=False
- `2026-04-21` rank 1 `0941.HK`: net=-0.171%, alpha=2.227%, adverse=-0.358%, qualified=True, diagnostic=False

# Investment Readiness

Generated: `2026-05-09T06:33:11Z`
Current allowed stage: `research_only`

## Production Summary
- samples: `551`
- production samples: `551`
- win_rate: `0.526`
- avg_net_return_pct: `0.943`
- median_net_return_pct: `0.439`
- adverse_breach_rate: `0.109`
- sample_quality: `sufficient`

## Data Quality
- no registry quality blockers detected

## Market Stats
- `hk`: samples=327, win=0.569, avg=1.01%, alpha=0.259%, max_adverse=-35.257%, breach_rate=0.122
- `cn`: samples=224, win=0.464, avg=0.846%, alpha=0.78%, max_adverse=-18.829%, breach_rate=0.089

## Worst Adverse Records
- `2026-03-18` `9992.HK` (hk): net=-34.841%, adverse=-35.257%
- `2025-10-16` `9992.HK` (hk): net=-20.614%, adverse=-20.819%
- `2024-01-04` `1093.HK` (hk): net=-18.612%, adverse=-19.735%
- `2024-07-11` `601899.SH` (cn): net=-19.179%, adverse=-18.829%
- `2024-08-28` `0386.HK` (hk): net=-18.949%, adverse=-18.599%
- `2024-09-02` `0386.HK` (hk): net=-15.874%, adverse=-18.176%
- `2024-10-09` `688981.SH` (cn): net=9.687%, adverse=-17.177%
- `2024-11-08` `0388.HK` (hk): net=-16.997%, adverse=-16.647%
- `2025-03-26` `601899.SH` (cn): net=-13.231%, adverse=-15.763%
- `2024-11-07` `6862.HK` (hk): net=-14.523%, adverse=-15.461%

## Tiers
- `shadow_logging`: passed=`False`
- `shadow_logging` blocked by `adverse_breach_rate`: actual `0.109`, expected `<= 0.0`
- `shadow_logging` blocked by `market[hk].adverse_breach_rate`: actual `0.122`, expected `<= 0.0`
- `shadow_logging` blocked by `market[cn].adverse_breach_rate`: actual `0.089`, expected `<= 0.0`
- `paper_trading`: passed=`False`
- `paper_trading` blocked by `avg_alpha_pct`: actual `0.47`, expected `>= 0.5`
- `paper_trading` blocked by `max_adverse_pct`: actual `-35.257`, expected `>= -6.0`
- `paper_trading` blocked by `adverse_breach_rate`: actual `0.109`, expected `<= 0.0`
- `paper_trading` blocked by `month[2024-04].win_rate`: actual `0.3`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-06].win_rate`: actual `0.333`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-07].win_rate`: actual `0.357`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-03].win_rate`: actual `0.333`, expected `>= 0.4`
- `paper_trading` blocked by `month[2026-02].win_rate`: actual `0.273`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-04].avg_net_return_pct`: actual `-0.674`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-06].avg_net_return_pct`: actual `-0.875`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-07].avg_net_return_pct`: actual `-0.956`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-11].avg_net_return_pct`: actual `-1.436`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-12].avg_net_return_pct`: actual `-1.147`, expected `>= -0.3`
- `paper_trading` blocked by `month[2025-03].avg_net_return_pct`: actual `-1.706`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-02].avg_net_return_pct`: actual `-3.507`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-03].avg_net_return_pct`: actual `-1.705`, expected `>= -0.3`
- `paper_trading` blocked by `market[hk].avg_alpha_pct`: actual `0.259`, expected `>= 0.5`
- `paper_trading` blocked by `market[hk].max_adverse_pct`: actual `-35.257`, expected `>= -6.0`
- `paper_trading` blocked by `market[hk].adverse_breach_rate`: actual `0.122`, expected `<= 0.0`
- `paper_trading` blocked by `market[cn].win_rate`: actual `0.464`, expected `>= 0.5`
- `paper_trading` blocked by `market[cn].median_net_return_pct`: actual `-0.454`, expected `>= 0.0`
- `paper_trading` blocked by `market[cn].max_adverse_pct`: actual `-18.829`, expected `>= -6.0`
- `paper_trading` blocked by `market[cn].adverse_breach_rate`: actual `0.089`, expected `<= 0.0`
- `small_live_observation`: passed=`False`
- `small_live_observation` blocked by `win_rate`: actual `0.526`, expected `>= 0.56`
- `small_live_observation` blocked by `avg_alpha_pct`: actual `0.47`, expected `>= 0.75`
- `small_live_observation` blocked by `max_adverse_pct`: actual `-35.257`, expected `>= -4.0`
- `small_live_observation` blocked by `adverse_breach_rate`: actual `0.109`, expected `<= 0.0`
- `small_live_observation` blocked by `forward_paper_days`: actual `0`, expected `>= 20`
- `small_live_observation` blocked by `market[hk].avg_alpha_pct`: actual `0.259`, expected `>= 0.75`
- `small_live_observation` blocked by `market[hk].max_adverse_pct`: actual `-35.257`, expected `>= -4.0`
- `small_live_observation` blocked by `market[hk].adverse_breach_rate`: actual `0.122`, expected `<= 0.0`
- `small_live_observation` blocked by `market[cn].win_rate`: actual `0.464`, expected `>= 0.56`
- `small_live_observation` blocked by `market[cn].median_net_return_pct`: actual `-0.454`, expected `>= 0.1`
- `small_live_observation` blocked by `market[cn].max_adverse_pct`: actual `-18.829`, expected `>= -4.0`
- `small_live_observation` blocked by `market[cn].adverse_breach_rate`: actual `0.089`, expected `<= 0.0`

## Month Stats
- `2024-01`: samples=36, win=0.667, avg=1.374%, median=2.142%
- `2024-02`: samples=20, win=0.5, avg=1.005%, median=0.337%
- `2024-03`: samples=6, win=0.5, avg=2.164%, median=1.333%
- `2024-04`: samples=10, win=0.3, avg=-0.674%, median=-1.22%
- `2024-05`: samples=8, win=0.75, avg=4.559%, median=5.45%
- `2024-06`: samples=33, win=0.333, avg=-0.875%, median=-0.818%
- `2024-07`: samples=42, win=0.357, avg=-0.956%, median=-2.689%
- `2024-08`: samples=35, win=0.486, avg=0.441%, median=-0.35%
- `2024-09`: samples=20, win=0.75, avg=9.62%, median=5.697%
- `2024-10`: samples=28, win=0.464, avg=3.819%, median=-0.756%
- `2024-11`: samples=27, win=0.444, avg=-1.436%, median=-0.657%
- `2024-12`: samples=34, win=0.471, avg=-1.147%, median=-1.133%
- `2025-01`: samples=28, win=0.607, avg=1.213%, median=2.214%
- `2025-02`: samples=19, win=0.526, avg=4.289%, median=0.212%
- `2025-03`: samples=12, win=0.333, avg=-1.706%, median=-0.924%
- `2025-04`: samples=26, win=0.462, avg=0.939%, median=-0.78%
- `2025-05`: samples=8, win=0.875, avg=3.147%, median=2.352%
- `2025-06`: samples=6, win=0.667, avg=0.926%, median=2.087%
- `2025-08`: samples=6, win=0.833, avg=3.404%, median=3.569%
- `2025-10`: samples=18, win=0.833, avg=3.703%, median=5.623%
- `2025-11`: samples=19, win=0.526, avg=0.358%, median=0.03%
- `2025-12`: samples=36, win=0.778, avg=2.613%, median=1.855%
- `2026-01`: samples=6, win=0.833, avg=4.672%, median=6.245%
- `2026-02`: samples=22, win=0.273, avg=-3.507%, median=-3.255%
- `2026-03`: samples=33, win=0.455, avg=-1.705%, median=-0.992%
- `2026-04`: samples=13, win=0.538, avg=0.523%, median=0.518%

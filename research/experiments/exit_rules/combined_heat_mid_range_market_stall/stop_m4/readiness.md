# Investment Readiness

Generated: `2026-05-09T05:16:57Z`
Current allowed stage: `shadow_logging`

## Production Summary
- samples: `425`
- production samples: `425`
- win_rate: `0.508`
- avg_net_return_pct: `0.775`
- median_net_return_pct: `0.062`
- adverse_breach_rate: `0.0`
- sample_quality: `sufficient`

## Data Quality
- no registry quality blockers detected

## Market Stats
- `hk`: samples=243, win=0.551, avg=0.988%, alpha=0.455%, max_adverse=-7.375%, breach_rate=0.0
- `cn`: samples=182, win=0.451, avg=0.489%, alpha=0.541%, max_adverse=-7.675%, breach_rate=0.0

## Worst Adverse Records
- `2024-04-12` `601899.SH` (cn): net=-8.025%, adverse=-7.675%
- `2024-08-01` `512480.SH` (cn): net=-7.94%, adverse=-7.59%
- `2024-10-09` `3690.HK` (hk): net=-7.725%, adverse=-7.375%
- `2025-01-02` `9992.HK` (hk): net=-7.662%, adverse=-7.312%
- `2026-04-09` `2331.HK` (hk): net=-7.587%, adverse=-7.237%
- `2024-12-24` `688981.SH` (cn): net=-7.474%, adverse=-7.124%
- `2024-07-26` `002594.SZ` (cn): net=-7.238%, adverse=-6.888%
- `2026-03-06` `6862.HK` (hk): net=-7.16%, adverse=-6.81%
- `2024-07-04` `0386.HK` (hk): net=-7.056%, adverse=-6.706%
- `2024-06-04` `300750.SZ` (cn): net=-6.991%, adverse=-6.641%

## Tiers
- `shadow_logging`: passed=`True`
- `paper_trading`: passed=`False`
- `paper_trading` blocked by `avg_alpha_pct`: actual `0.492`, expected `>= 0.5`
- `paper_trading` blocked by `max_adverse_pct`: actual `-7.675`, expected `>= -6.0`
- `paper_trading` blocked by `month[2024-06].win_rate`: actual `0.355`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-07].win_rate`: actual `0.325`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-08].win_rate`: actual `0.308`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-02].win_rate`: actual `0.364`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-03].win_rate`: actual `0.333`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-04].win_rate`: actual `0.231`, expected `>= 0.4`
- `paper_trading` blocked by `month[2026-02].win_rate`: actual `0.312`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-04].avg_net_return_pct`: actual `-1.667`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-06].avg_net_return_pct`: actual `-0.694`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-07].avg_net_return_pct`: actual `-0.961`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-08].avg_net_return_pct`: actual `-1.254`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-12].avg_net_return_pct`: actual `-1.043`, expected `>= -0.3`
- `paper_trading` blocked by `month[2025-04].avg_net_return_pct`: actual `-2.484`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-02].avg_net_return_pct`: actual `-1.12`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-03].avg_net_return_pct`: actual `-1.032`, expected `>= -0.3`
- `paper_trading` blocked by `market[hk].avg_alpha_pct`: actual `0.455`, expected `>= 0.5`
- `paper_trading` blocked by `market[hk].max_adverse_pct`: actual `-7.375`, expected `>= -6.0`
- `paper_trading` blocked by `market[cn].win_rate`: actual `0.451`, expected `>= 0.5`
- `paper_trading` blocked by `market[cn].median_net_return_pct`: actual `-0.825`, expected `>= 0.0`
- `paper_trading` blocked by `market[cn].max_adverse_pct`: actual `-7.675`, expected `>= -6.0`
- `small_live_observation`: passed=`False`
- `small_live_observation` blocked by `win_rate`: actual `0.508`, expected `>= 0.56`
- `small_live_observation` blocked by `median_net_return_pct`: actual `0.062`, expected `>= 0.1`
- `small_live_observation` blocked by `avg_alpha_pct`: actual `0.492`, expected `>= 0.75`
- `small_live_observation` blocked by `max_adverse_pct`: actual `-7.675`, expected `>= -4.0`
- `small_live_observation` blocked by `forward_paper_days`: actual `0`, expected `>= 20`
- `small_live_observation` blocked by `market[hk].win_rate`: actual `0.551`, expected `>= 0.56`
- `small_live_observation` blocked by `market[hk].avg_alpha_pct`: actual `0.455`, expected `>= 0.75`
- `small_live_observation` blocked by `market[hk].max_adverse_pct`: actual `-7.375`, expected `>= -4.0`
- `small_live_observation` blocked by `market[cn].win_rate`: actual `0.451`, expected `>= 0.56`
- `small_live_observation` blocked by `market[cn].median_net_return_pct`: actual `-0.825`, expected `>= 0.1`
- `small_live_observation` blocked by `market[cn].avg_alpha_pct`: actual `0.541`, expected `>= 0.75`
- `small_live_observation` blocked by `market[cn].max_adverse_pct`: actual `-7.675`, expected `>= -4.0`

## Month Stats
- `2024-01`: samples=35, win=0.543, avg=0.775%, median=1.471%
- `2024-02`: samples=17, win=0.588, avg=1.92%, median=0.911%
- `2024-03`: samples=3, win=0.333, avg=1.277%, median=-1.133%
- `2024-04`: samples=5, win=0.4, avg=-1.667%, median=-5.681%
- `2024-05`: samples=4, win=0.75, avg=3.097%, median=1.936%
- `2024-06`: samples=31, win=0.355, avg=-0.694%, median=-0.775%
- `2024-07`: samples=40, win=0.325, avg=-0.961%, median=-4.43%
- `2024-08`: samples=26, win=0.308, avg=-1.254%, median=-1.689%
- `2024-09`: samples=18, win=0.778, avg=7.648%, median=3.336%
- `2024-10`: samples=16, win=0.5, avg=5.812%, median=0.418%
- `2024-11`: samples=11, win=0.545, avg=1.002%, median=0.533%
- `2024-12`: samples=32, win=0.438, avg=-1.043%, median=-1.321%
- `2025-01`: samples=25, win=0.56, avg=0.288%, median=1.874%
- `2025-02`: samples=11, win=0.364, avg=0.007%, median=-3.58%
- `2025-03`: samples=6, win=0.333, avg=0.316%, median=-0.906%
- `2025-04`: samples=13, win=0.231, avg=-2.484%, median=-4.381%
- `2025-05`: samples=7, win=0.714, avg=2.406%, median=1.461%
- `2025-06`: samples=5, win=1.0, avg=2.171%, median=1.43%
- `2025-08`: samples=5, win=0.6, avg=-0.007%, median=0.284%
- `2025-10`: samples=10, win=0.9, avg=4.963%, median=5.712%
- `2025-11`: samples=10, win=0.6, avg=1.537%, median=1.572%
- `2025-12`: samples=35, win=0.771, avg=2.123%, median=1.591%
- `2026-01`: samples=6, win=1.0, avg=6.961%, median=7.721%
- `2026-02`: samples=16, win=0.312, avg=-1.12%, median=-3.096%
- `2026-03`: samples=27, win=0.444, avg=-1.032%, median=-2.073%
- `2026-04`: samples=11, win=0.545, avg=0.54%, median=0.518%

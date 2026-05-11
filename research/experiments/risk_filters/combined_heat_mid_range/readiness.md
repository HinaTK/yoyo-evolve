# Investment Readiness

Generated: `2026-05-08T17:06:32Z`
Current allowed stage: `research_only`

## Production Summary
- samples: `473`
- production samples: `473`
- win_rate: `0.535`
- avg_net_return_pct: `1.008`
- median_net_return_pct: `0.62`
- adverse_breach_rate: `0.074`
- sample_quality: `sufficient`

## Data Quality
- no registry quality blockers detected

## Market Stats
- `hk`: samples=277, win=0.592, avg=1.375%, alpha=0.614%, max_adverse=-19.735%, breach_rate=0.072
- `cn`: samples=196, win=0.454, avg=0.489%, alpha=0.556%, max_adverse=-18.829%, breach_rate=0.077

## Worst Adverse Records
- `2024-01-04` `1093.HK` (hk): net=-18.612%, adverse=-19.735%
- `2024-07-11` `601899.SH` (cn): net=-19.179%, adverse=-18.829%
- `2024-08-28` `0386.HK` (hk): net=-18.949%, adverse=-18.599%
- `2024-09-02` `0386.HK` (hk): net=-15.874%, adverse=-18.176%
- `2025-03-26` `601899.SH` (cn): net=-13.231%, adverse=-15.763%
- `2025-03-31` `000333.SZ` (cn): net=-11.862%, adverse=-15.188%
- `2025-04-03` `1093.HK` (hk): net=0.217%, adverse=-14.934%
- `2026-02-27` `0005.HK` (hk): net=-15.149%, adverse=-14.799%
- `2024-07-22` `3690.HK` (hk): net=-12.304%, adverse=-14.262%
- `2025-01-03` `9992.HK` (hk): net=-7.423%, adverse=-13.289%

## Tiers
- `shadow_logging`: passed=`False`
- `shadow_logging` blocked by `adverse_breach_rate`: actual `0.074`, expected `<= 0.0`
- `shadow_logging` blocked by `market[hk].adverse_breach_rate`: actual `0.072`, expected `<= 0.0`
- `shadow_logging` blocked by `market[cn].adverse_breach_rate`: actual `0.077`, expected `<= 0.0`
- `paper_trading`: passed=`False`
- `paper_trading` blocked by `max_adverse_pct`: actual `-19.735`, expected `>= -6.0`
- `paper_trading` blocked by `adverse_breach_rate`: actual `0.074`, expected `<= 0.0`
- `paper_trading` blocked by `month[2024-04].win_rate`: actual `0.3`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-06].win_rate`: actual `0.355`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-07].win_rate`: actual `0.325`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-08].win_rate`: actual `0.308`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-03].win_rate`: actual `0.2`, expected `>= 0.4`
- `paper_trading` blocked by `month[2025-04].win_rate`: actual `0.286`, expected `>= 0.4`
- `paper_trading` blocked by `month[2024-04].avg_net_return_pct`: actual `-1.125`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-06].avg_net_return_pct`: actual `-0.568`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-07].avg_net_return_pct`: actual `-1.336`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-08].avg_net_return_pct`: actual `-0.881`, expected `>= -0.3`
- `paper_trading` blocked by `month[2024-12].avg_net_return_pct`: actual `-0.968`, expected `>= -0.3`
- `paper_trading` blocked by `month[2025-03].avg_net_return_pct`: actual `-2.497`, expected `>= -0.3`
- `paper_trading` blocked by `month[2025-04].avg_net_return_pct`: actual `-2.861`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-02].avg_net_return_pct`: actual `-0.846`, expected `>= -0.3`
- `paper_trading` blocked by `month[2026-03].avg_net_return_pct`: actual `-1.069`, expected `>= -0.3`
- `paper_trading` blocked by `market[hk].max_adverse_pct`: actual `-19.735`, expected `>= -6.0`
- `paper_trading` blocked by `market[hk].adverse_breach_rate`: actual `0.072`, expected `<= 0.0`
- `paper_trading` blocked by `market[cn].win_rate`: actual `0.454`, expected `>= 0.5`
- `paper_trading` blocked by `market[cn].median_net_return_pct`: actual `-0.5`, expected `>= 0.0`
- `paper_trading` blocked by `market[cn].max_adverse_pct`: actual `-18.829`, expected `>= -6.0`
- `paper_trading` blocked by `market[cn].adverse_breach_rate`: actual `0.077`, expected `<= 0.0`
- `small_live_observation`: passed=`False`
- `small_live_observation` blocked by `win_rate`: actual `0.535`, expected `>= 0.56`
- `small_live_observation` blocked by `avg_alpha_pct`: actual `0.59`, expected `>= 0.75`
- `small_live_observation` blocked by `max_adverse_pct`: actual `-19.735`, expected `>= -4.0`
- `small_live_observation` blocked by `adverse_breach_rate`: actual `0.074`, expected `<= 0.0`
- `small_live_observation` blocked by `forward_paper_days`: actual `0`, expected `>= 20`
- `small_live_observation` blocked by `market[hk].avg_alpha_pct`: actual `0.614`, expected `>= 0.75`
- `small_live_observation` blocked by `market[hk].max_adverse_pct`: actual `-19.735`, expected `>= -4.0`
- `small_live_observation` blocked by `market[hk].adverse_breach_rate`: actual `0.072`, expected `<= 0.0`
- `small_live_observation` blocked by `market[cn].win_rate`: actual `0.454`, expected `>= 0.56`
- `small_live_observation` blocked by `market[cn].median_net_return_pct`: actual `-0.5`, expected `>= 0.1`
- `small_live_observation` blocked by `market[cn].avg_alpha_pct`: actual `0.556`, expected `>= 0.75`
- `small_live_observation` blocked by `market[cn].max_adverse_pct`: actual `-18.829`, expected `>= -4.0`
- `small_live_observation` blocked by `market[cn].adverse_breach_rate`: actual `0.077`, expected `<= 0.0`

## Month Stats
- `2024-01`: samples=35, win=0.657, avg=1.378%, median=2.251%
- `2024-02`: samples=18, win=0.667, avg=3.186%, median=2.241%
- `2024-03`: samples=5, win=0.6, avg=2.983%, median=3.798%
- `2024-04`: samples=10, win=0.3, avg=-1.125%, median=-1.22%
- `2024-05`: samples=7, win=0.714, avg=4.066%, median=2.989%
- `2024-06`: samples=31, win=0.355, avg=-0.568%, median=-0.775%
- `2024-07`: samples=40, win=0.325, avg=-1.336%, median=-2.462%
- `2024-08`: samples=26, win=0.308, avg=-0.881%, median=-1.501%
- `2024-09`: samples=19, win=0.737, avg=6.621%, median=2.545%
- `2024-10`: samples=22, win=0.5, avg=5.296%, median=0.928%
- `2024-11`: samples=14, win=0.643, avg=2.054%, median=1.47%
- `2024-12`: samples=33, win=0.485, avg=-0.968%, median=-1.033%
- `2025-01`: samples=26, win=0.577, avg=0.714%, median=1.993%
- `2025-02`: samples=14, win=0.5, avg=1.425%, median=0.204%
- `2025-03`: samples=10, win=0.2, avg=-2.497%, median=-1.065%
- `2025-04`: samples=14, win=0.286, avg=-2.861%, median=-2.598%
- `2025-05`: samples=7, win=0.857, avg=3.495%, median=3.242%
- `2025-06`: samples=6, win=0.667, avg=0.926%, median=2.087%
- `2025-08`: samples=6, win=0.833, avg=2.741%, median=2.334%
- `2025-10`: samples=12, win=1.0, avg=7.135%, median=6.33%
- `2025-11`: samples=14, win=0.571, avg=0.914%, median=0.524%
- `2025-12`: samples=38, win=0.789, avg=2.486%, median=1.808%
- `2026-01`: samples=6, win=0.833, avg=4.672%, median=6.245%
- `2026-02`: samples=21, win=0.429, avg=-0.846%, median=-1.556%
- `2026-03`: samples=28, win=0.429, avg=-1.069%, median=-1.626%
- `2026-04`: samples=11, win=0.545, avg=0.056%, median=0.518%

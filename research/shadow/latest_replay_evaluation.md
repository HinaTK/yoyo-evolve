# Shadow Forward Evaluation

Generated: `2026-05-11T01:35:18Z`
Evaluation mode: `historical_replay_diagnostic`
Counts toward forward evidence: `False`
Gate passed: `False`

## Summary
- forward shadow logs: `1`
- matured forward days: `0`
- samples: `3`
- pending samples: `0`
- win rate: `0.0`
- avg net return: `-14.622`%
- avg alpha: `-14.453`%
- max adverse: `-14.484`%
- adverse breach rate: `1.0`
- stop triggered rate: `1.0`

## Findings
- `forward_shadow_days` actual `1`, expected `>= 20`
- `matured_forward_shadow_days` actual `0`, expected `>= 20`
- `forward_adverse_breach_rate` actual `1.0`, expected `<= 0.0`

## Recent Records
- `2026-01-07` `0005.HK`: net=-14.693%, alpha=-13.069%, adverse=-14.343%, stop=True
- `2026-01-08` `0005.HK`: net=-14.338%, alpha=-14.29%, adverse=-13.988%, stop=True
- `2026-01-09` `0005.HK`: net=-14.834%, alpha=-15.999%, adverse=-14.484%, stop=True

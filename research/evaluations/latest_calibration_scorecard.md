# Recommendation Calibration Scorecard

Generated: `2026-05-17T09:10:42Z`
As-of: date=`2026-05-17`, session=`close`

## Overall
- scored samples: `486`
- low sample: `False`
- avg confidence: `0.663`
- hit rate: `0.487`
- calibration error: `0.176`
- brier score: `0.263`
- avg return: `-0.323`%

## Confidence Buckets
- `0.00-0.40`: scored=3, low_sample=True, avg_conf=0.38, hit=0.333, err=0.047, brier=0.224
- `0.40-0.55`: scored=32, low_sample=False, avg_conf=0.524, hit=0.812, err=0.289, brier=0.174
- `0.55-0.70`: scored=261, low_sample=False, avg_conf=0.625, hit=0.466, err=0.16, brier=0.255
- `0.70-0.85`: scored=188, low_sample=False, avg_conf=0.741, hit=0.468, err=0.273, brier=0.285
- `0.85-1.00`: scored=2, low_sample=True, avg_conf=0.86, hit=0.0, err=0.86, brier=0.74
- `unknown`: scored=0, low_sample=True, avg_conf=None, hit=None, err=None, brier=None

## Findings
- `info` `bucket:0.00-0.40` actual `3`, expected `>= 5`
- `info` `bucket:0.85-1.00` actual `2`, expected `>= 5`

## Recent Records
- `calls` `2026-04-24` `3067.HK` conf=0.5 bucket=`0.40-0.55` success=None return=1.553 verdict=informational learning=None
- `calls` `2026-04-24` `3067.HK` conf=0.5 bucket=`0.40-0.55` success=None return=3.398 verdict=informational learning=None
- `calls` `2026-04-27` `3033.HK` conf=0.45 bucket=`0.40-0.55` success=None return=-0.083 verdict=informational learning=None
- `calls` `2026-04-27` `3033.HK` conf=0.45 bucket=`0.40-0.55` success=None return=-2.234 verdict=informational learning=None
- `calls` `2026-04-27` `3033.HK` conf=0.45 bucket=`0.40-0.55` success=None return=-1.2 verdict=informational learning=None
- `calls` `2026-04-27` `3067.HK` conf=0.4 bucket=`0.40-0.55` success=None return=0.289 verdict=informational learning=None
- `calls` `2026-04-27` `3067.HK` conf=0.4 bucket=`0.40-0.55` success=None return=-2.122 verdict=informational learning=None
- `calls` `2026-04-27` `3067.HK` conf=0.4 bucket=`0.40-0.55` success=None return=-1.061 verdict=informational learning=None
- `calls` `2026-04-27` `2800.HK` conf=0.42 bucket=`0.40-0.55` success=None return=-0.58 verdict=informational learning=None
- `calls` `2026-04-27` `2800.HK` conf=0.42 bucket=`0.40-0.55` success=None return=-1.565 verdict=informational learning=None
- `calls` `2026-04-27` `2800.HK` conf=0.42 bucket=`0.40-0.55` success=None return=-1.145 verdict=informational learning=None
- `calls` `2026-04-27` `9988.HK` conf=0.35 bucket=`0.00-0.40` success=None return=-0.077 verdict=informational learning=None
- `calls` `2026-04-27` `9988.HK` conf=0.35 bucket=`0.00-0.40` success=None return=-2.916 verdict=informational learning=symbol_selection_error
- `calls` `2026-04-27` `9988.HK` conf=0.35 bucket=`0.00-0.40` success=None return=-3.3 verdict=informational learning=symbol_selection_error
- `calls` `2026-04-27` `0700.HK` conf=0.38 bucket=`0.00-0.40` success=None return=0.042 verdict=informational learning=None
- `calls` `2026-04-27` `0700.HK` conf=0.38 bucket=`0.00-0.40` success=None return=-0.962 verdict=informational learning=None
- `calls` `2026-04-27` `0700.HK` conf=0.38 bucket=`0.00-0.40` success=None return=-2.216 verdict=informational learning=None
- `calls` `2026-04-27` `1810.HK` conf=0.34 bucket=`0.00-0.40` success=None return=-0.064 verdict=informational learning=None
- `calls` `2026-04-27` `1810.HK` conf=0.34 bucket=`0.00-0.40` success=None return=-3.856 verdict=informational learning=None
- `calls` `2026-04-27` `1810.HK` conf=0.34 bucket=`0.00-0.40` success=None return=-6.748 verdict=informational learning=None

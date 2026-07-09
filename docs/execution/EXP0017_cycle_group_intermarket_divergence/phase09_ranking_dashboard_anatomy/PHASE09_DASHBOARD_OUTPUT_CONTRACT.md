# Phase 09 Dashboard Output Contract

## CSV Outputs

### `EXP0017_Phase09_Rankings_All.csv`

Complete sorted ranking table.

### `EXP0017_Phase09_Rankings_Top.csv`

Top N ranked buckets.

### `EXP0017_Phase09_Rankings_Bottom.csv`

Bottom N ranked buckets among eligible rows.

### `EXP0017_Phase09_Shortlist.csv`

Buckets that pass all shortlist gates.

### `EXP0017_Phase09_Diagnostics.csv`

File-read status, missing files, invalid headers, and run diagnostics.

## HTML Output

### `EXP0017_Phase09_Dashboard.html`

A simple browser-readable dashboard. It is written to the MQL5 Files directory. It is meant for quick review, not final analytics.

## Output Columns

- rank
- report_name
- bucket_key
- bucket_label
- sample_count
- win_rate_percent
- avg_r
- avg_points
- avg_normalized
- stop_rate_percent
- max_stop_streak
- quality_score
- grade
- component scores
- shortlist flag
- red flags
- recommendation text

## No-Execution Contract

No output in this phase is an executable instruction. Even a grade-A family is only a research candidate.

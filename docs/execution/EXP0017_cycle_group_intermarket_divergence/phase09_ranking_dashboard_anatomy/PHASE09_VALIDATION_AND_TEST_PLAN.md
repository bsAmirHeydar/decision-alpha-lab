# Phase 09 Validation and Test Plan

## 1. Missing File Test

Run Phase 09 before Phase 08 files exist. Expected behavior:

- no crash
- diagnostics report missing files
- empty or partial output permitted

## 2. Header Compatibility Test

Confirm that the reader accepts `bucket_key` / `bucket_label` and also tolerates `group_key` / `group_label`.

## 3. Ranking Eligibility Test

Rows below `InpMinimumSampleForRanking` should be marked `UNRANKED` and excluded from top/bottom ranking outputs.

## 4. Score Sanity Test

A bucket with better average R, better win rate, lower stop rate, and larger sample should outrank a weaker bucket.

## 5. Shortlist Gate Test

A bucket must pass all gates to appear in `EXP0017_Phase09_Shortlist.csv`.

## 6. No-Execution Test

Attach the expert to a chart and verify:

- no orders are opened
- no chart objects are required
- no risk input exists
- no target input exists
- no trade function is called

## 7. HTML Output Test

Open `EXP0017_Phase09_Dashboard.html` from the Files directory and verify top rows render correctly.

## 8. Timer Refresh Test

If `InpRunOnTimer=true`, update Phase 08 files and confirm Phase 09 rewrites dashboard outputs periodically.

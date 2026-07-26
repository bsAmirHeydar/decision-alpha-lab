# Phase 12 Python Module Architecture

## Script

`research/exp0017_phase12/python/phase12_research_workbench.py`

## Main components

- CSV loading with `csv.DictReader`.
- Data audit for expected Phase 10/11 files.
- Out-of-sample leaderboard from Phase 11 predictions.
- Bucket stability from fold-level bucket behavior.
- Feature drift review for selected numeric fields.
- Fold health summary.
- HTML report writer.
- Markdown summary writer.

## Dependency policy

The script uses Python standard library only. This makes the first research bridge portable and avoids environment fragility.

Later phases may add pandas, sklearn, plotting, or notebooks, but this phase intentionally keeps the bridge lightweight.

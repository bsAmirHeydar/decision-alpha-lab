# Install SAED V4-05

## Prerequisite

SAED V4-00 through V4-04 must already be present and V4-04 artifacts must remain immutable.

## Apply

1. Place `decision-alpha-lab-saed-v4-05-semantic-temporal-hypergraph-v1.0.0.zip` in the repository root.
2. Expand the archive into the repository root and remove the ZIP.
3. Run `python tools/strategy_factory/saed_v4_05/run_saed_v4_05_full_qa.py`.
4. Run `python tools/strategy_factory/saed_v4_05/validate_saed_v4_05_delivery.py`.
5. On Windows with MetaTrader 5, run `tools/strategy_factory/saed_v4_05/compile_saed_v4_05_semantic_hypergraph.ps1` and retain the logs as external actual evidence.
6. Stage only paths listed in `SAED_V4_05_FILE_INDEX.txt`.

## Verification

```powershell
python tools/strategy_factory/saed_v4_05/run_saed_v4_05_full_qa.py
python tools/strategy_factory/saed_v4_05/validate_saed_v4_05_delivery.py
```

Static MQL5 validation is not MetaEditor compile or runtime evidence.

## Rollback

Use source control to revert the V4-05 commit. The patch creates no canonical-data migration and no live state. Do not remove files with broad wildcard commands; use the commit or `SAED_V4_05_FILE_INDEX.txt` as the exact boundary.

# Installation — SAED V4-20

Expand the ZIP at the repository root. The patch is additive except for the canonical V4-20 roadmap note, which is upgraded from roadmap status to implemented-reference status. Run the full QA and delivery validator before staging. Stage only the paths in `SAED_V4_20_FILE_INDEX.txt`.

```powershell
python tools/strategy_factory/saed_v4_20/run_saed_v4_20_full_qa.py
python tools/strategy_factory/saed_v4_20/validate_saed_v4_20_delivery.py
git add --pathspec-from-file=SAED_V4_20_FILE_INDEX.txt
```

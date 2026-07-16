# Install SAED V4-25

Expand the ZIP at the repository root. The archive paths are repository-relative and additive. Remove the ZIP from the root after expansion.

Optional local validation:

```powershell
python tools/strategy_factory/saed_v4_25/run_saed_v4_25_full_qa.py
python tools/strategy_factory/saed_v4_25/validate_saed_v4_25_delivery.py
```

Stage only the patch inventory:

```powershell
git add --pathspec-from-file=SAED_V4_25_FILE_INDEX.txt
```

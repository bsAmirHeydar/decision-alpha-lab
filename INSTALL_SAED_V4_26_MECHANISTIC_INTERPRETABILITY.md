# Install SAED V4-26

Expand the ZIP at repository root and remove the ZIP after expansion.

```powershell
python tools/strategy_factory/saed_v4_26/run_saed_v4_26_full_qa.py
python tools/strategy_factory/saed_v4_26/validate_saed_v4_26_delivery.py
git add --pathspec-from-file=SAED_V4_26_FILE_INDEX.txt
```

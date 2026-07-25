# Install FP-I01 Compatibility Patch

Place the ZIP in the repository root, expand it into the current directory, remove the ZIP, stage only paths listed in `EXP0019_FP_I01_FILE_INDEX.txt`, run validation, commit, and push.

Before commit, confirm that these directories have no diff:

```powershell
git diff -- mql5/Include/IntermarketDivergenceExecution/CG
git diff -- mql5/Include/DayeTrader/EXP0018
```

They are immutable dependencies and must not be modified by FP-I01.

# Installation

Expand the ZIP at the repository root, remove the ZIP, run full QA and delivery validation, stage exactly the file index, inspect the staged diff, commit with the supplied message, and push.

Required QA:

```powershell
python tools/strategy_factory/saed_v4_21/run_saed_v4_21_full_qa.py
python tools/strategy_factory/saed_v4_21/validate_saed_v4_21_delivery.py
```

# Alpha Lab Engineering Tools

Run the same ordered, fail-closed preflight locally and in GitHub Actions:

```powershell
python .\tools\engineering\run_engineering_policy.py .
```

The Obsidian stage validates the authored canonical vault at `docs/architecture/master/ai_algorithm_engineering_os`. The legacy `docs/history/aieos_legacy` tree contains generated compatibility locators.

Individual diagnostic checks remain available:

```powershell
python .\tools\engineering\validate_alpha_lab_policy.py .
python .\docs\alpha_lab_master_architecture\ai_algorithm_engineering_os\tools\validate_vault.py .\docs\alpha_lab_master_architecture\ai_algorithm_engineering_os
python .\tools\engineering\check_mql5_compatibility.py .
python .\tools\engineering\audit_repository_layout.py .
python .\tools\engineering\new_alpha_lab_packet.py feature FEAT-001 "Feature title" .\work
```

These are deterministic standard-library preflights. They do not replace compiler, runtime, replay, visual, schema, or human review evidence.

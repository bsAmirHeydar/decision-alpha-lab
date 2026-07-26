# Install Decision Alpha Lab Engineering OS v2

This patch installs the repository-wide AI-assisted engineering policy, the full Obsidian operating system, language standards, quality automation, templates, project tools, and optional GitHub policy CI.

## Install

Run from repository root:

```powershell
Expand-Archive -Force ".\decision-alpha-lab-engineering-os-v2-patch.zip" ".\"
Remove-Item ".\decision-alpha-lab-engineering-os-v2-patch.zip"
```

## Validate

```powershell
python .\tools\engineering\validate_alpha_lab_policy.py .
python .\docs\ai_algorithm_engineering_os\tools\validate_vault.py .\docs\ai_algorithm_engineering_os
python .\tools\engineering\check_mql5_compatibility.py .
python .\tools\engineering\audit_repository_layout.py .
```

The MQL5 scan is a static preflight only. Actual MetaEditor compilation remains mandatory.

## Open in Obsidian

Open `docs/ai_algorithm_engineering_os` as a standalone vault, or include it within the repository vault. Start at `00_START_HERE/00_Home.md`.

## Compatibility

The patch adds policy and tooling. It does not change strategy logic, model behavior, order execution, risk, datasets, or experiment results.

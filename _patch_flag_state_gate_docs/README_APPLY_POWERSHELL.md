# Apply Flag State Gate Dashboard Docs Patch

Run from the root of `decision-alpha-lab` in Windows PowerShell:

```powershell
Expand-Archive -Path .\flag_state_gate_dashboard_docs_patch.zip -DestinationPath .\_patch_flag_state_gate_docs -Force
Remove-Item .\flag_state_gate_dashboard_docs_patch.zip -Force
git apply .\_patch_flag_state_gate_docs\flag_state_gate_dashboard_docs.patch
```

Check:

```powershell
git status
git diff --stat
```

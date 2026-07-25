# Install — NDS Hook 86.4 Exact Speed v1.2.0

Prerequisite: v1.1.1 compile hotfix is installed.

From repository root:

```powershell
Expand-Archive ".\decision-alpha-lab-nds-hook-864-cycle-r1-exact-speed-v1.2.0.zip" -DestinationPath "." -Force
Remove-Item ".\decision-alpha-lab-nds-hook-864-cycle-r1-exact-speed-v1.2.0.zip" -Force
powershell -ExecutionPolicy Bypass -File .\tools\flag_counting\run_nds_hook_864_cycle_r1_tests.ps1
Get-Content ".\NDS_HOOK_864_CYCLE_R1_EXACT_SPEED_V1_2_FILE_INDEX.txt" | ForEach-Object { git add -- $_ }
git commit -F ".\COMMIT_MESSAGE_NDS_HOOK_864_CYCLE_R1_EXACT_SPEED_V1_2.md"
git push
```

Rollback: revert the commit. No migration or persistent schema conversion is required.

# Rollback — UC04-W1B CI Recovery 01

## Before commit

From the repository root, restore the one modified tracked file and remove the files added by this patch using the exact paths in `PATCH_FILE_INDEX.txt`.

```powershell
$Patch = "releases/unified_consolidation/ci_recovery_03"
$Paths = Get-Content -LiteralPath "$Patch/PATCH_FILE_INDEX.txt" | Where-Object { $_ }
$Modified = "tools/consolidation/uc04w0/verify.py"
git restore --worktree --source=HEAD -- $Modified
$Paths | Where-Object { $_ -ne $Modified } | ForEach-Object {
    $Target = Join-Path (Get-Location) ($_.Replace('/', '\'))
    if (Test-Path -LiteralPath $Target -PathType Leaf) {
        Remove-Item -LiteralPath $Target -Force
    }
}
```

## After commit

Create a normal Git revert commit; do not rewrite history:

```powershell
git revert <UC04_W1B_CI_RECOVERY_COMMIT_SHA>
```

Push is intentionally outside this patch and requires an explicit user decision.

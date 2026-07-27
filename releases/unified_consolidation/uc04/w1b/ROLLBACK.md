# UC04-W1B-Q R4 — Rollback

The installer prints an operator-local `INSTALL_STATE.json` path. Rollback is allowed only from that exact state. It restores hash-verified backups and deletes newly introduced files only when their bytes still equal the installed hashes.

## Rollback before commit

```powershell
$ErrorActionPreference = "Stop"
$RepositoryRoot = (Resolve-Path -LiteralPath (Get-Location)).Path
$BackupStatePath = "C:\REPLACE\WITH\THE\PRINTED\INSTALL_STATE.json"
$RollbackIndex = Join-Path ([System.IO.Path]::GetTempPath()) ("UC04-W1B-Q-rollback-index-" + [Guid]::NewGuid().ToString('N') + ".txt")
$InstalledIndex = Join-Path $RepositoryRoot "releases\unified_consolidation\uc04\w1b\PATCH_FILE_INDEX.txt"
$RollbackScript = Join-Path $RepositoryRoot "releases\unified_consolidation\uc04\w1b\APPLY.ps1"

Copy-Item -LiteralPath $InstalledIndex -Destination $RollbackIndex -Force
& $RollbackScript -Action Rollback -RepositoryRoot $RepositoryRoot -BackupStatePath $BackupStatePath

$RollbackPaths = @(Get-Content -LiteralPath $RollbackIndex | ForEach-Object { $_.Trim() } | Where-Object { $_ })
git -C $RepositoryRoot status --short --untracked-files=all -- @RollbackPaths
Remove-Item -LiteralPath $RollbackIndex -Force
```

When installation had not been committed, the target-path status should return to its pre-install state.

## Rollback after commit

Copy the index before rollback because the rollback may remove the release directory itself:

```powershell
$ErrorActionPreference = "Stop"
$RepositoryRoot = (Resolve-Path -LiteralPath (Get-Location)).Path
$BackupStatePath = "C:\REPLACE\WITH\THE\PRINTED\INSTALL_STATE.json"
$RollbackIndex = Join-Path ([System.IO.Path]::GetTempPath()) ("UC04-W1B-Q-rollback-index-" + [Guid]::NewGuid().ToString('N') + ".txt")
$InstalledIndex = Join-Path $RepositoryRoot "releases\unified_consolidation\uc04\w1b\PATCH_FILE_INDEX.txt"
$RollbackScript = Join-Path $RepositoryRoot "releases\unified_consolidation\uc04\w1b\APPLY.ps1"

Copy-Item -LiteralPath $InstalledIndex -Destination $RollbackIndex -Force
& $RollbackScript -Action Rollback -RepositoryRoot $RepositoryRoot -BackupStatePath $BackupStatePath

Push-Location -LiteralPath $RepositoryRoot
try {
    git add --pathspec-from-file="$RollbackIndex"
    if ($LASTEXITCODE -ne 0) { throw "git add for rollback failed" }
    git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw "staged rollback contains whitespace errors" }
    git commit -m "revert(uc04-w1b): rollback native qualification tooling release"
    if ($LASTEXITCODE -ne 0) { throw "rollback commit failed" }
}
finally {
    Pop-Location
    Remove-Item -LiteralPath $RollbackIndex -Force -ErrorAction SilentlyContinue
}
```

## Fail-closed behavior

Rollback refuses to overwrite or delete a target file that changed after installation. Resolve that conflict manually using the backup files referenced by `INSTALL_STATE.json`; do not bypass the hash check.

No push command is included.

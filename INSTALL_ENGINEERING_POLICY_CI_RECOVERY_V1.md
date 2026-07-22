# Install Engineering Policy CI Recovery V1

Patch ID: `ENGPOL_CI_RECOVERY_V1_20260722`

The ZIP is root-relative and overwrites only the exact files recorded in `ENGINEERING_POLICY_CI_RECOVERY_V1_FILE_INDEX.txt`. Run these commands from the repository root in Windows PowerShell.

```powershell
$repoRoot = (Get-Location).Path
$patchZip = Join-Path $repoRoot 'ENGINEERING_POLICY_CI_RECOVERY_V1_PATCH.zip'

Expand-Archive -LiteralPath $patchZip -DestinationPath $repoRoot -Force
Remove-Item -LiteralPath $patchZip -Force

$hashLedger = Join-Path $repoRoot 'ENGINEERING_POLICY_CI_RECOVERY_V1_FILE_HASHES.sha256'
Get-Content -LiteralPath $hashLedger | ForEach-Object {
    $parts = $_ -split '  ', 2
    if ($parts.Count -ne 2) { throw "Invalid hash-ledger row: $_" }
    $payloadPath = Join-Path $repoRoot $parts[1]
    $actual = (Get-FileHash -LiteralPath $payloadPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $parts[0]) { throw "SHA-256 mismatch: $($parts[1])" }
}

python -m pytest .\lab\10_infrastructure\tests\engineering_policy_ci_recovery\test_engineering_policy_ci_recovery.py -q
python .\tools\engineering\run_engineering_policy.py .
```

Stage only the exact patch paths. This intentionally excludes the pre-existing legacy-vault ID-normalization worktree changes.

```powershell
$stagePaths = @(
    '.github/workflows/engineering-policy.yml',
    'COMMIT_MESSAGE_ENGINEERING_POLICY_CI_RECOVERY_V1.md',
    'docs/engineering/ENGINEERING_POLICY_CI_RECOVERY_2026-07-22.md',
    'docs/engineering/README.md',
    'ENGINEERING_POLICY_CI_RECOVERY_V1_FILE_HASHES.sha256',
    'ENGINEERING_POLICY_CI_RECOVERY_V1_FILE_INDEX.txt',
    'ENGINEERING_POLICY_CI_RECOVERY_V1_PATCH_MANIFEST.json',
    'ENGINEERING_POLICY_CI_RECOVERY_V1_QA_REPORT.json',
    'INSTALL_ENGINEERING_POLICY_CI_RECOVERY_V1.md',
    'lab/10_infrastructure/tests/engineering_policy_ci_recovery/test_engineering_policy_ci_recovery.py',
    'ROLLBACK_ENGINEERING_POLICY_CI_RECOVERY_V1.md',
    'tools/engineering/README.md',
    'tools/engineering/run_engineering_policy.py',
    'tools/engineering/validate_alpha_lab_policy.py'
)

git add -- $stagePaths
$staged = @(git diff --cached --name-only)
$missing = @($stagePaths | Where-Object { $_ -notin $staged })
$unexpected = @($staged | Where-Object { $_ -notin $stagePaths })
if ($missing.Count -or $unexpected.Count) {
    throw "Staging mismatch. Missing=$($missing -join ',') Unexpected=$($unexpected -join ',')"
}
git diff --cached --check
git commit -F .\COMMIT_MESSAGE_ENGINEERING_POLICY_CI_RECOVERY_V1.md
git push origin main
```

After the push, require the `Engineering Policy / Repository preflight` run to finish green before declaring the incident resolved.

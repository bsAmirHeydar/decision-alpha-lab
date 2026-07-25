# Install and Validate EXP0019 FP-I00

## Apply

Extract the patch at the repository root.

## Validate

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i00\powershell\run_exp0019_fp_i00_checks.ps1 -RepoRoot .
```

The script regenerates the local Git-aware baseline, executes all FP-I00 tests, runs the previous EXP0018 doctrine compatibility test, and runs repository engineering policy when available.

## Optional original-source verification

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i00\powershell\verify_exp0019_fp_source_package.ps1 `
  -RepoRoot . `
  -SourceRoot "C:\path\to\FP-NEW\FP-NEW"
```

## Acceptance

Do not start FP-I01 unless:

- `FP_I00_VALIDATION_REPORT.json` reports `READY`;
- only `FP-DEC-012` remains open;
- live execution remains `DISABLED_UNTIL_FROZEN`;
- all 19 shared dependency records resolve and hash;
- all 12 prior-context test entry points are discoverable;
- no Faerie Protocol runtime path exists;
- unrelated working-tree changes are explicitly reviewed.

# EXP0019 Faerie Protocol — FP-I00 Governance Harness

FP-I00 freezes the implementation baseline before any Faerie Protocol runtime module exists. The harness validates source hashes, owner decisions, the single open live-execution decision, relation registry, implementation program, shared-core dependencies, previous-context test discoverability, file ownership, rollback scope, and absence of Detector/Indicator/EA authority.

## Run

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i00\powershell\run_exp0019_fp_i00_checks.ps1 -RepoRoot .
```

To verify the original source package as well:

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i00\powershell\run_exp0019_fp_i00_checks.ps1 `
  -RepoRoot . `
  -SourceRoot "C:\path\to\FP-NEW\FP-NEW"
```

## Outputs

- `FP_I00_BASELINE_MANIFEST.v1.json`
- `FP_I00_SHARED_CORE_DEPENDENCY_INVENTORY.csv/json`
- `FP_I00_PREVIOUS_CONTEXT_TEST_INVENTORY.csv`
- `FP_I00_PHASE_FILE_OWNERSHIP.csv`
- `FP_I00_VALIDATION_REPORT.json`

## Authority

FP-I00 has no MQL5 detection, rendering, trading, broker, or network authority. Runtime implementation starts only after the FP-I01 compatibility harness is accepted.

# EXP0019 Faerie Protocol — FP-I01 Shared-Core Compatibility Harness

FP-I01 introduces the read-only compatibility boundary between Faerie Protocol and the accepted EXP0017, EXP0018, and Strategy Factory cores.

## Delivered

- 19 exact dependency pins
- 8 versioned read-only adapters
- 6 neutral compatibility contracts
- 8 deterministic golden fixtures
- Python compatibility/reporting CLI
- MQL5 contract mirror, registry, self-test, and diagnostic
- previous-context discovery and compile runbook
- duplicate implementation and forbidden-authority guards
- detailed Obsidian delivery documentation

## Explicitly absent

- Faerie A/L/N and relation semantics
- WW policy
- Indicator implementation
- trade eligibility, quota, risk, order, broker, or network authority

## Validation

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i01\powershell\run_exp0019_fp_i01_checks.ps1 -RepoRoot $PWD
```

## MetaEditor

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i01\powershell\compile_exp0019_fp_i01_compatibility.ps1 -RepoRoot $PWD
```

MetaEditor compilation is a separate local Windows gate and remains `pending_local_windows` in the generated evidence until logs are captured.

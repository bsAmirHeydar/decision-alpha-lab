# EXP0019 Faerie Protocol — FP-I06 Relation and Hunt Engine

FP-I06 compiles AL/AN/LN/NA/NL/NN relation instances from accepted FP-I05 windows and references, scans aligned M1 evidence, emits symbol-local HuntFacts, classifies M1 first sweep, assigns Hunter/Protected roles, and creates deterministic raw divergence candidates.

## Delivered

- 17 Python modules
- 48 phase tests
- 15 closed JSON schemas
- 15 public contracts
- 70 reason codes
- 7-relation registry with six supported and WW deferred
- 12 MQL5 includes plus diagnostic and self-test EAs
- 48 Obsidian delivery notes and 7 atomic concepts

## Authority

Runtime authority is `NONE`. This phase does not confirm signals, draw, alert, arbitrate quota, calculate risk, or submit orders.

## Validation

```powershell
& .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i06\powershell\run_fp_i06_tests.ps1 -RepoRoot $PWD
```

Start documentation at:

`docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i06/00_FP_I06_DELIVERY_MOC.md`

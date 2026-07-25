# EXP0019 FP-I08 Weekly WW Engine

FP-I08 implements the complete non-visual weekly WW context layer for Faerie Protocol.
It compiles the previous completed weekly window against the current check week, reuses
FP-I06 for M1 first-sweep classification, reuses FP-I07 for closed-host-candle confirmation,
tracks second-symbol neutralization, resolves the newest active confirmed WW context, and
publishes a deterministic downstream direction gate without deleting suppressed signals.

## Implemented boundaries

- Previous completed `W` window is the weekly reference source.
- Current `W` window is the weekly check interval.
- High-side and low-side WW plans remain symbol-local.
- First-sweep order remains M1-authoritative.
- Confirmation remains FP-I07-authoritative.
- A confirmed WW is both a directly tradeable setup and a downstream context gate.
- The protected symbol touching the corresponding weekly reference neutralizes the context.
- The newest confirmed context that is still active wins; older contexts remain auditable.
- Complete weekly data with no active WW allows both directions.
- Incomplete weekly data fails closed.
- Opposing downstream signals are suppressed, not deleted.

## Local verification

```powershell
.\lab_infrastructure\EXP0019_faerie_protocol\phase_i08\powershellun_fp_i08_tests.ps1
python .	ools\exp0019alidate_fp_i08_delivery.py .
python .	ools\exp0019\check_fp_i08_boundaries.py .
python .	ools\exp0019\check_fp_i08_mql5_static.py .
```

MetaEditor compilation is intentionally a separate Windows gate:

```powershell
.\lab_infrastructure\EXP0019_faerie_protocol\phase_i08\powershell\compile_fp_i08.ps1
```

## Execution boundary

FP-I08 has no order, position, broker, network, chart-object, or live-execution authority.
`FP-DEC-012` remains open and blocks only the later live-execution phase.

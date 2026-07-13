# EXP0019 Faerie Protocol — FP-I05 Reference Engine

FP-I05 converts the accepted FP-I04 synchronized closed-M1 data plane into deterministic A/L/N/W window aggregates, exact calendar-day N selections, symbol-local HIGH/LOW references, lifecycle evidence, bounded revision invalidation, and restart-safe store checkpoints.

## Core invariants

- A/L/N/W boundaries come only from FP-I03.
- M1 evidence comes only from FP-I04.
- Prior N selection uses exact calendar-day offsets and never compresses missing dates.
- Each symbol has independent HIGH and LOW references.
- Only complete source windows create canonical references.
- Hunter touch does not consume; protected touch consumes.
- Revision invalidation is overlap-bounded.
- No detection, drawing, alert, broker, order, position, or network authority exists.

## Validation

```powershell
$env:PYTHONPATH = @("$PWD\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python","$PWD\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python","$PWD\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i04\python","$PWD\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i05\python") -join ";"
python -m pytest -q .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i05\tests
python .\tools\exp0019\check_fp_i05_boundaries.py .
python .\tools\exp0019\check_fp_i05_mql5_static.py .
python .\tools\exp0019\generate_fp_i05_vectors.py . --verify-only
python .\tools\exp0019\validate_fp_i05_delivery.py .
```

Start with `docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i05/00_FP_I05_DELIVERY_MOC.md`.

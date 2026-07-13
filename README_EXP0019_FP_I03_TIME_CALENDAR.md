# EXP0019 Faerie Protocol — FP-I03 Time, Trading-Day, Session, and Week Kernel

FP-I03 implements the exact temporal foundation used by all later Faerie Protocol modules. It is a deterministic, broker-independent calendar kernel with no price, drawing, or trading authority.

## Canonical semantics

- UTC is the canonical instant axis.
- New York rules are versioned as `FP-NY-US-DST-2007PLUS@1.0.0` for 2007–2099.
- Trading day: previous civil date 18:00 through labeled date 17:00 New York.
- A: `[18:00,04:00)`.
- L: `[04:00,09:30)`.
- N: `[09:30,17:00)`.
- Daily gap: `[17:00,18:00)`.
- Week: `[Sunday 18:00, Friday 17:00)`.
- Broker timestamps require an explicit UTC offset.
- All interval boundaries are half-open.

## Delivered

- 15 Python modules.
- 83 phase tests.
- 12 closed JSON Schemas.
- 11 public contracts and 15 reason codes.
- 12 MQL5 include modules and two diagnostic/self-test entry points.
- 20 conformance checks and 12 exact boundary fixtures.
- 53 detailed delivery notes and 7 atomic Obsidian concepts.

## Quick validation

```powershell
$env:PYTHONPATH = ".\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i02\python;.\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\python"
python -m pytest -q .\lab\10_infrastructure\EXP0019_faerie_protocol\phase_i03\tests
python .\tools\exp0019\check_fp_i03_boundaries.py .
python .\tools\exp0019\check_fp_i03_mql5_static.py .
python .\tools\exp0019\generate_fp_i03_vectors.py . --verify-only
python .\tools\exp0019\validate_fp_i03_delivery.py .
```

## Documentation

Start at:

`docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i03/00_FP_I03_DELIVERY_MOC.md`

## Authority boundary

This phase cannot read market prices, create chart objects, send orders, modify positions, call a broker API, or make network requests. The MQL5 diagnostic reads current time and prints evidence only.

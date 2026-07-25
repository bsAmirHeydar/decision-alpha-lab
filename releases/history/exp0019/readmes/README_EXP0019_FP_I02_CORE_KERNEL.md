# EXP0019 Faerie Protocol — FP-I02 Core Context Types, Identity, and Reason-Code Kernel

## Delivery

FP-I02 freezes the closed public contract surface consumed by every later Faerie Protocol phase. It implements immutable Python records, deterministic semantic/projection identity, closed relation/reason/contract/state registries, strict JSON schemas, an explicit v1-to-v2 migration, MQL5 contract mirrors, self-tests, conformance vectors, and detailed Obsidian documentation.

## Included

- 16 Python modules in `phase_i02/python/fp_i02_kernel`
- 64 phase tests
- 18 closed Draft 2020-12 schemas
- 7 relation descriptors
- 35 reason codes
- 16 public contract descriptors
- 4 lifecycle state machines
- 11 MQL5 include files
- MQL5 contract self-test and diagnostic EAs
- 46 FP-I02 Obsidian notes and 7 atomic concepts
- Exact owner-decision traceability for FP-DEC-001 through FP-DEC-015

## Critical invariants

- Semantic identity is separate from chart projection identity.
- Style changes do not alter `signal_id`.
- Resolved host timeframe, data revision, registry/dependency hashes, relation, windows, roles, times, and policy semantics are identity-bearing.
- Unknown enums, reasons, relations, schema properties, versions, and illegal state transitions fail closed.
- FP-DEC-012 remains explicit as `QuotaConsumptionPolicy.UNSET`.
- Live authority and quota consumption remain blocked while FP-DEC-012 is open.
- FP-I02 performs no history access, detection, drawing, order, broker, position, or network action.

## Validation

```bash
export PYTHONPATH="$PWD/lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python"
pytest -q lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/tests
python lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/run_phase_i02.py
python tools/exp0019/check_fp_i02_boundaries.py .
python tools/exp0019/check_fp_i02_mql5_static.py .
python tools/exp0019/generate_fp_i02_vectors.py --verify-only
python tools/exp0019/validate_fp_i02_delivery.py .
```

MetaEditor compilation is a separate Windows gate and remains `pending_local_windows` until actual zero-error logs are retained.

## Documentation entry

`docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i02/00_FP_I02_DELIVERY_MOC.md`

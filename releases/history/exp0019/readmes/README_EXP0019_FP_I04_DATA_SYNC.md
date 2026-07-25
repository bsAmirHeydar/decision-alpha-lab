# EXP0019 Faerie Protocol — FP-I04 Multi-Symbol M1 Data Plane

FP-I04 implements the canonical two-symbol M1 synchronization layer used by later Faerie Protocol reference and divergence phases.

## Delivered

- exact canonical symbol and alias resolution;
- closed M1 bar validation on a symbol-local tick grid;
- deterministic identical-duplicate deduplication;
- fail-closed conflicting-duplicate handling;
- UTC M1 expected axes derived from the accepted FP-I03 New York calendar;
- explicit `PRESENT`, `MISSING`, `OUT_OF_COVERAGE`, `CONFLICT`, and `REVISED` cells;
- coverage, gap-run, data-revision, cursor, backfill, and dataset-snapshot contracts;
- batch/incremental differential parity;
- Python reference implementation, JSON schemas, MQL5 contract mirror, diagnostics, tests, vectors, and Obsidian documentation.

## Critical invariant

A bar pair is joined only by exact canonical UTC M1 open. No nearest-time join, forward fill, synthetic bar, broker-index join, or silent conflict winner is allowed.

## Authority boundary

This phase has no relation, hunt, divergence, confirmation, indicator, drawing, order, position, broker-action, or network authority.

## Validation

```bash
export PYTHONPATH="$PWD/lab/10_infrastructure/EXP0019_faerie_protocol/phase_i02/python:$PWD/lab/10_infrastructure/EXP0019_faerie_protocol/phase_i03/python:$PWD/lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/python"
pytest -q lab/10_infrastructure/EXP0019_faerie_protocol/phase_i04/tests
python tools/exp0019/check_fp_i04_boundaries.py .
python tools/exp0019/check_fp_i04_mql5_static.py .
python tools/exp0019/generate_fp_i04_vectors.py . --verify-only
python tools/exp0019/validate_fp_i04_delivery.py .
```

Start with:

`docs/execution/EXP0019_faerie_protocol_contextual_divergence/implementation_program/phase_deliveries/fp_i04/00_FP_I04_DELIVERY_MOC.md`

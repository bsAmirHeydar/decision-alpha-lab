---
title: "Test Baseline and Quality Debt"
tags: [strategy-factory, phase-00, testing, qa]
status: canonical
---

# Test Baseline and Quality Debt

## Current baseline

```text
python -m compileall -q lab  → PASS
python -m pytest -q          → FAIL during collection
```

The pytest failure is:

```text
ModuleNotFoundError: No module named 'lab'
```

## Meaning of the failure

The failure does not prove that L-rule or M0001 calculations are wrong. It proves that the repository is not currently packaged or bootstrapped in a way that supports clean-checkout test collection in this environment.

This matters because later Strategy Factory phases depend on reproducible tests. A test that passes only from a particular IDE, terminal working directory, or manually modified `PYTHONPATH` is not a reliable gate.

## Additional test debt

### Live-terminal dependency

Current scripts import `MetaTrader5` and call `connect()`. That makes them integration checks, not unit tests.

### Test naming ambiguity

Files named `test.py` and `test_*.py` contain manual print-oriented runners. Pytest attempts to collect them as tests.

### Interface drift

The M0001 test instantiates the class using a keyword not accepted by the current implementation.

### No frozen fixtures

There is no repository-owned bar fixture with exact expected node and metric outputs.

### No negative cases

Current scripts do not systematically prove behavior for:

- empty data;
- duplicate bars;
- missing symbols;
- equal highs/lows;
- provisional nodes;
- stale cache;
- corrupted Parquet;
- timezone boundaries;
- interrupted writes.

## Phase 00 test suite

The new auditor includes 13 deterministic tests covering:

- happy-path inventory;
- empty input;
- deterministic ordering and hashes;
- comment-safe authority scanning;
- executable authority detection;
- AST contract extraction;
- schema-version mismatch;
- missing schema version;
- duplicate persistence detection;
- missing repository root;
- end-to-end artifact generation;
- duplicate/replayed file hashing.

## Remediation ownership

- packaging and repository test bootstrap: Phase 02;
- fake connector and anatomy adapter fixtures: Phase 06;
- market-clock boundary fixtures: Phase 07;
- outcome ambiguity fixtures: Phase 10;
- anti-overfit fixtures: Phase 12;
- MQL5 differential tests: Phase 18.

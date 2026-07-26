# Phase 12.5 Python Deep Auditor Architecture

## Entry point

`research/exp0017_phase12_5/python/phase12_5_pipeline_integrity.py`

## Design

The script uses only Python's standard library and is deterministic. It loads each CSV once, stores rows by logical file, and runs independent audit passes.

## Passes

1. **File/schema pass** — existence, headers, required fields, primary keys, timestamps.
2. **Lineage pass** — set-based identity reconciliation across phases.
3. **Semantic pass** — strategy and label invariants.
4. **Temporal pass** — walk-forward fold chronology and overlap.
5. **Metric pass** — writer summaries versus physical artifacts.
6. **Readiness pass** — formal Phase 13 gates.
7. **Evidence writer** — CSV, JSON, Markdown, HTML.

## Exit codes

- `0`: usable result; warnings are allowed unless strict mode is enabled.
- `1`: warnings under `--fail-on-warning`.
- `2`: critical Phase 13 block.

## Why Python is authoritative for deep audit

Set reconciliation, duplicate examples, detailed issue rows, and HTML reporting are safer and more scalable outside the terminal. MQL5 remains the local preflight and Python performs full reconciliation.

# Phase 12.5 Obsidian Guide

## Primary MOC

Open:

`[[CG_EXP0017_PHASE12_5_PIPELINE_INTEGRITY_MOC]]`

## Recommended reading order

1. Pipeline Integrity Specification
2. Schema Contract
3. Lineage Reconciliation Contract
4. Semantic Invariants
5. Readiness Gate Contract
6. MQL5 Architecture
7. Python Architecture
8. Validation Plan
9. Handoff to Phase 13

## Review workflow

Link each observed defect to one of four classes:

- producer defect;
- schema migration defect;
- stale/mixed-run artifact;
- downstream reader defect.

Do not encode a workaround in Phase 13. Repair the originating phase and rerun the pipeline.

# Phase 50 Pre-Canon NDS Stabilization

## Purpose

Stabilize the existing NDS Hook implementation before the unresolved Valid Hook / Zone questionnaire is converted into final Canon.

## What changed

- Post-F3 temporal ownership now uses [[Canonical Bar Index Authority]].
- The F3 opposite-direction input is effective instead of decorative.
- `EARLIEST_FIRST` now selects by Hook origin bar first.
- Exact terminal-price tolerance values are respected.
- Selected F3 terminal evidence is carried into Hook sequence state and CSV.
- Summary/debug output declares the active post-F3 contract.

## What did not change

- [[Canonical Valid Visible Set]]
- [[Hook_After_Hook]] lineage semantics
- [[Origin Death Before Terminal Confirmation]]
- the four post-F3 family names
- Zone non-implementation boundary

## Open Canon boundary

The following are not closed by this patch:

- ownership window length and structural termination;
- proof of delayed/rebound movement;
- independent geometric 80% synthesis;
- Hook terminal confirmation count;
- Hook/Zone lifecycle after origin breach;
- all Zone boundary and risk-contract decisions.

## Traceability

- Engineering note: `docs/nds_hook_architecture/67_phase50_pre_canon_nds_stabilization.md`
- QA: `tools/flag_counting/nds_hook_contract_qa.py`
- Audit report: `NDS_PRE_CANON_AUDIT_REPORT.md`

---
title: RTHP UCEE Context Source Boundary
status: contract-ready
version: 1.0.2
---
# UCEE Context Source Boundary

UCEE receives RTHP only as a versioned, known-time-safe Context source.

## Available inputs

- `RTHP_EVENT_VIEW`
- `RTHP_REFERENCE_STATE_VIEW`
- Occurrence and reference-state schemas
- Known-time guards and source lineage

## Forbidden at ACL-03

- Creating unapproved labels.
- Training before an immutable ACL-05 batch.
- Changing Context semantics or state transitions.
- Converting polarity into an automatic trade side.
- Submitting orders or activating capital.

## Readiness

`research_entry_ready=false`

Required next gates: ACL-04 Dual Setup Factory and ACL-05 Immutable Research Batch.

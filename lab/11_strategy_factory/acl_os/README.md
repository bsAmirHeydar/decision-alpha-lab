# ACL-OS Reference Implementations

This package contains architecture-level conformance tests, fixtures and bounded reference implementations. It does not implement production orchestration or authorize trading.

## Implemented phases

- ACL-00 — Constitution and unified authority.
- ACL-01 — Repository identity and artifact locator.
- ACL-02 — Context standard intake.
- ACL-03 — Context compiler and onboarding factory.
- ACL-04 — Dual Setup Factory: human DSL, bounded deterministic AI generation, shared Setup Policy IR, baselines, Treatment validation, deduplication, provenance, exposure ledger and ACL-05 handoff.
- ACL-05 — Immutable Batch and Artifact Store: exact ACL-04 intake, candidate/search freeze, dataset and label contracts, purged walk-forward split, environment and budget locks, content-addressed storage, deterministic Batch identity, event/provenance evidence and ACL-06 handoff.

Each phase has an explicit claim ceiling. A reference implementation must not be interpreted as production readiness, live parity, statistical edge or capital authorization.

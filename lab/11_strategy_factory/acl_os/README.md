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

## ACL-06 — Research DAG Orchestration

Consumes the immutable ACL-05 Batch, plans a closed deterministic DAG, executes bounded descriptive research, writes task receipts and hands evidence to ACL-07. No execution or capital authority is granted.

## ACL-07 — Unified Validation Gate

Consumes ACL-06 descriptive evidence, applies a closed fifteen-gate validation policy, isolates diagnostics, corrects multiple testing and issues immutable non-promotional decisions for ACL-08. No execution or capital authority is granted.

## ACL-08 — Reporting and Experience

Consumes ACL-07 validation decisions and produces deterministic reports, redacted audience views and non-promotional experience candidates for ACL-09. No alpha, promotion, execution or capital authority is granted.

## ACL-09 — Research Memory and Active Planner

Consumes ACL-08 reports and experience records, performs governed append-only memory admission, duplicate analysis and bounded non-executing research planning. No automatic execution, promotion, order or capital authority is granted.

## ACL-10 — Promotion State Machine

Consumes ACL-09 memory and planner evidence, evaluates closed promotion prerequisites, preserves UNKNOWN, isolates baseline and diagnostic sources, and issues deterministic non-executing state decisions for ACL-11. The reference fixture contains zero runtime candidates and grants no runtime, order or capital authority.

## ACL-12 Security Hardening

ACL-12 consumes the ACL-11 non-executable runtime-custody package and produces a reference-only security hardening package and ACL-13 handoff.

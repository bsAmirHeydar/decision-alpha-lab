# Health Snapshot

**Phase:** 19 — Observability, Latency, Drift and Lifecycle Governance  
**Status:** implementation contract  
**Authority:** advisory only; operator approval required

## Purpose

Aggregates active alerts, dropped telemetry, duplicates, schema rejections, and invariant failures into one immutable state. This note is part of the permanent Strategy Factory operating model and applies to research, tester, paper, shadow, micro-live, and live-compatible execution modes.

## Contract

The implementation uses exact versioned identities. Every observation must carry its run and generation lineage, known-time boundary, correlation identity, and canonical hash. Missing lineage is not treated as a soft warning: the record is rejected before it can influence health or lifecycle output.

## Runtime rules

1. The MQL5 fast path uses typed calls and fixed-capacity storage. It does not parse JSON, call network services, train models, or open files.
2. Overflow, duplicates, non-monotonic sequence numbers, schema mismatch, and non-finite values are explicit telemetry-quality evidence. Nothing is silently repaired.
3. Python is an offline conformance, analysis, and reporting implementation. It cannot become the source of live market truth or broker authority.
4. All model, strategy, generation, and account-sensitive conclusions remain bound to the evidence that produced them. Cross-run aggregation requires an explicit offline report.

## Failure behavior

The subsystem fails closed for unknown schema versions, broken causality, incompatible baselines, invalid policies, and corrupted identities. Degradation is represented in an immutable health snapshot. Severe conditions create a recommendation, not a hidden mutation. The operator remains responsible for invoking Phase 14 model governance or Phase 18 safety controls.

## Verification evidence

Verification includes deterministic fixtures, Python unit tests, MQL5 self-tests, static boundary guards, local MetaEditor compilation, and a controlled replay. The expected evidence is the exact input manifest, emitted event sequence, alert transitions, health snapshot, recommendation, and report hash.

## Phase-specific acceptance criteria

- The behavior is deterministic for identical input records, policies, and baseline artifacts.
- Every output is attributable to exact evidence IDs and a known-time boundary.
- Memory and processing costs are bounded before activation.
- No order, position, kill-switch, registry, champion, or deployment mutation occurs inside Phase 19.
- Any operational recommendation sets `requires_operator_approval=true` and `automatic_mutation_allowed=false`.

## Review questions

- Which exact contract version governs this behavior?
- What is the maximum memory and processing cost?
- Which evidence proves causality and lineage?
- What happens under overflow, sparse data, or contradictory signals?
- Which human approval and downstream authority are required before action?

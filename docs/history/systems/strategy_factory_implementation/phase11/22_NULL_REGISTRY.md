---
title: "Null Registry and Versioning"
phase: 11
status: canonical
tags: [strategy-factory, statistics, matched-nulls, phase11]
---
# Null Registry and Versioning

## Scope

This document specifies **Null Registry and Versioning** as a reusable central-engine capability. Strategy-specific interpretations are plugins or declared grouping/null specifications; they are not embedded in the statistics kernel.

## Operational checklist

- Verify source manifest and artifact hashes.
- Reject unsupported schema major versions.
- Keep event-cluster identity attached to every sample.
- Record sample and effective-cluster counts separately.
- Produce explicit status for insufficient sample, unmatched null or non-finite data.
- Preserve deterministic sorting before hashing or exporting.

## Design position

Phase 11 consumes canonical MQL5 outcome identities and does not reconstruct anatomy, candidate geometry, fill semantics or cost semantics. MQL5 owns the source observations and compact online statistics. Python performs deeper cluster-aware intervals, matched-control construction, deterministic report assembly and analytical diagnostics from those canonical exports.

## Mandatory invariants

1. `event_id`, `cluster_id`, `candidate_id` and `outcome_id` are immutable.
2. No statistical row may exist without source run, manifest and artifact lineage.
3. No missing or ambiguous observation may silently improve an estimate.
4. Row count is not treated as independent sample count when rows share a market-event cluster.
5. Conditional groups are declared before report generation and receive stable schema identity.
6. Null controls must be matched on declared context and may not reuse the same market-event cluster when the specification forbids it.
7. Report generation is deterministic for the same source artifacts, registry versions and random seed.
8. A statistical report is evidence, not promotion or capital authority.

## Implementation consequences

- Compact streaming metrics remain available in MQL5 for tester-scale throughput.
- Distributional and cluster-aware analysis runs in Python from exported canonical samples.
- Report bundles contain a manifest, grouped tables, interval tables, null comparisons, Markdown interpretation boundaries and SHA-256 artifact index.
- Phase 12 owns multiple-testing control, purged walk-forward, reality checks, deflated performance and probability-of-overfit gates.

## Acceptance evidence

- Stable hashes reproduce across repeated runs.
- Group output order is deterministic.
- Wilson bounds remain in `[0,1]`.
- Cluster bootstrap samples clusters rather than rows.
- Exact matched nulls enforce stratum, cluster and reuse constraints.
- Empty, partial and invalid states remain explicit.
- Phase-owned MQL5 source contains no live execution authority.

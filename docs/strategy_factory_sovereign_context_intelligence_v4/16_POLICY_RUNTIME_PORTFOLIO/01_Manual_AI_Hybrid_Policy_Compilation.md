---
title: Manual, AI and Hybrid Policy Compilation
status: canonical
version: 4.0.0
created: '2026-07-13'
updated: '2026-07-13'
tags:
- saed-v4
- core-production
---

# Purpose

Compile research outputs into the bounded UCEE I13 policy graph with explicit authority, support, abstention, and fallback.

## Capability tier

**Core Production**

## System design

### Manual baseline

Human eligibility, treatment, vetoes, notes, and validity remain versioned.

### AI roles

Filter, rank, treatment choice, risk suggestion, or timing suggestion only within signed admission.

### Hybrid patterns

Manual eligibility plus AI ranking; AI filter plus manual treatment; regime router plus specialists; manual fallback.

### Compilation

Research model outputs become deterministic typed nodes, not arbitrary code.

## Input contracts

- `SignedAdmission`
- `ManualPolicy`
- `ModelArtifacts`
- `AuthorityMatrix`

## Output contracts

- `CompiledPolicyGraph`
- `FallbackPolicy`
- `ConformanceVectors`

## Measurement framework

- Manual parity.
- AI incremental attribution.
- Fallback equivalence.
- Graph determinism.

## Adversarial questions

- Can AI create a context?
- Can AI select outside support?
- Does fallback change manual behavior?

## Mandatory controls

1. Exact upstream hashes and data roles are recorded.
2. Candidate and failure ledgers are complete.
3. Costs, capacity, missingness, censoring, and support are explicit.
4. Validation uses chronological, cluster-aware, purged folds.
5. Advanced outputs cannot bypass manual policy, hard risk, portfolio, or UCEE promotion.
6. Any runtime handoff requires deterministic export, parity, latency, fallback, and revocation evidence.

## Acceptance boundary

Passing research metrics is necessary but never sufficient. The component remains non-authoritative until its evidence is admitted through UCEE I12, compiled by I14, challenged prospectively under I15, bounded by I17, and qualified under I18.

## Related notes

- [[UCEE_I01_I18_Compatibility]]

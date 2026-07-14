---
title: MQL5 Mirror Contract
status: implemented
version: 1.0.0
phase: V4-00
created: '2026-07-13'
updated: '2026-07-13'
capability_tier: core-production-control-plane
tags:
  - saed-v4
  - v4-00
  - program-constitution
---

# MQL5 Mirror Contract

> **Focus:** Static parity mirror, no trading authority and Windows compile gate.

## Institutional invariant

The phase-zero control plane is **subordinate** to canonical UCEE truth. It does not infer a Context, select a Treatment, sign a promotion, allocate capital, activate a runtime generation, access a broker, or place an order. Its job is to decide whether a research action, evidence use, process amendment or release claim is constitutionally admissible.

```text
Request
→ Closed contract validation
→ Known-time and lineage validation
→ Authority evaluation
→ Evidence-role firewall
→ Objective/baseline gate
→ Independence and budget gate
→ Deterministic constitutional decision
→ Tamper-evident ledger
```

## Hard properties

1. **Deny by default.** An actor receives only authorities listed in the exact-version authority matrix.
2. **No autonomous promotion.** Research agents and researchers cannot sign promotion or activate runtime.
3. **Protected evidence never trains.** Locked-final, prospective, shadow, micro-live and live evidence cannot feed training or adaptive search.
4. **Synthetic evidence is asymmetric.** It may reject or stress a candidate but cannot create positive promotion evidence.
5. **No retroactive governance.** Amendments apply only to programs created after their effective time.
6. **Complete exposure accounting.** Trials, queries, charts, narratives and agent suggestions are counted.
7. **External evidence is typed.** Static checks are never represented as actual MetaEditor compile, parity, shadow or live evidence.
8. **UCEE remains authoritative.** Every I01–I18 crosswalk entry is read-only from SAED.

## Required artifacts

- Active research constitution and SHA-256 hash.
- Exact-version authority matrix.
- Evidence-role policy.
- Objective and mandatory-baseline policy.
- Program manifest with owners and budgets.
- UCEE I01–I18 crosswalk.
- Exposure ledger and budget.
- Constitutional decision ledger.
- Core-boundary snapshot.
- Explicit limitations and external-evidence classification.

## Failure semantics

| Failure | Constitutional result | Required next action |
|---|---|---|
| Unknown field or malformed contract | Reject | Repair contract; never infer defaults |
| Research actor requests hard authority | Reject | Record incident if attempted escalation is material |
| Protected evidence used for training | Reject and quarantine | Invalidate affected trials and lineage |
| Synthetic result used to promote | Reject | Reclassify as stress-only evidence |
| Objective changes without amendment | Require review | Freeze family and submit amendment |
| Reviewer is proposer or same unit | Reject | Assign independent reviewers |
| Exposure budget exhausted | Reject | Stop the hypothesis family |
| Core UCEE snapshot changes | Reject patch | Split work and restore core boundary |
| Static evidence claimed as actual | Reject claim | Correct evidence class and requalify |
| Ledger/hash mismatch | Quarantine | Treat as integrity incident |

## Scale behavior

The kernel is stateless and deterministic. It can run in CI, a research-control service, an air-gapped hidden-evaluation service, or a local CLI. State is kept in immutable registries and hash-chained ledgers. Work can be sharded by program, hypothesis family, Context Cell and evidence role without weakening the constitution.

## Design focus

Static parity mirror, no trading authority and Windows compile gate. This area is implemented as a closed, exact-version contract rather than an informal convention. Unknown fields are rejected, hashes are pinned and all decisions carry explicit reason codes.


## Reference implementation

Python package:

```text
lab/11_strategy_factory/python/saed_v4_constitution/
```

The package separates pure policy evaluation from I/O. `ConstitutionKernel` composes the authority matrix and evidence firewall. Amendment, waiver, review, exposure, registry, ledger, bundle, crosswalk and core-boundary modules remain independently testable.

MQL5 mirror:

```text
mql5/Include/AlphaLab/StrategyFactory/SAEDV4Constitution/
```

The mirror exists only to verify that runtime-side diagnostics preserve the same denial semantics. It has no order-management implementation and static validation rejects trading/network tokens.

## Review questions

- Which actor is making the request and which organization unit owns that actor?
- What exact evidence role is involved, and what operation is requested?
- Is the claim descriptive, predictive, causal, stress-only or operational?
- Does the request change any frozen Objective, Baseline, Support, Treatment universe or Evidence role?
- Is the request prospective, independently reviewed and inside its exposure budget?
- Does the output preserve UCEE authority and the additive core boundary?
- What deterministic failure reason will be emitted if any invariant is absent?

## Audit evidence

Every accepted or rejected request is represented by a stable request ID and a deterministic decision ID. Operational timestamps may be recorded in the surrounding audit event, but they are not allowed to change the semantic identity of the request or decision. This permits exact replay after restart and independent reconstruction.

## Acceptance checklist

- [ ] All closed schemas validate under JSON Schema Draft 2020-12.
- [ ] Golden examples validate and negative examples fail for the intended reason.
- [ ] Research actors cannot obtain order, broker, network, risk, portfolio, runtime, promotion or context-mutation authority.
- [ ] Protected evidence cannot train or tune.
- [ ] Synthetic stress cannot positively promote.
- [ ] Objective drift requires a prospective amendment.
- [ ] Two independent approvals are mandatory.
- [ ] Non-waivable rules remain non-waivable.
- [ ] Exposure budget exhaustion stops the family.
- [ ] Decision replay is deterministic.
- [ ] Ledger tampering is detected.
- [ ] UCEE crosswalk has no mutation permission.
- [ ] Static MQL5 evidence is labeled `pending_local_windows` for actual compile.
- [ ] Patch file index changes only additive phase-zero paths.

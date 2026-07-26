---
title: ACL-04 — Dual Setup Factory
status: accepted-reference-implementation
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, acl-04, implementation]
---
# ACL-04 — Dual Setup Factory

## Delivery decision

ACL-04 is accepted as a **reference implementation** of bounded Setup definition mechanics. It consumes the immutable `ACL03_TO_ACL04` handoff and emits `ACL04_TO_ACL05`. The accepted claim ceiling is `SETUP_DEFINITION_REFERENCE_ONLY`.

## Implemented vertical slice

- ACL-03 bundle and digest binding.
- Subject-bound `ACL04_BUILD_SETUP_UNIVERSE` authority permit.
- Content-addressed Search Authority and Treatment envelope.
- Closed human Setup DSL.
- Registered deterministic Cartesian AI generator.
- Shared Setup Policy IR for human, AI and baseline lanes.
- Atom/action registry, finite parameter domains and constraint evaluation.
- Mandatory baselines including segregated diagnostic oracle.
- Canonical behavior hashing, stable IDs and cross-lane deduplication.
- Complete search-exposure ledger and provenance graph.
- Generated Obsidian projections, output manifest and factory receipt.
- Bounded ACL-05 handoff with no execution or capital authority.
- Python reference service, CLI, schemas, policies, fixtures, tests and static MQL5 mirrors.

## Architecture

```text
ACL03_TO_ACL04
      │
      ▼
Handoff + Authority Binding ──► Security Boundary
      │
      ├──────── Human DSL Compiler
      │
      ├──────── Bounded AI Generator
      │
      └──────── Baseline Program
                    │
                    ▼
            Setup Policy IR
                    │
      Search / Treatment / Known-Time Constraints
                    │
                    ▼
 Canonicalization ─ Deduplication ─ Provenance
                    │
                    ▼
 Exposure Ledger + Obsidian Projections + Receipt
                    │
                    ▼
              ACL04_TO_ACL05
```

## Non-claims

This phase does not run market research, evaluate returns, train predictive models, submit orders, compile broker-specific execution, prove MQL5 parity, promote a strategy or activate capital. Those claims require later lifecycle evidence and authority.

## Acceptance evidence

Acceptance requires the ACL-04 pytest suite, closed-schema and policy validation, deterministic replay of the reference fixture, static non-trading MQL5 scan, security-negative checks, artifact inventory, SHA-256 ledger and clean-checkout delivery validation.

## Operational entry point

```powershell
python -m src.engine.tooling.strategy_factory.acl_os.acl_04.cli `
  lab/11_strategy_factory/acl_os/fixtures/acl_03/reference_compilation `
  .acl04-output `
  --authority-permit lab/11_strategy_factory/acl_os/fixtures/acl_04/authority_permit.json `
  --search-authority lab/11_strategy_factory/acl_os/fixtures/acl_04/search_authority.json `
  --treatment-envelope lab/11_strategy_factory/acl_os/fixtures/acl_04/treatment_envelope.json `
  --human-setup lab/11_strategy_factory/acl_os/fixtures/acl_04/human_setup.yaml `
  --ai-request lab/11_strategy_factory/acl_os/fixtures/acl_04/ai_request.json
```

## Handoff

ACL-05 may freeze the candidate universe and exposure ledger into an immutable research Batch. ACL-05 may not infer alpha, authorize execution, activate capital or mutate candidate behavior.

## Related

- [[04_SETUP_FACTORY/00_MOC]]
- [[ACL_03_CONTEXT_COMPILER_AND_ONBOARDING]]
- [[ACL_05_IMMUTABLE_BATCH_AND_STORE]]
- [[ADR_006_DUAL_LANE_SETUP_SINGLE_IR]]

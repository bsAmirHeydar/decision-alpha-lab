---
title: "Security and Authority Boundary"
phase: 04
status: canonical
---

# Security and Authority Boundary

## Objective

Keep anatomy plugins outside risk and broker authority.

## Canonical decision

No anatomy plugin may size volume, approve capital or send orders.

## Architectural position

Phase 04 is a central-engine phase. It does not migrate NDS, EXP0017, Daye, ICT, Structural Nodes or any other legacy anatomy. It creates the permanent admission boundary those systems must satisfy later.

The live authority chain is:

```text
MQL5 shared market services
→ statically registered anatomy factory
→ exact plugin version
→ explicit resource requirements
→ bounded plugin lifecycle
→ canonical AnatomyEvent
```

Python mirrors metadata, validates artifacts and runs conformance tests. It does not own live discovery, event ordering or anatomy meaning.

## Required invariants

1. Plugin identity and semantic version are explicit.
2. Update scopes and capabilities are declared before startup.
3. Required symbols, timeframes, lookbacks, freshness and synchronization constraints are declared.
4. The plugin consumes only shared market/time/specification ports.
5. Emitted events pass the Phase 01 canonical contract.
6. Event IDs are deterministic and duplicate emission is rejected.
7. The event queue is bounded and overflow behavior is explicit.
8. Missing required data fails closed.
9. No plugin owns candidate, risk, model or broker authority.
10. Runtime behavior can be reconstructed from versioned configuration and audit evidence.

## Failure semantics

A contract error, unmet required dependency, illegal lifecycle transition, invalid event, queue overflow under a fail policy or replay mismatch must produce an explicit failure state. The engine must not silently downgrade a required condition into a guessed market state.

Optional requirements may degrade health but must remain observable in telemetry and run evidence.

## Verification

- Python contract and parity tests
- Static MQL5 boundary scan
- Exact registry resolution tests
- Queue duplicate and overflow tests
- Startup readiness tests
- Golden fixture replay
- MetaEditor compile
- MQL5 self-test EA journal evidence

## Relationship to later phases

Phase 05 will compile the selected plugin and configuration into an immutable runtime generation, bind append-only result sinks and add atomic generation activation and rollback. Candidate generation and outcome simulation remain later phases.

## Operational checklist

- [ ] Descriptor validates.
- [ ] Required capabilities are present.
- [ ] Requirements validate against shared services.
- [ ] Exact factory resolves.
- [ ] Queue capacity and overflow policy are tested.
- [ ] Golden fixture IDs are stable.
- [ ] No terminal-market or live-order API leaks into the plugin.
- [ ] Local compile and self-test pass.

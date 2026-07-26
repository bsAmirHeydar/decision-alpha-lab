---
id: UCPS-D344B0B95B32
title: "Non-Negotiable Invariants"
type: standard
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - consolidation
  - platform-seal
---
# Non-Negotiable Invariants

## Preservation invariants

- No material behavior is deleted before a canonical destination and preservation certificate exist.
- Historical recoverability is independent of the active working tree.
- File moves preserve Git history where practical.
- Existing stable artifact IDs are retained; path changes do not create new identities.

## Architecture invariants

- One canonical owner and one production implementation per shared capability.
- Context-specific logic never enters shared code without a demonstrated universal abstraction.
- Research cannot create broker or capital authority.
- Runtime consumes approved artifacts and does not import training implementations.
- External systems are accessed only through adapters.

## Time and evidence invariants

- Known-time and closed-bar semantics remain explicit and testable.
- Final-test and prospective evidence cannot be retroactively rewritten.
- Generated artifacts identify source digest and compiler version.
- Unknown mandatory evidence blocks progression.

## Repository invariants

- The repository itself is Alpha Lab; no nested product root repeats that identity.
- Root content is allowlisted.
- Production code has one root.
- Generated, runtime and historical artifacts do not masquerade as authored source.

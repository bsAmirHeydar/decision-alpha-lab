---
id: UCPS-950286389A8F
title: "Release Snapshot and Active Source Separation"
type: architecture-decision
status: accepted
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-27
updated: 2026-07-27
tags:
  - consolidation
  - uc04
  - integrity
  - immutable-evidence
  - active-source
---
# Release Snapshot and Active Source Separation

## Incident

UC04-W0 recorded every delivered path and SHA-256 in one historical patch ledger. The W0 verifier later treated that ledger as a permanent equality constraint on all 356 hashed paths, including active verifiers, tests and implementation modules.

This created three systemic failures:

1. a legitimate correction to an active verifier invalidated the historical stage that contained its old bytes;
2. correcting the verifier required a hard-coded amendment inside the same verifier, creating a self-referential maintenance loop;
3. checkout representations such as CRLF PowerShell files and hydrated Git LFS objects could differ from release-ZIP bytes without changing repository meaning.

## Decision

An accepted patch ledger is an audit snapshot of what was delivered. It is not a permanent lock on every active source file that happened to be present in that patch.

Historical integrity now has three distinct boundaries:

| Boundary | Continuing rule |
|---|---|
| Immutable stage evidence | Exact canonical content remains enforced. Corrections require an append-only generic amendment chain. |
| Evolvable active source and tests | The historical ledger proves inclusion and requires the path to remain accounted for, but current bytes are governed by current tests, schemas and stage verifiers. |
| Explicit semantic freeze | Exact behavior-critical identities remain governed by `semantic_baseline_freeze.json` until an approved semantic transition supersedes them. |

## Immutable W0 evidence

The active policy classifies the following historical W0 areas as immutable:

- the W0 release-control packet;
- W0 machine decisions under `registry/consolidation/uc04/w0/`;
- the W0 UC04 schemas delivered by the stage;
- the W0 Obsidian record set.

Everything else in the W0 patch index is treated as evolvable active material unless another explicit freeze governs it.

## Canonical content

Text content is compared after newline normalization to LF. This removes platform-only CRLF/LF differences while preserving every other byte, including UTF-8 BOM presence. Binary content is compared byte-for-byte.

Git LFS remains governed by the separate pointer-or-hydrated-object contract: canonical pointer metadata comes from Git when available, while a hydrated working tree must match pointer size and SHA-256.

## Generic amendments

The verifier discovers append-only amendment documents from the policy-defined amendment roots. It validates authority fields, document digests and a non-forking previous-to-current hash chain. No future immutable-evidence correction requires editing the W0 verifier or hard-coding a new recovery stage.

Amendments attached only to active/evolvable source remain historical records; they do not permanently pin the active file to the amendment's terminal hash.

## Preserved invariants

- The original W0 ledger is not rewritten.
- Missing paths still fail closed.
- Immutable evidence tampering still fails closed.
- Semantic baseline hashes remain strict.
- No semantic, runtime, order or capital authority is created.
- No market concept, trading rule, consumer or MQL5 behavior changes.

## Non-goals

This decision does not weaken current-stage tests, authorize deletion, change RTHP semantics, modify execution logic, alter Git LFS ownership, or accept arbitrary content drift in immutable evidence.

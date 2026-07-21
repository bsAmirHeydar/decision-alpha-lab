---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# LCM-09B Implementation Handbook

## 1. Purpose

This handbook is the durable implementation contract for the second Setup migration subphase. It explains how the accepted LCM-09A freeze is transformed into canonical Setup reference packages, how those references are exposed to the ACL-04 Setup Factory without becoming candidates, and how missing semantic evidence remains visible as blocking state.

The implementation is deliberately complete in accounting and deliberately incomplete in domain semantics. LCM-09A authorized zero Setup identities for semantic implementation. LCM-09B therefore creates one deterministic, content-addressed, fail-closed package per frozen identity and refuses to manufacture eligibility, trigger, confirmation, invalidation, cancellation, expiry, abstention, entitlement, Context, or Treatment meaning.

## 2. Bound input

The only portfolio authority is the accepted LCM-09A handoff:

- handoff digest: `sha256:9010023f1b182049cc9f7e0601689827c062f2dbb15e21a98d652744c625d2fb`
- freeze ID: `SETUPFREEZE_8638449DF9A774634FE9B8F9E17EF891`
- frozen identities: 60
- canonical contracts: 60
- implementation-authorized identities: 0

The service refuses a handoff digest mismatch and a portfolio count mismatch. It reads the frozen inventory and contracts, validates source bindings, and generates deterministic output under `SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9`.

## 3. Processing algorithm

For each frozen Setup identity, in lexical `setup_id` order:

1. bind the source path, SHA-256, identity digest, contract ID, and contract digest;
2. aggregate upstream blocking reasons and add `LCM09B_UPSTREAM_IMPLEMENTATION_NOT_AUTHORIZED`;
3. create one append-only blocker record per reason code;
4. materialize a canonical package with the complete rule surface present and unknown rules encoded as `null`;
5. set package status to `REFERENCE_BLOCKED` and `executable_reference` to `false`;
6. bind Context as read-only and prohibit an independent Context clock or recomputation;
7. declare Treatment binding `PENDING_LCM10` and prohibit Treatment semantics inside Setup core;
8. create a translation-only adapter registration that cannot execute legacy source;
9. create an ACL-04 reference registration with promotion, runtime, order, and capital authority all false;
10. emit a blocked golden case, blocked trace, restart checkpoint, parity disposition, Treatment dependency seed, and migration ledger event.

After all identities are processed, the service emits portfolio registries, provenance, hostile review, acceptance evidence, the exact artifact locator, a manifest, receipt, and bounded LCM-10A handoff.

## 4. Canonical package rule surface

Every package has eight named rule slots:

- eligibility;
- trigger;
- confirmation;
- invalidation;
- cancellation;
- expiry;
- abstention;
- entitlement.

A `REFERENCE_READY` package would require the mandatory rules to be structurally valid expressions and would require zero blockers. A `REFERENCE_BLOCKED` package must retain at least one blocker, must not be executable, and evaluates only to a first-class `BLOCKED` / `no_trade=true` decision.

## 5. Determinism

Persistent IDs are SHA-256-derived from stable bound inputs. JSON uses sorted keys; JSONL records are sorted by Setup identity; output manifests bind path, byte count, and SHA-256; handoff and receipt objects use self-excluding canonical digests. Wall-clock time is not an identity input. Rebuilding from the same LCM-09A handoff produces byte-identical canonical outputs.

## 6. Failure behavior

- upstream digest mismatch: hard failure;
- missing frozen identity or contract: hard failure;
- malformed package: hard failure;
- unknown rule semantics: explicit blocker, never inferred;
- absent legacy trace: parity `BLOCKED`, never `PASS`;
- incomplete known-time snapshot: evaluator rejects the input;
- blocked adapter: normalization rejects the request;
- Factory authority field not false: registration load fails;
- manifest or digest tamper: verification fails;
- incomplete publication: package is not deliverable.

## 7. Authority boundary

LCM-09B creates no promotion, runtime, order, capital, consumer-cutover, source-move, source-delete, or semantic-refactor authority. The Factory extension is a diagnostic reference port and is intentionally separate from normal candidate compilation. No MQL5 source is imported or executed by Python migration tooling.

## 8. Closure meaning

Closure means that all 60 frozen identities have one visible, machine-validated disposition and no identity disappeared between inventory and Factory reference registration. It does not mean that the 60 Setups are behaviorally approved or executable. Those claims remain blocked until owners provide observed characterization, exact rule semantics, canonical Context bindings, Treatment identities, and parity evidence.

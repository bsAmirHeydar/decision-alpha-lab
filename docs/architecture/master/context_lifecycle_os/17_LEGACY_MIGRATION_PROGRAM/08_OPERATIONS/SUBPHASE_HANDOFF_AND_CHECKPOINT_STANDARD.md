---
title: "Subphase Handoff and Checkpoint Standard"
status: implemented-reference
version: 1.0.0
updated: 2026-07-19
tags: [acl-os, lcm, legacy-migration, operations]
roadmap_id: LCM_ROADMAP_R1_BALANCED_PARTITION
---
# Subphase Handoff and Checkpoint Standard

## Purpose

Preserve exact continuity when a heavy master phase is implemented through two or three patches and when long internal processing must survive interruption.

## Internal checkpoint versus accepted handoff

An internal checkpoint is a resumable work record. It may contain partial registries, scan shards, cached hashes and failed diagnostics. It has no lifecycle authority and must not be staged as the phase result unless explicitly listed as diagnostic evidence.

An accepted handoff is immutable, digest-bound and issued only after the subphase acceptance gate passes. The next subphase consumes the handoff, not an inferred repository state.

## Required checkpoint fields

- roadmap ID, master phase and subphase;
- checkpoint sequence and deterministic ID;
- exact input digest;
- completed and pending workstreams;
- generated artifact paths and hashes;
- failures, blockers and UNKNOWNs;
- resumption command and idempotency notes;
- environment/tool versions where material.

## Required handoff fields

- source and output package digests;
- accepted artifact inventory;
- completed non-compensatory gates;
- failed, blocked and unknown dimensions;
- variance/waiver decisions;
- owner and reviewer approvals;
- allowed next actions;
- forbidden actions;
- rollback package and verification result;
- residual risks and expiry/review conditions.

## Continuity rules

1. The next subphase must verify the upstream handoff before work.
2. A handoff cannot be reconstructed from README text.
3. A later patch cannot silently edit an accepted upstream registry; it must publish an amendment or superseding version.
4. Interrupted work resumes from the newest valid checkpoint whose input digest still matches.
5. If the repository changed outside the checkpoint scope, the checkpoint is invalid and the workstream must rebase or restart.
6. Partial output must never be treated as PASS because most files were generated.

---
title: "LCM-01 Cross-Platform Integrity Hotfix"
status: implemented-hotfix
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, integrity, windows, crlf]
phase_id: LCM-01
claim_ceiling: CROSS_PLATFORM_INSTALLATION_VERIFICATION_ONLY
---
# LCM-01 Cross-Platform Integrity Hotfix

## Defect

The original installation verifier compared frozen LF repository hashes directly with a Windows working tree materialized by Git under `core.autocrlf=true`. CRLF checkout conversion therefore produced false `HASH_MISMATCH` findings even when Git reported a clean worktree and the package verifier passed.

## Corrected rule

Raw SHA-256 remains authoritative. After a raw mismatch, a file may pass only when all of the following are true:

1. the file is classified as text by the closed extension/binary registry and UTF-8 safety check;
2. the current bytes differ from their LF-canonical form;
3. replacing CRLF and solitary CR with LF reproduces the exact frozen baseline SHA-256.

No trimming, Unicode normalization, encoding conversion, final-newline insertion, whitespace rewrite, or semantic transformation is permitted.

Binary files never receive EOL canonicalization. Missing files, symlinks, path escapes, unreadable files, and genuine content changes remain fail-closed.

## Boundary

This hotfix does not modify the frozen baseline, Survey package, dependency inventory, capability findings, event ledger, provenance graph, LCM-02 handoff, Context logic, Setup logic, runtime authority, order authority, or capital authority.

## Verification evidence

The hotfix adds tests for:

- LF baseline against CRLF Windows checkout;
- genuine text mutation rejection;
- binary mutation rejection;
- path-escape rejection;
- exact line-ending-only canonicalization.

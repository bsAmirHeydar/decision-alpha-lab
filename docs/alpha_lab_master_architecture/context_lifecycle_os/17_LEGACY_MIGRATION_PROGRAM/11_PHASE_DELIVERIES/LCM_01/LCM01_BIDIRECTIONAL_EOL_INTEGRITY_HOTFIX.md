---
title: "LCM-01 Bidirectional EOL Integrity Hotfix"
status: implemented-corrective
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, integrity, windows, linux, eol]
phase_id: LCM-01
claim_ceiling: CROSS_PLATFORM_INSTALLATION_INTEGRITY_ONLY
---
# LCM-01 Bidirectional EOL Integrity Hotfix

## Evidence

The full baseline diagnostic classified all 874 non-raw working-tree matches as EOL-only equivalents:

- `LF_MATCH`: 768;
- `CRLF_MATCH`: 106;
- unresolved: 0.

## Corrective rule

Raw SHA-256 remains authoritative. After a raw mismatch, only UTF-8 text receives the two closed EOL materializations:

- all LF;
- all CRLF.

The file passes only when the frozen baseline digest matches one of those exact byte streams.

## Prohibited normalization

- whitespace trimming;
- Unicode normalization;
- encoding conversion;
- final-newline repair;
- semantic serialization;
- binary conversion;
- arbitrary newline insertion or deletion.

## Operational correction

The PowerShell apply script now validates `$LASTEXITCODE` after every Python, pytest, and Git command. A failure prevents all later commit and push actions.

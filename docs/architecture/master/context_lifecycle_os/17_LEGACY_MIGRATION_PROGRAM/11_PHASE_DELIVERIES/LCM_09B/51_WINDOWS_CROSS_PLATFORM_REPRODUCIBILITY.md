---
status: accepted-reference
version: 1.0.1
updated: 2026-07-21
tags: [acl-os, lcm, lcm-09b, windows, powershell, reproducibility]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Windows and Cross-Platform Reproducibility

## Source binding semantics

Legacy Setup source bindings represent repository content, not the newline form
chosen by a local checkout. Text sources therefore use deterministic LF newline
normalization before SHA-256 calculation. Binary artifacts remain byte-exact.
This preserves source mutation detection while allowing the same frozen binding
to verify on Windows CRLF and Linux LF checkouts.

## Rebuild determinism semantics

A clean rebuild is byte deterministic when repeated against the same bound input
and target. Core generated artifacts must also match the committed package
byte-for-byte across platforms. Publication wrappers may contain explicitly
installation-bound metadata; their stable semantic view must remain identical.
No domain rule, Setup state, blocker, Factory registration, parity disposition,
or handoff authority may vary by operating system.

## PowerShell operator policy

All Alpha Lab patch workflows are executed from Windows PowerShell. Patch
expansion uses `Expand-Archive`, removal uses `Remove-Item`, validation commands
stop on non-zero exit codes, and Git staging uses the exact phase path index.
Broad staging commands remain prohibited.

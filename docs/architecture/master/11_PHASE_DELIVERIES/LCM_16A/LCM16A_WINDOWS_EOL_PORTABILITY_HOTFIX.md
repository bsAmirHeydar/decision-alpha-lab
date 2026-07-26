---
id: ALPHA-LAB-LCM16A-WINDOWS-EOL-PORTABILITY-HOTFIX
title: LCM-16A Windows EOL Portability Hotfix
status: implemented-reference
version: 1.0.0
phase: LCM-16A
claim_ceiling: LCM_16A_EOL_PORTABILITY_HOTFIX_REFERENCE_ONLY
---

# LCM-16A Windows EOL Portability Hotfix

## Incident

A Windows worktree produced a false `unapproved baseline drift` result for `ACL_OS_06_ARTIFACT_INVENTORY.csv`. Git considered the worktree clean, but the verifier hashed physical CRLF bytes while the LCM-15C lock recorded LF bytes.

## Invariant

EOL representation is not semantic content. Integrity comparison may accept raw, LF, or CRLF representations of the same valid UTF-8 text. It must remain raw-byte strict for binary content and reject every non-EOL mutation.

## Boundaries

- No arbitrary drift allowlist.
- No path wildcard amendment.
- No whitespace normalisation.
- No Unicode normalisation.
- No binary normalisation.
- No weakening of the 242-path AIEOS amendment boundary.
- No authority creation.

## Acceptance

- known ACL-06 LF and Windows CRLF representations match one logical lock;
- semantic mutation fails;
- binary mutation fails;
- LCM-15A, LCM-15B, and LCM-15C historical verifiers pass;
- LCM-16A package QA can rebuild the bound amendment result on Windows.

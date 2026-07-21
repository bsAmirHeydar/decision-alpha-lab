---
title: RTHP ACL-03 Validation, QA, and Reproduction
status: passed
version: 1.0.2
---
# Validation, QA, and Reproduction

## Validation layers

1. RTHP package validation and fixture validation.
2. Official ACL-02 re-evaluation after the compiler-compatibility release.
3. Official ACL-03 deterministic compilation.
4. Golden replay with zero failures.
5. Security boundary and extension compatibility checks.
6. RTHP-specific SAED/UCEE binding validation.
7. Byte/digest determinism through two independent recompilations.
8. RTHP, ACL-02, ACL-03, and UCEE Context regression tests.
9. English-only content audit for all patch text paths.
10. Exact path inventory and SHA-256 ledger verification.

## Reproduction

The operator command recompiles into a temporary directory and requires the resulting receipt and binding-bundle digests to match the committed artifacts. Any source drift invalidates the snapshot-bound approval.

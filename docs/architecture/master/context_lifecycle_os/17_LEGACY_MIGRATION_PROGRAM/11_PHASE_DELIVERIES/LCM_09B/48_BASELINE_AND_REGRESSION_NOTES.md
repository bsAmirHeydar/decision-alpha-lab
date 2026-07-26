---
status: accepted-reference
version: 1.0.0
updated: 2026-07-20
tags: [acl-os, lcm, lcm-09b, setup-migration]
phase_id: LCM-09B
claim_ceiling: LCM_09B_REFERENCE_ONLY
---
# Baseline and Regression Notes

## Supplied baseline

The supplied project ZIP was treated as the immutable pre-patch baseline. No earlier experimental patch from this conversation is assumed to have been applied.

## Pre-existing failures

A clean extraction of the supplied ZIP reproduces two upstream generated-evidence integrity failures:

1. `tests_lcm_09a/test_schema_and_manifest.py::test_output_manifest_matches_files`;
2. `tests_lcm_08c/test_package_verification.py::test_reference_package_verifies` for `registries/context_blocker_registry.csv`.

The same two failures appear when the broader upstream suites are run after LCM-09B. The patch does not touch the affected LCM-08C/LCM-09A package files, so the failures are recorded as baseline debt rather than attributed to this phase.

## Bounded regression policy

LCM-09B acceptance requires:

- all phase-direct tests pass;
- all ACL-04 tests pass, including the new reference-port extension;
- package verification and QA pass;
- a clean original ZIP plus patch overlay passes the same direct and bounded suites;
- ZIP CRC and byte parity pass;
- source mutation count is zero.

The upstream baseline failures are not hidden, skipped, or converted into success. They are explicitly excluded from the LCM-09B direct acceptance count and retained in the QA report with clean-baseline reproduction evidence.

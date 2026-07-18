---
title: Research Memory
status: accepted-reference
version: 2.0.0
updated: 2026-07-18
tags: [acl-os, acl-09, memory]
---
# Research Memory

ACL-09 implements governed research-memory admission. It consumes immutable ACL-08 experience records, verifies their validation lineage, detects exact and near duplicates, applies poisoning defenses and emits an append-only memory snapshot.

A source record is never rewritten. Exact duplicates become aliases to one canonical memory entry. Diagnostic experience is quarantined. Baseline experience is retained as reference. UNKNOWN and explicit negative knowledge remain distinct.

Memory does not imply truth, alpha, promotion or execution authority. It is an indexed evidence history governed by versioned policy.

## Related
- [[ACL09_MEMORY_ADMISSION_POLICY]]
- [[ACL09_DUPLICATE_AND_EQUIVALENCE_REPORT]]
- [[ACL09_MEMORY_POISONING_DEFENSE]]

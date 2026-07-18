---
title: "Duplicate and Equivalence Policy"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Duplicate and Equivalence Policy

## Four levels

- **Byte duplicate:** identical SHA-256.
- **Normalized-text candidate:** differences limited to formatting or comments; still requires review.
- **Structural candidate:** similar control flow or declarations.
- **Semantic equivalent:** identical behavior over approved golden, edge and metamorphic cases.

Only byte duplicates can enter a direct consolidation review. Structural similarity never proves semantic equivalence. A semantic merge requires owner-approved scope, golden traces, state/event parity and a retained alias map.

The exact duplicate Astro oscillator pair is a candidate, not an automatic deletion.

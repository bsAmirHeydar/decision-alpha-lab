---
title: "Phase Gate Matrix"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Phase Gate Matrix

| Gate | 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07–12 | 13 | 14 | 15 | 16 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| baseline integrity | R | R | R | R | R | R | R | R | R | R | R | R |
| ownership | D | D | R | R | R | R | R | R | R | R | R | R |
| behavioral trace | - | - | - | - | D | R | R | R | R | R | R | R |
| parity | - | - | - | - | D | - | D | R | R | R | R | R |
| deletion eligibility | - | - | - | - | - | - | - | - | - | D | R | R |

`D` means produced; `R` means required.

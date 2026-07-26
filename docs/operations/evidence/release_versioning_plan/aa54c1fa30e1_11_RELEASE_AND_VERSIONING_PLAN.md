---
title: "Release and Versioning Plan"
tags:
  - strategy-factory
  - implementation-roadmap
  - alpha-lab
status: canonical
doc_version: 1.0.0
---

# Release and Versioning Plan

## Version Domains

Version independently:

- contracts;
- strategy doctrine;
- anatomy adapter;
- feature set;
- candidate universe;
- label policy;
- cost model;
- fold plan;
- model artifact;
- decision policy;
- risk profile;
- broker profile;
- runtime generation.

## Release Channels

- `dev`: active implementation;
- `research`: reproducible offline use;
- `paper`: forward paper authority;
- `micro_live`: restricted real capital;
- `production`: approved capital authority;
- `retired`: no new decisions.

## Rollback

Every runtime generation must be immutable and retain the previous known-good generation for atomic rollback.

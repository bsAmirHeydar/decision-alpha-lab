---
title: "Authority Approval Matrix"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Authority Approval Matrix

| Change | Domain owner | Migration engineer | Parity reviewer | Security reviewer | Release operator |
|---|---:|---:|---:|---:|---:|
| inventory | optional | required | optional | optional | required |
| semantic specification | required | required | required | conditional | required |
| move-only | informed | required | review | conditional | required |
| behavior refactor | required | required | required | conditional | required |
| execution adapter | required | required | required | required | required |
| quarantine | required | required | required | conditional | required |
| deletion | required | required | required | required for restricted files | required |

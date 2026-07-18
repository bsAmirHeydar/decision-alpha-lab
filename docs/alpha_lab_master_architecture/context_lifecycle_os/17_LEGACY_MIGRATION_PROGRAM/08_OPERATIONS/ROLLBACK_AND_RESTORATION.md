---
title: "Rollback and Restoration"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Rollback and Restoration

Rollback is tested at three levels: phase patch revert, domain wave rollback and quarantine restoration. Redirect wrappers and canonical locator versions support controlled fallback. After controlled deletion, rollback uses the tagged archive bundle rather than reconstructing source from memory.

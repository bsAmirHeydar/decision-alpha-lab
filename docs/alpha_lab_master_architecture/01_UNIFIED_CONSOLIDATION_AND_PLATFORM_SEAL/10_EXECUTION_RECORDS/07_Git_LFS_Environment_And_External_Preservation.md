---
id: UCPS-UC01-ENVIRONMENT-F413E9C2
title: "Git, LFS, Environment and External Preservation"
type: operations_standard
status: approved
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-23
updated: 2026-07-23
tags:
  - git
  - lfs
  - environment
---
# Git, LFS, Environment and External Preservation

The environment manifest records sanitized Git metadata, Python implementation, operating system, installed package names and versions, required command versions and detected MetaTrader or MetaEditor executables. Remote URLs have user information removed. Environment variables are limited to a safe allowlist.

Git LFS files are inventoried by path, object SHA-256, materialization marker, existence and current byte size. A pointer in place of required materialized content is blocking.

External consumer and terminal surveys use templates under `registry/consolidation/uc01/templates/`. They must record scope explicitly; lack of observation is not proof of absence.

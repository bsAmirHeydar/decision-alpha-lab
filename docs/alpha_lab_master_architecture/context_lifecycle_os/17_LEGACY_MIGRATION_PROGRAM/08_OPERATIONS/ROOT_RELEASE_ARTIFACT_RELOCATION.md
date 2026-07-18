---
title: "Root Release Artifact Relocation"
status: proposed-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, legacy-migration]
---
# Root Release Artifact Relocation

Target locations:

- manifests, inventories, hashes and QA: `registry/releases/<program>/<release_id>/`;
- installer scripts: `tools/release/powershell/<program>/`;
- release notes and human handoff: `docs/releases/<program>/<release_id>/`;
- large binary patches: external artifact store or approved archive location.

Locator entries and redirects are installed before root files move. Historical commit instructions remain readable.

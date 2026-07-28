---
id: UCPS-N1-03-EVIDENCE
title: "UC04-W1B-N1 Evidence Bundle and Authority Boundary"
type: authority-record
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-28
updated: 2026-07-28
tags:
  - consolidation
  - uc04
  - evidence
  - safety
---
# UC04-W1B-N1 Evidence Bundle and Authority Boundary

## Export contract

The shareable ZIP contains only evidence needed for independent review: sanitized receipt, independent review, compile logs, compiled EX5 copies, runtime CSV, bundle manifest and—when generated—the cutover candidate manifest. Absolute repository, terminal, MetaEditor and user-profile paths are removed from the exported receipt.

The bundle declares that it contains no credentials, broker secrets, account identifiers or apply authority. Every member is SHA-256 bound in `bundle_manifest.json`.

## Explicitly permitted

- compile the twelve frozen targets in an isolated mirror;
- run the thirteen-vector test-only script with live trading and DLL imports disabled;
- write evidence under `%LOCALAPPDATA%` and MT5 Common Files;
- independently recompute hashes and fixture equality;
- generate a candidate outside production repository paths.

## Explicitly forbidden

- applying the candidate;
- modifying the ten consumers or production include tree;
- deleting legacy helpers;
- staging, committing or pushing from the native runner;
- granting runtime, order or capital authority;
- using evidence as automatic permission to trade.

## Promotion boundary

A PASS evidence bundle only unlocks design and execution of post-cutover qualification. Final cutover still requires a separate bounded patch, a second native compile/runtime pass against the shared production primitive, and a final human-reviewed decision artifact.

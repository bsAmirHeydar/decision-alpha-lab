# UCEE-I01 — Canonical Contracts, Identity Kernel, and Compatibility Layer

This patch implements the first executable phase of the Universal Context Exploitation Engine implementation program. It extends the existing MQL5-first Strategy Factory with contract release 3.0 while preserving SF01 history.

## Delivered

- dependency-light Python `strategy_factory_contracts_v3` SDK;
- MQL5 `UCE03_*` typed headers;
- immutable identity taxonomy from context occurrences through evidence bundles;
- canonical compact ASCII JSON and fixed-scale numeric encoding;
- UTF-8 FNV-1a compact identity IDs and SHA-256 evidence digests;
- UTC known-time chain from event through label maturity;
- exact schema registry and closed v3 JSON schemas;
- explicit directional migration graph with source/destination hashes;
- component capability descriptors and bounded resource declarations;
- fail-closed compatibility engine and machine-readable reasons;
- SF01-to-UCEE v3 additive bridge;
- release manifest and artifact inventory contracts;
- cross-language golden vectors and negative fixtures;
- MQL5 self-test and diagnostic EAs;
- Python tests, static/boundary tools, MetaEditor runbook;
- extensive English Obsidian phase documentation and UCE-I02 handoff.

## Contract Doctrine

- Exact schemas only.
- Explicit migrations only.
- UTC availability time only.
- Raw floats forbidden in identity material.
- Compact ID never replaces strong evidence.
- Compatibility precedes compute.
- Live compatibility never grants capital authority.
- Legacy evidence is bridged, never rewritten.

## Validation

Run `tools/strategy_factory/run_uce_i01_tests.ps1`. Native MetaEditor and terminal self-test evidence must be produced on the local Windows MT5 environment before the phase receives full cross-language acceptance.

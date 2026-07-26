---
title: RTHP MT5 Automation — Terminal Discovery, Connection, and Health
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, mt5, terminal, connection, health]
---

# MT5 Terminal Discovery, Connection, and Health

## Supported connection strategy

The primary implementation uses the official MetaTrader 5 Python integration in read-only mode.

Approved function families include:

- terminal connection and shutdown;
- terminal, account, and version information;
- symbol enumeration, symbol selection, and symbol metadata;
- M1 bar-history retrieval;
- error retrieval.

Trade functions are outside the allowlist.

## Discovery order

1. Explicit terminal path from a versioned local profile.
2. Previously approved terminal locator receipt.
3. Automatic terminal discovery by the official integration.
4. Standard Windows installation paths as a final deterministic locator.

If more than one viable terminal is found, the system compares terminal build, server, account, and data-path identities. Ambiguity blocks the run.

## Health gates

Before acquisition, verify:

- terminal connection succeeds;
- terminal information is available;
- account information is readable;
- terminal build/version is recorded;
- terminal is connected to a server;
- selected symbols can be enabled in Market Watch;
- M1 history calls return data;
- last terminal error is clear or classified;
- no trade-capable call exists in the execution path.

## Secrets

Passwords must never be stored in repository configuration. The default path uses the account session already stored in the terminal. Alternative credentials must come from an approved OS secret provider and must not be serialized into run artifacts.

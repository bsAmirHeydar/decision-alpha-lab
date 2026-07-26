---
title: RTHP MT5 Automation — Security, Entitlements, Secrets, and No-Trade Sandbox
status: roadmap-approved-for-implementation
version: 1.0.0
updated: 2026-07-22
tags: [rthp, security, entitlements, no-trade]
---

# Security, Entitlements, Secrets, and No-Trade Sandbox

## Read-only API allowlist

The adapter may use terminal, account, version, symbol, and bar-history functions required for data acquisition. Trade and account-mutation functions are forbidden.

## Static and runtime guards

- Static scan rejects imports or calls to order/position mutation functions.
- Capability manifest denies broker write, order send, position modification, and capital activation.
- Runtime audit records every MT5 function family invoked.
- Network access is limited to the already-connected terminal integration.

## Entitlements

Every source binding records:

- provider/broker;
- account/server identity without secrets;
- entitlement identifier;
- permitted research use;
- redistribution restrictions;
- acquisition timestamp and source revision.

## Secrets

- No passwords in Git.
- No password in run manifests.
- No credentials in logs or exception messages.
- Default connection uses the active terminal session.
- Optional credentials come from an approved secret provider.

## No-trade proof

Release acceptance requires:

```text
order_send_calls = 0
trade_mutation_calls = 0
position_mutation_calls = 0
capital_authority = NONE
```

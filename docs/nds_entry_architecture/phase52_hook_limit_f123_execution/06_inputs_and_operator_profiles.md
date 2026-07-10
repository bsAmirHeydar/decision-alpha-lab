---
title: Phase 52 Inputs and Operator Profiles
status: implemented
version: 1.0.0
updated: 2026-07-10
---
# Phase 52 Inputs and Operator Profiles

## Essential inputs

| Input | Default | Meaning |
|---|---:|---|
| `InpNDSHookTradeEnabled` | `false` | enables Phase 52 decision engine |
| `InpNDSHookTradeSendLiveOrders` | `false` | grants broker-send authority |
| `InpNDSHookTradeAllowHookAfterHook` | `true` | allows HH child entries |
| `InpNDSHookTradeAllowHookAfterF3` | `true` | allows opposing-F3 Hook entries |
| `InpNDSHookTradeRequireClosedHook` | `true` | blocks unresolved Hook candidates |
| `InpNDSHookTradeOneAttemptPerHook` | `true` | prevents re-entry from same Hook |
| `InpNDSHookTradeCancelPendingOnDeath` | `true` | removes structurally dead pending orders |
| `InpNDSHookTradeRequireFullF123AfterEntry` | `true` | requires F1 and F2 to start after fill |
| `InpNDSHookTradeFixedVolume` | `0.01` | fixed-lot profile volume |
| `InpNDSHookTradeMagic` | `310052` | ownership and global exposure namespace |
| `InpNDSHookTradeEntryLockTimeoutSeconds` | `30` | stale terminal lock timeout |

## Profile A — observation only

```text
Enabled = false
SendLiveOrders = false
```

No Phase 52 action.

## Profile B — decision audit

```text
Enabled = true
SendLiveOrders = false
```

Builds and exports the Hook-terminal limit decision but does not submit it.

## Profile C — controlled live/paper-broker execution

```text
Enabled = true
SendLiveOrders = true
```

Requires terminal AutoTrading, account permission, and symbol permission. Start with the minimum acceptable volume and a non-production account until visual and broker-ledger validation passes.

## Sizing

Two sizing modes exist:

- fixed volume;
- cash risk from entry-to-stop distance plus optional round-turn commission estimate.

The single-exposure rule applies regardless of sizing mode.

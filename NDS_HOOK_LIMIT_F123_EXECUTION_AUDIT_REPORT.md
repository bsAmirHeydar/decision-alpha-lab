# NDS Hook Limit Entry and Same-Direction F123 Exit — Audit Report

- Patch: `NDS-HOOK-LIMIT-F123-EXECUTION-P52`
- Central EA version: `18.40`
- Date: `2026-07-10`
- Scope: NDS valid Hook execution overlay
- Default authority: disabled / no broker send

## 1. Requested behavior

```text
valid Hook-after-Hook or valid Hook-after-opposing-F3
→ place a limit at the Hook raw terminal
→ allow only one NDS managed pending/order exposure for the strategy magic
→ after fill, wait for a complete F1 → F2 → F3 chain in the position direction
→ close the managed position when the qualifying F3 becomes canonical
→ return to idle
```

## 2. Source authority

The executable profile accepts only `FP_HookPhase02Sequence` rows that are already classified as a valid Hook family and satisfy at least one of:

- `valid_after_hook = true` (`HH`);
- `valid_after_opposing_f3 = true` (`F3H`);
- both (`F3H+HH`).

The source must remain valid, not failed, and—under the default profile—cycle-closed. Generic Hook candidates, display objects, invalid parent companions, and research-only rows cannot create an order.

## 3. Entry geometry

The Phase 52 narrow execution contract uses the raw Hook terminal already resolved by Hook Phase02:

- positive Hook: Buy Limit at `resolve_price` (lowest terminal valley);
- negative Hook: Sell Limit at `resolve_price` (highest terminal peak).

Prices are rounded to the symbol trade tick. The order is blocked rather than converted to a market order when the terminal is no longer on the valid pending-limit side of the current quote or violates broker placement distance.

The protective stop is derived from `death_boundary_price`, falling back to `origin_price`, and is placed outside the structural death boundary with configurable point/spread padding. The order has no fixed take-profit; the structural F123 exit owns the planned profit exit.

## 4. One-exposure invariant

The hard invariant is magic-wide and terminal-wide:

```text
managed pending orders + managed open positions ≤ 1
```

The engine:

1. counts current orders and positions by strategy magic across all symbols;
2. blocks a new setup whenever one managed pending order or position exists;
3. acquires an account-and-magic-scoped terminal GlobalVariable compare-and-swap lock;
4. repeats the broker exposure scan while holding that lock;
5. submits only after both scans are empty;
6. releases the lock after the send decision.

Recovery behavior:

- duplicate managed pending orders: keep the oldest, remove extras;
- one managed position plus pending orders: remove managed pending orders;
- more than one managed position: fail closed and require manual reconciliation;
- foreign-magic position on the current symbol: block entry to avoid netting contamination.

Broker-state ownership uses magic number. The order comment is audit metadata only.

## 5. One attempt per Hook

The default profile persists one consumed decision per Hook using a terminal GlobalVariable keyed by:

```text
account login + strategy magic + hash(setup key)
```

The setup key includes symbol, timeframe, sequence id, direction, origin time, terminal time, and valid family. Restarting the EA does not re-arm the same Hook. An explicit reset input exists and must be returned to `false` after the intentional reset.

## 6. Exit contract

A position exits only when a canonical F3 in the position direction is accompanied by explicit F1 and F2 evidence in the same F sequence.

Required F3 evidence:

- `level = F3`;
- direction equals broker position direction;
- `visible_main = true`;
- `f3_terminal_complete = true`;
- status is `COMPLETED` or `LOCKED`.

Required chain evidence:

- visible F1 in the same sequence, authorized to spawn F2;
- visible F2 in the same sequence, parent-ready and authorized to spawn F3;
- ordering `F1 origin ≤ F2 origin ≤ F3 completion`.

With the default strict gate, both F1 and F2 must begin after the actual broker position open time, and F3 must complete afterward. This prevents a chain that was already underway before the fill from immediately closing a new trade.

The earliest qualifying post-entry F3 is selected. The managed position is closed by ticket at market and the close is reported complete only after the ticket is no longer present as an open position.

## 7. Operational state machine

```text
DISABLED
  → no Phase 52 action

IDLE
  → no eligible valid HH/F3H: remain idle
  → eligible but invalid geometry/authority: blocked
  → eligible and authorized: one pending limit

LIMIT_PENDING
  → alive/unfilled: hold and block all new setups
  → Hook death/SL boundary breached: cancel, remain one-attempt consumed
  → filled: POSITION_OPEN

POSITION_OPEN
  → no qualifying same-direction post-entry F123: hold
  → broker protective stop: position disappears, return idle
  → qualifying F123: close ticket at market, return idle
```

## 8. Safe authority defaults

```text
InpNDSHookTradeEnabled = false
InpNDSHookTradeSendLiveOrders = false
```

Both switches must be true before the module submits or closes a live broker order. With decision mode enabled but live send disabled, the engine records a paper limit decision only.

## 9. Audit output

```text
MQL5/Files/FlagCountingPhoenix/nds_hook_limit_f123_trade_ledger.csv
```

The ledger records authority, action, status, exposure counts, tickets, Hook family and sequence, entry/death/stop/volume, setup key, and F1/F2/F3 exit evidence.

## 10. Files introduced

### MQL5

- `FP_NDSHookTradeTypes.mqh`
- `FP_NDSHookTradeRules.mqh`
- `FP_NDSHookTradeExport.mqh`
- `FP_NDSHookTradeEngine.mqh`

### Engineering documentation

- `docs/nds_entry_architecture/phase52_hook_limit_f123_execution/`
- `docs/nds_hook_architecture/69_phase52_hook_limit_f123_execution.md`

### Obsidian

- `NDS Hook Limit Entry Contract`
- `NDS Single Exposure Lock`
- `NDS Same Direction F123 Exit`
- `NDS Hook Trade State Machine`
- `NDS Hook Trade Operator Checklist`
- `NDS Hook Trade Audit Ledger`
- `Phase 52 NDS Hook Limit F123 Execution`
- `Negative Hook Terminal Is Highest Peak`

### QA

- `tools/flag_counting/nds_hook_trade_contract_qa.py`

## 11. Validation completed

- Phase 52 source/authority contract QA: PASS
- Phase 51 no-send regression contract QA: PASS
- NDS Hook pre-canon contract QA: PASS
- engineering policy validation: 0 errors, 0 warnings
- MQL5 compatibility scan: 0 errors, 0 warnings
- repository layout audit: 0 missing directories
- AI Engineering OS vault validation: 0 errors, 0 warnings
- changed Obsidian note-link validation: 0 unresolved links
- new/modified MQL lexical delimiter validation: PASS
- Python QA syntax compilation: PASS

## 12. Remaining verification boundary

MetaEditor and a broker terminal are not available in the patch-build environment. The following remain mandatory before production authority:

1. MetaEditor compile with `0 errors, 0 warnings`;
2. visual confirmation that selected HH/F3H terminal matches the intended chart location;
3. decision-audit run with live send disabled;
4. demo-account pending-order placement, fill, stop, restart, and F123 exit tests;
5. multi-chart race test using the same magic;
6. netting/hedging account behavior confirmation with the target broker.

# NDS F2 Waist Limit Backtest — Audit Report

## Intent

Add a separate, fast Strategy Tester executable for a mechanical F2-only entry profile:

```text
confirmed F2
→ limit beyond F2 waist
→ Stop at canonical parent F1 waist
→ Take Profit at F2 Leg2 endpoint
→ one managed exposure
```

## Scope

### Added

- dedicated F2-only tester expert;
- F2-specific setup and execution contracts;
- exact structural SL/TP handling;
- one-attempt-per-F2 persistence;
- one-exposure enforcement;
- exposure fast path that skips the full detector;
- detailed documentation and Obsidian note;
- contract QA.

### Reused

- Phoenix closed-bar timebase;
- scale-list builder;
- canonical F1/F2 sequence and lifecycle engine;
- canonical parent-F1 resolution;
- Phase 52 price normalization, volume sizing, exposure counting, foreign-position guard, compare-and-swap entry lock, and duplicate-pending reconciliation.

### Explicitly excluded

- Hook Phase 02 validity;
- HH/F3H setup selection;
- Hook terminal entry;
- Zone construction;
- AI/CG scoring;
- F3 exit logic;
- rendering, CSV, UI, license and production governance runtime.

## Domain contract

### Bullish

```text
Buy Limit = F2 waist - offset
SL = parent F1 waist
TP = F2 Leg2
```

### Bearish

```text
Sell Limit = F2 waist + offset
SL = parent F1 waist
TP = F2 Leg2
```

F2 must be fully confirmed by the existing lifecycle authority and able to spawn F3. Default freshness is one bar.

## Hook boundary clarification

The order layer has no Hook input. The canonical Phoenix detector still allows internal Hook branch scanning because current approved F1 root construction may depend on phase-boundary evidence. No Hook Phase 02 classifier, Hook validity family, Hook snapshot or Hook execution module is called.

## Performance design

- once per new chart bar;
- F3 scan disabled;
- Hook Phase 02 absent;
- no drawing or CSV;
- FAST profile: 800 bars, scales 2/3/5;
- detector fully skipped while a managed pending order or position exists.

## Safety and invariants

- exact F1 waist and F2 Leg2 are never silently widened/moved;
- illegal broker geometry blocks the setup;
- no market fallback;
- one global managed exposure by dedicated magic;
- foreign position on symbol blocks entry;
- one successful paper/send attempt per F2 by default;
- stale historical F2 cannot arm by default.

## Files added

- `mql5/Experts/FlagCounting/NDSF2WaistLimitBacktest.mq5`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeTypes.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeRules.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistTradeEngine.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestTypes.mqh`
- `mql5/Include/FlagCountingPhoenix/FP_NDSF2WaistBacktestEngine.mqh`
- `docs/nds_entry_architecture/f2_waist_limit_backtest/*`
- `docs/obsidian_hook/08_entry_execution/NDS F2 Waist Limit Backtest.md`
- `tools/flag_counting/nds_f2_waist_backtest_contract_qa.py`

## Files modified

- `docs/nds_entry_architecture/README.md`
- `docs/flag_counting/README.md`
- `docs/evidence/nds_entry_execution_moc/52823598bbb7_NDS_ENTRY_EXECUTION_MOC.md`

## Files deliberately untouched

- production `FlagCountingPhoenixExperiment.mq5`;
- Hook Phase 02 recognition;
- existing HH/F3H lightweight tester;
- AI/CG research architecture;
- Zone Canon.

## Verification evidence

- F2 waist contract QA: PASS;
- Phase 53 lightweight backtest regression QA: PASS;
- Phase 52 trade contract QA: PASS;
- Phase 51 entry contract QA: PASS;
- NDS Hook contract QA: PASS;
- engineering policy: 0 errors, 0 warnings;
- MQL5 compatibility: 0 errors, 0 warnings;
- repository layout: 0 missing directories;
- AI Engineering OS vault: 0 errors, 0 warnings;
- MQL lexical balance: PASS;
- quoted include resolution: 0 missing includes;
- static QA: no blocking findings.

## Residual risks

1. MetaEditor was unavailable in the build environment; local compile remains mandatory.
2. FAST profile intentionally has a smaller history/scale envelope than PARITY.
3. Broker stop-level rules may reject exact structural SL/TP on some symbols; the code blocks instead of modifying anatomy.
4. The current F1 root detector may internally depend on Hook phase boundaries, but Hook is not an entry feature.
5. Pending orders are GTC because no expiration rule was supplied.

## Rollback

Remove the new F2 modules/expert/docs/QA and revert the three index additions. No existing execution file was modified.

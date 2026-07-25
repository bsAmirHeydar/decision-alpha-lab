# NDS Hook 86.4 Cycle R1 — No-Trade Engine Fix v1.1.0

This hotfix corrects the integrated execution path for the Phase 55 `HOOK_864_CYCLE_R1` profile. It is a delta patch and requires the original `decision-alpha-lab-nds-hook-864-cycle-r1-v1.0.0` patch to be installed first.

## Confirmed root causes

1. The dedicated Strategy Tester expert defaulted to the legacy `TERMINAL_F123` trade profile.
2. The tester defaulted to the sparse FAST scan: 1200 bars and four scales.
3. The setup treated Phase02 terminal availability as the final cycle-closure proof instead of consuming the canonical Phase03/04 closure engine.
4. The first-arrival gate used Phase02 terminal retracement instead of actual closed price travel after Phase04 closure.
5. Phase02 and Phase04 snapshots were bound too strongly to an array-local `sequence_id`.
6. A zero-trade run did not expose the gate at which candidates disappeared.

## Corrected integrated path

```text
Canonical closed timebase
→ existing F/Rally engine
→ existing Hook Phase02 identity/family/x-count
→ existing Hook Phase03 Y-axis engine
→ existing Hook Phase04 50% X-closure/death engine
→ closed-bar first 86.4 arrival evidence
→ existing selector, identity, risk, broker and order lifecycle
```

No parallel Hook detector, pivot detector, node counter, Y extractor, cycle-closure algorithm, sizing engine, or broker adapter has been added.

## Dedicated tester defaults

```text
Expert: NDSHookLimitF123Backtest
InpBTProfile: PARITY
InpBTTradeProfile: HOOK_864_CYCLE_R1
InpBTPrintRunSummary: true
InpBTSendTesterOrders: true
```

The actual tester input is `InpBTTradeProfile`. `InpNDSHookTradeProfile` belongs to the central Phoenix expert.

## Runtime contract

A setup reaches execution only when all of the following hold:

- existing valid HH/F3H Hook family;
- confirmed Phase02 terminal;
- canonical X count exactly 3 or 4; Origin is not counted;
- canonical Phase04 X closure at the locked 50% rule;
- no Phase04 origin-return death;
- no closed-bar 86.4 touch at or after the closure candle;
- existing one-attempt and one-exposure rules;
- valid limit side, stop/freeze distance, volume, margin and broker capabilities.

Entry remains:

```text
Entry = Crown + 0.864 × (Origin − Crown)
```

Stop remains behind the canonical death boundary with Origin fallback. Target remains exactly 1R through the existing normalized SL/TP path.

## Zero-trade diagnostic funnel

Every diagnostic run reports:

```text
total → canonical → family → allowed → confirmed → crown → x34
→ mature → p04 → closed → alive → untouched → ready
```

The session summary aggregates ready runs, paper-ready decisions, limit sends, pending/position state, blocked runs, Phase04 closures and untouched first arrivals.

A saved tester Journal can be analyzed with:

```powershell
python .\tools\flag_counting\analyze_nds_hook_864_tester_log.py .\path\to\tester.log
```

## Repository verification completed

- 43 deterministic Python tests passed.
- 359 PASS and zero FAIL source/contract/static records.
- Nine bounded Phase 55 QA stages passed.
- Repository engineering policy passed with zero errors and zero warnings.
- Modified Python files passed `py_compile`.
- MQL5 delimiter, compatibility, authority and integration scans passed.

## External evidence still required

Linux repository QA cannot execute MetaEditor, MT5 Strategy Tester, terminal restart, or broker order behavior. The following remain external:

- Windows MetaEditor clean compilation;
- execution of `NDSHook864CycleR1ContractSelfTest`;
- Strategy Tester run with reviewed funnel and Journal;
- broker/demo pending-order, fill, SL/TP, cancellation and restart evidence.

This patch corrects the route and diagnostics. It does not fabricate a setup in a historical interval that contains no valid x3/x4 Phase04-closed untouched Hook, and it does not assert profitability or live authorization.

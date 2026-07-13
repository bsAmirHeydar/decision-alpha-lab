# NDS F2 Exact Per-Trade F3 Exit — Audit Report

## Scope

Hotfix for `NDSF2WaistLimitBacktest.mq5` dynamic exit mode:

```text
FP_NDS_F2_EXIT_F3_FLAG_RETEST
```

## Confirmed defect

The previous manager resolved a dynamic exit from a broadly compatible confirmed F2. It matched direction, scale, source times, and parent waist, then selected a best compatible candidate. With parallel or overlapping F2 contexts, that allowed multiple positions to capture the same confirmation node or a node belonging to another F2 lineage.

The previous correction gate was also price-generic: one adverse tick could be treated as correction without proving that the exact child F3 of the trade had formed its own Waist.

## Corrected authority

Each order captures the full source lineage:

- setup hash;
- source F1 and F2 audit event IDs;
- stable sequence and parent-sequence IDs;
- F2 chain index;
- source F1 waist node ID/time;
- source F2 origin node ID/time;
- source F2 waist node ID/time;
- initial F2 Leg2 node ID/time;
- order ticket, position identifier, and position ticket.

Event IDs are retained for audit, but runtime identity uses stable sequence/chain/node anatomy because array event IDs can shift when earlier sequences emit new F3 events.

## Exact child F3 contract

A dynamic target can be created only from the direct child F3 of the exact source F2:

```text
child.parent_event_id   = current exact source F2.event_id
child.parent_sequence_id= exact source F2.sequence_id
child.sequence_id       = exact source F2.sequence_id
child.direction         = source direction
child.scale             = source scale
child.Leg1              = exact source F2.confirm node
```

If the source F1, source F2, or child F3 is missing or ambiguous, the context fails closed and does not borrow another structure.

## Correction and target

The exact child F3 must form its own Waist after Leg1:

```text
Exact Child F3 Leg1
→ Exact Child F3 Waist
→ correction authorized
→ TP = Exact Child F3 Leg1
```

The generic tick-distance correction function was removed from the execution path.

## Per-position isolation

```text
Position A → Source F2-A → Direct Child F3-A → TP-A
Position B → Source F2-B → Direct Child F3-B → TP-B
```

TP modification and fallback market close continue to use the exact bound position ticket.

## Reward/Risk boundary

Unchanged:

```text
RR reference = original F2 Leg2 known at setup creation
```

The future F3 target is not used for minimum-RR filtering or entry repricing.

## Runtime impact

- Fixed exit mode remains F1/F2-only.
- Dynamic mode enables only direct F3 lifecycle construction in the existing shared sequence engine.
- Hook, renderer, chart objects, CSV, timer, and AI runtime remain absent.
- F3 is rebuilt once per new entry-timeframe bar, not per tick.
- Per-tick work remains position binding, target-reached check, and TP/close handling.

## Version

```text
Expert:   1.70
Contract: NDS-F2-WAIST-BREAK-08
Schema:   nds_f2_waist_break_point2_v8
```

## Validation completed

- exact per-trade F3 lineage QA: PASS;
- dual-exit regression QA: PASS;
- HTF F-phase filter regression QA: PASS;
- overlap/wider and RR repricing QA: PASS;
- hedge/parallel-context QA: PASS;
- F2 Point-2 setup QA: PASS;
- fast-backtest contract QA: PASS;
- engineering policy: 0 errors, 0 warnings;
- MQL5 compatibility: 0 errors, 0 warnings;
- repository layout: 0 missing directories;
- engineering vault: 0 errors, 0 warnings;
- MQL lexical balance: PASS;
- ZIP integrity: PASS.

MetaEditor is not available in the build environment. Final compilation and Real-Tick Strategy Tester validation must be performed locally.

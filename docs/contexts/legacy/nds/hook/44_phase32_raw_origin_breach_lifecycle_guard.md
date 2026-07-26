# Phase 32 — Raw Origin-Breach Lifecycle Guard

## Purpose

This phase fixes a production-visibility bug in the Phase 02 Hook envelope layer.
The issue was not primarily a drawing problem. The renderer was receiving Hook
sequences that looked eligible at the same-side swing-node level, while raw
candle action had already violated the Hook origin before the terminal node was
structurally confirmed.

The corrected rule is:

```text
If the Hook origin is breached before the terminal node is confirmed,
the structure is not a failed Hook. It was never a valid Hook.
```

Therefore it must not produce:

```text
- a semantic Hook arc,
- a Hook zone,
- a valid Hook learning label,
- a production Hook visualization object.
```

## Authority

This phase implements the current Alpha Lab Hook validity doctrine:

```text
Hook Candidate != Confirmed Hook
Confirmed Hook != Valid Hook Family
Valid Hook Family != Zone-Qualified Hook
```

A candidate first has to survive its own origin boundary until the terminal
node is confirmed. Only after that can higher-level validity families such as
`Hook After Hook` or `Hook After Opposing F3` be considered.

## Problem observed

On the M1 chart, several semicircle/envelope arcs were drawn from Hook origins
that had already been hit or penetrated before the last Hook node was stable.
That created visual noise and made the chart look as if many valid Hooks were
present.

The root cause was that the previous guard checked same-side Hook nodes only.
A raw wick/high/low breach between nodes could invalidate the origin without
becoming a confirmed Phase 01 node. The sequence then survived long enough to
reach the renderer.

## New hard rule

For a positive / low-side Hook:

```text
origin = Hook floor
raw origin breach = any candle low <= origin price
```

For a negative / high-side Hook:

```text
origin = Hook ceiling
raw origin breach = any candle high >= origin price
```

When `death_on_boundary_touch = true`, equality also kills the candidate.
This is the intended default because the origin itself is the death boundary.

## Confirmation window

The guard scans raw bars from immediately after the origin bar through the
terminal node confirmation horizon:

```text
origin_bar_index + 1
...
resolve_bar_index + scale_l
```

This matters because a Phase 01 node is confirmed only after enough right-side
bars exist. A breach that happens before that confirmation point means the
terminal node did not stabilize before the origin died.

## Implementation summary

### Files changed

```text
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Types.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Rules.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Export.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase02Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase03Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase04Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase05Engine.mqh
mql5/Include/FlagCountingPhoenix/FP_HookPhase06Engine.mqh
mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5
```

### New config field

```text
reject_raw_origin_breach_before_terminal_confirmation = true
```

### New expert input

```text
InpHookPhase02RejectRawOriginBreachBeforeTerminalConfirmation = true
```

The default is intentionally strict. Turning it off is a diagnostic escape
hatch, not the production doctrine.

### New report counter

```text
raw_origin_breach_rejects
```

This counter makes the guard auditable from summary logs and CSV export.

### New sequence field

```text
resolve_bar_index
```

The raw confirmation window needs the terminal node's bar index, not just its
time and price.

## Correct lifecycle

```text
Raw candidate
  -> origin survives until terminal confirmation
  -> terminal node confirmed
  -> near-death condition checked
  -> render_eligible=true
  -> only then semantic arc can be drawn
```

Invalid lifecycle:

```text
Raw candidate
  -> origin touched/breached before terminal confirmation
  -> reject_reason=RAW_ORIGIN_BREACH_BEFORE_TERMINAL_CONFIRMATION
  -> render_eligible=false
  -> no arc
  -> no Hook zone
```

## Why this is not a drawing fix

The arc renderer was already checking:

```text
render_eligible
near_death_confirmed
hook_failed == false
resolve_confirmed == true
```

The missing part was earlier in the lifecycle. The sequence builder had to
reject candidates whose origin was killed by raw candle action before terminal
confirmation. Once the sequence stream is corrected, the renderer naturally
becomes cleaner.

## Trading meaning

A Hook whose origin dies before the final node stabilizes is not a bad Hook.
It is a non-Hook. That distinction matters for the zone engine:

```text
bad Hook     = a valid Hook that later fails
non-Hook     = a candidate that never earned Hook status
```

Only the first category may later become failure information. The second
category must not be used for primary zones, statistics, or training labels.

## Expected visual outcome

After this patch, M1 Hook display should become materially cleaner:

```text
- fewer false semicircle arcs,
- fewer origin-spanning envelopes across dead origins,
- fewer misleading Hook IDs,
- fewer zone candidates derived from non-Hooks.
```

The chart should show only Hooks whose origin survived long enough for the
terminal node to be confirmed.

## Validation checklist

1. Run `FlagCountingPhoenixExperiment` on a noisy M1 Gold segment.
2. Enable Hook Phase 02 summary printing if needed.
3. Confirm that `raw_origin_breach_rejects` increases on the segment where
   origin-dead arcs used to appear.
4. Confirm that semicircles whose origin was breached before terminal
   confirmation no longer draw.
5. Confirm that Rally/F-counting rendering is unchanged.
6. Confirm that disabling the new input is only used for diagnostics and brings
   back the pre-guard permissive behavior.

# Phase 50 — Pre-Canon NDS Hook Stabilization

## Status

Implemented infrastructure correction. This phase does **not** decide the open Hook/Zone questionnaire.

## Purpose

Before the final Valid Hook and Zone Canon is captured, the current NDS implementation must expose its existing behavior faithfully and must use the same structural coordinate system as the rest of the Phoenix engine.

The patch therefore corrects objective implementation defects while preserving every unresolved doctrine choice as an input or open decision.

## Audited corpus

The review covered the NDS Hook architecture pack, Hook-validity doctrine, Obsidian Hook vault, Phoenix Flag Counting implementation, Hook Phase01–10 modules, and the experience-capture material that references NDS Hook/Zone behavior.

The authoritative implementation chain is:

```text
FlagCountingPhoenixExperiment.mq5
→ FP_HookPhase01 node source
→ FP_HookPhase02 sequence and validity ownership
→ FP_HookPhase03–06 anatomy/closure/quality
→ FP_HookPhase07–10 visual, audit, smoke and freeze layers
```

## Locked doctrine preserved

1. Production valid-only view renders only canonical valid Hook families.
2. Hook-after-Hook uses exact parent/child lineage and renders the parent only as companion.
3. Post-F3 ownership is finite; an F3 does not validate every future Hook.
4. A candidate whose origin dies before terminal confirmation is not a closed Hook.
5. Structural time authority is canonical bar index; timestamps are metadata.
6. Hook code remains visualization/research infrastructure and must not send orders.
7. Zone implementation remains deferred until its boundaries and lifecycle are answered.

## Objective defects corrected

### 1. Wall-clock ownership was replaced by canonical bar-index ownership

The old post-F3 window converted a bar count into seconds with `PeriodSeconds(_Period)` and compared timestamps. That made ownership dependent on the chart period and session gaps even though the Phoenix structural stream is indexed by closed bars.

The corrected contract is:

```text
candidate_origin_bar_index >= f3_terminal_bar_index
candidate_origin_bar_index - f3_terminal_bar_index <= configured_max_bars
```

Direct-terminal tolerance uses the same bar-index axis.

### 2. F3 direction strictness input is no longer dead

`valid_f3_require_opposite_direction` was loaded from the EA but the recognition function always forced opposite direction. The input now controls the behavior it advertises. The production default remains `true`.

### 3. `EARLIEST_FIRST` now means earliest first

The old comparator preferred directness before origin time even when the selected enum was `EARLIEST_FIRST`. The comparator now evaluates canonical origin bar index first for that mode and applies family/directness only as tie-breakers.

### 4. Price tolerance is exact

A configured tolerance of `0` or `1` point was silently raised to `2`. The hidden floor was removed. Negative values normalize to zero; zero means exact price equality.

### 5. Ownership evidence is preserved

Each selected post-F3 sequence now records:

- F3 event ID;
- matched F3 terminal bar index;
- matched F3 terminal timestamp;
- matched F3 terminal price;
- F3-terminal-to-Hook-origin distance in bars.

This permits deterministic chart and CSV review.

### 6. Audit output now exposes the effective recognition contract

The summary export and terminal log include:

- direction strictness;
- recognition mode;
- selection priority;
- direct/delayed switches;
- maximum search bars;
- terminal bar and price tolerances;
- geometric threshold;
- structural axis declaration.

The sequence CSV schema was bumped from `v1` to `v2`.

## Intentionally unresolved

This phase does not invent answers for:

- final ownership-window length;
- structural events that terminate F3 ownership;
- exact Direct versus Rebound evidence;
- final 80% geometry denominator and wick/close rule;
- terminal confirmation count by timeframe;
- post-confirmation origin breach behavior;
- Zone source points, boundaries, padding, lifecycle, entry, stop or target;
- quality weights and family priority beyond existing configurable behavior.

## Known semantic limitation retained

The current delayed/rebound classifier still means “eligible inside the F3 window but not direct.” It does not yet prove a complete away-and-return rebound path. That proof requires the pending Canon answers and must be fixed in a later semantic phase, not guessed here.

Likewise, the current geometric-80 family is derived from existing Phase02 sequence candidates; it is not yet a fully independent geometric-cycle synthesizer.

## Changed implementation files

- `FP_HookPhase02Types.mqh`
- `FP_HookPhase02Rules.mqh`
- `FP_HookPhase02Export.mqh`
- `FP_HookPhase02Engine.mqh`
- `FlagCountingPhoenixExperiment.mq5`
- `tools/flag_counting/nds_hook_contract_qa.py`

## Acceptance criteria

1. Post-F3 ownership never calls `PeriodSeconds(_Period)`.
2. The direction strictness switch affects classification.
3. `EARLIEST_FIRST` compares origin bar index before directness.
4. CSV output contains matched F3 terminal and origin-distance evidence.
5. Valid-only remains enabled by default.
6. No execution token is introduced into Hook Phase02.
7. Existing engineering validators pass.
8. MetaEditor compile must be confirmed on the target terminal.

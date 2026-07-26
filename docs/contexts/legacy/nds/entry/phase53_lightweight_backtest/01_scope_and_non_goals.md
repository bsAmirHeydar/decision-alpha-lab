# Scope and Non-Goals

## Goal

Provide a fast Strategy Tester executable for the current NDS trading contract without loading the production expert's visualization, release, audit, UI, license, paper-research, and broker rehearsal layers.

## Preserved behavior

- canonical closed-bar timebase;
- the same F1/F2/F3 detector;
- the same Hook Phase 02 sequence builder;
- the same post-F3 and Hook-after-Hook validity annotations;
- limit entry at the raw Hook terminal;
- stop beyond Hook death/origin geometry;
- one-attempt-per-Hook persistence;
- one managed pending order or position;
- cancellation after Hook death;
- exit only after a complete same-direction post-entry F1-F2-F3 chain.

## Removed from the backtest runtime

- chart objects and rendering;
- Hook phases 03–10;
- production license validation;
- timers and chart events;
- export, validation, acceptance, release, ambiguity, and static-QA runtime passes;
- Level 19–30 research/paper/broker rehearsal pipelines;
- Phase 51 generic Zone/Setup/Command preview pipeline;
- continuous CSV writing.

## Non-goals

This phase does not redefine Hook validity, Zone Canon, entry price, stop placement, or F123 exit semantics. It changes orchestration and performance only.

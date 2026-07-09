# CH18 — Execution Freedom, Position Multiplicity, and No Base Constraints

## Purpose

Chapter 18 defines the raw execution field for EXP0017. The strategy architect states that, at the base layer, there is no execution restriction beyond true divergence invalidation at the final confirmation moment.

The chapter protects the research model from early limits such as:

- maximum number of positions
- maximum number of positions per cycle group
- blocking new trades after a loss
- blocking hedged exposure
- forcing one-direction-only behavior
- preventing repeated trades from the same CG
- excluding next-cycle opportunities after a failed prior cycle

These may become future research ideas, but they are not base rules.

## Chapter 18 Core Doctrine

A confirmed divergence has execution permission immediately after final candle-close confirmation if the divergence has not already been invalidated.

The base model does not impose a position limit, cycle-group limit, direction limit, hedge limit, or post-loss restriction. Every confirmed and still-valid divergence remains eligible for execution.

## Answer Compression

The answers in this chapter reduce to the following core principles:

1. Prior execution timing rules remain valid.
2. Each CG and each cycle is independent.
3. There is no base position limit.
4. A losing or failed cycle does not block the next cycle.
5. No directional or symbolic preference is added here.
6. Multiple positions from the same CG are allowed.
7. Repeated entries are logically allowed unless later statistics prove a reason to restrict them.
8. Hedging is allowed in the base layer.
9. Entry is immediately after candle close and final confirmation.
10. There is no restriction unless the divergence is invalidated at confirmation.

## Related Chapters

- Chapter 08: close confirmation and trade permission
- Chapter 09: clean-symbol execution
- Chapter 10: stop and time-exit doctrine
- Chapter 11: CG independence and daily reset
- Chapter 12: signal persistence and invalidation boundary
- Chapter 14: statistical red flags and future constraints
- Chapter 16–17: model and AI as analyst, not execution authority

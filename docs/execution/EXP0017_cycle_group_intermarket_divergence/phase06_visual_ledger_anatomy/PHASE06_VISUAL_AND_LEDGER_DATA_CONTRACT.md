# Phase 06 Visual and Ledger Data Contract

## Input contract

Phase 06 consumes `SCGCFinalSignal` from Phase 05.

Required fields include:

- signal id
- group name and group minutes
- current cycle and reference cycle
- trading-day start and end
- confirmation broker/UTC/NY time
- direction
- side
- status
- hunter symbol
- clean symbol
- one-sided hunt flag
- double-hunt invalidation flag
- hunter reference price
- clean reference price
- hunter current extreme
- clean current extreme
- clean stop reference preview

## Output contract: visual objects

The chart drawing layer may create:

- line object
- reference anchor vertical line
- confirmation marker vertical line
- text label

Each object name must use the Phase 06 object prefix and the signal id.

## Output contract: ledger

The ledger row is append-only and must preserve the final state as observed at the closed-candle boundary.

The ledger must not rewrite old rows as results evolve. Later outcome phases should add separate outcome files or join by ledger key.

## Non-mutating doctrine

Phase 06 does not alter signal status. It only displays and records it.

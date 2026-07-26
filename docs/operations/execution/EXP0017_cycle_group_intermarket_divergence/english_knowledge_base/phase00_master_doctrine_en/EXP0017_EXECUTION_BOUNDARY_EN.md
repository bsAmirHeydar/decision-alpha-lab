# Exp0017 Execution Boundary En

Future raw execution may enter immediately after final confirmation, trade the clean symbol, allow hedge states, allow multiple positions, and preserve all valid signals unless the divergence is invalid at confirmation.

## Canonical Current-Version Boundaries

- The robot must learn to see before it is allowed to decide.
- The current version is statistical-only and doctrine-preserving.
- All confirmed tradeable signals should be recorded before ranking or filtering.
- AI may explain, rank, compare, and warn, but it cannot mutate the strategy.
- Future optimization is allowed only through a separate version gate.

## Required Traceability

Every implemented module must expose the state it creates: time field, cycle group, reference candidate, hunt state, divergence state, confirmation state, invalidation state, signal record, and statistical result.

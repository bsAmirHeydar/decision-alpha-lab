# Exp0017 Master Strategy Constitution En

The master constitution defines EXP0017 as a cycle-group based intermarket divergence framework between SPXUSD and NDXUSD, with all symbols evaluated against their own references and all rule changes governed by statistics and strategy-architect approval.

## Canonical Current-Version Boundaries

- The robot must learn to see before it is allowed to decide.
- The current version is statistical-only and doctrine-preserving.
- All confirmed tradeable signals should be recorded before ranking or filtering.
- AI may explain, rank, compare, and warn, but it cannot mutate the strategy.
- Future optimization is allowed only through a separate version gate.

## Required Traceability

Every implemented module must expose the state it creates: time field, cycle group, reference candidate, hunt state, divergence state, confirmation state, invalidation state, signal record, and statistical result.

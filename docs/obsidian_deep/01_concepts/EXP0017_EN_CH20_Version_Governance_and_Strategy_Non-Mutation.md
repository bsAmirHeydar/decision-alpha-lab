# EXP0017 EN CH20 — Version Governance and Strategy Non-Mutation

## Thesis

The current version is statistical-only and cannot change strategy; future versions may optimize only after statistical review and explicit promotion.

## Doctrine

- Repeated questions map back to existing doctrine.
- The current model collects and reports statistics only.
- Future optimization may be allowed in later versions.
- The strategy architect decides after statistics.
- CG overlap may become a major modeling complexity source.

## Fields

- `version_id`
- `strategy_mutation_allowed`
- `optimization_gate`
- `architect_approval`
- `cg_overlap_complexity`

## Implementation Note

- Separate base version from optimized versions.
- Prevent premature optimization from contaminating raw statistics.

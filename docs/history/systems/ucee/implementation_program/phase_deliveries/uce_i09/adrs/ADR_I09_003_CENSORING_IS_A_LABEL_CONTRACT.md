# ADR I09-003 — Censoring Is a Label Contract

## Decision

Duration, event indicator, cause, maturity, and censoring reason are explicit schema fields rather than inferred from missing values.

## Consequence

Survival tasks can be audited, and ordinary classification cannot silently reinterpret censored outcomes as failures.

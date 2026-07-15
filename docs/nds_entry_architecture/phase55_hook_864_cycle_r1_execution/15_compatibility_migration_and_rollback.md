# 15 — Compatibility, Migration, and Rollback

## Compatibility guarantees

- `TERMINAL_F123` remains enum `0` and reset/default.
- Phase 52 Entry remains `resolve_price`.
- Phase 52 target remains zero and F123 exit remains active.
- Existing Phase 52 ledger file/header remains separate and unchanged.
- Old public engine/core function names remain compatibility wrappers.
- Existing family, sizing, exposure, registry, broker, and cancellation semantics are shared rather than duplicated.

## Migration

No used-setup registry migration is required. The Phase 55 setup key includes a profile code, so it cannot collide with a Phase 52 key. The dedicated ledger uses a new filename/schema.

The exact legacy Phase 52 broker comment form (`<prefix>|S<sequence>|<family>`) is preserved. New Phase 55 orders place the profile token near the beginning of the comment (`<prefix>|864R1|...`). On restart, Magic and symbol establish economic ownership; the comment then recovers only the lifecycle profile. Unknown/truncated/unrecognized profiles fail closed. Current input changes cannot convert a fixed-R position to F123 exit or a legacy F123 position to fixed-R handling.

## Upgrade sequence

1. install files atomically;
2. run Python/static QAs;
3. compile both EAs in MetaEditor;
4. run Phase 52 regression profile;
5. run Phase 55 vector/tester profile;
6. review CSV schema and one-attempt behavior;
7. only then consider paper/demo activation.

## Rollback

Disable both Hook trade authority inputs, remove or cancel controlled demo pending orders through the approved operator process, preserve logs/ledger, and revert the atomic patch commit. The rollback must not delete broker evidence or clear used-setup registry before reconciliation.

## Deliberately untouched behavior

No Hook detection doctrine, F lifecycle, chart rendering, generic NDS Zone pipeline, F2 execution profile, license boundary, or release authority is redefined by rollback or install.

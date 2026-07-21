---
title: RTHP Occurrence Identity IR
status: compiled
version: 1.0.2
---
# Occurrence Identity IR

- Occurrence IR digest: `sha256:22029214ddc97c8e94c65e23120de8e484f05afb884c617fc615d96b104d485b`
- Identity algorithm: `SHA256_CANONICAL_JSON`
- Namespace: `CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1@1.0.2`
- Append-only: `true`

## Ordered identity fields

1. `context_id`
2. `context_version`
3. `anchor_time`
4. `direction`
5. `subject_key`
6. `symbol_pair_id`
7. `cycle_definition_version`
8. `signal_family`
9. `active_cycle_id`
10. `reference_cycle_id`
11. `level_side`
12. `hunter_symbol`
13. `protected_symbol`
14. `first_touch_time`
15. `confirmation_close_time`

## Generic alias bindings

- `anchor_time = confirmation_close_time`
- `direction = relation_polarity`
- `subject_key = symbol_pair_id`

These aliases satisfy the cross-context compiler contract without erasing the richer RTHP identity. They are duplicated intentionally in the ordered identity recipe so the generic and domain-specific identities remain auditable.

`direction` is intrinsic Context polarity only. It is not an Entry side, Treatment, prediction of successful reversal, or order instruction.

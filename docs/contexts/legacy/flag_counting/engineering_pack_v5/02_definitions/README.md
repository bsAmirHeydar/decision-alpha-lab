# 02 Definitions README

This package contains canonical definitions. These definitions are implementation contracts.

Read these files before changing detector code.

## Files

- `NODE_AND_L_DEFINITION.md`
- `FLAG_BODY_DEFINITION.md`
- `F_LEVELS_DEFINITION.md`
- `ND_HOOK_DEFINITION.md`
- `SEQUENCE_IDENTITY_DEFINITION.md`
- `STATUS_AND_LIFECYCLE_DEFINITION.md`

## Definition Principle

A definition must be:

```text
observable from high/low node data
stable under replay
independent of renderer
explicitly owned by a sequence context
```

If an object cannot be identified with time, price, node identity, parent context, and status, it is not implementation-ready.

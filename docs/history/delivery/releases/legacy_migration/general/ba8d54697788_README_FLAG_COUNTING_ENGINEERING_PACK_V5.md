# Flag Counting Engineering Pack V5

This experiment now has an implementation-grade documentation package:

```text
docs/flag_counting/FLAG_COUNTING_ENGINEERING_PACK_V5.md
docs/flag_counting/engineering_pack_v5/
```

## Why This Exists

The previous implementation attempts exposed several critical ambiguity sources:

- sliding-window F1 creation;
- wrong correction extreme selection;
- parent/child invalidation confusion;
- missing ND/Hook branch logic;
- renderer drawing structures not backed by deterministic engine output;
- chart clutter caused by untraceable candidates.

The V5 pack separates concepts, definitions, explanations, algorithms, and visualization rules.

## Before Coding

Read in this order:

1. `docs/flag_counting/engineering_pack_v5/README.md`
2. `docs/flag_counting/engineering_pack_v5/01_concepts/README.md`
3. `docs/flag_counting/engineering_pack_v5/02_definitions/README.md`
4. `docs/flag_counting/engineering_pack_v5/03_explanations/README.md`
5. `docs/flag_counting/engineering_pack_v5/04_algorithms/README.md`
6. `docs/flag_counting/engineering_pack_v5/05_visualization/README.md`

## Coding Rule

Do not patch the old detector blindly. Audit it against:

```text
docs/flag_counting/engineering_pack_v5/04_algorithms/
```

Then rewrite or repair module by module.

## Visualization Rule

The renderer must draw all emitted structures if configured, but it must never invent structures.

# Phoenix Flag Counting Implementation Ladder V1

This document is part of the implementation ladder for the Phoenix Flag Counting engine. The ladder is intentionally layered so that lower layers become frozen foundations before higher layers are allowed to depend on them.

Global non-negotiables:

- All structural decisions use candle `high` and `low` only.
- `open`, `close`, candle body, candle color, volume, and indicators are not structural inputs.
- Equality is not a break. A level is broken only by a strict pass beyond it.
- The renderer is non-authoritative. It may only draw logical objects emitted by engines.
- Main-chart rendering and audit rendering are separate products.
- Every layer must expose enough audit fields to prove why an object exists.
- A higher layer may never silently repair a lower-layer defect.

# Ambiguities to Resolve Before Further Code

## Purpose

This document lists questions that should be answered before another broad Phoenix rewrite. Some can be coded as configurable variants, but they must not remain implicit.

## A. Phase reset rules

Current strict interpretation:

```text
A new same-direction F1 phase is allowed only after an opposite confirmed F1 locks a completed F3.
```

Questions:

1. Can an opposite confirmed F1 reset phase even if prior F3 was not completed?
2. Can a very large opposite Hook/ND reset phase before F3?
3. Can a broken F2/F3 parent reset ownership, or does F1 remain owner until opposite phase appears?

Recommended implementation:

```text
Config enum:
PHASE_RESET_OPPOSITE_F3_LOCK_ONLY
PHASE_RESET_OPPOSITE_CONFIRMED_F1
PHASE_RESET_OPPOSITE_HOOK_OR_F1
```

Default should remain strict until user confirms otherwise.

## B. F1 root preference

Questions:

1. If Hook-derived F1 and fail-open F1 differ slightly but both produce valid bodies, which wins?
2. Should lower-L local F1 always beat high-L umbrella F1 when both confirmed?
3. Should a later F1 with full F2/F3 chain beat an earlier F1 with only confirmation?

Recommended implementation:

Use transparent score components and print them in audit.

## C. F2 size handling

Questions:

1. If F2 body is valid but size is not yet enough, should it be visible as `qualified=false` or audit-only?
2. If F2 later extends to enough size, should its Leg2 update or should a new candidate be emitted?

Recommended default:

```text
F2 candidate may exist in audit.
Main-chart F2 requires size-qualified or explicitly enabled candidate display.
F3 authorization requires size-qualified confirmed F2.
```

## D. Hook/ND display

Questions:

1. Should Hook arcs be drawn when they do not seed visible F1?
2. Should ND label appear without drawing full arc?
3. Should branch numbers ever show on main chart?

Recommended default:

```text
Main chart: only Hook/ND connected to visible F1, no branch numbers.
Audit: all Hook/ND and branch numbers.
```

## E. Main-chart density

Questions:

1. What maximum number of visible F events per viewport is acceptable?
2. Should high-L structures be drawn thinner/background when local structures exist?
3. Should the chart have a scale focus input: local, balanced, high-L?

Recommended implementation:

```text
DisplayProfile = CLEAN_LOCAL | BALANCED | STRUCTURAL_AUDIT
```

## F. Live pending nodes

Questions:

1. Can pending nodes seed Hook/ND only?
2. Can pending nodes seed F1 body?
3. Should live mode and historical mode differ?

Recommended default:

```text
Pending nodes may support Hook live inspection.
Confirmed F structures require confirmed nodes unless explicitly in live diagnostic mode.
```

## G. Backfill windows

Questions:

1. For F2, is the backfill window strictly F1 Leg2 -> F1 confirmation, or may it include post-confirmation pullback before F2 Leg1?
2. Same question for F3.

Recommended default:

Follow the documented strict window. If extended window is desired, add an explicit config variant.

## Required answers before next major code patch

Minimum questions to answer:

1. What exactly resets same-direction F1 ownership?
2. Should main chart show developing F2/F3 or only confirmed/qualified ones?
3. Should high-L umbrella flags remain visible when local lower-L canonical flags exist?
4. Should pending live nodes be allowed in F bodies or only Hook/ND?

Until these are answered, code should implement the strict documented defaults and keep alternatives behind named inputs.

# FlagCounting MQL5 Include Layer

The active concept contract lives in:

`docs/flag_counting/FLAG_COUNTING_CONCEPT_SPEC_V2.md`

Do not treat this module as a simple flag-pattern scanner. The intended module is a fractal multi-scale, multi-sequence state engine.

Core contract:

- F1 is the root count.
- F2 is mandatory after F1 unless F1 invalidates or must be recounted.
- F3 is mandatory after F2 and has special terminal behavior.
- F1 invalidates at its Waist.
- F2 invalidates at its Origin.
- F3 completes after its two-leg body and may not require Leg2 rebreak.
- F2 must be at least as large as F1.
- F3 does not require parent-size symmetry.
- ND / Hook is part of the market partition.
- Rendering is body-only by default.

Implementation should expose queryable state to code, not just chart objects.

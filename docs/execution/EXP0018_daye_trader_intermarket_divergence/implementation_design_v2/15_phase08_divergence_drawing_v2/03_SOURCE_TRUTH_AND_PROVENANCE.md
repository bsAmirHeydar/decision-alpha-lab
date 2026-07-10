# Source Truth and Provenance

The chart is not the source of truth. An object can be manually moved, deleted, hidden, or duplicated by a user. P08 therefore rebuilds geometry exclusively from:

1. immutable accepted P07 use;
2. complete P03 reference period;
3. the Hunter-symbol extreme source bar;
4. P06 host confirmation bar.

The renderer never infers a missing use by looking at chart highs or lows. This prevents a drawing bug from mutating strategy state.

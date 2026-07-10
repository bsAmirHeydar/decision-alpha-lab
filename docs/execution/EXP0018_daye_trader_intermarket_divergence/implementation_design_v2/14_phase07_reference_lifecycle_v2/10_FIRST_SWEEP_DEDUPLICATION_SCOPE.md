# First-Sweep deduplication scope

The deduplication key is exact opportunity, side, hunter, and protected. This prevents repeated callbacks or repeated P06 result publication from drawing the same event twice.

It does **not** globally consume the entire reference after the first hunter touch. Global consumption at first use would contradict the explicit rule that later divergence remains possible while the protected symbol still has not touched its own level.

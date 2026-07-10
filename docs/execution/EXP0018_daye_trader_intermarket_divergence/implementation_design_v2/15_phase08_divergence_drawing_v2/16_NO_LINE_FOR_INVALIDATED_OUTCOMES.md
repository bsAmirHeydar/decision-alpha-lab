# No Line for Invalidated Outcomes

P08 draws only `DAYE_USE_STATUS_ACCEPTED`. No line is created for double-hunt invalidation, no-signal close, unavailable close, role change, exact-opportunity duplicate, retired-reference rejection, or missed-close replay-required outcome.

This is enforced by source-type admission rather than visual heuristics.

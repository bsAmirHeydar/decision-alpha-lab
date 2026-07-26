# Completeness Admission Policy

Default admission:

- COMPLETE: render;
- OPEN with at least one observed bar: render and update;
- PARTIAL: reject by default, optional explicit override;
- EMPTY, UNAVAILABLE, INVALID, UNKNOWN: reject.

The renderer never turns missing data into a zero-height box or an inferred range. `No data` remains a typed source condition.

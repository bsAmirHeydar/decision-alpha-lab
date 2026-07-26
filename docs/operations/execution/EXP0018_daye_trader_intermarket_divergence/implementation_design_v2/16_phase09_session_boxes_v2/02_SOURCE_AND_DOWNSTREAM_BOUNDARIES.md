# Source and Downstream Boundaries

Upstream authority belongs to P01 for time, P02 for exact-timestamp bars and P03 for session membership, OHLC, completeness and source lineage. P09 reads P03; it does not reimplement P01–P03.

P10 TWO/TDO, P11 replay and P12 audit may coexist with P09 but must not read rectangle geometry as analytical truth. Downstream components must use structured projection records or P03 snapshots.

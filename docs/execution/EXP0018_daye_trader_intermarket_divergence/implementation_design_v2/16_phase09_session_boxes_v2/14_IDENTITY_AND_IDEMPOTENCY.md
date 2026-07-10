# Identity and Idempotency

Projection identity combines the immutable symbol snapshot ID and chart ID. Object name derives only from the symbol snapshot ID. Repeated timers, reattachment and timeframe changes therefore converge on the same object rather than creating duplicates.

Price, color and processing time do not enter the object name.

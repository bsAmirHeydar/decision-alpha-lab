# BarRecord Contract

The normalized bar is the lowest market-data object consumed by later anatomy and simulation modules.

## Required invariants

- positive timeframe;
- open time strictly before close time;
- high greater than or equal to low;
- open and close inside the high-low range;
- nonnegative volumes and spread;
- ask not below bid when both exist;
- finite OHLC values;
- source identity recorded;
- deterministic stable bar ID.

## Why source identity matters

The same symbol and timestamp can differ across brokers, exchanges, synthetic CFD feeds, or corrected historical datasets. `source_id` and `source_bar_id` distinguish the observation. Later cross-feed validation must compare rather than silently merge them.

## Missing-data policy

A missing bid, ask, or real volume may be represented with the configured neutral value only if the source adapter documents that behavior. The quality of derived spread or execution features must then be marked missing or estimated. Bar normalization must never invent a future price.

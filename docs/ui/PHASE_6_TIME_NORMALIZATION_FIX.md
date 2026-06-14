# Phase 6 Time Normalization and Candle Loading Fix

## Root cause

The chart was not missing candles because of the frontend chart. The backend was returning only a handful of unique time values.

Some parquet caches store `time` as `datetime64[ms]`. Pandas can keep the millisecond unit after reading parquet. Calling:

```python
pd.to_datetime(df["time"]).astype("int64") // 10**9
```

on a `datetime64[ms]` series returns milliseconds first, then divides by one billion. A 2026 timestamp becomes around `1774` instead of `1774844100`. Thousands of M15 candles therefore collapsed into a few fake timestamps, and the UI showed `7 / 7`.

## Fix

- Force all datetime columns to `datetime64[ns]` before converting to Unix seconds.
- Apply the same conversion to event times: `node_time`, `entry_time`, `exit_time`, and `hunt_time`.
- Add a parquet compatibility reader that falls back to pyarrow without pandas metadata.
- Pick the largest readable OHLC cache file in each symbol/timeframe folder.
- Skip out-of-window events instead of collapsing them to candle index 0.

## Expected result

For `#US30 / M15` the visualization contract now returns:

```text
candles: 5000
actual_nodes: 621
actual_events: 1907
first event entry_index: 102
```

The chart should render real candles across the full time axis instead of only a few vertical candles.

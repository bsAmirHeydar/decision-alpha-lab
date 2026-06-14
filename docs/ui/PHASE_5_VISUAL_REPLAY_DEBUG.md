# Phase 5 Visual Replay Debug Fix

## Problems observed

1. The chart could show only 7/8 candles because `currentIndex` stayed near the beginning after the payload loaded.
2. The visualization request did not send the requested bar count to the backend.
3. Timeframe was a free-text input, which made repeated testing slower and error-prone.
4. Candle cache loading could accidentally select a tiny helper parquet file if multiple parquet files existed in the same dataset folder.
5. Crosshair labels needed to show both price and time in a clearer TradingView-style way.
6. Pylance warnings appeared when temporary test files were opened from Downloads instead of the project interpreter/source tree.

## Fixes

- The Replay Terminal now sets the replay cursor to the last loaded candle after a dataset reload.
- The UI sends `max_bars` to actual and random baseline endpoints.
- Symbol and timeframe controls are dropdowns.
- Cached datasets are listed from `/api/data/datasets`.
- Candle loader picks the largest readable OHLC parquet file for a symbol/timeframe.
- The chart fits content when the full loaded dataset is displayed.
- Crosshair readout updates from chart coordinates.
- Random baseline still overlays separately from actual nodes and can be toggled by layer.

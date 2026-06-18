# H0002 — Reversal vs Continuation Branch Volatility Model

## Abstract

H0002 classifies exact H0001/M0001 completed node-territory events into two node-side branches at the completed exit candle: reversal and continuation. The measurement remains locked to the original M0001 event RTV window. The branch label never changes the measured volatility window.

## Branch definition

For a LOW node, a completed exit close above the node price is `REVERSAL_AFTER_EXIT`, and a completed exit close below the node price is `CONTINUATION_AFTER_EXIT`. For a HIGH node, the mapping is inverted: a close below the node price is reversal, and a close above the node price is continuation.

## Branch model

The emerging model is not merely “which branch is higher.” It has four dimensions:

1. Frequency: reversal is the higher-frequency branch, while continuation tends to occur less often.
2. Intensity: continuation tends to produce higher event RTV and higher logRTV than reversal.
3. Tail: continuation tends to show fatter right-tail behavior, especially in P90/P95 and CVaR90/CVaR95.
4. Memory: continuation tends to preserve higher post-event horizon volatility than reversal.

The canonical model label is:

`continuation_lower_frequency_higher_intensity_higher_persistence_fatter_tail`

## Reporting

M0002 prints the branch model as separated non-truncated lines: `BRANCH_FREQUENCY`, `BRANCH_INTENSITY`, `BRANCH_TAIL`, `BRANCH_MEMORY`, and `BRANCH_MODEL_SUMMARY`. This replaces the earlier single long `BRANCH_MODEL` line that could be truncated by the MT5 Journal.

## Interpretation

H0002 is a branch-behavior model. It does not directly say buy or sell. It says that once a valid H0001 event has completed, the continuation-side exit is a lower-frequency but higher-intensity volatility state with stronger tail and memory characteristics.

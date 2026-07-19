# Pilot Context Model Card

## Identity

`CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1`

## Source

`lab/03_experiments/EXP0015_intermarket_time_divergence/experiment.py` at `sha256:99e5e03a4bf30a2ab94949e2ddc6cdc1d067f0441d25dbe0dc8a138026a9bd2f`.

## Intended use

Reference migration and deterministic behavioral parity testing only.

## Prohibited use

No active consumer cutover, production runtime, live orders, or capital decisions.

## Preserved limitations

Naive timestamps, no explicit timezone, no market-calendar model, no proof that evaluation bars are closed, batch-only state, and research-only suggested bias/outcome annotations.

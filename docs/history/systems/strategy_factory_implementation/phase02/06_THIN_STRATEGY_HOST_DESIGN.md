# Thin Strategy Host Design

`SF02_StrategyHost.mq5` is a composition root. It performs only:

1. Read inputs.
2. Build a validated runtime config.
3. Bind concrete adapters.
4. Initialize and start the runtime.
5. Forward `OnTick` and `OnTimer`.
6. Stop and shut down services.

It must never contain:

- Hook, F3, divergence, zone or Daye definitions;
- candidate geometry;
- risk sizing;
- model logic;
- broker request construction;
- statistics.

A static test scans the Host for strategy-specific vocabulary and order-authority calls.

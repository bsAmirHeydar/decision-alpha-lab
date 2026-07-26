# Consumed Low And High Cannot Reenter Divergence

Once price has passed through a low or high, that level is no longer fresh liquidity for this model.

The system must not keep comparing current price to an already-consumed internal level.

This applies before visual drawing, before ledger recording, and before future execution layers.

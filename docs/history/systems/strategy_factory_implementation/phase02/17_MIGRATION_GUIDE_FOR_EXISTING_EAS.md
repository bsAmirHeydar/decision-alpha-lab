# Migration Guide for Existing EAs

Existing EAs should not be rewritten immediately. Migration proceeds by strangler pattern:

1. Keep the current anatomy engine unchanged.
2. Add a small adapter that emits `SF01_AnatomyEvent`.
3. Route the event into the Strategy Runtime.
4. Compare existing visual truth with the event ledger.
5. Add the feature provider.
6. Only after parity, move downstream candidate and execution logic into shared modules.

The old EA remains available as rollback until golden fixtures and differential tests pass.

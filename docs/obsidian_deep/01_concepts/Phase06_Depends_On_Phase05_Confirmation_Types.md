# Phase 06 Depends On Phase 05 Confirmation Types

Phase 06 Visual Ledger is downstream of Phase 05 Confirmation and Invalidation Anatomy.

It must not redefine final signal status, direction, side, clean symbol, hunter symbol, or confirmation metadata.

Instead, it must consume the Phase 05 contract:

```text
SCGCFinalSignal
SCGCConfirmationConfig
CCGC_ConfirmationField
```

If these confirmation files are missing, Phase 06 cannot compile. The correct fix is to restore the Phase 05 dependency files, not to duplicate confirmation logic inside the visual-ledger layer.

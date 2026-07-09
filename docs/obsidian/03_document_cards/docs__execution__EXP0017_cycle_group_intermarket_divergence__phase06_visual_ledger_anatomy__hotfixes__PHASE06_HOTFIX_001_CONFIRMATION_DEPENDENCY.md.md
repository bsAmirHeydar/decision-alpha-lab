# Document Card — Phase 06 Hotfix 001 Confirmation Dependency

## Role

Restores the Phase 05 confirmation include files required by Phase 06 Visual Ledger.

## Root Cause

`CGC_Types.mqh` and `CGC_ConfirmationField.mqh` were missing from the terminal include path, causing cascade type errors in Phase 06 files.

## Doctrine

Phase 06 consumes Phase 05 final-signal anatomy. It must not duplicate confirmation logic.

# Packaging Pipeline

## Build order

1. Compile `GartalTerminal.mq5` in MetaEditor.
2. Compile `GartalNewsDownloaderEA.mq5` in MetaEditor.
3. Run `Check-GartalStage10.ps1`.
4. Run `Build-GartalReleaseCandidate.ps1`.
5. Inspect generated ZIP.
6. Install it into a clean MT5 data folder.
7. Run beta QA checklist.

## Script roles

- `Check-GartalStage10.ps1`: structural gate.
- `Package-GartalTerminal.ps1`: release zip builder.
- `Build-GartalReleaseCandidate.ps1`: opinionated beta wrapper.

## Important

PowerShell cannot compile MQL5 directly unless a dedicated MetaEditor CLI workflow is added later. Stage 10 therefore treats compilation as an external gate.

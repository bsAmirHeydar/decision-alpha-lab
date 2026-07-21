# Install — EXP0018 Phase 02 Multi-Symbol Data Synchronization v2

## Scope

Adds the isolated P02 exact-UTC, no-forward-fill data synchronization Expert, MQL5 modules, tests, contracts, documentation and Obsidian structure. P01 is a prerequisite and is not removed.

## Install

Extract this ZIP at the repository root with overwrite enabled. Run the provided PowerShell checks. Compile `mql5/Experts/DayeTrader/EXP0018_Daye_Data_Sync_Anatomy.mq5` in MetaEditor.

## Acceptance

- Python validator PASS
- pytest PASS
- MetaEditor 0 errors
- embedded self-tests PASS
- both symbols report synchronized history
- no synthetic pair for missing timestamp

## Rollback

Revert the phase commit or remove the new P02 Expert, `DAYE_Data*` include modules, P02 infra files, docs and Obsidian artifacts. Do not remove P01.

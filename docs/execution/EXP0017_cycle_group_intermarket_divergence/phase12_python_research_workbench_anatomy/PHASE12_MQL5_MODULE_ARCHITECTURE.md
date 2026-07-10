# Phase 12 MQL5 Module Architecture

## Expert

`EXP0017_CG_Python_Research_Bridge_Anatomy.mq5`

The expert runs once on init and writes a research bridge inventory.

## Include modules

- `CGP12_Types.mqh`: config, file inventory rows, run stats, CSV/JSON helpers.
- `CGP12_FileInventory.mqh`: checks expected Phase 07-11 files and estimates row/column counts.
- `CGP12_Writers.mqh`: writes inventory, manifest, registry template, Python run plan, diagnostics.
- `CGP12_Display.mqh`: compact chart comment and Experts-tab summary.
- `CGP12_Engine.mqh`: orchestrates the bridge run.

## No-trading boundary

The expert has no `CTrade`, no order function, no position scan, no risk size, and no signal execution.

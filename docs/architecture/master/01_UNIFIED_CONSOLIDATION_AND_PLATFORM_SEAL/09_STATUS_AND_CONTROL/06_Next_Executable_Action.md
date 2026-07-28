---
id: UCPS-FDC2715C3BC7
title: "Next Executable Action"
type: action
status: active
domain: unified-consolidation-platform-seal
version: 2.0.0
created: 2026-07-23
updated: 2026-07-28
tags:
  - consolidation
  - platform-seal
---
# Next Executable Action

## Action

Execute the one-shot UC-04 native seal using `tools/consolidation/uc04complete/Invoke-UC04CompleteNativeSeal.ps1` with `-FinalizeRepository` on the Windows MetaEditor/MetaTrader installation host.

## Required outcome

- every target in `native_acceptance_contract.json` compiles with zero errors and zero warnings;
- the complete runtime self-test reports PASS and zero failed rows;
- evidence hashes pass independent review;
- tracked production source remains unchanged;
- `uc04_acceptance.json` and `uc05_handoff_decision.json` are materialized only after PASS.

No further UC-04 implementation wave is authorized or required. A native failure reopens only the failing capability under the same contracts; it does not authorize unrelated changes.

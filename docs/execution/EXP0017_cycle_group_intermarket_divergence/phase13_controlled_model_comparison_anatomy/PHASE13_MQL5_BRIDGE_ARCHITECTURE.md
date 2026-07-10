# Phase 13 MQL5 Bridge Architecture

The MQL5 component does not fit statistical models. Its responsibilities are limited to terminal-side preflight and handoff:

- inspect Phase 10 dataset visibility;
- inspect Phase 11 fold-plan visibility;
- inspect Phase 12.5 readiness status;
- block the Python run plan when required inputs are absent;
- write a file inventory;
- write a research manifest;
- write an experiment-registry template;
- write the deterministic Python run plan.

Modules:

- `CGP13_Types.mqh` — contracts;
- `CGP13_FileInventory.mqh` — file and readiness inspection;
- `CGP13_Writers.mqh` — manifest and plan outputs;
- `CGP13_Display.mqh` — compact terminal status;
- `CGP13_Engine.mqh` — orchestration.

The canonical model-comparison implementation remains Python because model fitting, calibration analysis, coefficient review, and HTML reporting are research workloads rather than chart-event workloads.

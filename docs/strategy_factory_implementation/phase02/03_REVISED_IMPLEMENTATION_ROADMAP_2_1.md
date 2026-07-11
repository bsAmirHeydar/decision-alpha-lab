---
title: "Revised Implementation Roadmap 2.1 — MQL5 First"
---

# Revised Implementation Roadmap 2.1

The proposal changes the implementation order. Shared market and time services move immediately after the runtime foundation because every anatomy plugin depends on them. The plugin SDK follows those services so plugins cannot create private clocks or private bar caches.

## Revised Critical Path

```text
Phase 01 Contracts
→ Phase 02 Runtime Host and Ports
→ Phase 03 Market Cache / Time Kernel / Symbol Specs / Synchronization
→ Phase 04 Static Plugin Registry and Anatomy SDK
→ Phase 05 Runtime Generations and Result Sinks
→ Phase 06 First Anatomy Adapter
→ Phase 07 Context and Feature DAG
→ Phase 08 Candidate Policy Kernel
→ Phase 09 Outcome Engine
→ Phase 10 Strategy Tester Research Harness
→ Phase 11 Statistics Export and Python Research Pack
→ Phase 12 Anti-Overfit Gates
→ Phase 13–15 Training, ONNX and Decision Runtime
→ Phase 16–19 Risk, Paper, Execution and Observability
→ Phase 20–21 Pilot Closure
```

## Why the Order Changed

The previous roadmap placed plugin infrastructure before the shared market services. That would allow plugins to accidentally own time, symbol synchronization or data retrieval. The new order ensures market truth is centralized before plugins are admitted.

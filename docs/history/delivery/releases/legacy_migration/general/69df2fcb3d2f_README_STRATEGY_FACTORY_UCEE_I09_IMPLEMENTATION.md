# UCEE-I09 — Advanced Task Algorithm Pack

This patch implements governed ranking, treatment selection, survival, competing-risk, quantile/distributional, multi-task, regime-gating, and bounded offline-policy learning surfaces for the Universal Context Exploitation Engine.

The delivery is intentionally split between offline Python training/evaluation and MQL5 runtime contracts. It introduces no broker or order authority. Optional advanced libraries are catalogued explicitly; native deterministic reference implementations keep conformance runnable without extra dependencies.

Run `tools/strategy_factory/run_uce_i09_tests.ps1` before commit. MetaEditor compilation remains a local Windows acceptance gate.

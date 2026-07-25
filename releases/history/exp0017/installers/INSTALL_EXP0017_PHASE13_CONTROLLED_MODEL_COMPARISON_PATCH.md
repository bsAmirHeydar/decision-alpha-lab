# Install — EXP0017 Phase 13 Controlled Model Comparison

This patch adds:

- MQL5 terminal-side preflight bridge;
- deterministic standard-library Python model comparison;
- bucket, threshold, logistic, ridge, and constrained ensemble candidates;
- walk-forward metrics, calibration, stability, leakage audit, model cards, HTML report, and experiment registry;
- detailed documentation and Obsidian navigation.

## Sequence

1. Install patch at repository root.
2. Compile `EXP0017_CG_Controlled_Model_Comparison_Bridge.mq5`.
3. Ensure Phase 10, Phase 11, and Phase 12.5 outputs are available in the selected data directory.
4. Run the Phase 12.5 integrity gate.
5. Run `research/exp0017_phase13/powershell/run_phase13_model_comparison.ps1`.
6. Review model cards, leakage audit, fold stability, and leaderboard.

Phase 13 is research-only and grants no execution authority.

# Alpha Lab ACL-10 — Promotion State Machine

This patch implements the deterministic ACL-10 reference promotion-state evaluator. It verifies the complete ACL-09 memory/planner package, freezes closed state/transition/prerequisite registries, evaluates all source subjects, preserves UNKNOWN, quarantines diagnostics, keeps baselines reference-only and produces an empty runtime-candidate manifest for the zero-eligible reference fixture.

Claim ceiling: `PROMOTION_STATE_DECISION_REFERENCE_ONLY`.

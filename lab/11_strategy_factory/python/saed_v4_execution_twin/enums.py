EVIDENCE_CLASSES = {"reference_synthetic", "calibrated_research", "external_qualified"}
EVIDENCE_ROLES = {"development", "training", "validation", "protected_final", "prospective", "shadow", "live"}
ORDER_STATES = {
    "registered", "submitted", "acknowledged", "partially_filled", "filled",
    "cancel_requested", "cancelled", "expired", "rejected", "exit_submitted", "closed", "non_order"
}
TWIN_STATUSES = {"non_order", "rejected", "unfilled", "partially_filled", "filled", "broker_infeasible"}
SCENARIO_KINDS = {"nominal", "latency_stress", "spread_stress", "queue_stress", "partial_fill_stress", "broker_reject_stress", "combined_stress"}

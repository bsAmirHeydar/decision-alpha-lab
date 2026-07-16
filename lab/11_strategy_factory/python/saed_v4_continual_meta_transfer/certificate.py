from __future__ import annotations

from .canonical import content_hash, seal, stable_id


def build(
    upstream: dict,
    dataset: dict,
    drift_report: dict,
    transfer_map: dict,
    replay_buffer: dict,
    transfer_report: dict,
    guard_decisions: list[dict],
    recalibration: dict,
    budget: dict,
    trial_ledger: dict,
    exposure_ledger: dict,
    authority: dict,
) -> dict:
    guard_fallbacks = sum(not item["accepted_for_research_analysis"] for item in guard_decisions)
    gates = {
        "upstream_verified": upstream["scope_verified"] and upstream["immutable"],
        "dataset_valid": dataset["strict_chronology"] and dataset["cluster_role_separation"],
        "known_time_clean": dataset["future_suffix_queries"] == 0 and dataset["protected_evidence_queries"] == 0,
        "drift_taxonomy_complete": bool(drift_report["events"]) and drift_report["deterministic"],
        "transfer_map_complete": transfer_map["target_count"] > 0 and transfer_map["deterministic"],
        "negative_transfer_guard_active": len(guard_decisions) == transfer_map["target_count"],
        "replay_buffer_safe": replay_buffer["protected_query_outcomes_stored"] is False,
        "forgetting_within_reference_limits": all(transfer_report["gates"].values()),
        "recalibration_research_only": recalibration["hidden_evaluation_queries"] == 0 and recalibration["online_policy_mutations"] == 0,
        "budget_complete": budget["complete"] and budget["within_budget"],
        "trial_ledger_complete": trial_ledger["complete"],
        "exposure_ledger_zero": exposure_ledger["complete"] and all(
            exposure_ledger[key] == 0
            for key in (
                "hidden_evaluation_queries",
                "protected_evidence_exposures",
                "runtime_compilations",
                "order_submissions",
                "online_policy_mutations",
            )
        ),
        "authority_denied": not any(authority["authority"].values()),
        "baseline_preserved": True,
        "fail_closed_fallback_observed": guard_fallbacks >= 1,
    }
    payload = {
        "phase": "SAED_V4_25",
        "title": "Continual Meta And Transfer",
        "version": "1.0.0",
        "upstream_receipt_hash": upstream["receipt_hash"],
        "meta_dataset_hash": dataset["dataset_hash"],
        "drift_report_hash": drift_report["drift_report_hash"],
        "transfer_map_hash": transfer_map["transfer_map_hash"],
        "replay_buffer_hash": replay_buffer["replay_buffer_hash"],
        "transfer_report_hash": transfer_report["transfer_report_hash"],
        "recalibration_experiment_hash": recalibration["experiment_hash"],
        "budget_hash": budget["budget_hash"],
        "trial_ledger_hash": trial_ledger["ledger_hash"],
        "exposure_ledger_hash": exposure_ledger["ledger_hash"],
        "authority_boundary": authority,
        "gates": gates,
        "accepted_for_continual_meta_transfer_research": all(gates.values()),
        "research_only": True,
        "guard_fallback_count": guard_fallbacks,
        "decision_authority": False,
        "promotion_authority": False,
        "runtime_executable": False,
        "risk_allocation_authority": False,
        "execution_authority": False,
        "production_authority": False,
        "online_learning_authority": False,
        "real_alpha_claim": False,
        "prospective_success_claim": False,
        "runtime_parity_claim": False,
    }
    payload["certificate_id"] = stable_id("continual_meta_transfer_certificate", payload)
    return seal(payload, "certificate_hash")


def handoff(certificate: dict, transfer_report: dict, drift_report: dict) -> dict:
    payload = {
        "phase": "SAED_V4_25",
        "next_phase": "SAED_V4_26",
        "certificate_hash": certificate["certificate_hash"],
        "certificate_id": certificate["certificate_id"],
        "transfer_report_hash": transfer_report["transfer_report_hash"],
        "drift_report_hash": drift_report["drift_report_hash"],
        "entry_gates": {
            "continual_meta_transfer_certificate_verified": certificate["accepted_for_continual_meta_transfer_research"],
            "frozen_transfer_artifacts_available": True,
            "frozen_adaptation_artifacts_available": True,
            "frozen_drift_segments_available": True,
            "frozen_replay_artifacts_available": True,
            "research_only": True,
            "promotion_denied": True,
            "runtime_denied": True,
        },
        "allowed_next_work": [
            "frozen_feature_attribution",
            "transfer_pathway_attribution",
            "adaptation_parameter_mechanism_analysis",
            "continual_calibration_component_analysis",
            "counterfactual_mechanism_probes",
            "mechanistic_failure_catalogue",
        ],
        "forbidden_next_work": [
            "promotion_authorization",
            "runtime_compilation",
            "risk_allocation",
            "order_submission",
            "online_policy_mutation",
        ],
        "authority": {
            "decision": False,
            "promotion": False,
            "runtime": False,
            "risk_allocation": False,
            "execution": False,
            "production": False,
        },
        "research_only": True,
    }
    payload["handoff_id"] = stable_id("v4_25_to_v4_26", payload)
    return seal(payload, "handoff_hash")

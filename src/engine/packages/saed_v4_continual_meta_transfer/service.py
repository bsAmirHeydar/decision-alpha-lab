from __future__ import annotations

from .adaptation import adapt
from .authority import boundary
from .budget import ResearchLedger
from .canonical import content_hash
from .certificate import build as build_certificate, handoff as build_handoff
from .continual import fit_past_only
from .contracts import (
    AdaptationContract,
    ContinualCalibrationContract,
    DriftTaxonomyContract,
    ForgettingContract,
    MetaDatasetContract,
    RecalibrationExperimentContract,
    ReplayContract,
    ResearchBudget,
    TransferContract,
    UpstreamIntakeContract,
)
from .dataset import by_role, validate
from .drift import segment
from .guard import evaluate as evaluate_guard
from .meta_features import build as build_meta_features
from .metrics import evaluate as evaluate_transfers, predict, transfer_report
from .recalibration import run as run_recalibration
from .regularization import anchor
from .replay import build as build_replay
from .replay_receipt import build as build_replay_receipt
from .security import scan
from .transfer import map_transfers
from .upstream import verify


def run(config: dict, upstream_documents: dict, tasks: list[dict]) -> dict:
    scan(config)
    scan(upstream_documents)
    scan(tasks)

    upstream_contract = UpstreamIntakeContract.from_mapping(config["upstream_intake"])
    dataset_contract = MetaDatasetContract.from_mapping(config["meta_dataset_contract"])
    drift_contract = DriftTaxonomyContract.from_mapping(config["drift_taxonomy_contract"])
    transfer_contract = TransferContract.from_mapping(config["transfer_contract"])
    adaptation_contract = AdaptationContract.from_mapping(config["adaptation_contract"])
    continual_contract = ContinualCalibrationContract.from_mapping(config["continual_calibration_contract"])
    replay_contract = ReplayContract.from_mapping(config["replay_contract"])
    forgetting_contract = ForgettingContract.from_mapping(config["forgetting_contract"])
    recalibration_contract = RecalibrationExperimentContract.from_mapping(config["recalibration_experiment_contract"])
    budget_contract = ResearchBudget.from_mapping(config["research_budget"])
    ledger = ResearchLedger(budget_contract)

    upstream = verify(upstream_contract, upstream_documents)
    dataset_summary = validate(tasks, dataset_contract, ledger)
    roles = by_role(tasks)
    meta_features = build_meta_features(tasks)
    drift_report = segment(meta_features, drift_contract)

    transfer_map = map_transfers(
        targets=tasks,
        sources=roles["meta_train"],
        meta_features=meta_features,
        contract=transfer_contract,
        ledger=ledger,
    )
    prior_by_target = {item["target_task_id"]: item for item in transfer_map["priors"]}
    adaptations = [adapt(task, prior_by_target[task["task_id"]], adaptation_contract, ledger) for task in tasks]
    adaptation_by_task = {item["task_id"]: item for item in adaptations}
    regularizations = [anchor(adaptation_by_task[task["task_id"]], task) for task in tasks]
    regularization_by_task = {item["task_id"]: item for item in regularizations}

    evaluations = evaluate_transfers(tasks, regularizations)
    evaluation_by_task = {item["task_id"]: item for item in evaluations}
    ledger.consume("bootstrap_draws", forgetting_contract.bootstrap_draws, "cluster bootstrap transfer uncertainty")
    transfer_metrics = transfer_report(evaluations, forgetting_contract)
    drift_by_task = {item["task_id"]: item for item in drift_report["events"]}
    guard_decisions = [
        evaluate_guard(
            task,
            prior_by_target[task["task_id"]],
            drift_by_task[task["task_id"]],
            evaluation_by_task[task["task_id"]],
        )
        for task in tasks
    ]

    predictions_by_task = {
        task["task_id"]: predict(task["query_features"], regularization_by_task[task["task_id"]]["anchored_parameters"])
        for task in tasks
    }
    continual_states = fit_past_only(tasks, predictions_by_task, continual_contract)
    replay_buffer = build_replay(tasks, drift_report["events"], meta_features, replay_contract, ledger)
    recalibration = run_recalibration(evaluations, recalibration_contract, ledger)

    trial_ledger = {
        "phase": "SAED_V4_25",
        "trials": [
            {"trial_id": "trial_meta_dataset_001", "family": "chronological_cluster_safe_meta_dataset", "status": "completed", "promotion_eligible": False},
            {"trial_id": "trial_transfer_map_001", "family": "support_ood_distance_transfer_mapping", "status": "completed", "promotion_eligible": False},
            {"trial_id": "trial_adaptation_001", "family": "regularized_empirical_bayes_linear", "status": "completed", "promotion_eligible": False},
            {"trial_id": "trial_continual_calibration_001", "family": "past_only_sliding_conformal_calibration", "status": "completed", "promotion_eligible": False},
            {"trial_id": "trial_replay_001", "family": "deterministic_stratified_rehearsal", "status": "completed", "promotion_eligible": False},
            {"trial_id": "trial_recalibration_grid_001", "family": "offline_safe_recalibration", "status": "completed", "promotion_eligible": False},
        ],
        "complete": True,
    }
    trial_ledger["ledger_hash"] = content_hash(trial_ledger)
    exposure_ledger = {
        "phase": "SAED_V4_25",
        "hidden_evaluation_queries": 0,
        "protected_evidence_exposures": 0,
        "runtime_compilations": 0,
        "order_submissions": 0,
        "online_policy_mutations": 0,
        "network_requests": 0,
        "complete": True,
    }
    exposure_ledger["ledger_hash"] = content_hash(exposure_ledger)
    budget_snapshot = ledger.snapshot()
    authority_boundary = boundary()
    certificate = build_certificate(
        upstream,
        dataset_summary,
        drift_report,
        transfer_map,
        replay_buffer,
        transfer_metrics,
        guard_decisions,
        recalibration,
        budget_snapshot,
        trial_ledger,
        exposure_ledger,
        authority_boundary,
    )
    handoff = build_handoff(certificate, transfer_metrics, drift_report)

    outputs = {
        "upstream_receipt": upstream,
        "meta_dataset_summary": dataset_summary,
        "meta_features": meta_features,
        "drift_report": drift_report,
        "transfer_map": transfer_map,
        "adaptations": adaptations,
        "regularizations": regularizations,
        "transfer_evaluations": evaluations,
        "transfer_report": transfer_metrics,
        "negative_transfer_guards": guard_decisions,
        "continual_calibration_states": continual_states,
        "replay_buffer": replay_buffer,
        "recalibration_experiment": recalibration,
        "trial_ledger": trial_ledger,
        "exposure_ledger": exposure_ledger,
        "budget_snapshot": budget_snapshot,
        "authority_boundary": authority_boundary,
        "certificate": certificate,
        "handoff": handoff,
    }
    outputs["replay_receipt"] = build_replay_receipt(
        content_hash(config),
        {"upstream_documents": content_hash(upstream_documents), "tasks": content_hash(tasks)},
        {key: content_hash(value) for key, value in outputs.items()},
    )
    return outputs

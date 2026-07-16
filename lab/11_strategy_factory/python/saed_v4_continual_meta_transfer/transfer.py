from __future__ import annotations

import math

from .budget import ResearchLedger
from .canonical import content_hash, seal, stable_id
from .contracts import TransferContract
from .numerics import l2_distance, weighted_mean


def source_candidates(target: dict, sources: list[dict], feature_by_task: dict[str, dict], contract: TransferContract, ledger: ResearchLedger) -> list[dict]:
    target_feature = feature_by_task[target["task_id"]]
    candidates = []
    for source in sources:
        ledger.consume("source_evaluations", 1, f"{source['task_id']}->{target['task_id']}")
        if contract.same_cluster_forbidden and source["cluster_id"] == target["cluster_id"]:
            continue
        if contract.future_source_forbidden and source["decision_time"] >= target["decision_time"]:
            continue
        if float(source["support_score"]) < contract.minimum_source_support:
            continue
        if float(source["ood_pvalue"]) < contract.minimum_source_ood_pvalue:
            continue
        source_feature = feature_by_task[source["task_id"]]
        distance = l2_distance(source_feature["vector"], target_feature["vector"]) / max(1.0, len(target_feature["vector"]) ** 0.5)
        if distance > contract.maximum_meta_distance:
            continue
        regime_bonus = 1.15 if source["regime"] == target["regime"] else 1.0
        context_bonus = 1.10 if source["context_id"] == target["context_id"] else 1.0
        weight = regime_bonus * context_bonus * float(source["support_score"]) * float(source["ood_pvalue"]) / (1.0 + distance)
        candidates.append({
            "source_task_id": source["task_id"],
            "source_context_id": source["context_id"],
            "distance": distance,
            "weight": weight,
            "same_regime": source["regime"] == target["regime"],
            "same_context": source["context_id"] == target["context_id"],
            "query_outcomes_accessed": False,
        })
    candidates.sort(key=lambda item: (-item["weight"], item["distance"], item["source_task_id"]))
    return candidates[: contract.maximum_sources]


def build_prior(target: dict, candidates: list[dict], task_by_id: dict[str, dict]) -> dict:
    if not candidates:
        parameters = [float(value) for value in target["baseline_parameters"]]
        fallback = True
    else:
        vectors = [[float(value) for value in task_by_id[item["source_task_id"]]["baseline_parameters"]] for item in candidates]
        weights = [float(item["weight"]) for item in candidates]
        parameters = weighted_mean(vectors, weights)
        fallback = False
    payload = {
        "target_task_id": target["task_id"],
        "source_task_ids": [item["source_task_id"] for item in candidates],
        "source_weights": [item["weight"] for item in candidates],
        "prior_parameters": parameters,
        "fallback_to_scratch": fallback,
        "source_query_outcomes_accessed": False,
    }
    payload["transfer_prior_id"] = stable_id("transfer_prior", payload)
    return seal(payload, "transfer_prior_hash")


def map_transfers(targets: list[dict], sources: list[dict], meta_features: list[dict], contract: TransferContract, ledger: ResearchLedger) -> dict:
    feature_by_task = {item["task_id"]: item for item in meta_features}
    task_by_id = {item["task_id"]: item for item in sources + targets}
    edges = []
    priors = []
    for target in targets:
        candidates = source_candidates(target, sources, feature_by_task, contract, ledger)
        prior = build_prior(target, candidates, task_by_id)
        priors.append(prior)
        for candidate in candidates:
            edges.append({
                "edge_id": stable_id("transfer_edge", {"source": candidate["source_task_id"], "target": target["task_id"], "weight": candidate["weight"]}),
                "source_task_id": candidate["source_task_id"],
                "target_task_id": target["task_id"],
                "distance": candidate["distance"],
                "weight": candidate["weight"],
                "same_regime": candidate["same_regime"],
                "same_context": candidate["same_context"],
                "eligible": True,
            })
    payload = {
        "phase": "SAED_V4_25",
        "edge_count": len(edges),
        "target_count": len(targets),
        "edges": edges,
        "priors": priors,
        "future_source_queries": 0,
        "source_query_outcome_queries": 0,
        "deterministic": True,
    }
    payload["transfer_map_id"] = stable_id("transfer_map", payload)
    return seal(payload, "transfer_map_hash")

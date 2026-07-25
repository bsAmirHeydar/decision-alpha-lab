from __future__ import annotations

from .canonical import seal, stable_id


def build(config_hash: str, input_hashes: dict[str, str], output_hashes: dict[str, str]) -> dict:
    payload = {
        "phase": "SAED_V4_25",
        "config_hash": config_hash,
        "input_hashes": dict(sorted(input_hashes.items())),
        "output_hashes": dict(sorted(output_hashes.items())),
        "deterministic": True,
        "network_access": False,
        "future_suffix_queries": 0,
        "protected_evidence_queries": 0,
        "hidden_evaluation_queries": 0,
        "runtime_compilations": 0,
        "order_submissions": 0,
        "online_policy_mutations": 0,
    }
    payload["replay_id"] = stable_id("replay_receipt", payload)
    return seal(payload, "replay_hash")

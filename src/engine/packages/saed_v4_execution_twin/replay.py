from __future__ import annotations
from .canonical import content_hash, stable_id
from .twin import build_execution_twin


def replay(cube: dict, handoff: dict, profile, expected_twin: dict) -> tuple[dict, dict]:
    actual = build_execution_twin(cube, handoff, profile)
    matched = actual["twin_hash"] == expected_twin["twin_hash"] and actual == expected_twin
    receipt = {"expected_twin_hash": expected_twin["twin_hash"], "actual_twin_hash": actual["twin_hash"], "matched": matched}
    receipt["replay_id"] = stable_id("exectwinreplay", receipt); receipt["replay_hash"] = content_hash(receipt)
    return actual, receipt

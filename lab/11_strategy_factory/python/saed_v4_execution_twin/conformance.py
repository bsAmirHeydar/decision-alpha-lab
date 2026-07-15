from __future__ import annotations
from .models import ExecutionTwinProfile
from .twin import build_execution_twin


def run_vectors(vectors: dict, cube: dict, handoff: dict, profile_mapping: dict) -> dict:
    results = []
    for vector in vectors["vectors"]:
        mapping = dict(profile_mapping)
        mapping["scenarios"] = [s for s in profile_mapping["scenarios"] if s["scenario_id"] in vector["scenario_ids"]]
        try:
            twin = build_execution_twin(cube, handoff, ExecutionTwinProfile.from_mapping(mapping))
            passed = twin["complete_exposure"] and twin["scenario_count"] == len(vector["scenario_ids"])
            detail = twin["twin_hash"]
        except Exception as exc:
            passed = False; detail = f"{type(exc).__name__}:{exc}"
        results.append({"vector_id": vector["vector_id"], "passed": passed, "detail": detail})
    return {"phase": "SAED_V4_09", "results": results, "passed": all(r["passed"] for r in results)}

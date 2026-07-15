from .canonical import content_hash, stable_id, merkle_root
from .errors import IntegrityError

DECLARED_HASH_KEYS = (
    "compiled_program_hash",
    "trace_hash",
    "registry_hash",
    "benchmark_hash",
    "ledger_hash",
    "manifest_hash",
    "telemetry_hash",
)
ID_KEYS = (
    "compiled_program_id",
    "trace_id",
    "registry_id",
    "benchmark_id",
    "ledger_id",
    "manifest_id",
    "telemetry_id",
)

def build_receipt(*artifacts: dict) -> dict:
    commitments = []
    refs = []
    for artifact in artifacts:
        commitment = content_hash(artifact)
        commitments.append(commitment)
        refs.append({
            "artifact_id": next((artifact[key] for key in ID_KEYS if key in artifact), "anonymous"),
            "content_commitment": commitment,
            "declared_artifact_hash": next((artifact[key] for key in DECLARED_HASH_KEYS if key in artifact), None),
        })
    payload = {
        "phase": "SAED_V4_10",
        "artifact_refs": refs,
        "artifact_count": len(refs),
        "artifact_merkle_root": merkle_root(sorted(commitments)),
        "complete": True,
        "authority": "reference_only",
    }
    payload["receipt_id"] = stable_id("v410integrity", payload)
    payload["receipt_hash"] = content_hash(payload)
    return payload

def verify_receipt(receipt: dict, artifacts: list[dict]) -> None:
    rebuilt = build_receipt(*artifacts)
    if receipt["artifact_merkle_root"] != rebuilt["artifact_merkle_root"]:
        raise IntegrityError("integrity merkle mismatch")

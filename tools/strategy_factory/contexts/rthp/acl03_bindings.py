
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.strategy_factory.acl_os.acl_03.canonical import digest_object, stable_id


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _dump(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def build_rthp_bindings(package_root: Path, compiled_root: Path, output_root: Path) -> dict[str, Any]:
    manifest_text = (package_root / "context_manifest.yaml").read_text(encoding="utf-8")
    context_id = next(line.split(":", 1)[1].strip() for line in manifest_text.splitlines() if line.startswith("context_id:"))
    context_version = next(line.split(":", 1)[1].strip() for line in manifest_text.splitlines() if line.startswith("context_version:"))

    detector = _load(compiled_root / "ir/detector_ir.json")
    occurrence = _load(compiled_root / "ir/occurrence_ir.json")
    known = _load(compiled_root / "ir/known_time_ir.json")
    features = _load(compiled_root / "ir/feature_binding_ir.json")
    snapshot = _load(compiled_root / "source/source_snapshot.json")
    onboarding = _load(compiled_root / "reports/onboarding_report.json")
    handoff = _load(compiled_root / "handoff/acl04_handoff.json")
    receipt = _load(compiled_root / "compilation_receipt.json")

    twin_body = {
        "schema_version": "1.0.0",
        "seed_id": stable_id("RTHP_TWIN_SEED", context_id, context_version, snapshot["snapshot_digest"]),
        "context_id": context_id,
        "context_version": context_version,
        "source_snapshot_digest": snapshot["snapshot_digest"],
        "detector_ir_digest": detector["detector_ir_digest"],
        "occurrence_ir_digest": occurrence["occurrence_ir_digest"],
        "known_time_ir_digest": known["known_time_ir_digest"],
        "feature_binding_ir_digest": features["feature_binding_ir_digest"],
        "node_types": [
            "CONTEXT", "SYMBOL_PAIR", "SYMBOL", "CYCLE_DEFINITION", "CYCLE_INSTANCE",
            "REFERENCE_LEVEL", "TOUCH_OBSERVATION", "DIVERGENCE_OCCURRENCE", "REFERENCE_STATE", "SIGNAL_FAMILY"
        ],
        "edge_types": [
            "PAIR_CONTAINS_SYMBOL", "CYCLE_INSTANTIATES_DEFINITION", "LEVEL_BELONGS_TO_CYCLE",
            "TOUCH_OBSERVES_LEVEL", "OCCURRENCE_USES_REFERENCE", "OCCURRENCE_HAS_HUNTER",
            "OCCURRENCE_HAS_PROTECTED", "OCCURRENCE_BELONGS_TO_FAMILY", "STATE_PROJECTS_REFERENCE"
        ],
        "observable_views": [b["view_id"] for b in features["bindings"]],
        "causal_clock_order": [f"{g['left_clock']}<={g['right_clock']}" for g in known["guards"]],
        "immutable_semantics": True,
        "implementation_status": "TWIN_SEED_READY",
        "learning_authority_created": False,
        "treatment_authority_created": False,
        "live_order_submission_allowed": False,
        "capital_activation_allowed": False,
    }
    twin = {**twin_body, "seed_digest": digest_object(twin_body)}

    saed_body = {
        "schema_version": "1.0.0",
        "binding_id": stable_id("RTHP_SAED_BINDING", context_id, context_version),
        "binding_kind": "SAED_CONTEXT_DIGITAL_TWIN_SEED",
        "context_id": context_id,
        "context_version": context_version,
        "twin_seed_digest": twin["seed_digest"],
        "accepted_inputs": ["ACL03_DETECTOR_IR", "ACL03_OCCURRENCE_IR", "ACL03_KNOWN_TIME_IR", "ACL03_FEATURE_BINDING_IR"],
        "emitted_contracts": ["RTHP_CONTEXT_DIGITAL_TWIN_SEED", "RTHP_EVENT_VIEW", "RTHP_REFERENCE_STATE_VIEW"],
        "allowed_operations": ["BUILD_CONTEXT_TWIN", "MATERIALIZE_KNOWN_TIME_SAFE_VIEWS", "REGISTER_CONTEXT_LINEAGE"],
        "forbidden_operations": ["TRAIN_MODEL", "CREATE_LABEL", "DEFINE_TREATMENT", "SUBMIT_ORDER", "ACTIVATE_CAPITAL"],
        "implementation_status": "CONTRACT_AND_SEED_READY",
        "qualification_status": "ADAPTER_IMPLEMENTATION_REQUIRED",
        "live_order_submission_allowed": False,
        "capital_activation_allowed": False,
    }
    saed = {**saed_body, "binding_digest": digest_object(saed_body)}

    ucee_body = {
        "schema_version": "1.0.0",
        "binding_id": stable_id("RTHP_UCEE_BINDING", context_id, context_version),
        "binding_kind": "UCEE_CONTEXT_FEATURE_SOURCE",
        "context_id": context_id,
        "context_version": context_version,
        "feature_binding_ir_digest": features["feature_binding_ir_digest"],
        "available_context_views": [b["view_id"] for b in features["bindings"]],
        "allowed_operations": ["READ_CONTEXT_OCCURRENCES", "READ_REFERENCE_STATES", "VALIDATE_KNOWN_TIME"],
        "forbidden_operations": ["ALTER_CONTEXT_SEMANTICS", "INVENT_CONTEXT_FIELDS", "CREATE_UNAPPROVED_LABELS", "TRAIN_BEFORE_ACL05", "SUBMIT_ORDER", "ACTIVATE_CAPITAL"],
        "research_entry_ready": False,
        "research_entry_blockers": ["ACL04_DUAL_SETUP_FACTORY_REQUIRED", "ACL05_IMMUTABLE_BATCH_REQUIRED"],
        "implementation_status": "CONTRACT_READY",
        "live_order_submission_allowed": False,
        "capital_activation_allowed": False,
    }
    ucee = {**ucee_body, "binding_digest": digest_object(ucee_body)}

    mql_body = {
        "schema_version": "1.0.0",
        "mirror_id": stable_id("RTHP_MQL5_STATIC_MIRROR", context_id, context_version),
        "context_id": context_id,
        "context_version": context_version,
        "detector_ir_digest": detector["detector_ir_digest"],
        "occurrence_ir_digest": occurrence["occurrence_ir_digest"],
        "known_time_ir_digest": known["known_time_ir_digest"],
        "mirror_scope": ["IDENTITY_ALIAS_CONSTANTS", "CLAIM_CEILING", "IR_DIGEST_PINNING"],
        "runtime_detector_implemented": False,
        "order_submission_allowed": False,
        "capital_access_allowed": False,
        "implementation_status": "STATIC_DIAGNOSTIC_MIRROR_READY",
    }
    mql = {**mql_body, "mirror_digest": digest_object(mql_body)}

    matrix_body = {
        "schema_version": "1.0.0",
        "context_id": context_id,
        "context_version": context_version,
        "highest_state": onboarding["highest_state"],
        "acl03_decision": onboarding["decision"],
        "gates": {
            "independent_review": "PASS",
            "source_freeze": "PASS",
            "authority_binding": "PASS",
            "detector_ir": "PASS",
            "occurrence_ir": "PASS",
            "known_time_ir": "PASS",
            "feature_binding_ir": "PASS",
            "golden_replay": "PASS",
            "security_boundary": "PASS",
            "saed_seed_contract": "PASS",
            "ucee_context_source_contract": "PASS",
            "adapter_runtime_qualification": "PENDING",
            "acl04_setup_authority": "NOT_GRANTED",
            "acl05_research_batch": "NOT_CREATED",
            "live_activation": "FORBIDDEN",
        },
        "allowed_next_actions": onboarding["allowed_next_actions"],
        "acl04_handoff_digest": handoff["handoff_digest"],
        "compilation_receipt_digest": receipt["receipt_digest"],
        "claim_ceiling": "CONTEXT_COMPILATION_AND_ONBOARDING_REFERENCE_ONLY",
        "live_order_submission_allowed": False,
        "capital_activation_allowed": False,
    }
    matrix = {**matrix_body, "matrix_digest": digest_object(matrix_body)}

    output_root.mkdir(parents=True, exist_ok=True)
    paths = {
        "twin_seed": output_root / "rthp_context_twin_seed.json",
        "saed_binding": output_root / "rthp_saed_binding.json",
        "ucee_binding": output_root / "rthp_ucee_binding.json",
        "mql5_mirror": output_root / "rthp_mql5_static_mirror.json",
        "readiness_matrix": output_root / "rthp_acl03_readiness_matrix.json",
    }
    for key, value in (("twin_seed", twin), ("saed_binding", saed), ("ucee_binding", ucee), ("mql5_mirror", mql), ("readiness_matrix", matrix)):
        _dump(paths[key], value)

    bundle_body = {
        "schema_version": "1.0.0",
        "context_id": context_id,
        "context_version": context_version,
        "source_snapshot_digest": snapshot["snapshot_digest"],
        "compilation_receipt_digest": receipt["receipt_digest"],
        "artifacts": {key: value.name for key, value in paths.items()},
        "artifact_digests": {
            "twin_seed": twin["seed_digest"],
            "saed_binding": saed["binding_digest"],
            "ucee_binding": ucee["binding_digest"],
            "mql5_mirror": mql["mirror_digest"],
            "readiness_matrix": matrix["matrix_digest"],
        },
        "live_order_submission_allowed": False,
        "capital_activation_allowed": False,
    }
    bundle = {**bundle_body, "bundle_digest": digest_object(bundle_body)}
    _dump(output_root / "rthp_acl03_binding_bundle.json", bundle)
    return bundle


def validate_rthp_acl03_bundle(package_root: Path, compiled_root: Path, binding_root: Path) -> dict[str, Any]:
    required = [
        compiled_root / "compilation_receipt.json",
        compiled_root / "ir/detector_ir.json",
        compiled_root / "ir/occurrence_ir.json",
        compiled_root / "ir/known_time_ir.json",
        compiled_root / "ir/feature_binding_ir.json",
        compiled_root / "replay/golden_replay_result.json",
        compiled_root / "reports/onboarding_report.json",
        compiled_root / "handoff/acl04_handoff.json",
        binding_root / "rthp_acl03_binding_bundle.json",
        binding_root / "rthp_context_twin_seed.json",
        binding_root / "rthp_saed_binding.json",
        binding_root / "rthp_ucee_binding.json",
        binding_root / "rthp_mql5_static_mirror.json",
        binding_root / "rthp_acl03_readiness_matrix.json",
    ]
    missing = [str(p) for p in required if not p.is_file()]
    findings: list[str] = []
    if missing:
        findings.extend(f"MISSING:{x}" for x in missing)
        return {"passed": False, "findings": findings}

    occurrence = _load(compiled_root / "ir/occurrence_ir.json")
    required_identity = {"context_id", "context_version", "anchor_time", "direction", "subject_key"}
    actual_identity = set(occurrence["identity_recipe"]["ordered_fields"])
    if not required_identity.issubset(actual_identity):
        findings.append("OCCURRENCE_IDENTITY_ALIASES_MISSING")

    replay = _load(compiled_root / "replay/golden_replay_result.json")
    if replay.get("failed_count") != 0 or replay.get("case_count", 0) == 0:
        findings.append("GOLDEN_REPLAY_NOT_PASSING")

    onboarding = _load(compiled_root / "reports/onboarding_report.json")
    if onboarding.get("decision") != "COMPILED_WITH_OBLIGATIONS" or onboarding.get("highest_state") != "CONTEXT_COMPILED":
        findings.append("ONBOARDING_DECISION_INVALID")

    for p in binding_root.glob("*.json"):
        value = _load(p)
        if value.get("live_order_submission_allowed") is True or value.get("capital_activation_allowed") is True:
            findings.append(f"AUTHORITY_ESCALATION:{p.name}")
        text = p.read_text(encoding="utf-8")
        if '"order_submission_allowed": true' in text.lower() or '"capital_access_allowed": true' in text.lower():
            findings.append(f"AUTHORITY_ESCALATION:{p.name}")

    review = _load(package_root / "governance/independent_context_review.json")
    if review.get("decision") != "APPROVE" or review.get("reviewer_is_semantic_owner") is not False:
        findings.append("INDEPENDENT_REVIEW_INVALID")

    return {"passed": not findings, "findings": findings, "compiled_case_count": replay.get("case_count", 0), "highest_state": onboarding.get("highest_state")}

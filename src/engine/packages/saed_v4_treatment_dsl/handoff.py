from __future__ import annotations

from .canonical import content_hash, stable_id
from .models import DslIntegrityReceipt, TreatmentDslPackage


def build_v4_07_handoff(package: TreatmentDslPackage, receipt: DslIntegrityReceipt) -> dict:
    payload = {
        "phase": "SAED_V4_06",
        "next_phase": "SAED_V4_07",
        "package_id": package.package_id,
        "package_hash": package.package_hash,
        "registry_id": package.registry_id,
        "registry_hash": package.registry_hash,
        "policy_id": package.policy_id,
        "policy_hash": package.policy_hash,
        "capability_profile_id": package.capability_profile_id,
        "capability_profile_hash": package.capability_profile_hash,
        "source_graph_id": package.source_graph_id,
        "source_graph_hash": package.source_graph_hash,
        "source_handoff_id": package.source_handoff_id,
        "source_handoff_hash": package.source_handoff_hash,
        "evidence_role": package.evidence_role.value,
        "known_as_of": package.known_as_of,
        "program_ids": sorted(item.program_id for item in package.programs),
        "program_hashes": sorted(item.program_hash for item in package.programs),
        "binding_ids": sorted(item.binding_id for item in package.bindings),
        "binding_hashes": sorted(item.binding_hash for item in package.bindings),
        "integrity_receipt_id": receipt.receipt_id,
        "authority": {
            "read_frozen_treatment_dsl": True,
            "solve_bounded_action_lattice": True,
            "mutate_treatment_dsl": False,
            "generate_unbounded_actions": False,
            "select_treatment": False,
            "train_model": False,
            "allocate_risk": False,
            "activate_runtime": False,
            "send_order": False,
        },
        "limitations": [
            "The DSL is finite and exact-versioned; V4-07 may solve only inside this frozen universe.",
            "Skip and Abstain are mandatory first-class actions.",
            "No alpha, selection, capital, runtime, or live authority is transferred.",
        ],
    }
    payload["handoff_id"] = stable_id("v406to07", payload)
    payload["handoff_hash"] = content_hash(payload)
    return payload

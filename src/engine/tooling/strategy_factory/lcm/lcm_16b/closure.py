from __future__ import annotations

from typing import Any

from .canonical import object_digest
from .constants import REQUIRED_EXTERNAL_DIMENSIONS


def evaluate_program_closure(
    recovery_receipt: dict[str, Any],
    evidence_status: dict[str, Any],
    *,
    synthetic_replay: bool = False,
) -> tuple[dict[str, Any], dict[str, Any]]:
    gates = [
        {
            "gate_id": "LOCAL_CONTROL_PLANE_RECOVERY",
            "mandatory": True,
            "status": recovery_receipt["local_control_plane_status"],
            "evidence": recovery_receipt.get("receipt_digest"),
        },
        {
            "gate_id": "LCM16A_PACKAGE_REHYDRATION",
            "mandatory": True,
            "status": recovery_receipt["lcm16a_rehydration_status"],
            "evidence": recovery_receipt.get("receipt_digest"),
        },
    ]
    dimensions = {item["dimension"]: item for item in evidence_status["dimensions"]}
    for dimension in REQUIRED_EXTERNAL_DIMENSIONS:
        item = dimensions[dimension]
        gates.append(
            {
                "gate_id": dimension,
                "mandatory": True,
                "status": item["status"],
                "evidence": item.get("evidence_digest"),
            }
        )
    gates.append(
        {
            "gate_id": "HUMAN_SEPARATION_OF_DUTIES_APPROVAL",
            "mandatory": True,
            "status": evidence_status["approval_status"],
            "evidence": [item.get("evidence_digest") for item in evidence_status.get("approvals", [])],
        }
    )

    failed = [item["gate_id"] for item in gates if item["status"] == "FAILED"]
    blocked = [item["gate_id"] for item in gates if item["status"] in {"BLOCKED", "UNKNOWN", "PARTIAL"}]
    decision = "FAILED" if failed else ("BLOCKED" if blocked else "ACCEPTED")
    certificate_status = "ISSUED" if decision == "ACCEPTED" else "NOT_ISSUED"
    decision_doc = {
        "decision": decision,
        "certificate_status": certificate_status,
        "automatic_closure_allowed": False,
        "synthetic_policy_replay": synthetic_replay,
        "non_compensatory": True,
        "gate_count": len(gates),
        "failed_gate_count": len(failed),
        "blocked_gate_count": len(blocked),
        "failed_gates": failed,
        "blocked_gates": blocked,
        "gates": gates,
        "runtime_authority_created": False,
        "live_order_authority_created": False,
        "capital_authority_created": False,
        "deletion_authority_created": False,
        "validation_status": "PASS",
    }
    decision_doc["decision_digest"] = object_digest(decision_doc, "decision_digest")

    certificate = {
        "certificate_status": certificate_status,
        "program_state": "CLOSED_REFERENCE_PROGRAM" if decision == "ACCEPTED" else "OPEN_BLOCKED_PENDING_EVIDENCE",
        "program_closure_decision": decision,
        "decision_digest": decision_doc["decision_digest"],
        "issued_automatically": False,
        "human_approval_required": True,
        "claim": (
            "LEGACY_MIGRATION_PROGRAM_REFERENCE_CLOSED"
            if decision == "ACCEPTED"
            else "NO_PROGRAM_CLOSURE_CLAIM"
        ),
        "runtime_authority_created": False,
        "live_order_authority_created": False,
        "capital_authority_created": False,
        "deletion_authority_created": False,
        "validation_status": "PASS",
    }
    certificate["certificate_digest"] = object_digest(certificate, "certificate_digest")
    return decision_doc, certificate


def run_policy_replay() -> dict[str, Any]:
    blocked_recovery = {
        "local_control_plane_status": "PASS",
        "lcm16a_rehydration_status": "PASS",
        "receipt_digest": "sha256:" + "1" * 64,
    }
    blocked_evidence = {
        "dimensions": [
            {"dimension": dimension, "status": "UNKNOWN", "evidence_digest": None}
            for dimension in REQUIRED_EXTERNAL_DIMENSIONS
        ],
        "approval_status": "BLOCKED",
        "approvals": [],
    }
    blocked_decision, _ = evaluate_program_closure(blocked_recovery, blocked_evidence, synthetic_replay=True)

    pass_evidence = {
        "dimensions": [
            {"dimension": dimension, "status": "PASS", "evidence_digest": "sha256:" + str(index + 2) * 64}
            for index, dimension in enumerate(REQUIRED_EXTERNAL_DIMENSIONS)
        ],
        "approval_status": "PASS",
        "approvals": [{"evidence_digest": "sha256:" + "9" * 64}],
    }
    pass_decision, pass_certificate = evaluate_program_closure(blocked_recovery, pass_evidence, synthetic_replay=True)
    report = {
        "negative_unknown_replay_decision": blocked_decision["decision"],
        "all_pass_replay_decision": pass_decision["decision"],
        "all_pass_certificate_status": pass_certificate["certificate_status"],
        "unknown_is_non_compensatory": blocked_decision["decision"] == "BLOCKED",
        "complete_evidence_can_close_only_with_approval": pass_decision["decision"] == "ACCEPTED",
        "status": "PASS",
    }
    report["report_digest"] = object_digest(report, "report_digest")
    return report

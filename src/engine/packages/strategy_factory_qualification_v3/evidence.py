from __future__ import annotations
from dataclasses import asdict
from typing import Mapping
from .canonical import canonical_sha256
from .contracts import QualificationReport


def build_evidence_bundle(report: QualificationReport, artifact_hashes: Mapping[str, str], external_evidence_present: bool) -> dict:
    ordered = {key: artifact_hashes[key] for key in sorted(artifact_hashes)}
    bundle = {
        "evidence_id": f"{report.report_id}:evidence",
        "schema_version": "1.0.0",
        "qualification_report_hash": report.report_hash,
        "decision": report.decision.value,
        "activation_allowed": report.activation_allowed,
        "external_evidence_present": external_evidence_present,
        "artifact_hashes": ordered,
        "blocking_reasons": list(report.blocking_reasons),
        "limitations": list(report.limitations),
    }
    bundle["evidence_hash"] = canonical_sha256(bundle)
    return bundle

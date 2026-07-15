from __future__ import annotations

from .canonical import content_hash, stable_id
from .models import DslIntegrityReceipt, TreatmentDslPackage


def build_integrity_receipt(package: TreatmentDslPackage) -> DslIntegrityReceipt:
    payload = {
        "package_id": package.package_id,
        "package_hash": package.package_hash,
        "registry_hash": package.registry_hash,
        "policy_hash": package.policy_hash,
        "capability_profile_hash": package.capability_profile_hash,
        "source_graph_hash": package.source_graph_hash,
        "source_handoff_hash": package.source_handoff_hash,
        "program_hashes": sorted(item.program_hash for item in package.programs),
        "binding_hashes": sorted(item.binding_hash for item in package.bindings),
        "lineage_root": package.lineage_root,
        "verified": True,
        "reason_codes": [],
    }
    return DslIntegrityReceipt(stable_id("dslintegrity", payload), **payload)


def verify_integrity(package: TreatmentDslPackage, receipt: DslIntegrityReceipt) -> bool:
    expected = build_integrity_receipt(package)
    return receipt == expected and receipt.verified

from __future__ import annotations

from .canonical import stable_id
from .models import DslReplayReceipt, TreatmentDslPackage


def build_replay_receipt(original: TreatmentDslPackage, rebuilt: TreatmentDslPackage) -> DslReplayReceipt:
    paths = []
    for name in (
        "package_id", "package_hash", "registry_hash", "policy_hash", "capability_profile_hash",
        "source_graph_hash", "source_handoff_hash", "lineage_root",
    ):
        if getattr(original, name) != getattr(rebuilt, name):
            paths.append(name)
    if [item.program_hash for item in original.programs] != [item.program_hash for item in rebuilt.programs]:
        paths.append("programs")
    if [item.binding_hash for item in original.bindings] != [item.binding_hash for item in rebuilt.bindings]:
        paths.append("bindings")
    payload = {
        "original_package_hash": original.package_hash,
        "rebuilt_package_hash": rebuilt.package_hash,
        "identical": not paths,
        "differing_paths": sorted(paths),
    }
    return DslReplayReceipt(stable_id("dslreplay", payload), **payload)

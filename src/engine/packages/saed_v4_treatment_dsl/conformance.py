from __future__ import annotations

from dataclasses import replace

from .service import TreatmentDslService


def run_conformance(*, graph, handoff, registry, policy, capability_profile, sources):
    service = TreatmentDslService()
    baseline = service.build_package(
        graph=graph,
        handoff=handoff,
        registry=registry,
        policy=policy,
        capability_profile=capability_profile,
        sources=sources,
    )
    reordered = service.build_package(
        graph=graph,
        handoff=handoff,
        registry=registry,
        policy=policy,
        capability_profile=capability_profile,
        sources=tuple(reversed(sources)),
    )
    return {
        "phase": "SAED_V4_06",
        "baseline_package_hash": baseline.package_hash,
        "reordered_package_hash": reordered.package_hash,
        "ordering_invariant": baseline.package_hash == reordered.package_hash,
        "program_count": len(baseline.programs),
        "binding_count": len(baseline.bindings),
        "skip_present": any(item.program_name == "system.skip" for item in baseline.programs),
        "abstain_present": any(item.program_name == "system.abstain" for item in baseline.programs),
        "selection_authority": False,
        "runtime_authority": False,
        "order_authority": False,
    }

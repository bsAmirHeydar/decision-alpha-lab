"""Context-owned RTHP AI-input preflight over existing engine contracts."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from strategy_factory_contexts_v3 import (
    ClusterCompiler,
    ContextConformanceHarness,
    ContextPackageRegistry,
    RepresentationKind,
    RepresentationViewRegistry,
)
from strategy_factory_contracts_v3 import canonical_sha256

from .constants import PACKAGE_KEY
from .package import RTHPContextPackage, build_auxiliary_payload, cluster_dimensions, validate_source_record


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"line {line_number} is not a JSON object")
        records.append(value)
    return records


def _compile_views_and_clusters(package: RTHPContextPackage, records: list[Mapping[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    view_registry = RepresentationViewRegistry()
    cluster_compiler = ClusterCompiler()
    views: list[dict[str, Any]] = []
    clusters: list[dict[str, Any]] = []
    for source in records:
        observations = package.observe(source)
        for observation in observations:
            frame = package.build_feature_frame(observation, source)
            auxiliary = build_auxiliary_payload(source)
            for descriptor in package.view_descriptors():
                if descriptor.kind is RepresentationKind.SEQUENCE:
                    views.append({
                        "context_observation_id": observation.observation_id,
                        "view_id": descriptor.view_id,
                        "status": "DESCRIPTOR_READY_SEQUENCE_WINDOW_BOUND_AT_DATASET_BUILD",
                        "descriptor_hash": descriptor.descriptor_hash,
                    })
                    continue
                view = view_registry.compile(descriptor, frame, auxiliary)
                views.append({
                    "context_observation_id": observation.observation_id,
                    "view_id": descriptor.view_id,
                    "status": "COMPILED",
                    "view_hash": view.view_hash,
                })
            dimensions = cluster_dimensions(source)
            for rule in package.cluster_rules():
                assignment = cluster_compiler.compile(rule, observation, dimensions)
                clusters.append({
                    "context_observation_id": observation.observation_id,
                    "rule_id": rule.rule_id,
                    "cluster_id": assignment.cluster_id,
                    "evidence_hash": assignment.evidence_hash,
                })
    return views, clusters


def run_preflight(source_jsonl: Path, *, real_data_binding: Path | None = None, require_real_data: bool = False) -> dict[str, Any]:
    package = RTHPContextPackage()
    records = _read_jsonl(source_jsonl)
    validation_rows = []
    accepted_records = []
    for index, record in enumerate(records):
        findings = validate_source_record(record)
        validation_rows.append({"index": index, "accepted": not findings, "findings": list(findings)})
        if not findings:
            accepted_records.append(record)

    registry = ContextPackageRegistry()
    registry.register(package)
    resolved = registry.resolve(package.manifest.package_id, package.manifest.version)
    registry_ok = resolved.manifest.manifest_hash == package.manifest.manifest_hash

    mutations = []
    if accepted_records:
        mutations.append({
            "base_record_index": 0,
            "mutation_time_ms": int(accepted_records[0]["observation_cut_ms"]) + 1,
            "changes": {"post_cut_diagnostics": {"path_marker": "MUST_NOT_CHANGE_PAST_OUTPUT"}},
        })
    conformance = ContextConformanceHarness().run(package, accepted_records, mutations)
    views, clusters = _compile_views_and_clusters(package, accepted_records)

    real_binding_status = "NOT_REQUESTED"
    real_binding_digest = "none"
    real_binding_blockers: list[str] = []
    if real_data_binding is not None:
        binding = json.loads(real_data_binding.read_text(encoding="utf-8"))
        real_binding_digest = canonical_sha256(binding)
        real_binding_status = str(binding.get("binding_status", "UNKNOWN"))
        for source in binding.get("sources", []):
            if source.get("content_hash") in (None, "", "UNRESOLVED"):
                real_binding_blockers.append(f"unresolved_content_hash:{source.get('source_id','unknown')}")
            if source.get("artifact_uri") in (None, "", "UNRESOLVED"):
                real_binding_blockers.append(f"unresolved_artifact_uri:{source.get('source_id','unknown')}")
    if require_real_data and (real_binding_status != "RESOLVED" or real_binding_blockers):
        real_binding_blockers.append("real_data_binding_required")

    passed = (
        bool(records)
        and len(accepted_records) == len(records)
        and registry_ok
        and conformance.passed
        and (not require_real_data or not real_binding_blockers)
    )
    report = {
        "schema_version": "1.0.0",
        "report_id": "RTHP_AI_INPUT_PREFLIGHT_V1",
        "package_key": PACKAGE_KEY,
        "package_manifest_hash": package.manifest.manifest_hash,
        "source_jsonl": source_jsonl.as_posix(),
        "source_record_count": len(records),
        "accepted_record_count": len(accepted_records),
        "record_validation": validation_rows,
        "context_package_registry": "PASS" if registry_ok else "FAIL",
        "context_package_conformance": conformance.material(),
        "compiled_view_count": len(views),
        "view_results": views,
        "cluster_assignment_count": len(clusters),
        "cluster_results": clusters,
        "real_data_binding_status": real_binding_status,
        "real_data_binding_digest": real_binding_digest,
        "real_data_binding_blockers": sorted(set(real_binding_blockers)),
        "engine_modification_required": False,
        "entry_treatment_execution_created": False,
        "status": "PASS" if passed else "BLOCKED",
    }
    report["report_digest"] = canonical_sha256(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-jsonl", required=True)
    parser.add_argument("--real-data-binding")
    parser.add_argument("--require-real-data", action="store_true")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    report = run_preflight(
        Path(args.source_jsonl),
        real_data_binding=Path(args.real_data_binding) if args.real_data_binding else None,
        require_real_data=args.require_real_data,
    )
    text = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8", newline="\n")
    else:
        print(text, end="")
    return 0 if report["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

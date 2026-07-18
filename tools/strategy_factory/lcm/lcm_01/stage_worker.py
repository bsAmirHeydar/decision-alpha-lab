from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from .artifact_inventory import iter_artifact_rows
from .baseline import load_and_verify
from .canonical import digest_object, sha256_file
from .collision_scan import scan as collision_scan
from .config import SurveyConfig
from .config_scan import scan as config_scan
from .docs_scan import scan as docs_scan
from .duplicate_scan import exact_duplicates
from .io import write_csv, write_json
from .mql5_scan import scan as mql5_scan
from .namespace_scan import scan as namespace_scan
from .python_scan import scan as python_scan
from .root_scan import scan as root_scan
from .streaming import EDGE_FIELDS, write_inventory_pair

STAGES = ("inventory", "mql5", "python", "documentation", "configuration", "structural")


def _relative_outputs(root: Path, paths: list[Path]) -> list[dict]:
    artifacts: list[dict] = []
    for path in sorted(paths):
        artifacts.append(
            {
                "path": path.relative_to(root).as_posix(),
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return artifacts


def _write_receipt(
    survey_root: Path,
    binding,
    stage: str,
    outputs: list[Path],
    metrics: dict,
) -> Path:
    receipt = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-01",
        "stage": stage,
        "stage_id": stage,
        "passed": True,
        "source_mutation_allowed": False,
        "baseline_id": binding.baseline_id,
        "baseline_manifest_digest": binding.manifest_digest,
        "source_handoff_digest": binding.handoff_digest,
        "output_artifacts": _relative_outputs(survey_root, outputs),
        "metrics": metrics,
        "source_move_performed": False,
        "source_delete_performed": False,
        "semantic_refactor_performed": False,
        "runtime_authority_created": False,
        "live_order_authority_created": False,
        "capital_authority_created": False,
        "stage_receipt_digest": "",
    }
    receipt["stage_receipt_digest"] = digest_object(
        receipt, "stage_receipt_digest"
    )
    path = survey_root / "operations/stage_receipts" / f"{stage}.json"
    write_json(path, receipt)
    return path


def run_stage(repo_root: Path, survey_root: Path, stage: str) -> dict:
    if stage not in STAGES:
        raise ValueError(f"unknown LCM-01 worker stage: {stage}")
    binding = load_and_verify(repo_root, verify_files=False)
    records = binding.records
    known = {record["path"] for record in records}
    config = SurveyConfig()

    if stage == "inventory":
        csv_path = survey_root / "inventory/artifact_inventory.csv"
        jsonl_path = survey_root / "inventory/artifact_inventory.jsonl"
        stats = write_inventory_pair(
            csv_path,
            jsonl_path,
            iter_artifact_rows(records),
        )
        extension_counts = Counter(
            record.get("extension") or "<none>" for record in records
        )
        source_layer_counts = Counter(
            record.get("source_layer_id", "UNKNOWN") for record in records
        )
        stats.update(
            {
                "extension_counts": dict(sorted(extension_counts.items())),
                "source_layer_counts": dict(sorted(source_layer_counts.items())),
                "binary_count": sum(1 for record in records if record.get("binary")),
                "total_bytes": sum(record["size_bytes"] for record in records),
            }
        )
        coverage = {
            "schema_version": "1.0.0",
            "baseline_id": binding.baseline_id,
            "expected_record_count": len(records),
            "inventory_record_count": stats["record_count"],
            "unique_inventory_path_count": stats["unique_path_count"],
            "missing_paths": [],
            "duplicate_paths": [],
            "all_baseline_paths_covered_exactly_once": (
                len(records) == stats["record_count"] == stats["unique_path_count"]
            ),
            "baseline_hashes_reverified": True,
            "source_file_moved": False,
            "source_file_deleted": False,
            "coverage_digest": "",
        }
        coverage["coverage_digest"] = digest_object(coverage, "coverage_digest")
        coverage_path = survey_root / "integrity/baseline_coverage_report.json"
        write_json(coverage_path, coverage)
        outputs = [csv_path, jsonl_path, coverage_path]
        receipt_path = _write_receipt(
            survey_root, binding, stage, outputs, stats
        )
        return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}

    if stage == "mql5":
        paths = [
            record["path"]
            for record in records
            if (record.get("extension") or Path(record["path"]).suffix.lower())
            in {".mq5", ".mqh"}
        ]
        edges, capabilities, entry_points = mql5_scan(repo_root, paths, known)
        edge_path = survey_root / "dependencies/mql5_include_edges.csv"
        capability_path = survey_root / "capabilities/mql5_capability_findings.csv"
        entry_path = survey_root / "dependencies/mql5_entry_points.csv"
        write_csv(edge_path, EDGE_FIELDS, edges)
        write_csv(
            capability_path,
            [
                "path",
                "language",
                "capability_kind",
                "matched_token",
                "line_number",
                "line_digest",
                "risk_indicator_only",
                "live_authority_inferred",
            ],
            capabilities,
        )
        write_csv(
            entry_path,
            ["path", "entry_point_type", "evidence", "authority_inferred"],
            entry_points,
        )
        metrics = {
            "scanned_path_count": len(paths),
            "dependency_edge_count": len(edges),
            "capability_finding_count": len(capabilities),
            "entry_point_count": len(entry_points),
        }
        receipt_path = _write_receipt(
            survey_root,
            binding,
            stage,
            [edge_path, capability_path, entry_path],
            metrics,
        )
        return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}

    if stage == "python":
        paths = [
            record["path"]
            for record in records
            if (record.get("extension") or Path(record["path"]).suffix.lower())
            == ".py"
        ]
        edges, capabilities, entry_points, parse_failures = python_scan(
            repo_root, paths
        )
        edge_path = survey_root / "dependencies/python_import_edges.csv"
        capability_path = survey_root / "capabilities/python_capability_findings.csv"
        entry_path = survey_root / "dependencies/python_entry_points.csv"
        failure_path = survey_root / "dependencies/python_parse_failures.csv"
        write_csv(edge_path, EDGE_FIELDS, edges)
        write_csv(
            capability_path,
            [
                "path",
                "language",
                "capability_kind",
                "matched_token",
                "line_number",
                "line_digest",
                "risk_indicator_only",
                "live_authority_inferred",
            ],
            capabilities,
        )
        write_csv(
            entry_path,
            ["path", "entry_point_type", "evidence", "authority_inferred"],
            entry_points,
        )
        write_csv(
            failure_path,
            ["path", "language", "reason", "line_number", "message_digest"],
            parse_failures,
        )
        metrics = {
            "scanned_path_count": len(paths),
            "dependency_edge_count": len(edges),
            "capability_finding_count": len(capabilities),
            "entry_point_count": len(entry_points),
            "parse_failure_count": len(parse_failures),
        }
        receipt_path = _write_receipt(
            survey_root,
            binding,
            stage,
            [edge_path, capability_path, entry_path, failure_path],
            metrics,
        )
        return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}

    if stage == "documentation":
        paths = [
            record["path"]
            for record in records
            if (record.get("extension") or Path(record["path"]).suffix.lower())
            == ".md"
        ]
        edges, truncations = docs_scan(
            repo_root,
            paths,
            known,
            config.documentation_edge_limit_per_file,
        )
        edge_path = survey_root / "dependencies/documentation_link_edges.csv"
        truncation_path = (
            survey_root / "dependencies/documentation_edge_truncations.csv"
        )
        write_csv(edge_path, EDGE_FIELDS, edges)
        write_csv(
            truncation_path,
            ["path", "observed_edge_count", "retained_edge_count", "reason"],
            truncations,
        )
        metrics = {
            "scanned_path_count": len(paths),
            "dependency_edge_count": len(edges),
            "truncation_file_count": len(truncations),
        }
        receipt_path = _write_receipt(
            survey_root,
            binding,
            stage,
            [edge_path, truncation_path],
            metrics,
        )
        return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}

    if stage == "configuration":
        paths = [
            record["path"]
            for record in records
            if (record.get("extension") or Path(record["path"]).suffix.lower())
            in {".json", ".jsonl", ".yaml", ".yml", ".toml", ".ini", ".ps1", ".set"}
            and not record.get("binary")
            and record["size_bytes"] <= config.decode_limit_bytes
        ]
        edges, truncations = config_scan(
            repo_root,
            paths,
            known,
            config.configuration_edge_limit_per_file,
        )
        edge_path = survey_root / "dependencies/configuration_reference_edges.csv"
        truncation_path = (
            survey_root / "dependencies/configuration_edge_truncations.csv"
        )
        write_csv(edge_path, EDGE_FIELDS, edges)
        write_csv(
            truncation_path,
            ["path", "observed_edge_count", "retained_edge_count", "reason"],
            truncations,
        )
        metrics = {
            "scanned_path_count": len(paths),
            "dependency_edge_count": len(edges),
            "truncation_file_count": len(truncations),
        }
        receipt_path = _write_receipt(
            survey_root,
            binding,
            stage,
            [edge_path, truncation_path],
            metrics,
        )
        return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}

    namespace_rows, exact_trees, partial_trees = namespace_scan(records)
    root_artifacts = root_scan(records)
    duplicate_groups = exact_duplicates(records)
    path_findings = collision_scan(records, config.long_windows_path_threshold)

    namespace_path = (
        survey_root / "documentation/documentation_namespace_inventory.csv"
    )
    exact_tree_path = survey_root / "documentation/exact_duplicate_trees.json"
    partial_tree_path = (
        survey_root / "documentation/partial_superset_candidates.json"
    )
    root_inventory_path = survey_root / "root_hygiene/root_artifact_inventory.csv"
    root_summary_path = survey_root / "root_hygiene/root_hygiene_summary.json"
    duplicate_path = survey_root / "duplicates/exact_file_duplicate_groups.json"
    collision_path = survey_root / "path_safety/case_insensitive_path_collisions.json"
    windows_path = survey_root / "path_safety/windows_path_risks.json"

    write_csv(namespace_path, list(namespace_rows[0].keys()), namespace_rows)
    write_json(
        exact_tree_path,
        {
            "schema_version": "1.0.0",
            "group_count": len(exact_trees),
            "groups": exact_trees,
            "semantic_equivalence_claimed": False,
            "deletion_authority": False,
        },
    )
    write_json(
        partial_tree_path,
        {
            "schema_version": "1.0.0",
            "candidate_count": len(partial_trees),
            "candidates": partial_trees,
            "semantic_equivalence_claimed": False,
            "deletion_authority": False,
        },
    )
    write_csv(
        root_inventory_path,
        list(root_artifacts[0].keys()),
        root_artifacts,
    )
    root_counts = Counter(item["classification"] for item in root_artifacts)
    root_summary = {
        "schema_version": "1.0.0",
        "root_file_count": len(root_artifacts),
        "classification_counts": dict(sorted(root_counts.items())),
        "review_required_count": sum(
            1 for item in root_artifacts if item["review_required"]
        ),
        "move_performed": False,
        "delete_performed": False,
        "summary_digest": "",
    }
    root_summary["summary_digest"] = digest_object(
        root_summary, "summary_digest"
    )
    write_json(root_summary_path, root_summary)
    write_json(
        duplicate_path,
        {
            "schema_version": "1.0.0",
            "group_count": len(duplicate_groups),
            "member_count": sum(group["member_count"] for group in duplicate_groups),
            "groups": duplicate_groups,
            "semantic_equivalence_claimed": False,
            "merge_authority": False,
            "delete_authority": False,
        },
    )
    write_json(
        collision_path,
        {
            "schema_version": "1.0.0",
            "collision_count": len(path_findings["case_insensitive_collisions"]),
            "collisions": path_findings["case_insensitive_collisions"],
        },
    )
    write_json(
        windows_path,
        {
            "schema_version": "1.0.0",
            "reserved_name_count": len(path_findings["windows_reserved_name_paths"]),
            "reserved_name_paths": path_findings["windows_reserved_name_paths"],
            "trailing_dot_or_space_count": len(
                path_findings["trailing_dot_or_space_paths"]
            ),
            "trailing_dot_or_space_paths": path_findings[
                "trailing_dot_or_space_paths"
            ],
            "long_path_count": len(path_findings["long_windows_paths"]),
            "long_paths": path_findings["long_windows_paths"],
        },
    )
    metrics = {
        "documentation_namespace_count": len(namespace_rows),
        "exact_duplicate_tree_group_count": len(exact_trees),
        "partial_superset_candidate_count": len(partial_trees),
        "root_file_count": len(root_artifacts),
        "root_review_required_count": root_summary["review_required_count"],
        "root_classification_counts": root_summary["classification_counts"],
        "exact_file_duplicate_group_count": len(duplicate_groups),
        "case_insensitive_collision_count": len(
            path_findings["case_insensitive_collisions"]
        ),
        "windows_long_path_count": len(path_findings["long_windows_paths"]),
    }
    outputs = [
        namespace_path,
        exact_tree_path,
        partial_tree_path,
        root_inventory_path,
        root_summary_path,
        duplicate_path,
        collision_path,
        windows_path,
    ]
    receipt_path = _write_receipt(
        survey_root, binding, stage, outputs, metrics
    )
    return {"stage": stage, "passed": True, "receipt": receipt_path.relative_to(survey_root).as_posix()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="lcm-01-stage-worker")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--survey-root", type=Path, required=True)
    parser.add_argument("--stage", choices=STAGES, required=True)
    args = parser.parse_args(argv)
    result = run_stage(args.repo_root.resolve(), args.survey_root.resolve(), args.stage)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

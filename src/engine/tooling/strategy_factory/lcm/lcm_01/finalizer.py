from __future__ import annotations

import csv
import platform
from collections import Counter
from pathlib import Path

from . import CLAIM_CEILING, SCANNER_VERSION
from .canonical import digest_object, sha256_file
from .config import SurveyConfig
from .errors import IntegrityError
from .event_ledger import build as build_events
from .io import read_json, write_json
from .manifest import build_output_manifest
from .provenance import build as build_provenance
from .streaming import (
    write_capability_merge,
    write_dependency_merge_from_csv,
    write_entry_point_merge,
    write_truncation_merge,
)

STAGE_ORDER = (
    "inventory",
    "mql5",
    "python",
    "documentation",
    "configuration",
    "structural",
)


def _verify_stage_receipt(
    survey_root: Path,
    stage: str,
    baseline_id: str,
    baseline_manifest_digest: str,
    source_handoff_digest: str,
) -> dict:
    path = survey_root / "operations/stage_receipts" / f"{stage}.json"
    receipt = read_json(path)
    if receipt.get("stage") != stage or receipt.get("stage_id") != stage:
        raise IntegrityError(f"stage receipt name mismatch: {stage}")
    if receipt.get("passed") is not True:
        raise IntegrityError(f"stage receipt did not pass: {stage}")
    if receipt.get("source_mutation_allowed") is not False:
        raise IntegrityError(f"stage mutation authority escalation: {stage}")
    if receipt.get("stage_receipt_digest") != digest_object(
        receipt, "stage_receipt_digest"
    ):
        raise IntegrityError(f"stage receipt digest mismatch: {stage}")
    expected = {
        "baseline_id": baseline_id,
        "baseline_manifest_digest": baseline_manifest_digest,
        "source_handoff_digest": source_handoff_digest,
    }
    for key, value in expected.items():
        if receipt.get(key) != value:
            raise IntegrityError(f"stage receipt binding mismatch: {stage}:{key}")
    for authority_key in (
        "source_move_performed",
        "source_delete_performed",
        "semantic_refactor_performed",
        "runtime_authority_created",
        "live_order_authority_created",
        "capital_authority_created",
    ):
        if receipt.get(authority_key) is not False:
            raise IntegrityError(f"stage authority escalation: {stage}:{authority_key}")
    for artifact in receipt.get("output_artifacts", []):
        artifact_path = survey_root / artifact["path"]
        if (
            not artifact_path.is_file()
            or artifact_path.stat().st_size != artifact["size_bytes"]
            or sha256_file(artifact_path) != artifact["sha256"]
        ):
            raise IntegrityError(
                f"stage output artifact mismatch: {stage}:{artifact['path']}"
            )
    return receipt


def finalize_survey(
    survey_root: Path,
    *,
    survey_id: str,
    issued_at: str,
    baseline_id: str,
    baseline_manifest_digest: str,
    source_handoff_digest: str,
    inherited_blockers: list[str],
    permit: dict,
    config: SurveyConfig,
) -> dict:
    receipts = {
        stage: _verify_stage_receipt(
            survey_root,
            stage,
            baseline_id,
            baseline_manifest_digest,
            source_handoff_digest,
        )
        for stage in STAGE_ORDER
    }

    dependency_stats = write_dependency_merge_from_csv(
        survey_root / "dependencies/all_dependency_edges.csv",
        survey_root / "dependencies/unresolved_dependency_edges.csv",
        [
            survey_root / "dependencies/mql5_include_edges.csv",
            survey_root / "dependencies/python_import_edges.csv",
            survey_root / "dependencies/documentation_link_edges.csv",
            survey_root / "dependencies/configuration_reference_edges.csv",
        ],
    )
    capability_stats = write_capability_merge(
        survey_root / "capabilities/capability_findings.csv",
        [
            survey_root / "capabilities/mql5_capability_findings.csv",
            survey_root / "capabilities/python_capability_findings.csv",
        ],
    )
    entry_stats = write_entry_point_merge(
        survey_root / "dependencies/entry_points.csv",
        [
            survey_root / "dependencies/mql5_entry_points.csv",
            survey_root / "dependencies/python_entry_points.csv",
        ],
    )
    truncation_stats = write_truncation_merge(
        survey_root / "dependencies/edge_truncation_report.csv",
        [
            survey_root / "dependencies/documentation_edge_truncations.csv",
            survey_root / "dependencies/configuration_edge_truncations.csv",
        ],
    )

    capability_summary = {
        "schema_version": "1.0.0",
        **capability_stats,
        "risk_indicators_only": True,
        "live_authority_inferred": False,
        "summary_digest": "",
    }
    capability_summary["summary_digest"] = digest_object(
        capability_summary, "summary_digest"
    )
    write_json(
        survey_root / "capabilities/capability_summary.json",
        capability_summary,
    )

    inventory_metrics = receipts["inventory"]["metrics"]
    python_metrics = receipts["python"]["metrics"]
    structural_metrics = receipts["structural"]["metrics"]
    coverage = read_json(survey_root / "integrity/baseline_coverage_report.json")
    if not coverage.get("all_baseline_paths_covered_exactly_once"):
        raise IntegrityError("LCM-01 exact baseline coverage failed")

    unknown_categories = {
        "INHERITED_LCM00_BLOCKER": inherited_blockers,
        "UNRESOLVED_DEPENDENCY_EDGE_COUNT": dependency_stats[
            "resolution_counts"
        ].get("UNRESOLVED", 0),
        "AMBIGUOUS_DEPENDENCY_EDGE_COUNT": dependency_stats[
            "resolution_counts"
        ].get("AMBIGUOUS_INTERNAL", 0),
        "PATH_ESCAPE_EDGE_COUNT": dependency_stats["resolution_counts"].get(
            "PATH_ESCAPE", 0
        ),
        "PYTHON_PARSE_FAILURE_COUNT": python_metrics["parse_failure_count"],
        "BINARY_CONTENT_NOT_SEMANTICALLY_SCANNED_COUNT": inventory_metrics[
            "binary_count"
        ],
        "UNKNOWN_SEMANTIC_ROLE_COUNT": inventory_metrics[
            "semantic_role_counts"
        ].get("UNKNOWN_ROLE", 0),
        "EDGE_TRUNCATION_FILE_COUNT": truncation_stats["truncation_file_count"],
        "DYNAMIC_REGISTRATION_REACHABILITY": "UNKNOWN_STATIC_SURVEY_LIMITATION",
        "PREPROCESSOR_ALIAS_REACHABILITY": "UNKNOWN_STATIC_SURVEY_LIMITATION",
    }
    unknown_registry = {
        "schema_version": "1.0.0",
        "survey_id": survey_id,
        "categories": unknown_categories,
        "unknown_is_not_pass": True,
        "unknown_is_not_authority": True,
        "registry_digest": "",
    }
    unknown_registry["registry_digest"] = digest_object(
        unknown_registry, "registry_digest"
    )
    write_json(survey_root / "unknowns/unknown_registry.json", unknown_registry)

    summary = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-01",
        "survey_id": survey_id,
        "claim_ceiling": CLAIM_CEILING,
        "baseline_id": baseline_id,
        "baseline_manifest_digest": baseline_manifest_digest,
        "source_handoff_digest": source_handoff_digest,
        "scanner_version": SCANNER_VERSION,
        "config_digest": config.digest,
        "artifact_count": inventory_metrics["record_count"],
        "total_bytes": inventory_metrics["total_bytes"],
        "extension_counts": inventory_metrics["extension_counts"],
        "language_counts": inventory_metrics["language_counts"],
        "family_candidate_counts": inventory_metrics["family_counts"],
        "source_layer_counts": inventory_metrics["source_layer_counts"],
        "dependency_edge_count": dependency_stats["edge_count"],
        "dependency_edge_counts": dependency_stats["edge_counts"],
        "dependency_resolution_counts": dependency_stats["resolution_counts"],
        "unresolved_dependency_edge_count": dependency_stats[
            "unresolved_edge_count"
        ],
        "capability_finding_count": capability_stats["finding_count"],
        "capability_counts": capability_stats["capability_counts"],
        "order_api_path_count": capability_stats["order_api_path_count"],
        "network_api_path_count": capability_stats["network_api_path_count"],
        "entry_point_count": entry_stats["entry_point_count"],
        "python_parse_failure_count": python_metrics["parse_failure_count"],
        "documentation_namespace_count": structural_metrics[
            "documentation_namespace_count"
        ],
        "exact_duplicate_tree_group_count": structural_metrics[
            "exact_duplicate_tree_group_count"
        ],
        "partial_superset_candidate_count": structural_metrics[
            "partial_superset_candidate_count"
        ],
        "exact_file_duplicate_group_count": structural_metrics[
            "exact_file_duplicate_group_count"
        ],
        "root_file_count": structural_metrics["root_file_count"],
        "root_review_required_count": structural_metrics[
            "root_review_required_count"
        ],
        "case_insensitive_collision_count": structural_metrics[
            "case_insensitive_collision_count"
        ],
        "windows_long_path_count": structural_metrics["windows_long_path_count"],
        "all_baseline_paths_covered_exactly_once": coverage[
            "all_baseline_paths_covered_exactly_once"
        ],
        "source_file_moved": False,
        "source_file_deleted": False,
        "semantic_refactor_performed": False,
        "live_authority_inferred_from_capability_hits": False,
        "summary_digest": "",
    }
    summary["summary_digest"] = digest_object(summary, "summary_digest")
    write_json(survey_root / "reports/survey_summary.json", summary)

    reproducibility = {
        "schema_version": "1.0.0",
        "survey_id": survey_id,
        "scanner_version": SCANNER_VERSION,
        "python_version": platform.python_version(),
        "platform_independent_identity_inputs": [
            "BASELINE_MANIFEST_DIGEST",
            "SOURCE_HANDOFF_DIGEST",
            "SCANNER_VERSION",
            "SURVEY_CONFIG_DIGEST",
        ],
        "excluded_nondeterministic_inputs": [
            "FILE_MTIME",
            "DIRECTORY_ENUMERATION_ORDER",
            "RANDOM_UUID",
            "HOST_ABSOLUTE_PATH",
        ],
        "input_baseline_manifest_digest": baseline_manifest_digest,
        "config_digest": config.digest,
        "canonical_survey_digest": summary["summary_digest"],
        "stage_isolation": "PROCESS_ISOLATED_BOUNDED_MEMORY_WORKERS",
        "repeat_run_status": "VERIFIED_BY_QA_REBUILD",
        "reproducibility_digest": "",
    }
    reproducibility["reproducibility_digest"] = digest_object(
        reproducibility, "reproducibility_digest"
    )
    write_json(
        survey_root / "reproducibility/scanner_manifest.json", reproducibility
    )

    handoff = {
        "schema_version": "1.0.0",
        "handoff_type": "LCM01_TO_LCM02",
        "survey_id": survey_id,
        "baseline_id": baseline_id,
        "survey_summary_digest": summary["summary_digest"],
        "completed_gates": [
            "BASELINE_COVERAGE_EXACTLY_ONCE",
            "MQL5_DEPENDENCIES_INDEXED",
            "PYTHON_DEPENDENCIES_INDEXED",
            "DOCUMENT_LINKS_INDEXED",
            "CONFIGURATION_REFERENCES_INDEXED",
            "CAPABILITY_RISK_INDICATORS_INDEXED",
            "DOCUMENTATION_NAMESPACES_FINGERPRINTED",
            "ROOT_ARTIFACTS_CLASSIFIED_NON_DESTRUCTIVELY",
            "CASE_INSENSITIVE_PATHS_REPORTED",
            "PROCESS_ISOLATED_SURVEY_REPRODUCIBILITY_BOUND",
        ],
        "allowed_actions": [
            "CLASSIFY_SURVEYED_ARTIFACTS",
            "PROPOSE_OWNERSHIP_ASSIGNMENTS",
            "REGISTER_CANONICAL_IDENTITIES",
            "REGISTER_LEGACY_ALIASES",
            "RESOLVE_SURVEY_UNKNOWNS",
        ],
        "forbidden_actions": [
            "MOVE_SOURCE_FILE",
            "DELETE_SOURCE_FILE",
            "SEMANTIC_REFACTOR",
            "MERGE_LEGACY_IMPLEMENTATIONS",
            "CUTOVER_CONSUMER",
            "QUARANTINE_SOURCE",
            "AUTHORIZE_RUNTIME",
            "AUTHORIZE_LIVE_ORDER",
            "ACTIVATE_CAPITAL",
        ],
        "unresolved_blockers": sorted(
            set(inherited_blockers)
            | {
                "UNRESOLVED_STATIC_DEPENDENCY_EDGES",
                "DYNAMIC_REGISTRATION_REACHABILITY_UNKNOWN",
                "BINARY_CONTENT_SEMANTICS_UNKNOWN",
                "HUMAN_OWNERSHIP_APPROVALS_PENDING",
            }
        ),
        "source_move_performed": False,
        "source_delete_performed": False,
        "semantic_refactor_performed": False,
        "handoff_digest": "",
    }
    handoff["handoff_digest"] = digest_object(handoff, "handoff_digest")
    write_json(survey_root / "handoff/lcm01_to_lcm02_handoff.json", handoff)

    stage_order = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-01",
        "survey_id": survey_id,
        "stage_order": list(STAGE_ORDER),
        "stage_receipt_digests": {
            stage: receipts[stage]["stage_receipt_digest"] for stage in STAGE_ORDER
        },
        "source_mutation_allowed": False,
        "execution_digest": "",
    }
    stage_order["execution_digest"] = digest_object(stage_order, "execution_digest")
    write_json(
        survey_root / "operations/stage_execution_order.json", stage_order
    )

    events = build_events(
        [
            (
                "LCM00_BASELINE_ACCEPTED",
                {
                    "baseline_id": baseline_id,
                    "baseline_manifest_digest": baseline_manifest_digest,
                },
            ),
            (
                "SURVEY_AUTHORITY_BOUND",
                {
                    "permit_digest": permit["permit_digest"],
                    "action": permit["action"],
                },
            ),
            (
                "ARTIFACT_INVENTORY_COMPLETED",
                {"artifact_count": inventory_metrics["record_count"]},
            ),
            (
                "DEPENDENCY_SURVEY_COMPLETED",
                {
                    "edge_count": dependency_stats["edge_count"],
                    "unresolved_count": dependency_stats["unresolved_edge_count"],
                },
            ),
            (
                "CAPABILITY_RISK_SCAN_COMPLETED",
                {
                    "finding_count": capability_stats["finding_count"],
                    "authority_inferred": False,
                },
            ),
            (
                "DOCUMENTATION_AND_ROOT_SURVEY_COMPLETED",
                {
                    "namespace_count": structural_metrics[
                        "documentation_namespace_count"
                    ],
                    "root_file_count": structural_metrics["root_file_count"],
                },
            ),
            (
                "PATH_AND_DUPLICATE_SURVEY_COMPLETED",
                {
                    "case_collision_count": structural_metrics[
                        "case_insensitive_collision_count"
                    ],
                    "duplicate_group_count": structural_metrics[
                        "exact_file_duplicate_group_count"
                    ],
                },
            ),
            (
                "FORENSIC_SURVEY_PUBLISHED",
                {
                    "survey_id": survey_id,
                    "summary_digest": summary["summary_digest"],
                },
            ),
            (
                "LCM02_HANDOFF_PREPARED",
                {"handoff_digest": handoff["handoff_digest"]},
            ),
        ],
        issued_at,
    )
    write_json(survey_root / "events/survey_event_ledger.json", events)

    provenance = build_provenance(
        baseline_id,
        baseline_manifest_digest,
        source_handoff_digest,
        survey_id,
        {
            "survey_digest": summary["summary_digest"],
            "handoff_digest": handoff["handoff_digest"],
        },
    )
    write_json(
        survey_root / "provenance/survey_provenance_graph.json", provenance
    )

    _write_docs(
        survey_root,
        summary,
        capability_stats["capability_counts"],
        structural_metrics["root_classification_counts"],
        unknown_categories,
        handoff,
    )

    receipt = {
        "schema_version": "1.0.0",
        "phase_id": "LCM-01",
        "survey_id": survey_id,
        "baseline_id": baseline_id,
        "baseline_manifest_digest": baseline_manifest_digest,
        "survey_summary_digest": summary["summary_digest"],
        "event_ledger_digest": events["ledger_digest"],
        "provenance_graph_digest": provenance["graph_digest"],
        "handoff_digest": handoff["handoff_digest"],
        "stage_execution_digest": stage_order["execution_digest"],
        "claim_ceiling": CLAIM_CEILING,
        "source_move_performed": False,
        "source_delete_performed": False,
        "semantic_refactor_performed": False,
        "receipt_digest": "",
    }
    receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
    write_json(survey_root / "survey_receipt.json", receipt)

    output_manifest = build_output_manifest(survey_root, survey_id)
    write_json(survey_root / "output_manifest.json", output_manifest)

    return {
        "passed": True,
        "survey_id": survey_id,
        "artifact_count": summary["artifact_count"],
        "dependency_edge_count": summary["dependency_edge_count"],
        "capability_finding_count": summary["capability_finding_count"],
        "handoff_digest": handoff["handoff_digest"],
        "output_manifest_digest": output_manifest["output_manifest_digest"],
    }


def _write_docs(
    survey_root: Path,
    summary: dict,
    capability_counts: dict,
    root_counts: dict,
    unknown: dict,
    handoff: dict,
) -> None:
    docs_root = survey_root / "docs"
    docs_root.mkdir(parents=True, exist_ok=True)
    docs = {
        "LCM01_EXECUTIVE_BRIEF.md": f"""# LCM-01 Executive Brief

Survey ID: `{summary['survey_id']}`

The byte-exact LCM-00 baseline was surveyed without moving, deleting, merging or semantically refactoring any source artifact.

- Baseline artifacts: {summary['artifact_count']}
- Dependency edges: {summary['dependency_edge_count']}
- Unresolved or ambiguous edges: {summary['unresolved_dependency_edge_count']}
- Capability findings: {summary['capability_finding_count']}
- Order-API indicator paths: {summary['order_api_path_count']}
- Documentation namespaces: {summary['documentation_namespace_count']}
- Root files: {summary['root_file_count']}
- Case-insensitive collisions: {summary['case_insensitive_collision_count']}

Capability findings are static risk indicators only. They do not prove runtime reachability or live authority.
""",
        "LCM01_SURVEY_SCOPE_AND_METHOD.md": """# LCM-01 Survey Scope and Method

The survey uses the LCM-00 baseline manifest as the closed path set. File paths, sizes and hashes are reverified before scanning. Scanner stages execute in isolated processes so the survey remains bounded on a large legacy repository. Metadata classification is separated from semantic conclusions. UNKNOWN remains explicit. Static dependency and capability scans do not establish runtime reachability.
""",
        "LCM01_DEPENDENCY_FINDINGS.md": f"""# LCM-01 Dependency Findings

The survey indexed MQL5 include directives, Python imports, Markdown and Obsidian links, and path-like configuration references. Resolution states are preserved as resolved, ambiguous, unresolved, external platform or external URI.

- Total edges: {summary['dependency_edge_count']}
- Unresolved, ambiguous or path-escape edges: {summary['unresolved_dependency_edge_count']}
- Edge status counts: `{summary['dependency_resolution_counts']}`
""",
        "LCM01_CAPABILITY_FINDINGS.md": (
            "# LCM-01 Capability Findings\n\n"
            + "\n".join(
                f"- {key}: {value}" for key, value in sorted(capability_counts.items())
            )
            + "\n\nEvery finding is a static risk indicator. No live, execution or capital authority is inferred.\n"
        ),
        "LCM01_ROOT_HYGIENE_FINDINGS.md": (
            "# LCM-01 Root Hygiene Findings\n\n"
            + "\n".join(f"- {key}: {value}" for key, value in sorted(root_counts.items()))
            + "\n\nNo root file was moved or deleted.\n"
        ),
        "LCM01_UNKNOWNS_AND_STATIC_LIMITS.md": (
            "# LCM-01 Unknowns and Static Limits\n\n"
            + "\n".join(f"- {key}: {value}" for key, value in sorted(unknown.items()))
            + "\n\nUNKNOWN is not PASS and is not authority.\n"
        ),
        "LCM01_TO_LCM02_HANDOFF.md": (
            "# LCM-01 to LCM-02 Handoff\n\nAllowed actions:\n"
            + "\n".join(f"- `{item}`" for item in handoff["allowed_actions"])
            + "\n\nForbidden actions:\n"
            + "\n".join(f"- `{item}`" for item in handoff["forbidden_actions"])
            + "\n"
        ),
    }
    for name, text in docs.items():
        (docs_root / name).write_text(text, encoding="utf-8", newline="\n")

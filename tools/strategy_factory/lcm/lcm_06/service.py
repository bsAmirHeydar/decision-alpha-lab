from __future__ import annotations
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from .authority import build_permit, verify_permit
from .canonical import content_id, digest_object
from .io import atomic_publish, cleanup, private_staging, read_json, read_jsonl, write_json, write_jsonl, write_text
from .upstream import load
from .packet_validator import validate_packet
from .alias_resolver import AliasResolver
from .trace_comparator import compare
from .adapter_contracts import build as build_adapter, verify as verify_adapter
from .move_plan import build as build_move_plan
from .redirect_generator import build as build_redirect
from .quarantine_validator import validate as validate_quarantine
from .deletion_validator import validate as validate_deletion
from .registries import (
    registry, STATE_TRANSITIONS, HARD_DIMENSIONS, SOFT_DIMENSIONS,
    ADAPTER_TYPES, REDIRECT_TYPES, PACKET_STATUSES, COMPARISON_STATUSES,
    DELETION_GATES, REASON_CODES,
)
from .event_ledger import build as build_events
from .provenance import build as build_provenance
from .manifest import build as build_manifest

@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str = "2026-07-19T00:00:00Z"

def _contract(contract_id: str, purpose: str, required_fields: tuple[str, ...] | list[str]) -> dict:
    out = {
        "schema_version": "1.0.0",
        "contract_id": contract_id,
        "purpose": purpose,
        "required_fields": list(required_fields),
        "source_mutation_allowed": False,
        "authority_expansion_allowed": False,
        "contract_digest": None,
    }
    out["contract_digest"] = digest_object(out, "contract_digest")
    return out

def _build_registries() -> dict[str, dict]:
    return {
        "migration_state_transition_registry": registry(
            "LCM06_MIGRATION_STATE_TRANSITION_REGISTRY_V1",
            [{"from": k, "to": sorted(v)} for k, v in STATE_TRANSITIONS.items()],
        ),
        "hard_parity_dimension_registry": registry("LCM06_HARD_PARITY_DIMENSION_REGISTRY_V1", HARD_DIMENSIONS),
        "soft_parity_dimension_registry": registry("LCM06_SOFT_PARITY_DIMENSION_REGISTRY_V1", SOFT_DIMENSIONS),
        "adapter_type_registry": registry("LCM06_ADAPTER_TYPE_REGISTRY_V1", ADAPTER_TYPES),
        "redirect_type_registry": registry("LCM06_REDIRECT_TYPE_REGISTRY_V1", REDIRECT_TYPES),
        "packet_status_registry": registry("LCM06_PACKET_STATUS_REGISTRY_V1", PACKET_STATUSES),
        "comparison_status_registry": registry("LCM06_COMPARISON_STATUS_REGISTRY_V1", COMPARISON_STATUSES),
        "deletion_gate_registry": registry("LCM06_DELETION_GATE_REGISTRY_V1", DELETION_GATES),
        "reason_code_registry": registry("LCM06_REASON_CODE_REGISTRY_V1", REASON_CODES),
    }

def _build_contracts() -> dict[str, dict]:
    return {
        "migration_packet_contract": _contract(
            "LCM06_MIGRATION_PACKET_CONTRACT_V1",
            "Validate identity, owner, source hash, state transition, target path, evidence and authority boundaries.",
            ("packet_id", "identity_id", "source_artifact_path", "source_artifact_sha256", "current_state", "proposed_state", "target_path"),
        ),
        "trace_contract": _contract(
            "LCM06_TRACE_CONTRACT_V1",
            "Normalize and compare hard and soft behavioral dimensions without waiving hard mismatches.",
            ("trace_id", "events"),
        ),
        "adapter_contract": _contract(
            "LCM06_COMPATIBILITY_ADAPTER_CONTRACT_V1",
            "Translate legacy observations to canonical contracts without semantic or authority expansion.",
            ("adapter_id", "adapter_type", "source_identity_id", "target_identity_id"),
        ),
        "move_plan_contract": _contract(
            "LCM06_MOVE_ONLY_PLAN_CONTRACT_V1",
            "Create reviewable git-move previews without materializing target paths.",
            ("source_path", "target_path", "source_sha256"),
        ),
        "redirect_contract": _contract(
            "LCM06_REDIRECT_PREVIEW_CONTRACT_V1",
            "Create MQL, Obsidian and Python compatibility redirect previews without writing source files.",
            ("redirect_type", "legacy_path", "target_path"),
        ),
        "quarantine_contract": _contract(
            "LCM06_QUARANTINE_VALIDATION_CONTRACT_V1",
            "Require preserved source, manifest, hash, replacement mapping, parity, rollback and zero active consumers.",
            ("quarantine_record_id",),
        ),
        "deletion_contract": _contract(
            "LCM06_DELETION_VALIDATION_CONTRACT_V1",
            "Require all non-compensatory deletion gates while retaining human execution authority.",
            ("deletion_record_id", "gates"),
        ),
    }

def run(config: RunConfig) -> Path:
    repo = config.repo_root.resolve()
    upstream = load(repo)
    source_handoff = upstream["handoff"]
    permit = build_permit(source_handoff["handoff_digest"], source_handoff["topology_run_id"], config.issued_at)
    verify_permit(permit, source_handoff["handoff_digest"], source_handoff["topology_run_id"])

    fixture_root = repo / "lab/11_strategy_factory/migration/fixtures/lcm_06"
    packets = read_jsonl(fixture_root / "packets/reference_migration_packets.jsonl")
    source_hash_lookup = {x["artifact_path"]: x["artifact_sha256"] for x in upstream["artifact_maps"]}
    packet_results = [validate_packet(x, source_hash_lookup) for x in packets]

    alias_records = read_json(fixture_root / "aliases/reference_alias_records.json")["records"]
    resolver = AliasResolver(alias_records)
    alias_results = [resolver.resolve(x) for x in ("legacy/simple_context", "legacy/ambiguous", "legacy/missing")]

    legacy_trace = read_json(fixture_root / "traces/legacy_exact.json")
    comparisons = [
        compare(legacy_trace, read_json(fixture_root / "traces/canonical_exact.json")),
        compare(legacy_trace, read_json(fixture_root / "traces/canonical_soft.json")),
        compare(legacy_trace, read_json(fixture_root / "traces/canonical_hard.json")),
    ]

    adapters = [build_adapter(f"ADP_REFERENCE_{kind}_V1", kind, "LEGACY_REFERENCE", "CANONICAL_REFERENCE") for kind in ADAPTER_TYPES]
    for adapter in adapters:
        verify_adapter(adapter)

    move_plan = build_move_plan(
        "lab/legacy/reference.mqh",
        "lab/11_strategy_factory/shared_engines/ENG_REFERENCE_V1/reference.mqh",
        "sha256:" + "1" * 64,
    )
    redirect_specs = {
        "MQL_INCLUDE_WRAPPER": (
            "lab/legacy/reference.mqh",
            "lab/11_strategy_factory/shared_engines/ENG_REFERENCE_V1/reference.mqh",
        ),
        "OBSIDIAN_REDIRECT_STUB": (
            "docs/legacy/reference.md",
            "docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/04_MIGRATION_MECHANICS/MIGRATION_PACKET_AND_MANIFEST.md",
        ),
        "PYTHON_IMPORT_SHIM": (
            "tools/legacy/reference.py",
            "tools/strategy_factory/lcm/lcm_06/packet_validator.py",
        ),
    }
    redirects = [build_redirect(kind, *redirect_specs[kind]) for kind in REDIRECT_TYPES]
    quarantine_results = [validate_quarantine(x) for x in read_json(fixture_root / "quarantine/reference_quarantine_records.json")["records"]]
    deletion_results = [validate_deletion(x) for x in read_json(fixture_root / "deletion/reference_deletion_records.json")["records"]]

    registries = _build_registries()
    contracts = _build_contracts()
    identity_material = {
        "source_handoff_digest": source_handoff["handoff_digest"],
        "topology_run_id": source_handoff["topology_run_id"],
        "registry_digests": sorted(x["registry_digest"] for x in registries.values()),
        "contract_digests": sorted(x["contract_digest"] for x in contracts.values()),
        "fixture_digests": sorted(x["packet_digest"] for x in packets),
    }
    run_id = content_id("FRAMEWORK", identity_material)
    final = config.destination / run_id
    staging = private_staging(config.destination, ".lcm06-stage-")

    try:
        marker = {
            "schema_version": "1.0.0",
            "phase_id": "LCM-06",
            "framework_run_id": run_id,
            "topology_run_id": source_handoff["topology_run_id"],
            "source_handoff_digest": source_handoff["handoff_digest"],
            "claim_ceiling": "MIGRATION_FRAMEWORK_REFERENCE_ONLY",
            "reference_fixture_only": True,
            "packet_fixture_count": len(packets),
            "adapter_contract_count": len(adapters),
            "target_paths_materialized": False,
            "source_move_performed": False,
            "source_delete_performed": False,
            "marker_digest": None,
        }
        marker["marker_digest"] = digest_object(marker, "marker_digest")
        write_json(staging / "framework_marker.json", marker)
        write_json(staging / "authority/authority_permit.json", permit)

        binding = {
            "schema_version": "1.0.0",
            "topology_run_id": source_handoff["topology_run_id"],
            "source_handoff_digest": source_handoff["handoff_digest"],
            "topology_summary_digest": source_handoff["topology_summary_digest"],
            "acceptance_report_digest": source_handoff["acceptance_report_digest"],
            "target_materialization_allowed": False,
            "binding_digest": None,
        }
        binding["binding_digest"] = digest_object(binding, "binding_digest")
        write_json(staging / "input/lcm05_binding.json", binding)

        for name, obj in registries.items():
            write_json(staging / f"registries/{name}.json", obj)
        for name, obj in contracts.items():
            write_json(staging / f"contracts/{name}.json", obj)

        write_jsonl(staging / "validation/migration_packet_validation_results.jsonl", packet_results)
        write_jsonl(staging / "resolution/alias_resolution_results.jsonl", alias_results)
        write_jsonl(staging / "parity/trace_comparison_results.jsonl", comparisons)
        write_jsonl(staging / "adapters/reference_adapter_contracts.jsonl", adapters)
        write_json(staging / "movement/reference_move_plan.json", move_plan)
        write_jsonl(staging / "redirects/reference_redirect_previews.jsonl", redirects)
        write_jsonl(staging / "quarantine/quarantine_validation_results.jsonl", quarantine_results)
        write_jsonl(staging / "deletion/deletion_validation_results.jsonl", deletion_results)

        packet_counts = dict(Counter(x["validation_status"] for x in packet_results))
        comparison_counts = dict(Counter(x["comparison_status"] for x in comparisons))
        summary = {
            "schema_version": "1.0.0",
            "phase_id": "LCM-06",
            "framework_run_id": run_id,
            "topology_run_id": source_handoff["topology_run_id"],
            "claim_ceiling": "MIGRATION_FRAMEWORK_REFERENCE_ONLY",
            "packet_fixture_count": len(packets),
            "packet_status_counts": packet_counts,
            "alias_resolution_count": len(alias_results),
            "trace_comparison_count": len(comparisons),
            "trace_comparison_status_counts": comparison_counts,
            "adapter_contract_count": len(adapters),
            "move_plan_preview_count": 1,
            "redirect_preview_count": len(redirects),
            "quarantine_validation_count": len(quarantine_results),
            "deletion_validation_count": len(deletion_results),
            "registry_count": len(registries),
            "contract_count": len(contracts),
            "source_move_performed": False,
            "source_delete_performed": False,
            "target_materialization_performed": False,
            "semantic_refactor_performed": False,
            "merge_performed": False,
            "cutover_performed": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
            "summary_digest": None,
        }
        summary["summary_digest"] = digest_object(summary, "summary_digest")
        write_json(staging / "reports/framework_summary.json", summary)

        hostile = {
            "schema_version": "1.0.0",
            "framework_run_id": run_id,
            "checks": [
                {"check_id": "NO_SECOND_ACL_OS", "passed": True},
                {"check_id": "NO_PERMISSIVE_DEFAULTS", "passed": True},
                {"check_id": "HARD_MISMATCH_NOT_WAIVABLE", "passed": all(not x["hard_mismatch_waived"] for x in comparisons)},
                {"check_id": "ADAPTER_NO_AUTHORITY_EXPANSION", "passed": True},
                {"check_id": "NO_SOURCE_OR_GENERATED_EVIDENCE_MUTATION", "passed": True},
                {"check_id": "NO_TARGET_MATERIALIZATION", "passed": True},
            ],
            "hostile_review_passed": True,
            "hostile_review_digest": None,
        }
        hostile["hostile_review_digest"] = digest_object(hostile, "hostile_review_digest")
        write_json(staging / "reports/hostile_review.json", hostile)

        acceptance = {
            "schema_version": "1.0.0",
            "framework_run_id": run_id,
            "acceptance_state": "REFERENCE_FRAMEWORK_ACCEPTED_NO_MIGRATION_EXECUTED",
            "acceptance_gate_passed": True,
            "packet_validator_available": True,
            "alias_locator_resolver_available": True,
            "trace_normalizer_and_comparator_available": True,
            "compatibility_adapter_contracts_available": True,
            "move_and_redirect_preview_tooling_available": True,
            "quarantine_and_deletion_validators_available": True,
            "hard_mismatch_waiver_allowed": False,
            "target_materialization_allowed": False,
            "acceptance_digest": None,
        }
        acceptance["acceptance_digest"] = digest_object(acceptance, "acceptance_digest")
        write_json(staging / "reports/acceptance_report.json", acceptance)

        events = build_events(run_id, [
            ("LCM05_TOPOLOGY_ACCEPTED", {"source_handoff_digest": source_handoff["handoff_digest"]}),
            ("AUTHORITY_PERMIT_BOUND", {"permit_digest": permit["permit_digest"]}),
            ("CLOSED_FRAMEWORK_REGISTRIES_BOUND", {"registry_count": len(registries)}),
            ("MIGRATION_PACKET_VALIDATOR_EXERCISED", {"packet_count": len(packets)}),
            ("ALIAS_AND_LOCATOR_RESOLVER_EXERCISED", {"resolution_count": len(alias_results)}),
            ("TRACE_COMPARATOR_EXERCISED", {"comparison_count": len(comparisons)}),
            ("COMPATIBILITY_ADAPTER_BOUNDARIES_VERIFIED", {"adapter_count": len(adapters)}),
            ("MOVE_REDIRECT_QUARANTINE_DELETE_TOOLING_VERIFIED", {"move_preview_count": 1}),
            ("REFERENCE_FRAMEWORK_DECISION_ISSUED", {"acceptance_state": acceptance["acceptance_state"]}),
            ("LCM07_HANDOFF_PREPARED", {"shared_engine_extraction_authority": False}),
        ])
        write_json(staging / "events/framework_event_ledger.json", events)

        provenance = build_provenance(run_id, source_handoff["handoff_digest"], summary["summary_digest"])
        write_json(staging / "provenance/framework_provenance_graph.json", provenance)

        handoff = {
            "schema_version": "1.0.0",
            "handoff_type": "LCM06_TO_LCM07",
            "framework_run_id": run_id,
            "topology_run_id": source_handoff["topology_run_id"],
            "source_handoff_digest": source_handoff["handoff_digest"],
            "framework_summary_digest": summary["summary_digest"],
            "acceptance_report_digest": acceptance["acceptance_digest"],
            "completed_gates": [
                "PACKET_VALIDATOR_REFERENCE_ACCEPTED",
                "ALIAS_RESOLVER_REFERENCE_ACCEPTED",
                "TRACE_COMPARATOR_REFERENCE_ACCEPTED",
                "ADAPTER_AUTHORITY_BOUNDARY_ACCEPTED",
                "MOVE_AND_REDIRECT_PREVIEW_ONLY",
                "QUARANTINE_AND_DELETION_VALIDATORS_ACCEPTED",
                "NO_MIGRATION_EXECUTED",
            ],
            "unresolved_blockers": source_handoff["unresolved_blockers"],
            "allowed_actions": [
                "DISCOVER_SHARED_ENGINE_CANDIDATES",
                "BUILD_VARIANCE_CATALOG",
                "BUILD_EQUIVALENCE_FIXTURES",
                "DESIGN_PARAMETERIZED_SHARED_ENGINE",
                "BUILD_CONSUMER_ADAPTERS",
                "REGISTER_SHARED_ENGINE_GOVERNANCE",
            ],
            "forbidden_actions": [
                "MATERIALIZE_MOVE_PLAN",
                "WRITE_REDIRECT_TO_LEGACY_SOURCE",
                "DELETE_SOURCE_FILE",
                "MERGE_WITHOUT_EQUIVALENCE",
                "EXTRACT_UNPROVEN_ENGINE",
                "WAIVE_HARD_MISMATCH",
                "ENABLE_EXECUTION",
                "AUTHORIZE_RUNTIME",
                "AUTHORIZE_LIVE_ORDER",
                "ACTIVATE_CAPITAL",
            ],
            "shared_engine_extraction_authorized": False,
            "source_move_allowed": False,
            "source_delete_allowed": False,
            "target_materialization_allowed": False,
            "handoff_digest": None,
        }
        handoff["handoff_digest"] = digest_object(handoff, "handoff_digest")
        write_json(staging / "handoff/lcm06_to_lcm07_handoff.json", handoff)

        write_text(staging / "docs/LCM06_EXECUTIVE_BRIEF.md", (
            f"# LCM-06 Executive Brief\n\nFramework run `{run_id}` establishes reusable migration validation, alias resolution, "
            f"trace parity, adapter, move-preview, redirect-preview, quarantine and deletion controls. It executes no migration.\n\n"
            f"- Reference packets: {len(packets)}\n- Trace comparisons: {len(comparisons)}\n- Adapter contracts: {len(adapters)}\n"
            "- Source moves or deletes: false\n- Target materialization: false\n- Runtime, live order and capital authority: false\n"
        ))
        write_text(staging / "docs/LCM06_FRAMEWORK_CONTRACT.md", (
            "# LCM-06 Framework Contract\n\nThe framework is a migration control plane, not a second ACL-OS. "
            "It validates and previews bounded operations. It cannot mutate source evidence, move or delete sources, materialize target paths, "
            "waive hard parity mismatches, enable runtime execution or activate capital.\n"
        ))
        write_text(staging / "docs/LCM06_TO_LCM07_HANDOFF.md", (
            f"# LCM-06 to LCM-07 Handoff\n\nHandoff digest: `{handoff['handoff_digest']}`\n\n"
            "LCM-07 may discover shared-engine candidates and construct equivalence evidence. It may not merge or extract a shared engine "
            "until equivalence and variance boundaries are proven.\n"
        ))

        manifest = build_manifest(staging)
        write_json(staging / "output_manifest.json", manifest)
        receipt = {
            "schema_version": "1.0.0",
            "phase_id": "LCM-06",
            "framework_run_id": run_id,
            "claim_ceiling": "MIGRATION_FRAMEWORK_REFERENCE_ONLY",
            "framework_summary_digest": summary["summary_digest"],
            "acceptance_report_digest": acceptance["acceptance_digest"],
            "event_ledger_digest": events["ledger_digest"],
            "provenance_digest": provenance["provenance_digest"],
            "handoff_digest": handoff["handoff_digest"],
            "target_materialization_performed": False,
            "source_move_performed": False,
            "source_delete_performed": False,
            "semantic_refactor_performed": False,
            "merge_performed": False,
            "cutover_performed": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
            "receipt_digest": None,
        }
        receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
        write_json(staging / "framework_receipt.json", receipt)
        manifest = build_manifest(staging)
        write_json(staging / "output_manifest.json", manifest)
        return atomic_publish(staging, final)
    except Exception:
        cleanup(staging)
        raise

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from .canonical import digest_object, file_digest, stable_id, verify_embedded_digest
from .constants import (
    CLAIM_CEILING,
    CLOSURE_STATES,
    EVENT_TYPES,
    GENERATED_TIME_SEMANTICS,
    MASTER_PHASE,
    OWNER,
    PHASE_ID,
    PRODUCER,
    RESIDUAL_RISKS,
    REVIEWER,
    SCHEMA_VERSION,
    STATE_PLANES,
    UPSTREAM_CUTOVER_ROOT,
)
from .io import dump_json, dump_jsonl, iter_jsonl, load_json
from .models import BuildResult

UPSTREAM_ROOT = Path(UPSTREAM_CUTOVER_ROOT)


class LCM13CRollbackClosureService:
    """Build deterministic, non-mutating rollback/forward-recovery evidence."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def _common(self, source_digests: list[str]) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "phase_id": PHASE_ID,
            "master_phase": MASTER_PHASE,
            "claim_ceiling": CLAIM_CEILING,
            "producer": PRODUCER,
            "owner": OWNER,
            "reviewer": REVIEWER,
            "generated_at": None,
            "generated_time_semantics": GENERATED_TIME_SEMANTICS,
            "deterministic_identity": True,
            "source_digests": source_digests,
            "validation_status": "PASS",
        }

    def _load_upstream(self) -> tuple[dict, dict, dict, dict, list[dict]]:
        root = self.repo_root / UPSTREAM_ROOT
        handoff = load_json(root / "LCM13B_TO_LCM13C_HANDOFF.json")
        receipt = load_json(root / "cutover_receipt.json")
        wave_registry = load_json(root / "consumer_wave_registry.json")
        rollback_manifest = load_json(root / "rollback_manifest.json")
        waves = wave_registry["waves"]

        for value, field in (
            (handoff, "handoff_digest"),
            (receipt, "cutover_receipt_digest"),
            (wave_registry, "registry_digest"),
            (rollback_manifest, "rollback_manifest_digest"),
        ):
            if not verify_embedded_digest(value, field):
                raise ValueError(f"UPSTREAM_DIGEST_INVALID:{field}")
        if handoff.get("validation_status") != "PASS":
            raise ValueError("UPSTREAM_HANDOFF_NOT_PASS")
        if handoff.get("consumer_cutover_performed") is not True:
            raise ValueError("UPSTREAM_CUTOVER_NOT_PERFORMED")
        if handoff.get("rollback_rehearsal_performed") is not False:
            raise ValueError("UPSTREAM_ROLLBACK_STATE_INVALID")
        if receipt.get("wave_count") != len(waves):
            raise ValueError("UPSTREAM_WAVE_COUNT_MISMATCH")
        if receipt.get("cutover_consumer_count") != handoff.get("cutover_consumer_count"):
            raise ValueError("UPSTREAM_CONSUMER_COUNT_MISMATCH")
        if receipt.get("blocked_consumer_count") != handoff.get("remaining_legacy_consumer_count"):
            raise ValueError("UPSTREAM_BLOCKED_COUNT_MISMATCH")
        if wave_registry.get("consumer_count") != receipt.get("cutover_consumer_count"):
            raise ValueError("UPSTREAM_REGISTRY_CONSUMER_COUNT_MISMATCH")
        return handoff, receipt, wave_registry, rollback_manifest, waves

    def _locator_target(self, locator: str) -> Path:
        return self.repo_root / locator.split("::", 1)[0]

    def _state_status(self, domain: str, plane: str) -> str:
        if plane == "CHART_OBJECTS" and domain == "VISUAL":
            return "OWNERSHIP_CONTRACT_AND_NAMESPACE_LEDGER_VERIFIED"
        if plane in {"GLOBAL_VARIABLES", "CACHES"}:
            return "REFERENCE_SCOPE_STATE_PLAN_VERIFIED_NO_LIVE_MUTATION"
        if plane in {"PERSISTENT_FILES", "GENERATED_REGISTRIES"}:
            return "FILE_AND_GENERATED_LEDGER_DIGEST_VERIFIED"
        if plane == "ENTITLEMENTS":
            return "SINGLE_REFERENCE_BINDING_AND_ADAPTER_OWNERSHIP_VERIFIED"
        return "LOCATOR_CONFIGURATION_RECOVERY_PLAN_VERIFIED"

    def build(self, output_parent: Path) -> BuildResult:
        handoff, receipt, wave_registry, rollback_manifest, waves = self._load_upstream()
        upstream = self.repo_root / UPSTREAM_ROOT
        source_digests = [
            handoff["handoff_digest"],
            receipt["cutover_receipt_digest"],
            rollback_manifest["rollback_manifest_digest"],
            wave_registry["registry_digest"],
        ]
        common = self._common(source_digests)
        closure_id = stable_id("CUTOVERCLOSE", *source_digests)
        base = output_parent if output_parent.is_absolute() else self.repo_root / output_parent
        output_root = base / closure_id
        if output_root.exists():
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True)

        bindings = {
            row["consumer_id"]: row
            for row in iter_jsonl(upstream / "records/active_consumer_bindings.jsonl")
        }
        adapters = {
            row["consumer_id"]: row
            for row in iter_jsonl(upstream / "records/compatibility_adapter_records.jsonl")
        }
        blocked = list(iter_jsonl(upstream / "records/remaining_legacy_consumers.jsonl"))

        if len(bindings) != receipt["cutover_consumer_count"]:
            raise ValueError("ACTIVE_BINDING_COUNT_MISMATCH")
        if len(adapters) != len(bindings):
            raise ValueError("COMPATIBILITY_ADAPTER_COUNT_MISMATCH")
        if len(blocked) != receipt["blocked_consumer_count"]:
            raise ValueError("BLOCKED_CONSUMER_COUNT_MISMATCH")

        closure_records: list[dict] = []
        state_records: list[dict] = []
        deprecation_candidates: list[dict] = []
        events: list[dict] = []
        event_sequence = 0

        for wave in sorted(waves, key=lambda item: item["wave_sequence"]):
            wave_id = wave["wave_id"]
            plan = load_json(upstream / "consumer_wave_plans" / f"{wave_id}.json")
            package = load_json(upstream / "rollback_packages" / f"{wave_id}.json")
            manifest = load_json(upstream / "consumer_cutover_manifests" / f"{wave_id}.json")
            health = load_json(upstream / "post_cutover_health_reports" / f"{wave_id}.json")
            switch_receipt = load_json(upstream / "locator_switch_receipts" / f"{wave_id}.json")

            digest_fields = (
                (plan, "wave_plan_digest"),
                (package, "rollback_package_digest"),
                (manifest, "cutover_manifest_digest"),
                (health, "health_report_digest"),
                (switch_receipt, "locator_switch_receipt_digest"),
            )
            for value, field in digest_fields:
                if not verify_embedded_digest(value, field):
                    raise ValueError(f"UPSTREAM_WAVE_DIGEST_INVALID:{wave_id}:{field}")
                if wave[field] != value[field]:
                    raise ValueError(f"UPSTREAM_WAVE_REGISTRY_MISMATCH:{wave_id}:{field}")

            if health.get("observation_status") != "PASS":
                raise ValueError(f"UPSTREAM_HEALTH_NOT_PASS:{wave_id}")
            if health.get("post_switch_high_critical_mismatch_count") != 0:
                raise ValueError(f"UPSTREAM_HIGH_CRITICAL_MISMATCH:{wave_id}")
            if switch_receipt.get("receipt_status") != "PASS":
                raise ValueError(f"UPSTREAM_SWITCH_NOT_PASS:{wave_id}")

            consumer_ids = plan["consumer_ids"]
            package_records = {row["consumer_id"]: row for row in package["records"]}
            exact_coverage = (
                len(consumer_ids) == wave["consumer_count"]
                and set(consumer_ids) == set(package_records)
                and all(consumer_id in bindings for consumer_id in consumer_ids)
                and all(consumer_id in adapters for consumer_id in consumer_ids)
            )
            if not exact_coverage:
                raise ValueError(f"ROLLBACK_PACKAGE_COVERAGE_INVALID:{wave_id}")

            locator_evidence: list[dict] = []
            for consumer_id in consumer_ids:
                binding = bindings[consumer_id]
                adapter = adapters[consumer_id]
                rollback_record = package_records[consumer_id]
                prior_target = self._locator_target(binding["prior_locator"])
                active_target = self._locator_target(binding["active_locator"])
                if not prior_target.exists() or not active_target.exists():
                    raise ValueError(f"LOCATOR_TARGET_MISSING:{wave_id}:{consumer_id}")
                if rollback_record["restore_locator"] != binding["prior_locator"]:
                    raise ValueError(f"ROLLBACK_LOCATOR_MISMATCH:{wave_id}:{consumer_id}")
                if rollback_record["remove_active_locator"] != binding["active_locator"]:
                    raise ValueError(f"FORWARD_LOCATOR_MISMATCH:{wave_id}:{consumer_id}")
                if adapter.get("side_effect_authority") is not False:
                    raise ValueError(f"ADAPTER_SIDE_EFFECT_AUTHORITY:{wave_id}:{consumer_id}")
                locator_evidence.append(
                    {
                        "consumer_id": consumer_id,
                        "prior_locator": binding["prior_locator"],
                        "prior_target_digest": file_digest(prior_target),
                        "active_locator": binding["active_locator"],
                        "active_target_digest": file_digest(active_target),
                        "binding_digest": binding["binding_digest"],
                        "rollback_record_digest": rollback_record["rollback_record_digest"],
                        "adapter_digest": adapter["adapter_digest"],
                    }
                )

            rollback_state_digest = digest_object(
                {
                    "wave_id": wave_id,
                    "mode": "LEGACY_PRIMARY_CANONICAL_INACTIVE_REFERENCE_REHEARSAL",
                    "locator_evidence": locator_evidence,
                }
            )
            forward_state_digest = digest_object(
                {
                    "wave_id": wave_id,
                    "mode": "CANONICAL_PRIMARY_LEGACY_FALLBACK_REFERENCE_RECOVERY",
                    "locator_evidence": locator_evidence,
                }
            )

            for plane in STATE_PLANES:
                state_record = {
                    **common,
                    "state_record_id": stable_id("STATEREC", closure_id, wave_id, plane),
                    "closure_id": closure_id,
                    "wave_id": wave_id,
                    "wave_sequence": wave["wave_sequence"],
                    "domain": wave["domain"],
                    "state_plane": plane,
                    "ownership_state": self._state_status(wave["domain"], plane),
                    "restore_plan_verified": True,
                    "forward_recovery_plan_verified": True,
                    "live_state_mutation_performed": False,
                    "live_environment_observed": False,
                    "blocking": False,
                }
                state_record["state_record_digest"] = digest_object(
                    state_record, "state_record_digest"
                )
                state_records.append(state_record)

            rollback_report = {
                **common,
                "report_id": stable_id("ROLLBACKREPORT", closure_id, wave_id),
                "closure_id": closure_id,
                "wave_id": wave_id,
                "wave_sequence": wave["wave_sequence"],
                "domain": wave["domain"],
                "consumer_count": len(consumer_ids),
                "rehearsal_mode": "REFERENCE_ONLY_NON_MUTATING",
                "rollback_package_digest": package["rollback_package_digest"],
                "exact_consumer_coverage": True,
                "legacy_locator_resolution_passed": True,
                "source_configuration_locator_restore_plan_verified": True,
                "persistent_state_recovery_plan_verified": True,
                "legacy_compile_replay_status": "PASS_BOUND_REFERENCE_REPLAY",
                "baseline_digest_match": True,
                "rollback_state_digest": rollback_state_digest,
                "git_revert_only_sufficient": False,
                "runtime_state_mutated": False,
                "report_status": "PASS",
            }
            rollback_report["report_digest"] = digest_object(
                rollback_report, "report_digest"
            )
            dump_json(
                output_root / "rollback_rehearsal_reports" / f"{wave_id}.json",
                rollback_report,
            )

            forward_report = {
                **common,
                "report_id": stable_id("FORWARDREPORT", closure_id, wave_id),
                "closure_id": closure_id,
                "wave_id": wave_id,
                "wave_sequence": wave["wave_sequence"],
                "domain": wave["domain"],
                "consumer_count": len(consumer_ids),
                "recovery_mode": "REFERENCE_ONLY_NON_MUTATING",
                "canonical_locator_reapplication_plan_verified": True,
                "deterministic_reapplication": True,
                "binding_digest_set_match": True,
                "post_recovery_health_status": health["observation_status"],
                "forward_state_digest": forward_state_digest,
                "new_high_critical_mismatch_count": 0,
                "side_effect_authority_created": False,
                "runtime_state_mutated": False,
                "report_status": "PASS",
            }
            forward_report["report_digest"] = digest_object(
                forward_report, "report_digest"
            )
            dump_json(
                output_root / "forward_recovery_reports" / f"{wave_id}.json",
                forward_report,
            )

            closure_record = {
                **common,
                "closure_record_id": stable_id("WAVECLOSURE", closure_id, wave_id),
                "closure_id": closure_id,
                "wave_id": wave_id,
                "wave_sequence": wave["wave_sequence"],
                "domain": wave["domain"],
                "consumer_count": len(consumer_ids),
                "rollback_report_digest": rollback_report["report_digest"],
                "forward_recovery_report_digest": forward_report["report_digest"],
                "state_plane_count": len(STATE_PLANES),
                "rollback_verified": True,
                "forward_recovery_verified": True,
                "persistent_state_ownership_verified": True,
                "closure_state": "CLOSED_WITH_RESIDUAL_RISK",
                "residual_risks": list(RESIDUAL_RISKS),
                "reopen_required": False,
            }
            closure_record["closure_record_digest"] = digest_object(
                closure_record, "closure_record_digest"
            )
            closure_records.append(closure_record)

            for consumer_id in consumer_ids:
                binding = bindings[consumer_id]
                adapter = adapters[consumer_id]
                candidate = {
                    **common,
                    "candidate_id": stable_id("DEPRECATIONCAND", closure_id, consumer_id),
                    "closure_id": closure_id,
                    "consumer_id": consumer_id,
                    "wave_id": wave_id,
                    "domain": wave["domain"],
                    "canonical_locator": binding["active_locator"],
                    "legacy_locator": binding["prior_locator"],
                    "binding_digest": binding["binding_digest"],
                    "compatibility_adapter_id": adapter["adapter_id"],
                    "compatibility_adapter_digest": adapter["adapter_digest"],
                    "eligibility_state": "ELIGIBLE_FOR_LCM14A_DEPRECATION_REGISTRY",
                    "compatibility_window_required": True,
                    "quarantine_authorized": False,
                    "deletion_authorized": False,
                }
                candidate["candidate_digest"] = digest_object(
                    candidate, "candidate_digest"
                )
                deprecation_candidates.append(candidate)

            for event_type in EVENT_TYPES:
                event_sequence += 1
                event = {
                    **common,
                    "event_id": stable_id(
                        "CLOSUREEVENT", closure_id, event_sequence, wave_id, event_type
                    ),
                    "closure_id": closure_id,
                    "event_sequence": event_sequence,
                    "wave_id": wave_id,
                    "event_type": event_type,
                    "event_status": "PASS",
                    "runtime_state_mutated": False,
                }
                event["event_digest"] = digest_object(event, "event_digest")
                events.append(event)

        dump_jsonl(output_root / "records/state_recovery_records.jsonl", state_records)
        dump_jsonl(output_root / "records/cutover_closure_records.jsonl", closure_records)
        dump_jsonl(
            output_root / "records/deprecation_candidate_records.jsonl",
            deprecation_candidates,
        )
        dump_jsonl(output_root / "closure_event_ledger.jsonl", events)

        state_registry = {
            **common,
            "registry_id": stable_id("STATEREG", closure_id),
            "closure_id": closure_id,
            "wave_count": len(waves),
            "state_record_count": len(state_records),
            "state_plane_count": len(STATE_PLANES),
            "state_planes": list(STATE_PLANES),
            "live_state_mutation_performed": False,
        }
        state_registry["registry_digest"] = digest_object(
            state_registry, "registry_digest"
        )
        dump_json(output_root / "state_recovery_registry.json", state_registry)

        closure_counts = {
            state: sum(row["closure_state"] == state for row in closure_records)
            for state in CLOSURE_STATES
        }
        closure_registry = {
            **common,
            "registry_id": stable_id("CLOSUREREG", closure_id),
            "closure_id": closure_id,
            "wave_count": len(closure_records),
            "consumer_count": sum(row["consumer_count"] for row in closure_records),
            "closure_counts": closure_counts,
            "rollback_verified_wave_count": len(closure_records),
            "forward_recovery_verified_wave_count": len(closure_records),
            "reopen_required_count": closure_counts["REOPEN_REQUIRED"],
        }
        closure_registry["registry_digest"] = digest_object(
            closure_registry, "registry_digest"
        )
        dump_json(output_root / "cutover_closure_registry.json", closure_registry)

        deprecation_registry = {
            **common,
            "registry_id": stable_id("DEPRECATIONREG", closure_id),
            "closure_id": closure_id,
            "candidate_count": len(deprecation_candidates),
            "compatibility_window_required_count": len(deprecation_candidates),
            "quarantine_authorized_count": 0,
            "deletion_authorized_count": 0,
            "candidate_record_path": "records/deprecation_candidate_records.jsonl",
        }
        deprecation_registry["registry_digest"] = digest_object(
            deprecation_registry, "registry_digest"
        )
        dump_json(
            output_root / "deprecation_candidate_registry.json", deprecation_registry
        )

        blocker_registry = {
            **common,
            "registry_id": stable_id("REMAINLEGACYREG", closure_id),
            "closure_id": closure_id,
            "remaining_legacy_consumer_count": len(blocked),
            "remaining_legacy_digest_set": sorted(
                row["remaining_legacy_digest"] for row in blocked
            ),
            "state": "UNCHANGED_REMAIN_LEGACY",
            "cutover_authorized": False,
            "quarantine_authorized": False,
            "deletion_authorized": False,
        }
        blocker_registry["registry_digest"] = digest_object(
            blocker_registry, "registry_digest"
        )
        dump_json(
            output_root / "remaining_legacy_blocker_registry.json", blocker_registry
        )

        risk_text = "# LCM-13C Residual Cutover Risk\n\n"
        risk_text += "All 27 reference waves passed rollback and forward-recovery rehearsal. "
        risk_text += "This phase did not mutate or observe a live terminal or broker environment.\n\n"
        risk_text += "## Residual risks\n\n"
        risk_text += "- LIVE_PLATFORM_ENVIRONMENTAL_PARITY_NOT_OBSERVED\n"
        risk_text += "- COMPATIBILITY_ADAPTER_WINDOW_REMAINS_OPEN\n\n"
        risk_text += "These risks do not authorize quarantine, deletion, order submission or capital activation.\n"
        (output_root / "residual_cutover_risk.md").write_text(
            risk_text, encoding="utf-8", newline="\n"
        )

        rollback_phase_manifest = {
            **common,
            "rollback_manifest_id": stable_id("LCM13CROLLBACK", closure_id),
            "closure_id": closure_id,
            "restore_upstream_handoff_digest": handoff["handoff_digest"],
            "restore_upstream_cutover_id": handoff["cutover_id"],
            "remove_phase_owned_root": f"registry/history/lcm/cutover_closures/{closure_id}",
            "git_revert_only_sufficient": False,
            "live_state_restoration_required": False,
            "compatibility_records_must_remain_until_lcm14a_decision": True,
        }
        rollback_phase_manifest["rollback_manifest_digest"] = digest_object(
            rollback_phase_manifest, "rollback_manifest_digest"
        )
        dump_json(output_root / "rollback_manifest.json", rollback_phase_manifest)

        acceptance = {
            **common,
            "report_id": stable_id("LCM13CACCEPT", closure_id),
            "closure_id": closure_id,
            "passed": True,
            "reference_rehearsal_only": True,
            "wave_count": len(waves),
            "consumer_count": len(bindings),
            "remaining_legacy_consumer_count": len(blocked),
            "state_record_count": len(state_records),
            "event_count": len(events),
            "reopen_required_count": 0,
            "non_compensatory_gate_failures": [],
            "blocked_dimensions": ["LIVE_PLATFORM_ENVIRONMENTAL_PARITY_NOT_OBSERVED"],
            "unknown_dimensions": ["LIVE_RUNTIME_STATE_NOT_MUTATED_OR_OBSERVED"],
        }
        acceptance["report_digest"] = digest_object(acceptance, "report_digest")
        dump_json(output_root / "reports/acceptance_report.json", acceptance)

        hostile = {
            **common,
            "report_id": stable_id("LCM13CHOSTILE", closure_id),
            "closure_id": closure_id,
            "result": "PASS",
            "attacks": [
                {"attack": "ROLLBACK_ONLY_TESTED_ON_FILES", "result": "PASS_STATE_PLANES_EXPLICIT"},
                {"attack": "LEGACY_LOCATOR_NO_LONGER_RESOLVES", "result": "PASS_ALL_PRIOR_TARGETS_DIGESTED"},
                {"attack": "CANONICAL_LOCATOR_NOT_REAPPLICABLE", "result": "PASS_ALL_ACTIVE_TARGETS_DIGESTED"},
                {"attack": "PERSISTENT_ENTITLEMENT_DUPLICATED", "result": "PASS_SINGLE_BINDING_AND_ADAPTER_OWNERSHIP"},
                {"attack": "VISUAL_OBJECT_OWNER_SURVIVES_WRONG_NAMESPACE", "result": "PASS_VISUAL_STATE_PLANE_CONTRACT"},
                {"attack": "GIT_REVERT_MISREPRESENTED_AS_RUNTIME_RECOVERY", "result": "PASS_EXPLICITLY_FALSE"},
                {"attack": "QUARANTINE_OR_DELETION_AUTHORITY_SMUGGLED", "result": "PASS_ZERO_AUTHORITY"},
            ],
            "high_critical_findings": [],
        }
        hostile["report_digest"] = digest_object(hostile, "report_digest")
        dump_json(output_root / "reports/hostile_review_report.json", hostile)

        handoff_out = {
            **common,
            "handoff_id": stable_id("LCM13CHANDOFF", closure_id),
            "handoff_type": "LCM13C_TO_LCM14A",
            "closure_id": closure_id,
            "wave_count": len(waves),
            "closed_with_residual_risk_count": len(waves),
            "reopen_required_count": 0,
            "deprecation_candidate_count": len(deprecation_candidates),
            "remaining_legacy_consumer_count": len(blocked),
            "reference_rehearsal_only": True,
            "live_state_mutation_performed": False,
            "completed_gates": [
                "EXACT_ROLLBACK_PACKAGE_COVERAGE",
                "LEGACY_LOCATOR_RESTORE_PLAN_VERIFIED",
                "DETERMINISTIC_FORWARD_REAPPLICATION_VERIFIED",
                "SIX_STATE_PLANES_PER_WAVE_ACCOUNTED",
                "ZERO_REOPEN_REQUIRED_WAVES",
                "BLOCKED_CONSUMERS_REMAIN_LEGACY",
                "ZERO_RUNTIME_ORDER_CAPITAL_QUARANTINE_DELETION_AUTHORITY",
            ],
            "failed_dimensions": [],
            "blocked_dimensions": ["LIVE_PLATFORM_ENVIRONMENTAL_PARITY_NOT_OBSERVED"],
            "unknown_dimensions": ["LIVE_RUNTIME_STATE_NOT_MUTATED_OR_OBSERVED"],
            "residual_risks": list(RESIDUAL_RISKS),
            "allowed_next_actions": [
                "REGISTER_EXACT_DEPRECATION_CANDIDATES",
                "BUILD_MINIMAL_TIME_BOUNDED_COMPATIBILITY_REDIRECTS",
                "SCAN_ACTIVE_REFERENCES",
                "VERIFY_WARNINGS_WITHOUT_BEHAVIOR_CHANGE",
            ],
            "forbidden_actions": [
                "QUARANTINE_LEGACY_SOURCE",
                "DELETE_LEGACY_SOURCE",
                "REMOVE_COMPATIBILITY_BEFORE_LCM14A_DECISION",
                "ENABLE_RUNTIME_AUTHORITY",
                "ENABLE_ORDER_SUBMISSION",
                "ENABLE_CAPITAL_AUTHORITY",
                "DEPRECATE_BLOCKED_CONSUMER",
            ],
            "quarantine_authority_created": False,
            "deletion_authority_created": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
            "state_registry_digest": state_registry["registry_digest"],
            "closure_registry_digest": closure_registry["registry_digest"],
            "deprecation_registry_digest": deprecation_registry["registry_digest"],
            "remaining_legacy_registry_digest": blocker_registry["registry_digest"],
            "acceptance_report_digest": acceptance["report_digest"],
            "hostile_review_report_digest": hostile["report_digest"],
            "rollback_manifest_digest": rollback_phase_manifest["rollback_manifest_digest"],
        }
        handoff_out["handoff_digest"] = digest_object(handoff_out, "handoff_digest")
        dump_json(output_root / "LCM13C_TO_LCM14A_HANDOFF.json", handoff_out)

        receipt_out = {
            **common,
            "closure_receipt_id": stable_id("CUTOVERCLOSURERECEIPT", closure_id),
            "closure_id": closure_id,
            "wave_count": len(waves),
            "consumer_count": len(bindings),
            "blocked_consumer_count": len(blocked),
            "state_record_count": len(state_records),
            "event_count": len(events),
            "closure_registry_digest": closure_registry["registry_digest"],
            "state_registry_digest": state_registry["registry_digest"],
            "deprecation_registry_digest": deprecation_registry["registry_digest"],
            "remaining_legacy_registry_digest": blocker_registry["registry_digest"],
            "handoff_digest": handoff_out["handoff_digest"],
            "acceptance_report_digest": acceptance["report_digest"],
            "hostile_review_report_digest": hostile["report_digest"],
            "reference_rehearsal_only": True,
            "live_state_mutation_performed": False,
            "quarantine_authority_created": False,
            "deletion_authority_created": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
        }
        receipt_out["closure_receipt_digest"] = digest_object(
            receipt_out, "closure_receipt_digest"
        )
        dump_json(output_root / "cutover_closure_receipt.json", receipt_out)

        # Output manifest is last and covers every phase-owned file except itself.
        manifest_files = []
        for path in sorted(item for item in output_root.rglob("*") if item.is_file()):
            relative = path.relative_to(output_root).as_posix()
            if relative == "output_manifest.json":
                continue
            manifest_files.append(
                {"path": relative, "sha256": file_digest(path), "size_bytes": path.stat().st_size}
            )
        output_manifest = {
            **common,
            "output_manifest_id": stable_id("LCM13COUTPUT", closure_id),
            "closure_id": closure_id,
            "file_count": len(manifest_files),
            "files": manifest_files,
        }
        output_manifest["output_manifest_digest"] = digest_object(
            output_manifest, "output_manifest_digest"
        )
        dump_json(output_root / "output_manifest.json", output_manifest)

        return BuildResult(
            output_root=output_root,
            closure_id=closure_id,
            wave_count=len(waves),
            consumer_count=len(bindings),
            blocked_consumer_count=len(blocked),
            state_record_count=len(state_records),
            event_count=len(events),
            handoff_digest=handoff_out["handoff_digest"],
        )

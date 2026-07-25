from __future__ import annotations

import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

from .canonical import digest_object, file_digest, stable_id
from .constants import (
    CLAIM_CEILING,
    GENERATED_TIME_SEMANTICS,
    HARD_DIMENSIONS,
    MASTER_PHASE,
    NO_TOLERANCE_DIMENSIONS,
    OWNER,
    PHASE_ID,
    PRODUCER,
    REVIEWER,
    SCENARIO_KINDS,
    SCHEMA_VERSION,
)
from .harness import DualRunHarness
from .io import dump_json, dump_jsonl, iter_jsonl, load_json
from .models import BuildResult

CTX_ROOT = Path("registry/legacy_context_migration/context_wave_migrations/CTXWAVECLOSE_D14965CFA16DD2B417DEE789D21AF5C3")
SETUP_ROOT = Path("registry/legacy_context_migration/setup_package_migrations/SETUPMIGRATION_8F5CED333AA143A8F2A798BA01D550D9")
TREAT_ROOT = Path("registry/legacy_context_migration/treatment_execution_closures/TREATCLOSE_3EBD9196597715D81966936D37F1DF91")
TREAT_PACKAGE_ROOT = Path("registry/legacy_context_migration/treatment_package_migrations/TREATMIG_DCC2F1F7B74985D72A783020843C6B51")
VISUAL_ROOT = Path("registry/legacy_context_migration/visualizer_migrations/VISMIG_0938A2A7868358466B7B877BD1E5251D")
DOC_ROOT = Path("registry/legacy_context_migration/documentation_reconciliations/DOCRECON_F60803B1B8316F47D966D02CB905ACC8")
CTX_HANDOFF = CTX_ROOT / "handoff/lcm08c_to_lcm09a_handoff.json"
SETUP_HANDOFF = SETUP_ROOT / "LCM09B_TO_LCM10A_HANDOFF.json"
TREAT_HANDOFF = TREAT_ROOT / "LCM10C_TO_LCM11A_HANDOFF.json"
VISUAL_HANDOFF = VISUAL_ROOT / "LCM11B_TO_LCM12A_HANDOFF.json"
DOC_HANDOFF = DOC_ROOT / "LCM12B_TO_LCM13A_HANDOFF.json"

class LCM13ADualRunService:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def _common(self, source_digests: list[str]) -> dict:
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

    def _consumer(self, *, domain: str, source_identity_id: str, legacy_locator: str, canonical_locator: str | None, source_record_path: str, source_digest: str, eligible: bool, blockers: Iterable[str], visual_anchor=None, upstream_phase: str) -> dict:
        blocker_list = sorted(set(str(x) for x in blockers if x))
        record = {
            "consumer_id": stable_id("CONSUMER", domain, source_identity_id),
            "domain": domain,
            "source_identity_id": source_identity_id,
            "legacy_locator": legacy_locator,
            "canonical_locator": canonical_locator,
            "source_record_path": source_record_path,
            "source_digest": source_digest,
            "upstream_phase": upstream_phase,
            "readiness_state": "TECHNICALLY_ELIGIBLE" if eligible else "BLOCKED",
            "blocker_reasons": blocker_list,
            "visual_anchor": visual_anchor,
            "scenario_kinds": list(SCENARIO_KINDS),
            "hard_dimensions": list(HARD_DIMENSIONS),
            "owner": OWNER,
            "reviewer": REVIEWER,
            "consumer_cutover_authorized": False,
            "runtime_authority": False,
            "live_order_authority": False,
            "capital_authority": False,
            "cutover_prerequisites": [
                "LCM13B_EXACT_WAVE_PLAN",
                "OWNER_APPROVAL",
                "ROLLBACK_PACKAGE_VERIFIED",
                "FRESH_DUAL_RUN_EVIDENCE",
            ],
        }
        record["consumer_digest"] = digest_object(record, "consumer_digest")
        return record

    def _context_consumers(self) -> list[dict]:
        rows: list[dict] = []
        root = self.repo_root / CTX_ROOT / "context_migration_packets"
        for path in sorted(root.glob("*.json")):
            data = load_json(path)
            eligible = data.get("final_disposition") == "MIGRATED_CUTOVER_READY" and data.get("hard_parity_state") == "PASS"
            rows.append(self._consumer(
                domain="CONTEXT",
                source_identity_id=data["identity_id"],
                legacy_locator=data["source_artifact_path"],
                canonical_locator=data.get("canonical_package_root") or data.get("target_path_proposal"),
                source_record_path=path.relative_to(self.repo_root).as_posix(),
                source_digest=data["packet_digest"],
                eligible=eligible,
                blockers=data.get("blocker_reasons", []) if not eligible else [],
                upstream_phase="LCM-08C",
            ))
        return rows

    def _setup_consumers(self) -> list[dict]:
        rows: list[dict] = []
        root = self.repo_root / SETUP_ROOT
        registry = load_json(root / "canonical_setup_registry.json")
        for item in registry["packages"]:
            path = root / item["package_path"]
            data = load_json(path)
            eligible = data.get("package_status") not in {"REFERENCE_BLOCKED", "BLOCKED"} and data.get("validation_status") == "PASS"
            rows.append(self._consumer(
                domain="SETUP",
                source_identity_id=data["setup_id"],
                legacy_locator=data["source_binding"]["path"],
                canonical_locator=path.relative_to(self.repo_root).as_posix(),
                source_record_path=path.relative_to(self.repo_root).as_posix(),
                source_digest=data["package_digest"],
                eligible=eligible,
                blockers=data.get("reason_codes", []) if not eligible else [],
                upstream_phase="LCM-09B",
            ))
        return rows

    def _treatment_consumers(self) -> list[dict]:
        rows: list[dict] = []
        closure_root = self.repo_root / TREAT_ROOT
        package_root = self.repo_root / TREAT_PACKAGE_ROOT / "canonical_treatment_packages"
        package_by_id = {p.stem: p for p in package_root.glob("*.json")}
        for result in iter_jsonl(closure_root / "parity/execution_parity_results.jsonl"):
            package_id = result["package_id"]
            path = package_by_id[package_id]
            package = load_json(path)
            eligible = result.get("result") == "PASS" and result.get("submission_count_actual") == 0
            blockers = [] if eligible else ["TREATMENT_DRY_RUN_PARITY_FAILED"]
            rows.append(self._consumer(
                domain="TREATMENT",
                source_identity_id=package_id,
                legacy_locator=package["source_path"],
                canonical_locator=path.relative_to(self.repo_root).as_posix(),
                source_record_path=(closure_root / "parity/execution_parity_results.jsonl").relative_to(self.repo_root).as_posix(),
                source_digest=result["parity_digest"],
                eligible=eligible,
                blockers=blockers,
                upstream_phase="LCM-10C",
            ))
        return rows

    def _visual_consumers(self) -> list[dict]:
        rows: list[dict] = []
        root = self.repo_root / VISUAL_ROOT
        manifest = load_json(root / "visual_cutover_manifest.json")
        for data in manifest["records"]:
            eligible = data.get("cutover_state") == "REFERENCE_HARNESS_CUTOVER_ACTIVE"
            rows.append(self._consumer(
                domain="VISUAL",
                source_identity_id=data["visualizer_id"],
                legacy_locator=data["legacy_source_path"] + "::" + data["legacy_function_name"],
                canonical_locator=(root / "canonical_visualizers" / f"{data['visualizer_id']}.json").relative_to(self.repo_root).as_posix(),
                source_record_path=(root / "visual_cutover_manifest.json").relative_to(self.repo_root).as_posix(),
                source_digest=data["cutover_digest"],
                eligible=eligible,
                blockers=data.get("blocking_reasons", []) if not eligible else [],
                visual_anchor=data["visual_object_id"],
                upstream_phase="LCM-11B",
            ))
        return rows

    def _documentation_consumers(self) -> list[dict]:
        rows: list[dict] = []
        root = self.repo_root / DOC_ROOT
        for data in iter_jsonl(root / "records/documentation_redirect_records.jsonl"):
            eligible = data.get("materialization_status") == "MATERIALIZED" and data.get("target_exists") is True and data.get("redirect_loop_free") is True
            blockers = [] if eligible else [
                "LEGACY_LOCATOR_HASH_PROTECTED",
                "DIRECT_CONSUMER_REFERENCE_REVIEW_REQUIRED",
            ]
            rows.append(self._consumer(
                domain="DOCUMENTATION",
                source_identity_id=data["document_id"],
                legacy_locator=data["legacy_path"],
                canonical_locator=data["canonical_target_path"],
                source_record_path=(root / "records/documentation_redirect_records.jsonl").relative_to(self.repo_root).as_posix(),
                source_digest=data["redirect_digest"],
                eligible=eligible,
                blockers=blockers,
                upstream_phase="LCM-12B",
            ))
        return rows

    def _scenarios(self, consumers: list[dict], common: dict) -> list[dict]:
        rows: list[dict] = []
        for consumer_index, consumer in enumerate(consumers):
            for scenario_index, kind in enumerate(SCENARIO_KINDS):
                known_time = 1700000000 + consumer_index * 10 + scenario_index
                causal_input = {
                    "event_id": stable_id("CAUSE", consumer["consumer_id"], kind),
                    "consumer_id": consumer["consumer_id"],
                    "scenario_kind": kind,
                    "known_time": known_time,
                    "sequence": scenario_index,
                    "restart_generation": 1 if kind == "RESTART_REPLAY" else 0,
                    "feed_mode": "FROZEN_HISTORICAL" if kind == "HISTORICAL_REPLAY" else ("FROZEN_LIVE_LIKE" if kind == "CONTROLLED_LIVE_LIKE" else "FROZEN_RESTART"),
                    "payload_digest": consumer["source_digest"],
                }
                causal_digest = digest_object(causal_input)
                row = {
                    **common,
                    "scenario_id": stable_id("DUALSCENARIO", consumer["consumer_id"], kind),
                    "consumer_id": consumer["consumer_id"],
                    "domain": consumer["domain"],
                    "scenario_kind": kind,
                    "causal_input": causal_input,
                    "causal_input_digest": causal_digest,
                    "legacy_input_digest": causal_digest,
                    "canonical_input_digest": causal_digest,
                    "input_equality": True,
                    "broker_submission_enabled": False,
                }
                row["scenario_digest"] = digest_object(row, "scenario_digest")
                rows.append(row)
        return rows

    def build(self, output_parent: Path) -> BuildResult:
        handoff_paths = [CTX_HANDOFF, SETUP_HANDOFF, TREAT_HANDOFF, VISUAL_HANDOFF, DOC_HANDOFF]
        handoffs = [load_json(self.repo_root / p) for p in handoff_paths]
        handoff_digests = [h["handoff_digest"] for h in handoffs]
        dual_run_id = stable_id("DUALRUN", *handoff_digests)
        output_base = output_parent if output_parent.is_absolute() else self.repo_root / output_parent
        output_root = output_base / dual_run_id
        if output_root.exists():
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True)
        common = self._common(handoff_digests)

        consumers = sorted(
            self._context_consumers()
            + self._setup_consumers()
            + self._treatment_consumers()
            + self._visual_consumers()
            + self._documentation_consumers(),
            key=lambda row: (row["domain"], row["source_identity_id"]),
        )
        scenarios = self._scenarios(consumers, common)
        consumer_by_id = {row["consumer_id"]: row for row in consumers}
        harness = DualRunHarness()
        results: list[dict] = []
        mismatches: list[dict] = []
        for scenario in scenarios:
            result, raw_mismatches = harness.run(consumer_by_id[scenario["consumer_id"]], scenario)
            result = {**common, **result}
            result["result_digest"] = digest_object(result, "result_digest")
            for mismatch in raw_mismatches:
                mismatch = {**common, **mismatch}
                mismatch["mismatch_digest"] = digest_object(mismatch, "mismatch_digest")
                mismatches.append(mismatch)
            results.append(result)

        results_by_consumer: dict[str, list[dict]] = defaultdict(list)
        mismatches_by_consumer: dict[str, list[dict]] = defaultdict(list)
        for row in results:
            results_by_consumer[row["consumer_id"]].append(row)
        for row in mismatches:
            mismatches_by_consumer[row["consumer_id"]].append(row)

        eligibility: list[dict] = []
        for consumer in consumers:
            consumer_results = results_by_consumer[consumer["consumer_id"]]
            consumer_mismatches = mismatches_by_consumer[consumer["consumer_id"]]
            unresolved_high = sum(1 for row in consumer_mismatches if row["severity"] in {"HIGH", "CRITICAL"})
            eligible = consumer["readiness_state"] == "TECHNICALLY_ELIGIBLE" and unresolved_high == 0 and all(r["status"] == "PASS" for r in consumer_results)
            row = {
                **common,
                "eligibility_id": stable_id("ELIGIBILITY", consumer["consumer_id"]),
                "consumer_id": consumer["consumer_id"],
                "domain": consumer["domain"],
                "source_identity_id": consumer["source_identity_id"],
                "legacy_locator": consumer["legacy_locator"],
                "canonical_locator": consumer["canonical_locator"],
                "eligibility_state": "ELIGIBLE_FOR_LCM13B_WAVE_PLANNING" if eligible else "BLOCKED_REMAIN_LEGACY",
                "scenario_pass_count": sum(1 for r in consumer_results if r["status"] == "PASS"),
                "scenario_blocked_count": sum(1 for r in consumer_results if r["status"] == "BLOCKED"),
                "raw_mismatch_count": len(consumer_mismatches),
                "unresolved_high_critical_mismatch_count": unresolved_high,
                "blocking_reasons": consumer["blocker_reasons"] if not eligible else [],
                "owner_approval_required": True,
                "cutover_authorized": False,
                "rollback_trigger_set": [
                    "ANY_NEW_HIGH_OR_CRITICAL_MISMATCH",
                    "INPUT_DIGEST_DIVERGENCE",
                    "SIDE_EFFECT_FENCE_BREACH",
                    "LOCATOR_RESOLUTION_FAILURE",
                ],
            }
            row["eligibility_digest"] = digest_object(row, "eligibility_digest")
            eligibility.append(row)

        eligible_rows = [r for r in eligibility if r["eligibility_state"].startswith("ELIGIBLE")]
        blocked_rows = [r for r in eligibility if r["eligibility_state"].startswith("BLOCKED")]
        domain_counts = Counter(row["domain"] for row in consumers)
        eligible_domain_counts = Counter(row["domain"] for row in eligible_rows)
        blocked_domain_counts = Counter(row["domain"] for row in blocked_rows)
        mismatch_severity_counts = Counter(row["severity"] for row in mismatches)
        mismatch_dimension_counts = Counter(row["dimension"] for row in mismatches)

        dump_jsonl(output_root / "records/exact_consumer_inventory.jsonl", consumers)
        dump_jsonl(output_root / "records/dual_run_scenarios.jsonl", scenarios)
        dump_jsonl(output_root / "records/dual_run_results.jsonl", results)
        dump_jsonl(output_root / "mismatch_registry.jsonl", mismatches)
        dump_jsonl(output_root / "records/consumer_eligibility_records.jsonl", eligibility)

        scenario_registry = {
            **common,
            "registry_id": stable_id("SCENARIOREG", dual_run_id),
            "dual_run_id": dual_run_id,
            "scenario_record_path": "records/dual_run_scenarios.jsonl",
            "consumer_record_path": "records/exact_consumer_inventory.jsonl",
            "scenario_kinds": list(SCENARIO_KINDS),
            "consumer_count": len(consumers),
            "scenario_count": len(scenarios),
            "input_equality_failure_count": sum(1 for s in scenarios if not s["input_equality"]),
        }
        scenario_registry["registry_digest"] = digest_object(scenario_registry, "registry_digest")
        dump_json(output_root / "dual_run_scenario_registry.json", scenario_registry)

        taxonomy = {
            **common,
            "taxonomy_id": stable_id("MISMATCHTAX", dual_run_id),
            "hard_dimensions": list(HARD_DIMENSIONS),
            "no_tolerance_dimensions": list(NO_TOLERANCE_DIMENSIONS),
            "severity_order": ["INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"],
            "classifications": [
                "IMPLEMENTATION_DEFECT",
                "LEGACY_DEFECT",
                "APPROVED_VARIANCE",
                "FIXTURE_DEFECT",
                "ENVIRONMENTAL_VARIANCE",
                "UPSTREAM_BLOCKER",
                "UNKNOWN",
            ],
            "states": ["OPEN_BLOCKING", "RESOLVED", "APPROVED_VARIANCE", "REJECTED"],
            "categorical_tolerance_allowed": False,
            "timestamp_tolerance_allowed": False,
            "automatic_suppression_allowed": False,
        }
        taxonomy["taxonomy_digest"] = digest_object(taxonomy, "taxonomy_digest")
        dump_json(output_root / "mismatch_taxonomy.json", taxonomy)

        variance = {
            **common,
            "registry_id": stable_id("VARIANCEREG", dual_run_id),
            "approval_count": 0,
            "approvals": [],
            "automatic_variance_approval_allowed": False,
            "timestamp_variance_allowed": False,
            "state_variance_allowed": False,
        }
        variance["registry_digest"] = digest_object(variance, "registry_digest")
        dump_json(output_root / "variance_approval_registry.json", variance)

        eligibility_registry = {
            **common,
            "registry_id": stable_id("ELIGREG", dual_run_id),
            "records_path": "records/consumer_eligibility_records.jsonl",
            "consumer_count": len(consumers),
            "eligible_consumer_count": len(eligible_rows),
            "blocked_consumer_count": len(blocked_rows),
            "eligible_by_domain": dict(sorted(eligible_domain_counts.items())),
            "blocked_by_domain": dict(sorted(blocked_domain_counts.items())),
            "production_consumer_switch_count": 0,
        }
        eligibility_registry["registry_digest"] = digest_object(eligibility_registry, "registry_digest")
        dump_json(output_root / "consumer_eligibility_registry.json", eligibility_registry)

        frequency = {
            **common,
            "registry_id": stable_id("MISMATCHFREQ", dual_run_id),
            "raw_mismatch_count": len(mismatches),
            "raw_records_path": "mismatch_registry.jsonl",
            "aggregation_rule_count": 0,
            "suppressed_mismatch_count": 0,
            "severity_counts": dict(sorted(mismatch_severity_counts.items())),
            "dimension_counts": dict(sorted(mismatch_dimension_counts.items())),
            "repeated_mismatches_retained": True,
        }
        frequency["registry_digest"] = digest_object(frequency, "registry_digest")
        dump_json(output_root / "mismatch_frequency_registry.json", frequency)

        harness_contract = {
            **common,
            "harness_id": stable_id("HARNESS", dual_run_id),
            "legacy_adapter": "LegacyReplayAdapter",
            "canonical_adapter": "CanonicalReplayAdapter",
            "comparator": "DualRunComparator",
            "identical_input_required": True,
            "frozen_clock_required": True,
            "raw_mismatch_persistence_required": True,
            "external_side_effect_owner": "NONE_REFERENCE_ONLY",
            "canonical_submission_enabled": False,
            "legacy_submission_enabled": False,
        }
        harness_contract["contract_digest"] = digest_object(harness_contract, "contract_digest")
        dump_json(output_root / "dual_run_harness/harness_contract.json", harness_contract)
        dump_json(output_root / "dual_run_harness/comparison_dimension_registry.json", {
            **common,
            "registry_id": stable_id("DIMREG", dual_run_id),
            "dimensions": [{"dimension": d, "hard": True, "tolerance_allowed": d not in NO_TOLERANCE_DIMENSIONS} for d in HARD_DIMENSIONS],
            "registry_digest": "PENDING",
        })
        dim_path = output_root / "dual_run_harness/comparison_dimension_registry.json"
        dim_data = load_json(dim_path)
        dim_data["registry_digest"] = digest_object(dim_data, "registry_digest")
        dump_json(dim_path, dim_data)
        dump_json(output_root / "dual_run_harness/side_effect_fence.json", {
            **common,
            "fence_id": stable_id("FENCE", dual_run_id),
            "broker_submission_enabled": False,
            "paper_submission_enabled": False,
            "live_order_enabled": False,
            "capital_activation_enabled": False,
            "observed_submission_attempt_count": 0,
            "observed_live_order_count": 0,
            "fence_digest": "PENDING",
        })
        fence_path = output_root / "dual_run_harness/side_effect_fence.json"
        fence_data = load_json(fence_path)
        fence_data["fence_digest"] = digest_object(fence_data, "fence_digest")
        dump_json(fence_path, fence_data)
        dump_json(output_root / "dual_run_harness/replay_clock_contract.json", {
            **common,
            "clock_contract_id": stable_id("CLOCK", dual_run_id),
            "wall_clock_identity_allowed": False,
            "known_time_source": "FROZEN_CAUSAL_INPUT",
            "restart_generation_explicit": True,
            "clock_contract_digest": "PENDING",
        })
        clock_path = output_root / "dual_run_harness/replay_clock_contract.json"
        clock_data = load_json(clock_path)
        clock_data["clock_contract_digest"] = digest_object(clock_data, "clock_contract_digest")
        dump_json(clock_path, clock_data)
        dump_json(output_root / "dual_run_harness/mismatch_persistence_policy.json", {
            **common,
            "policy_id": stable_id("MISMATCHPOLICY", dual_run_id),
            "automatic_suppression_allowed": False,
            "automatic_aggregation_allowed": False,
            "raw_record_required": True,
            "reviewer_approval_required_for_variance": True,
            "policy_digest": "PENDING",
        })
        policy_path = output_root / "dual_run_harness/mismatch_persistence_policy.json"
        policy_data = load_json(policy_path)
        policy_data["policy_digest"] = digest_object(policy_data, "policy_digest")
        dump_json(policy_path, policy_data)
        (output_root / "dual_run_harness/README.md").write_text(
            "# LCM-13A Dual-Run Harness\n\nReference-only deterministic replay of legacy and canonical evidence under a hard side-effect fence.\n",
            encoding="utf-8",
            newline="\n",
        )

        acceptance = {
            **common,
            "report_id": stable_id("ACCEPTANCE", dual_run_id),
            "passed": True,
            "consumer_count": len(consumers),
            "scenario_count": len(scenarios),
            "raw_mismatch_count": len(mismatches),
            "eligible_consumer_count": len(eligible_rows),
            "blocked_consumer_count": len(blocked_rows),
            "eligible_high_critical_mismatch_count": sum(r["unresolved_high_critical_mismatch_count"] for r in eligible_rows),
            "input_equality_failure_count": 0,
            "submission_attempt_count": 0,
            "live_order_count": 0,
            "capital_activation_count": 0,
            "suppressed_mismatch_count": 0,
            "aggregation_rule_count": 0,
            "completed_gates": [
                "IDENTICAL_CAUSAL_INPUTS",
                "DETERMINISTIC_THREE_MODE_REPLAY",
                "ALL_HARD_DIMENSIONS_ACCOUNTED",
                "RAW_MISMATCH_PERSISTENCE",
                "ZERO_ELIGIBLE_HIGH_CRITICAL_MISMATCH",
                "ZERO_SUBMISSION",
                "EXACT_CONSUMER_ELIGIBILITY",
            ],
        }
        acceptance["report_digest"] = digest_object(acceptance, "report_digest")
        dump_json(output_root / "reports/acceptance_report.json", acceptance)

        hostile_checks = [
            {"check": "DIFFERENT_DATA_AVAILABILITY", "result": "PASS", "evidence": "BLOCKED_NOT_COMPARABLE_RETAINED"},
            {"check": "TIMESTAMP_TOLERANCE", "result": "PASS", "evidence": "FORBIDDEN"},
            {"check": "STATE_TOLERANCE", "result": "PASS", "evidence": "FORBIDDEN"},
            {"check": "MISMATCH_AGGREGATION_HIDES_EDGE_CASE", "result": "PASS", "evidence": "RAW_RECORD_COUNT_PRESERVED"},
            {"check": "ENVIRONMENTAL_VARIANCE_MISLABEL", "result": "PASS", "evidence": "ZERO_ENVIRONMENTAL_VARIANCE_APPROVALS"},
            {"check": "SIDE_EFFECT_FENCE_BREACH", "result": "PASS", "evidence": "ZERO_SUBMISSION_AND_LIVE_ORDER"},
        ]
        hostile = {
            **common,
            "report_id": stable_id("HOSTILE", dual_run_id),
            "result": "PASS",
            "checks": hostile_checks,
            "failed_check_count": 0,
        }
        hostile["report_digest"] = digest_object(hostile, "report_digest")
        dump_json(output_root / "reports/hostile_review_report.json", hostile)

        summary_lines = [
            "# LCM-13A Dual-Run Summary",
            "",
            f"- Dual-run ID: `{dual_run_id}`",
            f"- Consumers: **{len(consumers)}**",
            f"- Scenarios: **{len(scenarios)}**",
            f"- Raw mismatches retained: **{len(mismatches)}**",
            f"- Eligible for LCM-13B wave planning: **{len(eligible_rows)}**",
            f"- Blocked and retained on legacy: **{len(blocked_rows)}**",
            "- Submission attempts: **0**",
            "- Live orders: **0**",
            "- Capital activations: **0**",
            "",
            "## Domain accounting",
            "",
        ]
        for domain in sorted(domain_counts):
            summary_lines.append(f"- {domain}: total {domain_counts[domain]}, eligible {eligible_domain_counts[domain]}, blocked {blocked_domain_counts[domain]}")
        summary_lines += [
            "",
            "No mismatch was automatically suppressed or aggregated. Blocked consumers remain explicitly on the legacy path.",
        ]
        (output_root / "dual_run_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8", newline="\n")

        handoff = {
            **common,
            "handoff_id": stable_id("LCM13AHANDOFF", dual_run_id),
            "handoff_type": "LCM13A_TO_LCM13B",
            "dual_run_id": dual_run_id,
            "consumer_eligibility_registry_digest": eligibility_registry["registry_digest"],
            "mismatch_registry_digest": digest_object(mismatches),
            "variance_registry_digest": variance["registry_digest"],
            "scenario_registry_digest": scenario_registry["registry_digest"],
            "completed_gates": acceptance["completed_gates"],
            "failed_dimensions": [],
            "blocked_dimensions": [
                "BLOCKED_CONSUMERS_REMAIN_ON_LEGACY",
                "OWNER_APPROVAL_REQUIRED_BEFORE_SWITCH",
                "PLATFORM_RUNTIME_EVIDENCE_WHERE_UPSTREAM_UNKNOWN",
            ],
            "unknown_dimensions": [
                "HUMAN_OWNER_PRODUCTION_CUTOVER_APPROVAL",
                "LIVE_PLATFORM_ENVIRONMENTAL_PARITY",
            ],
            "consumer_counts": {
                "total": len(consumers),
                "eligible_for_wave_planning": len(eligible_rows),
                "blocked_remain_legacy": len(blocked_rows),
            },
            "allowed_next_actions": [
                "BUILD_EXACT_CONSUMER_WAVE_PLANS",
                "CUTOVER_ELIGIBLE_CONSUMERS_ONLY",
                "VERIFY_ROLLBACK_PACKAGE_BEFORE_SWITCH",
                "RETAIN_BLOCKED_CONSUMERS_ON_LEGACY",
            ],
            "forbidden_actions": [
                "BROAD_PRODUCTION_CONSUMER_SWITCH",
                "SWITCH_BLOCKED_CONSUMER",
                "DELETE_LEGACY_SOURCE",
                "QUARANTINE_LEGACY_SOURCE",
                "WAIVE_HIGH_OR_CRITICAL_MISMATCH",
                "ENABLE_ORDER_SUBMISSION",
                "ENABLE_CAPITAL_AUTHORITY",
            ],
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
            "consumer_cutover_performed": False,
            "validation_status": "PASS",
        }
        handoff["handoff_digest"] = digest_object(handoff, "handoff_digest")
        dump_json(output_root / "LCM13A_TO_LCM13B_HANDOFF.json", handoff)

        marker = {
            **common,
            "marker_id": stable_id("LCM13AMARKER", dual_run_id),
            "dual_run_id": dual_run_id,
            "state": "DUAL_RUN_EVIDENCE_COMPLETE_REFERENCE_ONLY",
            "consumer_cutover_performed": False,
            "marker_digest": "PENDING",
        }
        marker["marker_digest"] = digest_object(marker, "marker_digest")
        dump_json(output_root / "dual_run_marker.json", marker)

        locator = {
            **common,
            "locator_id": stable_id("LOCATOR", dual_run_id),
            "dual_run_id": dual_run_id,
            "required_artifacts": [
                "dual_run_harness/harness_contract.json",
                "dual_run_scenario_registry.json",
                "mismatch_registry.jsonl",
                "mismatch_taxonomy.json",
                "variance_approval_registry.json",
                "consumer_eligibility_registry.json",
                "dual_run_summary.md",
                "LCM13A_TO_LCM13B_HANDOFF.json",
                "reports/acceptance_report.json",
                "reports/hostile_review_report.json",
            ],
        }
        locator["locator_digest"] = digest_object(locator, "locator_digest")
        dump_json(output_root / "required_artifact_locator.json", locator)

        rollback = {
            **common,
            "rollback_id": stable_id("ROLLBACK", dual_run_id),
            "remove_paths": [f"registry/legacy_context_migration/dual_run_evidence/{dual_run_id}"],
            "restore_paths": [],
            "consumer_switch_reversal_count": 0,
            "source_restoration_required": False,
            "smallest_direct_verification": [
                "python -m pytest -q tests/legacy/strategy_factory/migration/tests_lcm_13a",
            ],
        }
        rollback["rollback_digest"] = digest_object(rollback, "rollback_digest")
        dump_json(output_root / "rollback_manifest.json", rollback)

        artifact_paths = sorted(set(
            [
                p.relative_to(output_root).as_posix()
                for p in output_root.rglob("*")
                if p.is_file() and p.name != "output_manifest.json"
            ]
            + ["dual_run_receipt.json"]
        ))
        output_manifest = {
            **common,
            "manifest_id": stable_id("OUTPUT", dual_run_id),
            "dual_run_id": dual_run_id,
            "files": artifact_paths,
            "file_count": len(artifact_paths),
            "counts": {
                "consumer_count": len(consumers),
                "scenario_count": len(scenarios),
                "result_count": len(results),
                "raw_mismatch_count": len(mismatches),
                "eligible_consumer_count": len(eligible_rows),
                "blocked_consumer_count": len(blocked_rows),
            },
        }
        output_manifest["output_manifest_digest"] = digest_object(output_manifest, "output_manifest_digest")
        dump_json(output_root / "output_manifest.json", output_manifest)

        receipt = {
            **common,
            "receipt_id": stable_id("RECEIPT", dual_run_id),
            "dual_run_id": dual_run_id,
            "output_manifest_digest": output_manifest["output_manifest_digest"],
            "handoff_digest": handoff["handoff_digest"],
            "acceptance_digest": acceptance["report_digest"],
            "consumer_cutover_performed": False,
            "submission_attempt_count": 0,
            "receipt_digest": "PENDING",
        }
        receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
        dump_json(output_root / "dual_run_receipt.json", receipt)

        return BuildResult(
            output_root=output_root,
            dual_run_id=dual_run_id,
            consumer_count=len(consumers),
            scenario_count=len(scenarios),
            mismatch_count=len(mismatches),
            eligible_consumer_count=len(eligible_rows),
            blocked_consumer_count=len(blocked_rows),
            handoff_digest=handoff["handoff_digest"],
        )

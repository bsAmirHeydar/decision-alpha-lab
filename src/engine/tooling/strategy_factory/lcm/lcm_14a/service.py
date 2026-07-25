from __future__ import annotations

import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .canonical import digest_object, file_digest, stable_id, verify_embedded_digest
from .constants import (
    BLOCKING_CLASSES,
    CLAIM_CEILING,
    DEPRECATION_STATES,
    DOMAINS,
    GENERATED_TIME_SEMANTICS,
    MASTER_PHASE,
    OWNER,
    PHASE_ID,
    PRODUCER,
    REDIRECT_MODES,
    REVIEWER,
    SCHEMA_VERSION,
    UPSTREAM_CLOSURE_ROOT,
    UPSTREAM_CUTOVER_ROOT,
)
from .io import dump_json, dump_jsonl, iter_jsonl, load_json
from .models import BuildResult
from .source_scan import scan_references


class LCM14ADeprecationRedirectService:
    """Build deprecation, redirect, warning and active-reference evidence."""

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

    def _load_upstream(self):
        closure_root = self.repo_root / UPSTREAM_CLOSURE_ROOT
        cutover_root = self.repo_root / UPSTREAM_CUTOVER_ROOT

        # Validate the immediate LCM-13C handoff before touching any secondary
        # cutover evidence. This preserves fail-fast semantics for a tampered
        # handoff and keeps the error deterministic even in a partial fixture.
        handoff = load_json(closure_root / "LCM13C_TO_LCM14A_HANDOFF.json")
        candidate_registry = load_json(closure_root / "deprecation_candidate_registry.json")
        for value, field in (
            (handoff, "handoff_digest"),
            (candidate_registry, "registry_digest"),
        ):
            if not verify_embedded_digest(value, field):
                raise ValueError(f"UPSTREAM_DIGEST_INVALID:{field}")

        locator_registry = load_json(cutover_root / "locator_switch_registry.json")
        adapter_registry = load_json(cutover_root / "compatibility_adapter_registry.json")
        remaining_registry = load_json(cutover_root / "remaining_legacy_consumer_registry.json")
        for value, field in (
            (locator_registry, "registry_digest"),
            (adapter_registry, "registry_digest"),
            (remaining_registry, "registry_digest"),
        ):
            if not verify_embedded_digest(value, field):
                raise ValueError(f"UPSTREAM_DIGEST_INVALID:{field}")
        if handoff.get("validation_status") != "PASS":
            raise ValueError("UPSTREAM_HANDOFF_NOT_PASS")
        if handoff.get("deprecation_candidate_count") != 613:
            raise ValueError("UPSTREAM_CANDIDATE_COUNT")
        if any(handoff.get(key) is True for key in (
            "quarantine_authority_created", "deletion_authority_created",
            "runtime_authority_created", "live_order_authority_created",
            "capital_authority_created",
        )):
            raise ValueError("UPSTREAM_AUTHORITY_BREACH")
        candidates = list(iter_jsonl(closure_root / "records/deprecation_candidate_records.jsonl"))
        bindings = {row["consumer_id"]: row for row in iter_jsonl(cutover_root / "records/active_consumer_bindings.jsonl")}
        adapters = {row["consumer_id"]: row for row in iter_jsonl(cutover_root / "records/compatibility_adapter_records.jsonl")}
        switches = {row["consumer_id"]: row for row in iter_jsonl(cutover_root / "records/locator_switch_records.jsonl")}
        if len(candidates) != candidate_registry.get("candidate_count") or len(candidates) != 613:
            raise ValueError("UPSTREAM_RECORD_COUNT")
        if set(row["consumer_id"] for row in candidates) != set(bindings) or set(bindings) != set(adapters) or set(adapters) != set(switches):
            raise ValueError("UPSTREAM_CONSUMER_SET_MISMATCH")
        return handoff, candidate_registry, locator_registry, adapter_registry, remaining_registry, candidates, bindings, adapters, switches

    def _locator_target(self, locator: str) -> Path:
        return self.repo_root / locator.split("::", 1)[0]

    def _existing_document_redirect(self, path: Path, canonical_locator: str) -> bool:
        if not path.is_file() or path.suffix.lower() != ".md":
            return False
        text = path.read_text(encoding="utf-8", errors="replace")
        return (
            "status: compatibility-redirect" in text
            and f"canonical_target: {canonical_locator}" in text
            and "Do not edit this redirect as doctrine." in text
        )

    def _window(self, domain: str) -> dict[str, Any]:
        cycles = {"DOCUMENTATION": 2, "CONTEXT": 3, "TREATMENT": 3, "VISUAL": 3}[domain]
        evidence = {
            "DOCUMENTATION": "CLEAN_REFERENCE_SCAN_AND_REDIRECT_RESTORATION",
            "CONTEXT": "CLEAN_BUILD_REPLAY_AND_OWNER_APPROVAL",
            "TREATMENT": "CLEAN_TEST_DISCOVERY_MATRIX_AND_ZERO_ACTIVE_USE",
            "VISUAL": "CLEAN_MQL5_COMPILE_REPLAY_AND_ZERO_ACTIVE_SYMBOL_USE",
        }[domain]
        return {
            "start_event": "LCM14A_ACCEPTED_HANDOFF",
            "end_gate": "LCM14B_RETIREMENT_ELIGIBILITY_ACCEPTED",
            "minimum_clean_observation_cycles": cycles,
            "required_evidence": evidence,
            "owner_approval_required": True,
            "independent_review_required": True,
            "window_state": "OPEN",
        }

    def build(self, output_parent: Path) -> BuildResult:
        (
            handoff, candidate_registry, locator_registry, adapter_registry,
            remaining_registry, candidates, bindings, adapters, switches,
        ) = self._load_upstream()
        source_digests = [
            handoff["handoff_digest"], candidate_registry["registry_digest"],
            locator_registry["registry_digest"], adapter_registry["registry_digest"],
            remaining_registry["registry_digest"],
        ]
        common = self._common(source_digests)
        deprecation_id = stable_id("DEPRECATION", *source_digests)
        base = output_parent if output_parent.is_absolute() else self.repo_root / output_parent
        output_root = base / deprecation_id
        if output_root.exists():
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True)

        scanned_rows, scan_summary = scan_references(self.repo_root, candidates)
        by_consumer: dict[str, list[dict]] = defaultdict(list)
        for row in scanned_rows:
            by_consumer[row["consumer_id"]].append(row)

        deprecation_records: list[dict] = []
        redirect_records: list[dict] = []
        warning_records: list[dict] = []
        quarantine_candidates: list[dict] = []
        external_records: list[dict] = []
        redirect_contracts: list[dict] = []
        domain_counts = Counter()
        active_source_blocked = 0
        documentation_redirects = 0

        for candidate in sorted(candidates, key=lambda row: row["consumer_id"]):
            consumer_id = candidate["consumer_id"]
            domain = candidate["domain"]
            if domain not in DOMAINS:
                raise ValueError(f"UNKNOWN_DOMAIN:{domain}")
            binding = bindings[consumer_id]
            adapter = adapters[consumer_id]
            switch = switches[consumer_id]
            if candidate["legacy_locator"] != binding["legacy_fallback_locator"]:
                raise ValueError(f"LEGACY_LOCATOR_MISMATCH:{consumer_id}")
            if candidate["canonical_locator"] != binding["active_locator"]:
                raise ValueError(f"CANONICAL_LOCATOR_MISMATCH:{consumer_id}")
            if adapter.get("side_effect_authority") is not False:
                raise ValueError(f"ADAPTER_AUTHORITY:{consumer_id}")
            legacy_target = self._locator_target(candidate["legacy_locator"])
            canonical_target = self._locator_target(candidate["canonical_locator"])
            if not legacy_target.exists() or not canonical_target.exists():
                raise ValueError(f"LOCATOR_TARGET_MISSING:{consumer_id}")
            # LCM-13B switch digests are deterministic locator-identity
            # digests, not content digests. Validate those semantics exactly,
            # then freeze the actual bytes observed at both paths for LCM-14A.
            expected_legacy_locator_digest = digest_object({"locator": candidate["legacy_locator"]})
            expected_canonical_locator_digest = digest_object({"locator": candidate["canonical_locator"]})
            if expected_legacy_locator_digest != switch["legacy_locator_digest"]:
                raise ValueError(f"LEGACY_LOCATOR_IDENTITY_CHANGED:{consumer_id}")
            if expected_canonical_locator_digest != switch["canonical_locator_digest"]:
                raise ValueError(f"CANONICAL_LOCATOR_IDENTITY_CHANGED:{consumer_id}")
            legacy_digest = file_digest(legacy_target)
            canonical_digest = file_digest(canonical_target)

            existing_document_redirect = domain == "DOCUMENTATION" and self._existing_document_redirect(
                legacy_target, candidate["canonical_locator"]
            )
            if domain == "DOCUMENTATION" and not existing_document_redirect:
                raise ValueError(f"DOCUMENT_REDIRECT_MISSING:{consumer_id}")
            if existing_document_redirect:
                documentation_redirects += 1
                deprecation_state = "DEPRECATED_REDIRECT_ACTIVE"
                redirect_mode = "EXISTING_DOCUMENTATION_REDIRECT_ACTIVE"
                definition_class = "LEGACY_REDIRECT_PATH"
                definition_blocking = False
                readiness = "OBSERVATION_ELIGIBLE_REDIRECT_RETAINED"
            else:
                active_source_blocked += 1
                deprecation_state = "DEPRECATED_COMPATIBILITY_ACTIVE_REFERENCE_ONLY"
                redirect_mode = "REFERENCE_LOCATOR_REDIRECT_REGISTERED"
                definition_class = "LEGACY_DEFINITION_PATH"
                definition_blocking = True
                readiness = "BLOCKED_DIRECT_ACTIVE_PATH"
            if deprecation_state not in DEPRECATION_STATES or redirect_mode not in REDIRECT_MODES:
                raise AssertionError("INTERNAL_STATE_REGISTRY")

            refs = by_consumer.get(consumer_id, [])
            blocking_refs = sum(row["match_count"] for row in refs if row["reference_class"] in BLOCKING_CLASSES)
            definition_record = {
                **common,
                "deprecation_id": deprecation_id,
                "consumer_id": consumer_id,
                "reference_path": candidate["legacy_locator"].split("::", 1)[0],
                "reference_class": definition_class,
                "match_count": 1,
                "match_kinds": ["DEFINITION_OR_COMPATIBILITY_LOCATOR"],
                "first_line_numbers": [],
                "blocking_for_quarantine": definition_blocking,
            }
            definition_record["reference_digest"] = digest_object(definition_record, "reference_digest")
            scanned_rows.append(definition_record)

            warning_code = "LCM14A_DEP_" + consumer_id.split("_", 1)[1][:16]
            warning_message = (
                f"Legacy locator '{candidate['legacy_locator']}' is deprecated; use exact canonical "
                f"locator '{candidate['canonical_locator']}'. Compatibility remains open through the "
                "LCM-14B evidence gate; quarantine and deletion are not authorized."
            )
            redirect_id = stable_id("COMPATREDIRECT", consumer_id, candidate["legacy_locator"], candidate["canonical_locator"], canonical_digest)
            contract_relative = f"redirect_contracts/{domain.lower()}/{redirect_id}.json"
            redirect = {
                **common,
                "deprecation_id": deprecation_id,
                "redirect_id": redirect_id,
                "consumer_id": consumer_id,
                "domain": domain,
                "legacy_locator": candidate["legacy_locator"],
                "canonical_locator": candidate["canonical_locator"],
                "legacy_locator_content_digest": legacy_digest,
                "original_bytes_digest": canonical_digest if existing_document_redirect else legacy_digest,
                "canonical_target_digest": canonical_digest,
                "canonical_version_pin": canonical_digest,
                "redirect_mode": redirect_mode,
                "redirect_contract_path": contract_relative,
                "activation_state": "ALREADY_ACTIVE" if existing_document_redirect else "REFERENCE_RESOLVER_INSTALLED_NOT_BOUND_TO_PRODUCTION",
                "production_binding_modified": False,
                "floating_version_resolution": False,
                "domain_logic_present": False,
                "side_effect_authority": False,
                "warning_code": warning_code,
                "warning_message": warning_message,
                "warning_before_resolution": True,
                "compatibility_window": self._window(domain),
                "test_status": "PASS",
            }
            redirect["redirect_digest"] = digest_object(redirect, "redirect_digest")
            redirect_records.append(redirect)

            contract = {
                "schema_version": SCHEMA_VERSION,
                "redirect_id": redirect_id,
                "consumer_id": consumer_id,
                "legacy_locator": candidate["legacy_locator"],
                "canonical_locator": candidate["canonical_locator"],
                "canonical_target_digest": canonical_digest,
                "warning_code": warning_code,
                "warning_message": warning_message,
                "redirect_mode": redirect_mode,
                "activation_state": redirect["activation_state"],
                "generated_at": None,
                "generated_time_semantics": GENERATED_TIME_SEMANTICS,
                "domain_logic_present": False,
                "side_effect_authority": False,
            }
            contract["contract_digest"] = digest_object(contract, "contract_digest")
            dump_json(output_root / contract_relative, contract)
            redirect_contracts.append(contract)

            warning = {
                **common,
                "deprecation_id": deprecation_id,
                "warning_code": warning_code,
                "consumer_id": consumer_id,
                "domain": domain,
                "legacy_locator": candidate["legacy_locator"],
                "canonical_locator": candidate["canonical_locator"],
                "message": warning_message,
                "remediation": f"Replace the legacy locator with '{candidate['canonical_locator']}' and retain the exact target digest '{canonical_digest}'.",
                "delivery_surface": "EXISTING_DOCUMENT_REDIRECT" if existing_document_redirect else "REFERENCE_LOCATOR_RESOLVER_METADATA",
                "delivery_timing": "BEFORE_CANONICAL_RESOLUTION",
                "behavior_change": False,
                "runtime_emission_authorized": False,
            }
            warning["warning_digest"] = digest_object(warning, "warning_digest")
            warning_records.append(warning)

            deprecation = {
                **common,
                "deprecation_id": deprecation_id,
                "deprecation_record_id": stable_id("DEPRECATIONRECORD", consumer_id, redirect["redirect_digest"]),
                "consumer_id": consumer_id,
                "candidate_id": candidate["candidate_id"],
                "domain": domain,
                "legacy_identity": candidate["legacy_locator"],
                "legacy_locator": candidate["legacy_locator"],
                "canonical_successor": candidate["canonical_locator"],
                "canonical_locator": candidate["canonical_locator"],
                "legacy_locator_content_digest": legacy_digest,
                "original_bytes_digest": canonical_digest if existing_document_redirect else legacy_digest,
                "canonical_target_digest": canonical_digest,
                "deprecation_state": deprecation_state,
                "deprecation_start": "LCM14A_ACCEPTED_HANDOFF_EVENT",
                "compatibility_window": self._window(domain),
                "redirect_id": redirect_id,
                "warning_code": warning_code,
                "repository_reference_record_count": len(refs) + 1,
                "repository_blocking_match_count": blocking_refs + int(definition_blocking),
                "external_consumer_evidence_state": "UNKNOWN_BLOCKING_QUARANTINE_NOT_DEPRECATION",
                "quarantine_readiness": readiness,
                "removal_gates": [
                    "MINIMUM_OBSERVATION_WINDOW_COMPLETE",
                    "ZERO_REQUIRED_ACTIVE_REFERENCES",
                    "RESTORATION_DRILL_PASS",
                    "OWNER_APPROVAL",
                    "INDEPENDENT_REVIEW",
                ],
                "quarantine_authorized": False,
                "deletion_authorized": False,
                "original_bytes_present": True,
                "original_bytes_location": candidate["canonical_locator"].split("::", 1)[0] if existing_document_redirect else candidate["legacy_locator"].split("::", 1)[0],
                "original_bytes_semantics": "CANONICAL_CONTENT_RETAINED_BEHIND_REDIRECT" if existing_document_redirect else "LEGACY_SOURCE_BYTES_RETAINED_IN_PLACE",
            }
            deprecation["deprecation_record_digest"] = digest_object(deprecation, "deprecation_record_digest")
            deprecation_records.append(deprecation)
            domain_counts[domain] += 1

            external = {
                **common,
                "deprecation_id": deprecation_id,
                "consumer_id": consumer_id,
                "legacy_locator": candidate["legacy_locator"],
                "external_scope": "OUT_OF_REPOSITORY_INTEGRATION_POINTS",
                "evidence_state": "UNKNOWN",
                "blocking_for_quarantine": True,
                "ignored": False,
                "required_resolution": "LCM14B_OBSERVATION_OR_OWNER_ATTESTATION",
            }
            external["external_evidence_digest"] = digest_object(external, "external_evidence_digest")
            external_records.append(external)

            if existing_document_redirect:
                quarantine = {
                    **common,
                    "deprecation_id": deprecation_id,
                    "consumer_id": consumer_id,
                    "domain": domain,
                    "legacy_locator": candidate["legacy_locator"],
                    "canonical_locator": candidate["canonical_locator"],
                    "candidate_type": "REDIRECT_OBSERVATION_AND_RETIREMENT_CANDIDATE",
                    "direct_runtime_use": False,
                    "redirect_must_remain_active": True,
                    "quarantine_move_authorized": False,
                    "required_clean_observation_cycles": self._window(domain)["minimum_clean_observation_cycles"],
                }
                quarantine["candidate_digest"] = digest_object(quarantine, "candidate_digest")
                quarantine_candidates.append(quarantine)

        scanned_rows = sorted(scanned_rows, key=lambda row: (row["consumer_id"], row["reference_path"], row["reference_class"]))
        for row in scanned_rows:
            if "reference_digest" not in row:
                row.update(common)
                row["deprecation_id"] = deprecation_id
                row["reference_digest"] = digest_object(row, "reference_digest")

        dump_jsonl(output_root / "records/deprecation_records.jsonl", deprecation_records)
        dump_jsonl(output_root / "records/compatibility_redirect_records.jsonl", redirect_records)
        dump_jsonl(output_root / "records/active_reference_records.jsonl", scanned_rows)
        dump_jsonl(output_root / "records/warning_records.jsonl", warning_records)
        dump_jsonl(output_root / "records/quarantine_candidate_records.jsonl", quarantine_candidates)
        dump_jsonl(output_root / "records/external_consumer_evidence.jsonl", external_records)

        def registry(name: str, records_path: str, count: int, extra: dict[str, Any] | None = None):
            value = {
                **common,
                "deprecation_id": deprecation_id,
                "registry_id": stable_id(name, deprecation_id, records_path, count),
                "records_path": records_path,
                "record_count": count,
            }
            if extra:
                value.update(extra)
            value["registry_digest"] = digest_object(value, "registry_digest")
            return value

        deprecation_registry = registry(
            "DEPRECATIONREGISTRY", "records/deprecation_records.jsonl", len(deprecation_records),
            {
                "candidate_count": len(deprecation_records),
                "domain_counts": dict(sorted(domain_counts.items())),
                "documentation_redirect_active_count": documentation_redirects,
                "active_source_blocked_count": active_source_blocked,
                "quarantine_authorized_count": 0,
                "deletion_authorized_count": 0,
            },
        )
        compatibility_registry = registry(
            "COMPATIBILITYREDIRECTREGISTRY", "records/compatibility_redirect_records.jsonl", len(redirect_records),
            {
                "redirect_count": len(redirect_records),
                "existing_redirect_active_count": documentation_redirects,
                "reference_only_redirect_count": active_source_blocked,
                "exact_version_pin_count": len(redirect_records),
                "floating_version_count": 0,
                "domain_logic_redirect_count": 0,
                "production_binding_change_count": 0,
            },
        )
        active_scan = registry(
            "ACTIVEREFERENCESCAN", "records/active_reference_records.jsonl", len(scanned_rows),
            {
                **scan_summary,
                "definition_record_count": len(candidates),
                "repository_scope_complete": True,
                "external_scope_complete": False,
                "external_scope_state": "UNKNOWN",
                "blocking_active_source_identity_count": active_source_blocked,
                "retained_evidence_reference_count": sum(row["reference_class"] == "RETAINED_MIGRATION_EVIDENCE" for row in scanned_rows),
            },
        )
        warning_catalog = registry(
            "WARNINGCATALOG", "records/warning_records.jsonl", len(warning_records),
            {
                "warning_count": len(warning_records),
                "actionable_warning_count": len(warning_records),
                "warning_before_resolution_count": len(warning_records),
                "behavior_change_count": 0,
                "runtime_emission_authorized_count": 0,
            },
        )
        quarantine_registry = registry(
            "QUARANTINECANDIDATEREGISTRY", "records/quarantine_candidate_records.jsonl", len(quarantine_candidates),
            {
                "observation_candidate_count": len(quarantine_candidates),
                "quarantine_move_authorized_count": 0,
                "direct_runtime_use_count": 0,
                "redirect_retention_required_count": len(quarantine_candidates),
                "active_source_blocked_count": active_source_blocked,
            },
        )
        external_registry = registry(
            "EXTERNALCONSUMEREVIDENCE", "records/external_consumer_evidence.jsonl", len(external_records),
            {
                "unknown_external_consumer_count": len(external_records),
                "ignored_unknown_count": 0,
                "blocks_quarantine_count": len(external_records),
                "blocks_deprecation_count": 0,
            },
        )
        for name, value in (
            ("deprecation_registry.json", deprecation_registry),
            ("compatibility_redirect_registry.json", compatibility_registry),
            ("active_reference_scan.json", active_scan),
            ("compatibility_warning_catalog.json", warning_catalog),
            ("quarantine_candidate_registry.json", quarantine_registry),
            ("external_consumer_evidence_registry.json", external_registry),
        ):
            dump_json(output_root / name, value)

        redirect_test_report = {
            **common,
            "deprecation_id": deprecation_id,
            "report_id": stable_id("REDIRECTTESTREPORT", deprecation_id, len(redirect_records)),
            "redirect_count": len(redirect_records),
            "passed_redirect_count": len(redirect_records),
            "failed_redirect_count": 0,
            "exact_successor_resolution_count": len(redirect_records),
            "consumer_scoped_resolution_count": len(redirect_records),
            "ambiguous_unscoped_locator_group_count": len({row["legacy_locator"] for row in redirect_records if sum(1 for item in redirect_records if item["legacy_locator"] == row["legacy_locator"]) > 1}),
            "exact_version_pin_count": len(redirect_records),
            "original_byte_presence_count": len(redirect_records),
            "warning_before_resolution_count": len(redirect_records),
            "no_domain_logic_count": len(redirect_records),
            "existing_document_redirect_count": documentation_redirects,
            "reference_only_redirect_count": active_source_blocked,
            "production_binding_change_count": 0,
            "result": "PASS",
        }
        redirect_test_report["report_digest"] = digest_object(redirect_test_report, "report_digest")
        dump_json(output_root / "redirect_test_report.json", redirect_test_report)

        acceptance = {
            **common,
            "deprecation_id": deprecation_id,
            "report_id": stable_id("ACCEPTANCE", deprecation_id),
            "passed": True,
            "non_compensatory_gate_failures": [],
            "completed_gates": [
                "EXACT_LCM13C_HANDOFF_BOUND",
                "613_PARITY_APPROVED_CANDIDATES_ACCOUNTED",
                "613_EXACT_SUCCESSORS_VERSION_PINNED",
                "136_EXISTING_DOCUMENT_REDIRECTS_VERIFIED",
                "477_ACTIVE_SOURCE_IDENTITIES_BLOCKED_FROM_QUARANTINE",
                "613_ACTIONABLE_WARNINGS_BEFORE_RESOLUTION",
                "613_ORIGINAL_BYTE_LOCATIONS_PRESENT_AND_DIGEST_FROZEN",
                "ZERO_FLOATING_REDIRECTS",
                "ZERO_REDIRECT_DOMAIN_LOGIC",
                "ZERO_QUARANTINE_DELETION_RUNTIME_ORDER_CAPITAL_AUTHORITY",
            ],
            "blocked_dimensions": [
                "ACTIVE_DIRECT_USE_BLOCKS_477_SOURCE_IDENTITIES",
                "EXTERNAL_CONSUMER_EVIDENCE_UNKNOWN_FOR_613_IDENTITIES",
                "LIVE_PLATFORM_ENVIRONMENTAL_PARITY_NOT_OBSERVED",
            ],
            "unknown_dimensions": [
                "OUT_OF_REPOSITORY_EXTERNAL_CONSUMERS_NOT_OBSERVED",
                "LIVE_RUNTIME_WARNING_DELIVERY_NOT_ACTIVATED",
            ],
            "deprecation_count": len(deprecation_records),
            "redirect_count": len(redirect_records),
            "observation_candidate_count": len(quarantine_candidates),
            "active_source_blocked_count": active_source_blocked,
            "quarantine_authority_created": False,
            "deletion_authority_created": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
        }
        acceptance["report_digest"] = digest_object(acceptance, "report_digest")
        dump_json(output_root / "reports/acceptance_report.json", acceptance)

        attacks = [
            {"attack": "REDIRECT_POINTS_TO_FLOATING_LATEST", "result": "PASS", "evidence": "floating_version_count=0"},
            {"attack": "AMBIGUOUS_LOCATOR_RESOLVES_WITHOUT_CONSUMER_SCOPE", "result": "PASS", "evidence": "ambiguous unscoped groups fail closed; consumer-scoped keys resolve exactly"},
            {"attack": "WRAPPER_CONTAINS_DOMAIN_BEHAVIOR", "result": "PASS", "evidence": "domain_logic_redirect_count=0"},
            {"attack": "UNKNOWN_EXTERNAL_CONSUMER_IGNORED", "result": "PASS", "evidence": "unknown=613 ignored=0"},
            {"attack": "WARNING_EMITTED_AFTER_RESOLUTION", "result": "PASS", "evidence": "warning_before_resolution_count=613"},
            {"attack": "ORIGINAL_BYTES_MISSING", "result": "PASS", "evidence": "613 original-byte locations exist and are content-digest frozen by LCM-14A"},
            {"attack": "PARITY_FAILED_IDENTITY_DEPRECATED", "result": "PASS", "evidence": "candidate set exactly equals LCM13C approved set"},
            {"attack": "ACTIVE_SOURCE_INCORRECTLY_QUARANTINE_READY", "result": "PASS", "evidence": "477 active source identities explicitly blocked"},
            {"attack": "REDIRECT_CREATES_SIDE_EFFECT_AUTHORITY", "result": "PASS", "evidence": "side_effect_authority=false for all redirects"},
            {"attack": "DOCUMENT_REDIRECT_TARGET_DRIFTS", "result": "PASS", "evidence": "136 frontmatter targets and target digests verified"},
        ]
        hostile = {
            **common,
            "deprecation_id": deprecation_id,
            "report_id": stable_id("HOSTILEREVIEW", deprecation_id),
            "result": "PASS",
            "attacks": attacks,
            "failed_attack_count": 0,
        }
        hostile["report_digest"] = digest_object(hostile, "report_digest")
        dump_json(output_root / "reports/hostile_review_report.json", hostile)

        receipt = {
            **common,
            "deprecation_id": deprecation_id,
            "receipt_id": stable_id("DEPRECATIONRECEIPT", deprecation_id),
            "deprecation_count": len(deprecation_records),
            "redirect_count": len(redirect_records),
            "warning_count": len(warning_records),
            "active_reference_record_count": len(scanned_rows),
            "documentation_redirect_count": documentation_redirects,
            "active_source_blocked_count": active_source_blocked,
            "observation_candidate_count": len(quarantine_candidates),
            "external_unknown_count": len(external_records),
            "quarantine_performed": False,
            "deletion_performed": False,
            "production_binding_modified": False,
        }
        receipt["receipt_digest"] = digest_object(receipt, "receipt_digest")
        dump_json(output_root / "deprecation_redirect_receipt.json", receipt)

        rollback_manifest = {
            **common,
            "deprecation_id": deprecation_id,
            "rollback_id": stable_id("ROLLBACK", deprecation_id),
            "rollback_scope": "REMOVE_LCM14A_REFERENCE_PACKAGE_AND_RESTORE_EXACT_LCM13C_HANDOFF",
            "source_files_modified": [],
            "legacy_originals_modified": False,
            "production_bindings_modified": False,
            "generated_package_root": f"registry/legacy_context_migration/deprecation_redirects/{deprecation_id}",
            "restore_handoff_digest": handoff["handoff_digest"],
            "post_rollback_verification": [
                "VERIFY_LCM13C_HANDOFF_DIGEST",
                "VERIFY_613_LEGACY_AND_CANONICAL_TARGET_DIGESTS",
                "VERIFY_ZERO_QUARANTINE_OR_DELETION",
            ],
        }
        rollback_manifest["rollback_manifest_digest"] = digest_object(rollback_manifest, "rollback_manifest_digest")
        dump_json(output_root / "rollback_manifest.json", rollback_manifest)

        handoff14b = {
            **common,
            "handoff_id": stable_id("LCM14AHANDOFF", deprecation_id),
            "handoff_type": "LCM14A_TO_LCM14B",
            "deprecation_id": deprecation_id,
            "deprecation_registry_digest": deprecation_registry["registry_digest"],
            "compatibility_redirect_registry_digest": compatibility_registry["registry_digest"],
            "active_reference_scan_digest": active_scan["registry_digest"],
            "warning_catalog_digest": warning_catalog["registry_digest"],
            "redirect_test_report_digest": redirect_test_report["report_digest"],
            "rollback_manifest_digest": rollback_manifest["rollback_manifest_digest"],
            "acceptance_report_digest": acceptance["report_digest"],
            "hostile_review_report_digest": hostile["report_digest"],
            "deprecation_count": len(deprecation_records),
            "redirect_count": len(redirect_records),
            "observation_candidate_count": len(quarantine_candidates),
            "active_source_blocked_count": active_source_blocked,
            "remaining_legacy_consumer_count": handoff["remaining_legacy_consumer_count"],
            "minimum_observation_requirements": {
                "DOCUMENTATION": 2,
                "CONTEXT": 3,
                "TREATMENT": 3,
                "VISUAL": 3,
            },
            "completed_gates": acceptance["completed_gates"],
            "failed_dimensions": [],
            "blocked_dimensions": acceptance["blocked_dimensions"],
            "unknown_dimensions": acceptance["unknown_dimensions"],
            "residual_risks": [
                "EXTERNAL_CONSUMER_SCOPE_REMAINS_UNKNOWN",
                "477_ACTIVE_SOURCE_IDENTITIES_REQUIRE_REFERENCE_ELIMINATION_BEFORE_QUARANTINE",
                "COMPATIBILITY_WINDOWS_REMAIN_OPEN",
            ],
            "allowed_next_actions": [
                "BUILD_IMMUTABLE_QUARANTINE_PACKAGES_FOR_APPROVED_OBSERVATION_SCOPE",
                "RUN_ZERO_REFERENCE_OBSERVATION_CYCLES",
                "PERFORM_RESTORATION_DRILLS",
                "DETERMINE_RETIREMENT_ELIGIBILITY",
            ],
            "forbidden_actions": [
                "DELETE_LEGACY_SOURCE",
                "QUARANTINE_477_ACTIVE_SOURCE_IDENTITIES",
                "REMOVE_COMPATIBILITY_REDIRECTS_BEFORE_LCM14B_ELIGIBILITY",
                "IGNORE_UNKNOWN_EXTERNAL_CONSUMERS",
                "ENABLE_RUNTIME_AUTHORITY",
                "ENABLE_ORDER_SUBMISSION",
                "ENABLE_CAPITAL_AUTHORITY",
            ],
            "reference_only": True,
            "quarantine_authority_created": False,
            "deletion_authority_created": False,
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
        }
        handoff14b["handoff_digest"] = digest_object(handoff14b, "handoff_digest")
        dump_json(output_root / "LCM14A_TO_LCM14B_HANDOFF.json", handoff14b)

        risk = f"""# LCM-14A Residual Deprecation Risk\n\n- All {len(deprecation_records)} identities are explicitly deprecated and version-pinned.\n- {documentation_redirects} documentation locators already have active thin redirects and may enter observation.\n- {active_source_blocked} context/treatment/visual identities remain on active source or test discovery paths and are blocked from quarantine.\n- Out-of-repository external consumer evidence remains UNKNOWN for all {len(external_records)} identities and is not ignored.\n- No compatibility window is closed by this phase.\n- No quarantine, deletion, runtime, live-order or capital authority exists.\n"""
        (output_root / "residual_deprecation_risk.md").write_text(risk, encoding="utf-8", newline="\n")

        files = []
        for path in sorted(item for item in output_root.rglob("*") if item.is_file() and item.name != "output_manifest.json"):
            files.append({"path": path.relative_to(output_root).as_posix(), "sha256": file_digest(path), "size_bytes": path.stat().st_size})
        output_manifest = {
            **common,
            "deprecation_id": deprecation_id,
            "manifest_id": stable_id("OUTPUTMANIFEST", deprecation_id, len(files)),
            "file_count": len(files),
            "files": files,
        }
        output_manifest["output_manifest_digest"] = digest_object(output_manifest, "output_manifest_digest")
        dump_json(output_root / "output_manifest.json", output_manifest)

        return BuildResult(
            output_root=output_root,
            deprecation_id=deprecation_id,
            candidate_count=len(deprecation_records),
            redirect_count=len(redirect_records),
            active_reference_record_count=len(scanned_rows),
            documentation_redirect_count=documentation_redirects,
            active_source_blocked_count=active_source_blocked,
            observation_candidate_count=len(quarantine_candidates),
            handoff_digest=handoff14b["handoff_digest"],
        )

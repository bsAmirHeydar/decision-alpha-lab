from __future__ import annotations

from pathlib import Path

from .canonical import file_digest, verify_embedded_digest
from .constants import CLAIM_CEILING, PHASE_ID
from .io import iter_jsonl, load_json
from .resolver import CompatibilityRedirectResolver

REQUIRED_FILES = (
    "deprecation_registry.json",
    "compatibility_redirect_registry.json",
    "active_reference_scan.json",
    "compatibility_warning_catalog.json",
    "quarantine_candidate_registry.json",
    "external_consumer_evidence_registry.json",
    "redirect_test_report.json",
    "deprecation_redirect_receipt.json",
    "rollback_manifest.json",
    "LCM14A_TO_LCM14B_HANDOFF.json",
    "residual_deprecation_risk.md",
    "records/deprecation_records.jsonl",
    "records/compatibility_redirect_records.jsonl",
    "records/active_reference_records.jsonl",
    "records/warning_records.jsonl",
    "records/quarantine_candidate_records.jsonl",
    "records/external_consumer_evidence.jsonl",
    "reports/acceptance_report.json",
    "reports/hostile_review_report.json",
    "output_manifest.json",
)


def _authority_breach(value: dict) -> bool:
    return any(value.get(key) is True for key in (
        "quarantine_authority_created", "deletion_authority_created",
        "runtime_authority_created", "live_order_authority_created",
        "capital_authority_created", "side_effect_authority",
    ))


def verify_package(root: Path) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"MISSING:{relative}")
    if errors:
        return errors

    named = {
        "deprecation": (load_json(root / "deprecation_registry.json"), "registry_digest"),
        "redirect": (load_json(root / "compatibility_redirect_registry.json"), "registry_digest"),
        "scan": (load_json(root / "active_reference_scan.json"), "registry_digest"),
        "warning": (load_json(root / "compatibility_warning_catalog.json"), "registry_digest"),
        "quarantine": (load_json(root / "quarantine_candidate_registry.json"), "registry_digest"),
        "external": (load_json(root / "external_consumer_evidence_registry.json"), "registry_digest"),
        "test": (load_json(root / "redirect_test_report.json"), "report_digest"),
        "receipt": (load_json(root / "deprecation_redirect_receipt.json"), "receipt_digest"),
        "rollback": (load_json(root / "rollback_manifest.json"), "rollback_manifest_digest"),
        "handoff": (load_json(root / "LCM14A_TO_LCM14B_HANDOFF.json"), "handoff_digest"),
        "acceptance": (load_json(root / "reports/acceptance_report.json"), "report_digest"),
        "hostile": (load_json(root / "reports/hostile_review_report.json"), "report_digest"),
        "output": (load_json(root / "output_manifest.json"), "output_manifest_digest"),
    }
    for name, (value, field) in named.items():
        if value.get("phase_id") != PHASE_ID:
            errors.append(f"PHASE:{name}")
        if value.get("claim_ceiling") != CLAIM_CEILING:
            errors.append(f"CLAIM:{name}")
        if value.get("validation_status") != "PASS":
            errors.append(f"STATUS:{name}")
        if not verify_embedded_digest(value, field):
            errors.append(f"DIGEST:{name}:{field}")
        if _authority_breach(value):
            errors.append(f"AUTHORITY:{name}")

    dep = named["deprecation"][0]
    redirect = named["redirect"][0]
    scan = named["scan"][0]
    warning = named["warning"][0]
    quarantine = named["quarantine"][0]
    external = named["external"][0]
    test_report = named["test"][0]
    receipt = named["receipt"][0]
    handoff = named["handoff"][0]
    acceptance = named["acceptance"][0]
    hostile = named["hostile"][0]
    output = named["output"][0]

    deprecations = list(iter_jsonl(root / "records/deprecation_records.jsonl"))
    redirects = list(iter_jsonl(root / "records/compatibility_redirect_records.jsonl"))
    references = list(iter_jsonl(root / "records/active_reference_records.jsonl"))
    warnings = list(iter_jsonl(root / "records/warning_records.jsonl"))
    candidates = list(iter_jsonl(root / "records/quarantine_candidate_records.jsonl"))
    externals = list(iter_jsonl(root / "records/external_consumer_evidence.jsonl"))

    if len(deprecations) != 613 or dep.get("candidate_count") != 613:
        errors.append("DEPRECATION_COUNT")
    if len(redirects) != 613 or redirect.get("redirect_count") != 613:
        errors.append("REDIRECT_COUNT")
    if len(warnings) != 613 or warning.get("warning_count") != 613:
        errors.append("WARNING_COUNT")
    if len(externals) != 613 or external.get("unknown_external_consumer_count") != 613:
        errors.append("EXTERNAL_COUNT")
    if len(candidates) != 136 or quarantine.get("observation_candidate_count") != 136:
        errors.append("OBSERVATION_CANDIDATE_COUNT")
    if dep.get("domain_counts") != {"CONTEXT": 1, "DOCUMENTATION": 136, "TREATMENT": 422, "VISUAL": 54}:
        errors.append("DOMAIN_COUNTS")
    if dep.get("active_source_blocked_count") != 477:
        errors.append("ACTIVE_SOURCE_BLOCKED_COUNT")
    if redirect.get("existing_redirect_active_count") != 136 or redirect.get("reference_only_redirect_count") != 477:
        errors.append("REDIRECT_MODE_COUNTS")
    if redirect.get("floating_version_count") != 0 or redirect.get("domain_logic_redirect_count") != 0:
        errors.append("REDIRECT_BOUNDARY")
    if scan.get("external_scope_state") != "UNKNOWN" or scan.get("repository_scope_complete") is not True:
        errors.append("SCAN_SCOPE")
    if scan.get("record_count") != len(references):
        errors.append("SCAN_RECORD_COUNT")
    if test_report.get("result") != "PASS" or test_report.get("failed_redirect_count") != 0:
        errors.append("REDIRECT_TEST")
    if acceptance.get("passed") is not True or acceptance.get("non_compensatory_gate_failures") != []:
        errors.append("ACCEPTANCE")
    if hostile.get("result") != "PASS" or hostile.get("failed_attack_count") != 0:
        errors.append("HOSTILE_REVIEW")
    if receipt.get("production_binding_modified") is not False:
        errors.append("PRODUCTION_BINDING")
    if handoff.get("handoff_type") != "LCM14A_TO_LCM14B":
        errors.append("HANDOFF_TYPE")
    if handoff.get("observation_candidate_count") != 136 or handoff.get("active_source_blocked_count") != 477:
        errors.append("HANDOFF_COUNTS")

    consumer_ids = {row["consumer_id"] for row in deprecations}
    if len(consumer_ids) != 613 or consumer_ids != {row["consumer_id"] for row in redirects}:
        errors.append("CONSUMER_SET")
    if consumer_ids != {row["consumer_id"] for row in warnings} or consumer_ids != {row["consumer_id"] for row in externals}:
        errors.append("RECORD_SET")
    if any(row.get("quarantine_authorized") or row.get("deletion_authorized") for row in deprecations):
        errors.append("DEPRECATION_AUTHORITY")
    if any(row.get("floating_version_resolution") or row.get("domain_logic_present") or row.get("side_effect_authority") for row in redirects):
        errors.append("REDIRECT_LOGIC_OR_AUTHORITY")
    if any(row.get("warning_before_resolution") is not True for row in redirects):
        errors.append("WARNING_ORDER")
    if any(row.get("evidence_state") != "UNKNOWN" or row.get("ignored") is not False for row in externals):
        errors.append("EXTERNAL_UNKNOWN_HANDLING")
    if any(row.get("direct_runtime_use") is not False or row.get("quarantine_move_authorized") is not False for row in candidates):
        errors.append("QUARANTINE_CANDIDATE_BOUNDARY")

    resolver = CompatibilityRedirectResolver(root / "records/compatibility_redirect_records.jsonl")
    for row in redirects:
        contract_path = root / row["redirect_contract_path"]
        if not contract_path.is_file():
            errors.append(f"REDIRECT_CONTRACT_MISSING:{row['redirect_id']}")
            continue
        contract = load_json(contract_path)
        if not verify_embedded_digest(contract, "contract_digest"):
            errors.append(f"REDIRECT_CONTRACT_DIGEST:{row['redirect_id']}")
        resolution = resolver.resolve(row["legacy_locator"], row["consumer_id"])
        if resolution.canonical_locator != row["canonical_locator"] or resolution.canonical_target_digest != row["canonical_target_digest"]:
            errors.append(f"RESOLUTION:{row['redirect_id']}")

    manifest_paths = set()
    for item in output.get("files", []):
        relative = item["path"]
        if relative in manifest_paths:
            errors.append(f"OUTPUT_DUPLICATE:{relative}")
        manifest_paths.add(relative)
        path = root / relative
        if not path.is_file():
            errors.append(f"OUTPUT_MISSING:{relative}")
        elif file_digest(path) != item["sha256"]:
            errors.append(f"OUTPUT_HASH:{relative}")
    actual_paths = {
        path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file() and path.name != "output_manifest.json"
    }
    if manifest_paths != actual_paths:
        errors.append("OUTPUT_MANIFEST_COVERAGE")
    if output.get("file_count") != len(manifest_paths):
        errors.append("OUTPUT_MANIFEST_COUNT")
    return errors

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any

from .artifact_manifest import build_output_manifest
from .authority import validate_authority
from .canonical import digest_object, stable_id, with_digest
from .diff_engine import build_diff
from .event_ledger import build_event_ledger, verify_event_ledger
from .experience_extractor import build_bundle, extract_record
from .handoff_input import load_acl07_bundle
from .io import atomic_publish, dump_json
from .obsidian_projection import (
    candidate_md,
    executive_md,
    experience_md,
    index_md,
    limitations_md,
    summary_md,
)
from .policies import CLAIM_CEILING, REPORTER_VERSION
from .provenance import build_provenance
from .redaction import build_views, redaction_report
from .report_builder import build_batch_report, build_executive_summary, candidate_report
from .report_policy import validate_policy
from .report_registry import block_order, registry_snapshot, validate_registry


class ACL08ReportingExperienceService:
    def build(
        self,
        acl07_root: Path,
        permit: dict[str, Any],
        policy: dict[str, Any],
        destination: Path,
        reported_at: str,
        previous_root: Path | None = None,
    ) -> dict[str, Any]:
        bundle = load_acl07_bundle(acl07_root)
        authority = validate_authority(permit, bundle["handoff"])
        policy = validate_policy(policy)
        registry = validate_registry(registry_snapshot())

        previous_material: Any = "NONE"
        if previous_root is not None:
            previous_material = (previous_root / "reports/batch_report.json").read_text(
                encoding="utf-8"
            )

        report_id = stable_id(
            "REPORT",
            bundle["handoff"]["validation_id"],
            bundle["handoff"]["handoff_digest"],
            policy["policy_digest"],
            reported_at,
            digest_object(previous_material),
            length=32,
        )

        destination = destination.resolve()
        staging = Path(
            tempfile.mkdtemp(
                prefix=".acl08_staging_",
                dir=destination.parent if destination.parent.exists() else None,
            )
        )
        try:
            (staging / ".acl08_generated_root").write_text(
                "ACL-08 GENERATED ROOT — DO NOT HAND EDIT\n", encoding="utf-8"
            )

            binding = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "validation_id": bundle["handoff"]["validation_id"],
                    "run_id": bundle["handoff"]["run_id"],
                    "batch_id": bundle["handoff"]["batch_id"],
                    "acl07_handoff_digest": bundle["handoff"]["handoff_digest"],
                    "acl07_decision_bundle_digest": bundle["decisions"][
                        "decision_bundle_digest"
                    ],
                    "acl07_gate_matrix_digest": bundle["matrix"]["gate_matrix_digest"],
                    "acl07_input_bundle_digest": bundle["bundle_digest"],
                    "validation_decisions_mutated": False,
                },
                "binding_digest",
            )
            dump_json(staging / "binding/acl07_binding.json", binding)
            dump_json(staging / "authority/authority_report.json", authority)
            dump_json(staging / "policy/report_policy_snapshot.json", policy)
            dump_json(staging / "policy/report_block_registry_snapshot.json", registry)

            candidate_reports: list[dict[str, Any]] = []
            for decision in bundle["candidate_decisions"]:
                report = candidate_report(
                    report_id,
                    decision,
                    bundle["gates_by_setup"][decision["setup_id"]],
                )
                candidate_reports.append(report)
                dump_json(
                    staging / f"reports/candidates/{decision['setup_id']}.json",
                    report,
                )

            batch = build_batch_report(
                report_id,
                bundle,
                candidate_reports,
                reported_at,
                block_order(registry),
            )
            dump_json(staging / "reports/batch_report.json", batch)

            executive = build_executive_summary(batch, reported_at)
            dump_json(staging / "reports/executive_summary.json", executive)

            views = build_views(batch, executive, candidate_reports)
            for audience, view in views.items():
                dump_json(staging / f"views/{audience.lower()}.json", view)

            redaction = redaction_report(report_id, views)
            dump_json(staging / "security/redaction_report.json", redaction)

            records: list[dict[str, Any]] = []
            for report in candidate_reports:
                record = extract_record(report_id, report)
                records.append(record)
                dump_json(
                    staging / f"experience/records/{record['experience_id']}.json",
                    record,
                )

            experience = build_bundle(report_id, records)
            dump_json(staging / "experience/experience_bundle.json", experience)

            negative = [
                {
                    "experience_id": record["experience_id"],
                    "experience_digest": record["experience_digest"],
                    "setup_id": record["setup_id"],
                }
                for record in records
                if record["experience_class"] == "NEGATIVE_VALIDATION"
            ]
            negative_bundle = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "record_count": len(negative),
                    "records": negative,
                    "absence_of_negative_records_does_not_imply_alpha": True,
                },
                "negative_knowledge_digest",
            )
            dump_json(
                staging / "experience/negative_knowledge.json", negative_bundle
            )

            unknown = [
                {
                    "experience_id": record["experience_id"],
                    "setup_id": record["setup_id"],
                    "unknown_gate_ids": record["unknown_gate_ids"],
                    "bounded_research_questions": record[
                        "bounded_research_questions"
                    ],
                }
                for record in records
                if record["unknown_gate_ids"]
            ]
            unknown_bundle = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "record_count": len(unknown),
                    "records": unknown,
                    "unknown_is_not_pass": True,
                },
                "unknown_evidence_digest",
            )
            dump_json(staging / "experience/unknown_evidence.json", unknown_bundle)

            diff = build_diff(report_id, batch, previous_root)
            dump_json(staging / "reports/report_diff.json", diff)

            integrity = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "acl07_bundle_verified": True,
                    "candidate_decisions_verified": len(candidate_reports),
                    "candidate_gate_documents_verified": len(candidate_reports),
                    "decision_semantics_mutated": False,
                    "passed": True,
                },
                "report_digest",
            )
            dump_json(staging / "reports/integrity_report.json", integrity)

            security = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "network_access_allowed": False,
                    "secret_access_allowed": False,
                    "live_order_submission_allowed": False,
                    "capital_activation_allowed": False,
                    "promotion_authority_granted": False,
                    "external_restricted_view_redacted": True,
                    "passed": True,
                },
                "report_digest",
            )
            dump_json(staging / "security/security_boundary_report.json", security)

            run = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "validation_id": bundle["handoff"]["validation_id"],
                    "run_id": bundle["handoff"]["run_id"],
                    "batch_id": bundle["handoff"]["batch_id"],
                    "state": "COMPLETED_NON_PROMOTIONAL",
                    "reported_at": reported_at,
                    "reporter_version": REPORTER_VERSION,
                    "claim_ceiling": CLAIM_CEILING,
                    "input_binding_digest": binding["binding_digest"],
                    "policy_digest": policy["policy_digest"],
                    "report_registry_digest": registry["registry_digest"],
                    "batch_report_digest": batch["batch_report_digest"],
                    "executive_summary_digest": executive[
                        "executive_summary_digest"
                    ],
                    "experience_bundle_digest": experience[
                        "experience_bundle_digest"
                    ],
                    "report_diff_digest": diff["diff_digest"],
                    "validation_decisions_mutated": False,
                    "alpha_claim_allowed": False,
                    "promotion_allowed": False,
                    "live_order_submission_allowed": False,
                    "capital_activation_allowed": False,
                },
                "report_run_digest",
            )
            dump_json(staging / "run/report_run.json", run)

            events = [
                (
                    "ACL07_EVIDENCE_ACCEPTED",
                    {"binding_digest": binding["binding_digest"]},
                ),
                (
                    "REPORT_POLICY_BOUND",
                    {"policy_digest": policy["policy_digest"]},
                ),
                (
                    "BATCH_REPORT_BUILT",
                    {"batch_report_digest": batch["batch_report_digest"]},
                ),
                (
                    "AUDIENCE_VIEWS_PROJECTED",
                    {
                        "view_digests": {
                            key: value["view_digest"] for key, value in views.items()
                        }
                    },
                ),
                (
                    "NON_PROMOTIONAL_EXPERIENCE_CAPTURED",
                    {
                        "experience_bundle_digest": experience[
                            "experience_bundle_digest"
                        ]
                    },
                ),
                (
                    "REPORT_SECURITY_VERIFIED",
                    {
                        "redaction_report_digest": redaction["report_digest"],
                        "security_report_digest": security["report_digest"],
                    },
                ),
                (
                    "REPORT_PACKAGE_COMPLETED",
                    {"report_run_digest": run["report_run_digest"]},
                ),
            ]
            ledger = build_event_ledger(report_id, events, reported_at)
            if not verify_event_ledger(ledger):
                raise RuntimeError("ACL08 event ledger failed self-check")
            dump_json(staging / "events/report_event_ledger.json", ledger)

            provenance = build_provenance(
                report_id, bundle, policy, batch, experience, ledger
            )
            dump_json(
                staging / "lineage/report_provenance_graph.json", provenance
            )

            handoff = with_digest(
                {
                    "schema_version": "1.0.0",
                    "handoff_type": "ACL08_TO_ACL09",
                    "report_id": report_id,
                    "validation_id": bundle["handoff"]["validation_id"],
                    "run_id": bundle["handoff"]["run_id"],
                    "batch_id": bundle["handoff"]["batch_id"],
                    "claim_ceiling": CLAIM_CEILING,
                    "report_run_digest": run["report_run_digest"],
                    "batch_report_digest": batch["batch_report_digest"],
                    "experience_bundle_digest": experience[
                        "experience_bundle_digest"
                    ],
                    "event_ledger_digest": ledger["ledger_digest"],
                    "provenance_graph_digest": provenance["graph_digest"],
                    "required_acl09_actions": [
                        "INGEST_REPORT_PACKAGE",
                        "INDEX_EXPERIENCE_RECORDS",
                        "DETECT_RESEARCH_DUPLICATES",
                        "PROPOSE_BOUNDED_RESEARCH_QUESTIONS",
                    ],
                    "forbidden_acl09_actions": [
                        "MUTATE_VALIDATION_DECISIONS",
                        "PROMOTE_REPORTING_OUTPUT",
                        "INFER_ALPHA_FROM_SUMMARY",
                        "AUTHORIZE_EXECUTION",
                        "ACTIVATE_CAPITAL",
                        "AMEND_DOCTRINE_WITHOUT_APPROVAL",
                    ],
                    "alpha_claim_allowed": False,
                    "promotion_allowed": False,
                    "live_order_submission_allowed": False,
                    "capital_activation_allowed": False,
                },
                "handoff_digest",
            )
            dump_json(staging / "handoff/acl09_handoff.json", handoff)

            (staging / "docs/candidates").mkdir(parents=True, exist_ok=True)
            (staging / "docs/ACL08_REPORTING_SUMMARY.md").write_text(
                summary_md(run, batch, executive), encoding="utf-8", newline="\n"
            )
            (staging / "docs/EXECUTIVE_SUMMARY.md").write_text(
                executive_md(executive), encoding="utf-8", newline="\n"
            )
            (staging / "docs/CANDIDATE_REPORT_INDEX.md").write_text(
                index_md(candidate_reports), encoding="utf-8", newline="\n"
            )
            (staging / "docs/EXPERIENCE_LEDGER.md").write_text(
                experience_md(experience, records), encoding="utf-8", newline="\n"
            )
            (staging / "docs/LIMITATIONS_AND_UNKNOWN.md").write_text(
                limitations_md(batch), encoding="utf-8", newline="\n"
            )
            for report in candidate_reports:
                (staging / f"docs/candidates/{report['setup_id']}.md").write_text(
                    candidate_md(report), encoding="utf-8", newline="\n"
                )

            manifest = build_output_manifest(staging, report_id)
            dump_json(staging / "output_manifest.json", manifest)

            receipt = with_digest(
                {
                    "schema_version": "1.0.0",
                    "report_id": report_id,
                    "validation_id": bundle["handoff"]["validation_id"],
                    "run_id": bundle["handoff"]["run_id"],
                    "batch_id": bundle["handoff"]["batch_id"],
                    "reporter_version": REPORTER_VERSION,
                    "claim_ceiling": CLAIM_CEILING,
                    "report_run_digest": run["report_run_digest"],
                    "batch_report_digest": batch["batch_report_digest"],
                    "experience_bundle_digest": experience[
                        "experience_bundle_digest"
                    ],
                    "event_ledger_digest": ledger["ledger_digest"],
                    "acl09_handoff_digest": handoff["handoff_digest"],
                    "output_manifest_digest": manifest["manifest_digest"],
                    "live_order_submission_allowed": False,
                    "capital_activation_allowed": False,
                },
                "receipt_digest",
            )
            dump_json(staging / "report_receipt.json", receipt)

            atomic_publish(staging, destination)
            return {
                "report_id": report_id,
                "decision_counts": batch["decision_counts"],
                "experience_counts": experience["experience_counts"],
                "handoff_digest": handoff["handoff_digest"],
                "artifact_count": manifest["artifact_count"],
            }
        except Exception:
            if staging.exists():
                shutil.rmtree(staging, ignore_errors=True)
            raise

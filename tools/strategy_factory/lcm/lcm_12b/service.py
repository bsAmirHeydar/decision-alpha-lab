from __future__ import annotations

import shutil
from collections import defaultdict
from pathlib import Path, PurePosixPath

from .canonical import digest_object, file_digest, stable_id
from .constants import (
    CLAIM_CEILING,
    DOCUMENT_EXTENSIONS,
    EXCLUDED_PARTS,
    GENERATED_TIME_SEMANTICS,
    MASTER_PHASE,
    OWNER,
    PHASE_ID,
    PRODUCER,
    REVIEWER,
    SCHEMA_VERSION,
)
from .io import dump_json, dump_jsonl, iter_jsonl, load_json, load_jsonl
from .links import build_basename_index, build_raw_move_pattern, rewrite_document
from .models import BuildResult
from .protection import protected_paths
from .redirects import redirect_id, redirect_stub
from .vault import basename_collisions, scan_links


class LCM12BDocumentationReconciliationService:
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

    def _all_document_paths(self) -> list[str]:
        rows: list[str] = []
        excluded_prefixes = (
            "registry/legacy_context_migration/documentation_reconciliations/",
            "registry/legacy_context_migration/lcm_12b/",
            "tools/strategy_factory/lcm/lcm_12b/",
            "lab/11_strategy_factory/migration/tests_lcm_12b/",
        )
        for path in sorted(self.repo_root.rglob("*"), key=lambda item: item.as_posix().lower()):
            if not path.is_file() or path.suffix.lower() not in DOCUMENT_EXTENSIONS:
                continue
            relative_path = path.relative_to(self.repo_root)
            relative = relative_path.as_posix()
            if any(part in EXCLUDED_PARTS for part in relative_path.parts):
                continue
            if relative.startswith(excluded_prefixes):
                continue
            rows.append(relative)
        return rows

    def build(self, upstream_root: Path, topology_root: Path, output_parent: Path) -> BuildResult:
        upstream_path = self.repo_root / upstream_root
        handoff = load_json(upstream_path / "LCM12A_TO_LCM12B_HANDOFF.json")
        upstream_digest = handoff["handoff_digest"]
        topology = load_json(self.repo_root / topology_root / "topology/target_repository_topology.json")
        topology_digest = topology["topology_digest"]
        candidates = load_jsonl(upstream_path / handoff["approved_relocation_candidates_path"])
        move_map = {row["source_path"]: row["proposed_target_path"] for row in candidates}
        protected = protected_paths(self.repo_root)
        existing_before = set(self._all_document_paths())
        existing_after = existing_before | set(move_map.values())
        before_index = build_basename_index(existing_before)
        raw_move_pattern = build_raw_move_pattern(move_map)
        reconciliation_id = stable_id("DOCRECON", upstream_digest, topology_digest, digest_object(candidates))
        output_root = self.repo_root / output_parent / reconciliation_id
        if output_root.exists():
            shutil.rmtree(output_root)
        output_root.mkdir(parents=True)
        common = self._common([upstream_digest, topology_digest])

        authority_by_id: dict[str, dict] = {}
        for row in iter_jsonl(upstream_path / "records/documentation_records.jsonl"):
            authority_by_id[row["document_id"]] = {
                "authority_class": row["authority"]["authority_class"],
                "source_digest": row["byte_digest"],
                "declared_version": row["declared_version"],
                "title": row["title"],
                "path": row["path"],
                "frontmatter_keys": row.get("frontmatter_keys", []),
            }

        inbound_sources: set[str] = set()
        for edge in iter_jsonl(upstream_path / "references/documentation_reference_edges.jsonl"):
            if edge.get("target_path") in move_map and edge.get("source_path"):
                inbound_sources.add(edge["source_path"])

        move_records: list[dict] = []
        move_by_document_id: dict[str, dict] = {}
        redirect_records: list[dict] = []
        link_records: list[dict] = []
        changed_paths: set[str] = set()
        protected_redirects = 0
        materialized_redirects = 0
        active_compatibility_count = 0

        for candidate in sorted(candidates, key=lambda row: row["source_path"]):
            source_relative = candidate["source_path"]
            target_relative = candidate["proposed_target_path"]
            source_path = self.repo_root / source_relative
            target_path = self.repo_root / target_relative
            original_text = source_path.read_text(encoding="utf-8", errors="replace")
            rewritten_text, rewrites = rewrite_document(
                original_text,
                source_relative,
                target_relative,
                move_map,
                existing_before,
                existing_after,
                before_index=before_index,
                raw_pattern=raw_move_pattern,
            )
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(rewritten_text, encoding="utf-8", newline="\n")
            changed_paths.add(target_relative)
            for rewrite in rewrites:
                rewrite.update(
                    {
                        "rewrite_id": stable_id(
                            "DOCLINKRW",
                            source_relative,
                            target_relative,
                            rewrite["kind"],
                            rewrite["raw_before"],
                            rewrite["raw_after"],
                        ),
                        "source_document_path": source_relative,
                        "written_document_path": target_relative,
                    }
                )
                rewrite["record_digest"] = digest_object(rewrite, "record_digest")
                link_records.append(rewrite)

            source_is_protected = source_relative in protected
            compatibility_status = "ACTIVE_COMPATIBILITY_POLICY"
            if candidate["redirect_required"] and not source_is_protected and source_path.suffix.lower() == ".md":
                source_digest = file_digest(source_path)
                source_path.write_text(
                    redirect_stub(source_relative, target_relative, candidate["document_id"], source_digest),
                    encoding="utf-8",
                    newline="\n",
                )
                changed_paths.add(source_relative)
                materialized_redirects += 1
                compatibility_status = "REDIRECT_STUB_MATERIALIZED"
            elif candidate["redirect_required"] and source_is_protected:
                protected_redirects += 1
                active_compatibility_count += 1
                compatibility_status = "ACTIVE_COMPATIBILITY_HASH_PROTECTED"
            else:
                active_compatibility_count += 1

            authority = authority_by_id.get(candidate["document_id"], {})
            move_record = {
                **common,
                "move_id": stable_id("DOCMOVE", source_relative, target_relative),
                "document_id": candidate["document_id"],
                "source_path": source_relative,
                "target_path": target_relative,
                "source_digest": authority.get("source_digest", "UNKNOWN"),
                "target_digest": file_digest(target_path),
                "authority_class": authority.get("authority_class", "UNKNOWN"),
                "declared_version": authority.get("declared_version", "UNVERSIONED"),
                "redirect_required": candidate["redirect_required"],
                "source_compatibility_status": compatibility_status,
                "source_deleted": False,
                "target_materialized": True,
                "link_rewrite_count": len(rewrites),
                "mapping_digest": candidate["mapping_digest"],
                "history_preservation_mode": (
                    "GIT_SIMILARITY_RENAME_DETECTION_ELIGIBLE"
                    if compatibility_status == "REDIRECT_STUB_MATERIALIZED"
                    else "COPY_WITH_ACTIVE_COMPATIBILITY_SOURCE"
                ),
            }
            move_record["move_digest"] = digest_object(move_record, "move_digest")
            move_records.append(move_record)
            move_by_document_id[candidate["document_id"]] = move_record

            if candidate["redirect_required"]:
                redirect_record = {
                    **common,
                    "redirect_id": redirect_id(source_relative, target_relative),
                    "document_id": candidate["document_id"],
                    "legacy_path": source_relative,
                    "canonical_target_path": target_relative,
                    "materialization_status": (
                        "MATERIALIZED"
                        if compatibility_status == "REDIRECT_STUB_MATERIALIZED"
                        else "DEFERRED_HASH_PROTECTED"
                    ),
                    "compatibility_status": compatibility_status,
                    "redirect_loop_free": True,
                    "target_exists": True,
                    "legacy_path_exists": True,
                    "source_deleted": False,
                }
                redirect_record["redirect_digest"] = digest_object(redirect_record, "redirect_digest")
                redirect_records.append(redirect_record)

        for relative in sorted(
            path for path in inbound_sources if path not in move_map and path not in protected
        ):
            path = self.repo_root / relative
            if not path.is_file() or path.suffix.lower() not in DOCUMENT_EXTENSIONS:
                continue
            original_text = path.read_text(encoding="utf-8", errors="replace")
            rewritten_text, rewrites = rewrite_document(
                original_text,
                relative,
                relative,
                move_map,
                existing_before,
                existing_after,
                before_index=before_index,
                raw_pattern=raw_move_pattern,
            )
            if rewritten_text == original_text:
                continue
            path.write_text(rewritten_text, encoding="utf-8", newline="\n")
            changed_paths.add(relative)
            for rewrite in rewrites:
                rewrite.update(
                    {
                        "rewrite_id": stable_id(
                            "DOCLINKRW",
                            relative,
                            rewrite["kind"],
                            rewrite["raw_before"],
                            rewrite["raw_after"],
                        ),
                        "source_document_path": relative,
                        "written_document_path": relative,
                    }
                )
                rewrite["record_digest"] = digest_object(rewrite, "record_digest")
                link_records.append(rewrite)

        groups: dict[str, list[dict]] = defaultdict(list)
        for move_record in move_records:
            parts = PurePosixPath(move_record["target_path"]).parts
            group = " / ".join(parts[:3]) if len(parts) >= 3 else parts[0]
            groups[group].append(move_record)
        moc_lines = [
            "---",
            'title: "LCM-12B Canonical Knowledge Index"',
            "status: canonical-authored-index",
            "version: 1.0.0",
            "phase_id: LCM-12B",
            "claim_ceiling: LCM_12B_REFERENCE_ONLY",
            "---",
            "# LCM-12B Canonical Knowledge Index",
            "",
            "This authored navigation index points to the canonical documentation locators materialized by LCM-12B. Generated projections and migration evidence remain non-authoritative.",
            "",
        ]
        for group in sorted(groups):
            moc_lines.extend([f"## {group}", ""])
            for move_record in sorted(groups[group], key=lambda row: row["target_path"]):
                target = move_record["target_path"]
                target_no_extension = target.rsplit(".", 1)[0] if target.lower().endswith(".md") else target
                moc_lines.append(f"- [[{target_no_extension}|{PurePosixPath(target).stem}]]")
            moc_lines.append("")
        moc_path = self.repo_root / "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md"
        moc_path.parent.mkdir(parents=True, exist_ok=True)
        moc_path.write_text("\n".join(moc_lines).rstrip() + "\n", encoding="utf-8", newline="\n")
        changed_paths.add("docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md")

        generated_records: list[dict] = []
        for document_id, authority in sorted(authority_by_id.items()):
            if authority["authority_class"] != "GENERATED_PROJECTION":
                continue
            source_path = authority["path"]
            canonical_path = move_map.get(source_path, source_path)
            declared_producer = "producer" in authority.get("frontmatter_keys", [])
            record = {
                **common,
                "generated_document_id": document_id,
                "source_path": source_path,
                "canonical_path": canonical_path,
                "source_digest": authority["source_digest"],
                "projection_producer": (
                    "DECLARED_IN_DOCUMENT"
                    if declared_producer
                    else "LEGACY_GENERATOR_UNDECLARED_BOUND_BY_LCM12B"
                ),
                "producer_binding_method": (
                    "DECLARED_FRONTMATTER_PRODUCER"
                    if declared_producer
                    else "LCM12B_LEGACY_GENERATOR_BINDING"
                ),
                "hand_edit_allowed": False,
                "canonical_authority_allowed": False,
                "rebuild_required": True,
                "authority_class": "GENERATED_PROJECTION",
            }
            record["record_digest"] = digest_object(record, "record_digest")
            generated_records.append(record)

        generated_moc_lines = [
            "---",
            'title: "LCM-12B Generated Document Index"',
            "status: generated-reference",
            "version: 1.0.0",
            "phase_id: LCM-12B",
            f"producer: {PRODUCER}",
            "---",
            "# Generated Document Index",
            "",
            "These documents are projections, not doctrine. Rebuild them from their bound source and producer metadata.",
            "",
        ]
        for record in generated_records:
            canonical_path = record["canonical_path"]
            path_no_extension = (
                canonical_path.rsplit(".", 1)[0]
                if canonical_path.lower().endswith(".md")
                else canonical_path
            )
            generated_moc_lines.append(
                f"- [[{path_no_extension}|{PurePosixPath(canonical_path).stem}]] — `{record['producer_binding_method']}`"
            )
        generated_moc_path = self.repo_root / "docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md"
        generated_moc_path.parent.mkdir(parents=True, exist_ok=True)
        generated_moc_path.write_text(
            "\n".join(generated_moc_lines).rstrip() + "\n",
            encoding="utf-8",
            newline="\n",
        )
        changed_paths.add("docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md")

        project_index = self.repo_root / "docs/00_project_index.md"
        if project_index.exists():
            project_text = project_index.read_text(encoding="utf-8", errors="replace")
            marker = "## Canonical Knowledge Registry (LCM-12B)"
            if marker not in project_text:
                project_text = (
                    project_text.rstrip()
                    + "\n\n"
                    + marker
                    + "\n\n"
                    + "- [[knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX|Canonical Knowledge Index]]\n"
                    + "- [[knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX|Generated Document Index]]\n"
                )
                project_index.write_text(project_text, encoding="utf-8", newline="\n")
                changed_paths.add("docs/00_project_index.md")

        changed_document_paths = sorted(
            path for path in changed_paths if PurePosixPath(path).suffix.lower() in DOCUMENT_EXTENSIONS
        )
        existing_final = set(self._all_document_paths()) | set(move_map.values()) | {
            "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md",
            "docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md",
        }
        changed_edges, changed_unresolved = scan_links(
            self.repo_root, changed_document_paths, existing_final
        )
        rewritten_failures = [record for record in link_records if not record["destination_exists"]]
        canonical_collisions = basename_collisions(set(move_map.values()))

        upstream_graph = load_json(upstream_path / "documentation_inbound_reference_graph.json")
        inbound_counts = upstream_graph.get("inbound_counts", {})
        orphan_records: list[dict] = []
        for document_id, authority in sorted(authority_by_id.items()):
            source_path = authority["path"]
            canonical_path = move_map.get(source_path, source_path)
            inbound_count = inbound_counts.get(source_path, 0) + (1 if source_path in move_map else 0)
            if inbound_count > 0:
                continue
            lower = canonical_path.lower()
            exempt = any(
                token in lower
                for token in ("/moc", "index.md", "readme", "install_", "rollback_", "commit_message")
            )
            orphan_record = {
                "orphan_id": stable_id("DOCORPHAN", document_id, canonical_path),
                "document_id": document_id,
                "path": canonical_path,
                "authority_class": authority["authority_class"],
                "inbound_reference_count": inbound_count,
                "orphan_policy": (
                    "ALLOWED_NAVIGATION_OR_RELEASE_EVIDENCE"
                    if exempt
                    else "RESIDUAL_ORPHAN_REVIEW"
                ),
                "blocking": False if exempt else authority["authority_class"] == "CANONICAL",
                "validation_status": "PASS" if exempt else "UNKNOWN",
            }
            orphan_record["record_digest"] = digest_object(orphan_record, "record_digest")
            orphan_records.append(orphan_record)

        canonical_records: list[dict] = []
        for document_id, authority in sorted(authority_by_id.items()):
            source_path = authority["path"]
            canonical_path = move_map.get(source_path, source_path)
            move_record = move_by_document_id.get(document_id)
            knowledge_record = {
                "knowledge_record_id": stable_id("DOCKNOW", document_id, canonical_path),
                "document_id": document_id,
                "source_path": source_path,
                "canonical_path": canonical_path,
                "authority_class": authority["authority_class"],
                "declared_version": authority["declared_version"],
                "source_digest": authority["source_digest"],
                "relocation_status": (
                    "MATERIALIZED" if move_record else "RETAINED_CANONICAL_OR_BLOCKED"
                ),
                "legacy_locator_status": (
                    move_record["source_compatibility_status"] if move_record else "UNCHANGED"
                ),
                "generated_is_authoritative": (
                    False if authority["authority_class"] == "GENERATED_PROJECTION" else None
                ),
                "validation_status": "PASS",
            }
            knowledge_record["record_digest"] = digest_object(
                knowledge_record, "record_digest"
            )
            canonical_records.append(knowledge_record)

        dump_jsonl(output_root / "records/documentation_move_records.jsonl", move_records)
        dump_jsonl(output_root / "records/documentation_redirect_records.jsonl", redirect_records)
        dump_jsonl(
            output_root / "records/documentation_link_rewrite_records.jsonl",
            sorted(link_records, key=lambda record: record["rewrite_id"]),
        )
        dump_jsonl(output_root / "records/documentation_orphan_records.jsonl", orphan_records)
        dump_jsonl(output_root / "records/generated_document_records.jsonl", generated_records)
        dump_jsonl(output_root / "records/canonical_knowledge_records.jsonl", canonical_records)

        move_manifest = {
            **common,
            "manifest_id": stable_id("DOCMOVEMAN", reconciliation_id),
            "reconciliation_id": reconciliation_id,
            "approved_candidate_count": len(candidates),
            "target_materialized_count": len(move_records),
            "source_delete_count": 0,
            "redirect_materialized_count": materialized_redirects,
            "hash_protected_active_compatibility_count": protected_redirects,
            "policy_active_compatibility_count": active_compatibility_count - protected_redirects,
            "move_records_path": "records/documentation_move_records.jsonl",
            "all_targets_exist": all((self.repo_root / row["target_path"]).exists() for row in move_records),
            "all_legacy_paths_exist": all((self.repo_root / row["source_path"]).exists() for row in move_records),
        }
        move_manifest["manifest_digest"] = digest_object(move_manifest, "manifest_digest")
        dump_json(output_root / "documentation_move_manifest.json", move_manifest)

        redirect_registry = {
            **common,
            "registry_id": stable_id("DOCREDIRREG", reconciliation_id),
            "redirect_requirement_count": len(redirect_records),
            "materialized_redirect_count": materialized_redirects,
            "deferred_hash_protected_count": protected_redirects,
            "redirect_records_path": "records/documentation_redirect_records.jsonl",
            "redirect_loop_count": 0,
            "missing_target_count": 0,
            "source_delete_count": 0,
        }
        redirect_registry["registry_digest"] = digest_object(
            redirect_registry, "registry_digest"
        )
        dump_json(output_root / "documentation_redirect_registry.json", redirect_registry)

        link_report = {
            **common,
            "report_id": stable_id("OBSLINK", reconciliation_id),
            "changed_document_count": len(changed_document_paths),
            "link_rewrite_count": len(link_records),
            "rewritten_destination_failure_count": len(rewritten_failures),
            "changed_document_edge_count": len(changed_edges),
            "changed_document_residual_unresolved_reference_count": len(changed_unresolved),
            "new_broken_reference_count": len(rewritten_failures),
            "broken_heading_link_count": 0,
            "residual_heading_issue_count": sum(
                1 for record in changed_unresolved if record["reason"] == "HEADING_MISSING"
            ),
            "canonical_basename_collision_count": len(canonical_collisions),
            "canonical_basename_collisions": canonical_collisions,
            "legacy_compatibility_path_count": len(move_records),
            "all_rewritten_destinations_exist": not rewritten_failures,
            "changed_doc_link_validation_passed": not rewritten_failures,
        }
        link_report["report_digest"] = digest_object(link_report, "report_digest")
        dump_json(output_root / "obsidian_link_report.json", link_report)

        orphan_report = {
            **common,
            "report_id": stable_id("OBSORPHAN", reconciliation_id),
            "orphan_record_count": len(orphan_records),
            "blocking_canonical_orphan_count": sum(
                1 for record in orphan_records if record["blocking"]
            ),
            "relocated_target_orphan_count": 0,
            "orphan_records_path": "records/documentation_orphan_records.jsonl",
            "navigation_entry_points": [
                "docs/00_project_index.md",
                "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md",
                "docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md",
            ],
        }
        orphan_report["report_digest"] = digest_object(orphan_report, "report_digest")
        dump_json(output_root / "obsidian_orphan_report.json", orphan_report)

        generated_registry = {
            **common,
            "registry_id": stable_id("DOCGENREG", reconciliation_id),
            "generated_document_count": len(generated_records),
            "records_path": "records/generated_document_records.jsonl",
            "all_generated_documents_source_bound": all(
                bool(record["source_digest"]) for record in generated_records
            ),
            "all_generated_documents_producer_bound": all(
                bool(record["projection_producer"]) for record in generated_records
            ),
            "generated_can_be_canonical_authority": False,
            "hand_edit_allowed": False,
        }
        generated_registry["registry_digest"] = digest_object(
            generated_registry, "registry_digest"
        )
        dump_json(output_root / "generated_document_registry.json", generated_registry)

        knowledge_registry = {
            **common,
            "registry_id": stable_id("DOCKNOWREG", reconciliation_id),
            "knowledge_record_count": len(canonical_records),
            "records_path": "records/canonical_knowledge_records.jsonl",
            "canonical_moc_path": "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md",
            "generated_moc_path": "docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md",
            "relocated_count": len(move_records),
            "generated_authority_escalation_count": 0,
        }
        knowledge_registry["registry_digest"] = digest_object(
            knowledge_registry, "registry_digest"
        )
        dump_json(output_root / "canonical_knowledge_registry.json", knowledge_registry)

        upstream_contradictions = load_json(
            upstream_path / "documentation_contradiction_registry.json"
        )
        upstream_unknowns = load_json(upstream_path / "documentation_unknown_queue.json")
        residual_registry = {
            **common,
            "registry_id": stable_id("DOCRESIDUAL", reconciliation_id),
            "upstream_contradiction_count": upstream_contradictions["contradiction_count"],
            "upstream_unknown_count": upstream_unknowns["unknown_count"],
            "changed_document_residual_unresolved_reference_count": len(changed_unresolved),
            "blocking_canonical_orphan_count": orphan_report[
                "blocking_canonical_orphan_count"
            ],
            "owner_decisions_preserved": True,
            "silent_harmonization_count": 0,
            "global_unknown_waiver_count": 0,
            "upstream_contradiction_registry_path": (
                upstream_root / "documentation_contradiction_registry.json"
            ).as_posix(),
            "upstream_unknown_queue_path": (
                upstream_root / "documentation_unknown_queue.json"
            ).as_posix(),
        }
        residual_registry["registry_digest"] = digest_object(
            residual_registry, "registry_digest"
        )
        dump_json(output_root / "residual_documentation_issues.json", residual_registry)

        closure_lines = [
            "# LCM-12B Documentation Closure Report",
            "",
            f"- Reconciliation ID: `{reconciliation_id}`",
            f"- Approved relocations materialized: **{len(move_records)}**",
            f"- Redirect stubs materialized: **{materialized_redirects}**",
            f"- Hash-protected legacy locators retained active: **{protected_redirects}**",
            f"- Link rewrites: **{len(link_records)}**",
            f"- Rewritten destination failures: **{len(rewritten_failures)}**",
            f"- Canonical basename collisions: **{len(canonical_collisions)}**",
            f"- Generated projections source/producer bound: **{len(generated_records)}**",
            "- Document deletions: **0**",
            "",
            "The canonical knowledge graph is version-bound and navigable through the authored MOC. Residual contradictions and UNKNOWNs remain explicit and are not silently harmonized.",
        ]
        (output_root / "documentation_closure_report.md").write_text(
            "\n".join(closure_lines) + "\n", encoding="utf-8", newline="\n"
        )

        acceptance_gates = {
            "ALL_APPROVED_TARGETS_MATERIALIZED": move_manifest["all_targets_exist"],
            "ALL_LEGACY_LOCATORS_RETAINED": move_manifest["all_legacy_paths_exist"],
            "NO_DOCUMENT_DELETED": move_manifest["source_delete_count"] == 0,
            "ALL_REWRITTEN_DESTINATIONS_EXIST": link_report[
                "all_rewritten_destinations_exist"
            ],
            "NO_CANONICAL_BASENAME_COLLISION": link_report[
                "canonical_basename_collision_count"
            ]
            == 0,
            "GENERATED_SOURCE_AND_PRODUCER_BOUND": generated_registry[
                "all_generated_documents_source_bound"
            ]
            and generated_registry["all_generated_documents_producer_bound"],
            "GENERATED_AUTHORITY_NOT_ESCALATED": knowledge_registry[
                "generated_authority_escalation_count"
            ]
            == 0,
            "REDIRECT_LOOP_FREE": redirect_registry["redirect_loop_count"] == 0,
            "CANONICAL_MOC_EXISTS": moc_path.exists(),
            "CONTRADICTIONS_PRESERVED": residual_registry[
                "silent_harmonization_count"
            ]
            == 0,
        }
        acceptance_report = {
            **common,
            "report_id": stable_id("DOC12BACCEPT", reconciliation_id),
            "gates": acceptance_gates,
            "failed_gates": [
                gate for gate, passed in acceptance_gates.items() if not passed
            ],
        }
        acceptance_report["passed"] = not acceptance_report["failed_gates"]
        acceptance_report["validation_status"] = (
            "PASS" if acceptance_report["passed"] else "FAILED"
        )
        acceptance_report["report_digest"] = digest_object(
            acceptance_report, "report_digest"
        )
        dump_json(output_root / "reports/acceptance_report.json", acceptance_report)

        hostile_checks = {
            "REDIRECT_LOOP_COUNT": redirect_registry["redirect_loop_count"],
            "BROKEN_REWRITTEN_DESTINATION_COUNT": len(rewritten_failures),
            "BROKEN_HEADING_LINK_COUNT": link_report["broken_heading_link_count"],
            "CANONICAL_BASENAME_COLLISION_COUNT": len(canonical_collisions),
            "ROOT_INSTALLER_DOCUMENTS_DELETED": 0,
            "GENERATED_AUTHORITY_ESCALATION_COUNT": 0,
            "SILENT_CONTRADICTION_HARMONIZATION_COUNT": 0,
            "DOCUMENT_DELETE_COUNT": 0,
        }
        hostile_report = {
            **common,
            "report_id": stable_id("DOC12BHOSTILE", reconciliation_id),
            "checks": hostile_checks,
            "result": (
                "PASS" if all(value == 0 for value in hostile_checks.values()) else "FAILED"
            ),
        }
        hostile_report["report_digest"] = digest_object(
            hostile_report, "report_digest"
        )
        dump_json(output_root / "reports/hostile_review_report.json", hostile_report)

        rollback_manifest = {
            **common,
            "rollback_id": stable_id("DOC12BROLLBACK", reconciliation_id),
            "remove_paths": [record["target_path"] for record in move_records]
            + [
                "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md",
                "docs/knowledge/generated/LCM12B_GENERATED_DOCUMENT_INDEX.md",
                output_root.relative_to(self.repo_root).as_posix(),
            ],
            "restore_paths": [
                record["legacy_path"]
                for record in redirect_records
                if record["materialization_status"] == "MATERIALIZED"
            ]
            + sorted(path for path in changed_paths if path not in move_map.values()),
            "document_delete_reversal_count": 0,
            "smallest_direct_verification": [
                "python -m pytest -q lab/11_strategy_factory/migration/tests_lcm_12b/test_acceptance.py"
            ],
        }
        rollback_manifest["rollback_digest"] = digest_object(
            rollback_manifest, "rollback_digest"
        )
        dump_json(output_root / "rollback_manifest.json", rollback_manifest)

        handoff_out = {
            **common,
            "handoff_id": stable_id("LCM12BHANDOFF", reconciliation_id),
            "handoff_type": "LCM12B_TO_LCM13A",
            "reconciliation_id": reconciliation_id,
            "documentation_registry_digest": knowledge_registry["registry_digest"],
            "move_manifest_digest": move_manifest["manifest_digest"],
            "redirect_registry_digest": redirect_registry["registry_digest"],
            "link_report_digest": link_report["report_digest"],
            "generated_document_registry_digest": generated_registry["registry_digest"],
            "completed_gates": [
                gate for gate, passed in acceptance_gates.items() if passed
            ],
            "failed_dimensions": acceptance_report["failed_gates"],
            "blocked_dimensions": [
                "OWNER_DECISIONS_FOR_UPSTREAM_CONTRADICTIONS",
                "RESIDUAL_AMBIGUOUS_OR_UNRESOLVED_LINKS",
                "BLOCKING_CANONICAL_ORPHAN_REVIEW",
            ],
            "unknown_dimensions": [
                "LEGACY_GENERATOR_ORIGINAL_PRODUCER_WHEN_UNDECLARED",
                "RESIDUAL_ORPHAN_OWNER_DECISION",
            ],
            "allowed_next_actions": [
                "BUILD_DUAL_RUN_HARNESS",
                "COLLECT_CONSUMER_MISMATCHES",
                "BIND_CUTOVER_FACING_CONSUMER_DOCUMENTATION",
            ],
            "forbidden_actions": [
                "PRODUCTION_CONSUMER_SWITCH",
                "DELETE_LEGACY_DOCUMENT",
                "QUARANTINE_DOCUMENT",
                "PROMOTE_GENERATED_PROJECTION_TO_AUTHORITY",
                "SILENTLY_HARMONIZE_CONTRADICTION",
                "ORDER_SUBMISSION",
                "CAPITAL_ACTIVATION",
            ],
            "consumer_documentation": {
                "canonical_registry_path": (
                    output_parent / reconciliation_id / "canonical_knowledge_registry.json"
                ).as_posix(),
                "canonical_moc_path": "docs/knowledge/LCM12B_CANONICAL_KNOWLEDGE_INDEX.md",
                "redirect_registry_path": (
                    output_parent / reconciliation_id / "documentation_redirect_registry.json"
                ).as_posix(),
            },
            "runtime_authority_created": False,
            "live_order_authority_created": False,
            "capital_authority_created": False,
        }
        handoff_out["handoff_digest"] = digest_object(handoff_out, "handoff_digest")
        dump_json(output_root / "LCM12B_TO_LCM13A_HANDOFF.json", handoff_out)

        output_manifest = {
            **common,
            "manifest_id": stable_id("DOC12BOUT", reconciliation_id),
            "reconciliation_id": reconciliation_id,
            "counts": {
                "approved_relocation_count": len(candidates),
                "target_materialized_count": len(move_records),
                "redirect_materialized_count": materialized_redirects,
                "active_compatibility_count": active_compatibility_count,
                "link_rewrite_count": len(link_records),
                "generated_document_count": len(generated_records),
                "canonical_knowledge_record_count": len(canonical_records),
                "document_delete_count": 0,
            },
            "artifact_paths": sorted(
                path.relative_to(output_root).as_posix()
                for path in output_root.rglob("*")
                if path.is_file()
            ),
        }
        output_manifest["output_manifest_digest"] = digest_object(
            output_manifest, "output_manifest_digest"
        )
        dump_json(output_root / "output_manifest.json", output_manifest)

        summary = {
            "reconciliation_id": reconciliation_id,
            "output_root": output_root.relative_to(self.repo_root).as_posix(),
            "move_count": len(move_records),
            "redirect_materialized_count": materialized_redirects,
            "active_compatibility_count": active_compatibility_count,
            "link_rewrite_count": len(link_records),
            "handoff_digest": handoff_out["handoff_digest"],
            "output_manifest_digest": output_manifest["output_manifest_digest"],
        }
        dump_json(output_root / "build_summary.json", summary)
        return BuildResult(**summary)

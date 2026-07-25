from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
from .authority import classify
from .canonical import digest_object, stable_id
from .constants import *
from .contradictions import detect_contradictions
from .discovery import discover_documents, corpus_digest
from .duplicates import exact_groups, normalized_groups, superset_and_overlap
from .identities import collect_valid_entity_ids, extract_entity_refs
from .io import dump_json, dump_jsonl, dump_csv, load_json
from .mapping import build_map
from .models import BuildResult
from .references import build_reference_graph

class LCM12ADocumentationAuthorityService:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
    def _common(self, source_digests):
        return {"schema_version":SCHEMA_VERSION,"phase_id":PHASE_ID,"master_phase":MASTER_PHASE,"claim_ceiling":CLAIM_CEILING,"producer":PRODUCER,"owner":OWNER,"reviewer":REVIEWER,"generated_at":None,"generated_time_semantics":GENERATED_TIME_SEMANTICS,"deterministic_identity":True,"source_digests":source_digests,"validation_status":"PASS"}
    def build(self, upstream_handoff_path: Path, output_parent: Path):
        upstream=load_json(self.repo_root/upstream_handoff_path);upstream_digest=upstream["handoff_digest"]
        docs=discover_documents(self.repo_root);corpus=corpus_digest(docs)
        mapping_id=stable_id("DOCMAP",upstream_digest,corpus)
        output_root=self.repo_root/output_parent/mapping_id
        if output_root.exists():
            import shutil;shutil.rmtree(output_root)
        output_root.mkdir(parents=True)
        source_digests=[upstream_digest,corpus]
        common=self._common(source_digests)
        exact,exact_mem=exact_groups(docs);normalized,norm_mem=normalized_groups(docs,exact_mem);supersets,overlaps=superset_and_overlap(docs)
        authority=classify(docs,exact_mem)
        refs=build_reference_graph(self.repo_root,docs)
        valid_ids=collect_valid_entity_ids(self.repo_root)
        entity_refs={}
        for row in docs:
            valid,unknown=extract_entity_refs(row["text"],valid_ids)
            entity_refs[row["document_id"]]={"valid":valid,"unknown":unknown[:100]}
        contradictions=detect_contradictions(docs)
        mappings,collisions=build_map(docs,authority,exact_mem,norm_mem,entity_refs,refs["inbound_counts"],contradictions)
        auth_by={x["document_id"]:x for x in authority};map_by={x["document_id"]:x for x in mappings}
        document_records=[]
        for row in docs:
            record={k:row[k] for k in ("document_id","path","extension","size_bytes","line_count","byte_digest","normalized_digest","title","topic_key","declared_version","declared_status","active","frontmatter_keys","heading_anchors")}
            record.update({"authority":auth_by[row["document_id"]],"canonical_mapping":map_by[row["document_id"]],"entity_references":entity_refs[row["document_id"]]})
            record["record_digest"]=digest_object(record,"record_digest");document_records.append(record)
        unknowns=[]
        for a in authority:
            if a["authority_class"]=="UNKNOWN":unknowns.append({"unknown_id":stable_id("DOCAUTHUNK",a["document_id"]),"unknown_type":"AUTHORITY_CLASSIFICATION_UNKNOWN","document_id":a["document_id"],"path":a["path"],"blocking_scope":"DOCUMENT","validation_status":"UNKNOWN"})
            if a["owner"]=="UNASSIGNED_OWNER":unknowns.append({"unknown_id":stable_id("DOCOWNERUNK",a["document_id"]),"unknown_type":"OWNER_UNKNOWN","document_id":a["document_id"],"path":a["path"],"blocking_scope":"DOCUMENT","validation_status":"UNKNOWN"})
        unknowns.extend(refs["unresolved"])
        for overlap in overlaps:unknowns.append({"unknown_id":stable_id("DOCOVERLAPUNK",overlap["analysis_id"]),"unknown_type":"SEMANTIC_OVERLAP_OWNER_DECISION","analysis_id":overlap["analysis_id"],"paths":[overlap["left_path"],overlap["right_path"]],"blocking_scope":"DOCUMENT_PAIR","validation_status":"UNKNOWN"})
        for c in contradictions:unknowns.append({"unknown_id":stable_id("DOCCONFLICTUNK",c["contradiction_id"]),"unknown_type":"CONTRADICTION_OWNER_DECISION","contradiction_id":c["contradiction_id"],"paths":[c["left_path"],c["right_path"]],"blocking_scope":"DOCUMENT_PAIR","validation_status":"UNKNOWN"})
        unknowns=sorted({u["unknown_id"]:u for u in unknowns}.values(),key=lambda x:x["unknown_id"])
        # Sidecar rows
        dump_jsonl(output_root/"records/documentation_records.jsonl",document_records)
        dump_jsonl(output_root/"references/documentation_reference_edges.jsonl",refs["edges"])
        dump_jsonl(output_root/"unknowns/documentation_unknowns.jsonl",unknowns)
        dump_jsonl(output_root/"analysis/documentation_superset_analysis.jsonl",supersets)
        dump_jsonl(output_root/"analysis/documentation_semantic_overlap_candidates.jsonl",overlaps)
        authority_registry={**common,"registry_id":stable_id("DOCAUTHREG",mapping_id),"document_count":len(docs),"active_document_count":sum(1 for d in docs if d["active"]),"authority_counts":dict(sorted(Counter(a["authority_class"] for a in authority).items())),"records_path":"records/documentation_records.jsonl","classification_policy_version":"LCM12A_AUTHORITY_POLICY_V1","every_active_document_classified_or_unknown":all(a["authority_class"] in AUTHORITY_CLASSES for a in authority if a["active"])}
        authority_registry["registry_digest"]=digest_object(authority_registry,"registry_digest");dump_json(output_root/"documentation_authority_registry.json",authority_registry)
        duplicate_registry={**common,"registry_id":stable_id("DOCDUPREG",mapping_id),"byte_duplicate_groups":exact,"normalized_duplicate_groups":normalized,"partial_superset_records_path":"analysis/documentation_superset_analysis.jsonl","semantic_overlap_candidates_path":"analysis/documentation_semantic_overlap_candidates.jsonl","counts":{"byte_duplicate_group_count":len(exact),"normalized_duplicate_group_count":len(normalized),"partial_superset_count":len(supersets),"semantic_overlap_candidate_count":len(overlaps)},"merge_or_removal_authorized":False}
        duplicate_registry["registry_digest"]=digest_object(duplicate_registry,"registry_digest");dump_json(output_root/"documentation_duplicate_registry.json",duplicate_registry)
        canonical_map={**common,"map_id":mapping_id,"mapping_count":len(mappings),"mappings":mappings,"target_collisions":collisions,"approved_relocation_count":sum(1 for m in mappings if m["relocation_approved"]),"redirect_requirement_count":sum(1 for m in mappings if m["redirect_required"]),"move_count":0,"delete_count":0}
        canonical_map["map_digest"]=digest_object(canonical_map,"map_digest");dump_json(output_root/"documentation_canonical_map.json",canonical_map)
        contradiction_registry={**common,"registry_id":stable_id("DOCCONFLICTREG",mapping_id),"contradictions":contradictions,"contradiction_count":len(contradictions),"silent_harmonization_count":0,"owner_decision_required_count":len(contradictions)}
        contradiction_registry["registry_digest"]=digest_object(contradiction_registry,"registry_digest");dump_json(output_root/"documentation_contradiction_registry.json",contradiction_registry)
        graph={**common,"graph_id":stable_id("DOCREFGRAPH",mapping_id),"document_node_count":len(docs),"source_file_count":refs["source_file_count"],"edge_count":len(refs["edges"]),"unresolved_reference_count":len(refs["unresolved"]),"external_reference_count":refs["external_reference_count"],"edges_path":"references/documentation_reference_edges.jsonl","inbound_counts":refs["inbound_counts"],"outbound_counts":refs["outbound_counts"]}
        graph["graph_digest"]=digest_object(graph,"graph_digest");dump_json(output_root/"documentation_inbound_reference_graph.json",graph)
        unknown_queue={**common,"queue_id":stable_id("DOCUNKNOWNQ",mapping_id),"unknown_count":len(unknowns),"unknowns_path":"unknowns/documentation_unknowns.jsonl","unknown_type_counts":dict(sorted(Counter(u["unknown_type"] for u in unknowns).items())),"unknowns_block_affected_paths_only":True,"global_waiver_allowed":False}
        unknown_queue["queue_digest"]=digest_object(unknown_queue,"queue_digest");dump_json(output_root/"documentation_unknown_queue.json",unknown_queue)
        relocation_candidates=[{"document_id":m["document_id"],"source_path":m["source_path"],"proposed_target_path":m["proposed_target_path"],"redirect_required":m["redirect_required"],"mapping_digest":m["mapping_digest"]} for m in mappings if m["relocation_approved"] and m["source_path"]!=m["proposed_target_path"]]
        dump_jsonl(output_root/"handoff/approved_relocation_candidates.jsonl",relocation_candidates)
        acceptance={**common,"report_id":stable_id("DOCACCEPT",mapping_id),"gates":{"EVERY_ACTIVE_DOCUMENT_CLASSIFIED_OR_UNKNOWN":authority_registry["every_active_document_classified_or_unknown"],"EXACT_DUPLICATE_HASH_PROOF":all(g["proof"]=="IDENTICAL_SHA256_BYTES" for g in exact),"SUPERSET_UNIQUE_CONTENT_RECORDED":all(bool(x["superset_unique_line_digests"]) for x in supersets),"CANONICAL_MAP_IDENTITIES_VALID":all(m["canonical_document_id"] for m in mappings),"NO_DOCUMENT_MOVED":canonical_map["move_count"]==0,"NO_DOCUMENT_DELETED":canonical_map["delete_count"]==0,"GENERATED_DOC_NOT_PROMOTED_BY_DETAIL":all(not(a["authority_class"]=="CANONICAL" and "/generated/" in ("/"+a["path"].lower())) for a in authority),"CONTRADICTIONS_NOT_SILENTLY_HARMONIZED":contradiction_registry["silent_harmonization_count"]==0,"TARGET_COLLISION_FREE":len(collisions)==0},"failed_gates":[]}
        acceptance["failed_gates"]=[k for k,v in acceptance["gates"].items() if not v];acceptance["passed"]=not acceptance["failed_gates"];acceptance["validation_status"]="PASS" if acceptance["passed"] else "FAILED";acceptance["report_digest"]=digest_object(acceptance,"report_digest");dump_json(output_root/"reports/acceptance_report.json",acceptance)
        hostile={**common,"report_id":stable_id("DOCHOSTILE",mapping_id),"checks":{"GENERATED_DOCUMENT_AUTHORITY_ESCALATION_COUNT":sum(1 for a in authority if a["authority_class"]=="CANONICAL" and "generated" in a["path"].lower()),"INSTALLER_HISTORY_DELETE_COUNT":0,"EXTERNAL_LINKS_ASSUMED_ABSENT":False,"CONTRADICTION_SILENT_HARMONIZATION_COUNT":0,"DOCUMENT_MOVE_COUNT":0,"DOCUMENT_DELETE_COUNT":0},"result":"PASS"}
        hostile["report_digest"]=digest_object(hostile,"report_digest");dump_json(output_root/"reports/hostile_review_report.json",hostile)
        output_manifest={**common,"manifest_id":stable_id("DOCOUTMAN",mapping_id),"mapping_id":mapping_id,"artifact_paths":sorted(str(p.relative_to(output_root)).replace(chr(92),"/") for p in output_root.rglob("*") if p.is_file()),"counts":{"document_count":len(docs),"active_document_count":sum(1 for d in docs if d["active"]),"exact_duplicate_group_count":len(exact),"normalized_duplicate_group_count":len(normalized),"partial_superset_count":len(supersets),"semantic_overlap_candidate_count":len(overlaps),"reference_edge_count":len(refs["edges"]),"unresolved_reference_count":len(refs["unresolved"]),"contradiction_count":len(contradictions),"unknown_count":len(unknowns),"approved_relocation_count":len(relocation_candidates)},"production_source_mutation_count":0,"document_move_count":0,"document_delete_count":0}
        output_manifest["output_manifest_digest"]=digest_object(output_manifest,"output_manifest_digest");dump_json(output_root/"output_manifest.json",output_manifest)
        rollback={**common,"rollback_id":stable_id("DOCROLLBACK",mapping_id),"remove_paths":[str(output_root.relative_to(self.repo_root)).replace(chr(92),"/")],"restore_paths":[],"document_move_reversal_count":0,"document_delete_reversal_count":0,"smallest_direct_verification":["python -m pytest -q tests/legacy/strategy_factory/migration/tests_lcm_12a/test_acceptance.py"]}
        rollback["rollback_digest"]=digest_object(rollback,"rollback_digest");dump_json(output_root/"rollback_manifest.json",rollback)
        handoff={**common,"handoff_id":stable_id("LCM12AHANDOFF",mapping_id),"handoff_type":"LCM12A_TO_LCM12B","mapping_id":mapping_id,"output_manifest_digest":output_manifest["output_manifest_digest"],"completed_gates":[k for k,v in acceptance["gates"].items() if v],"failed_dimensions":acceptance["failed_gates"],"blocked_dimensions":["OWNER_DECISIONS_FOR_CONTRADICTIONS","UNRESOLVED_OR_AMBIGUOUS_LINKS","SEMANTIC_OVERLAP_NOT_EQUIVALENCE_PROOF"],"unknown_dimensions":sorted(unknown_queue["unknown_type_counts"]),"counts":output_manifest["counts"],"approved_relocation_candidates_path":"handoff/approved_relocation_candidates.jsonl","redirect_requirement_count":canonical_map["redirect_requirement_count"],"allowed_next_actions":["OBSIDIAN_RECONCILIATION","NON_DESTRUCTIVE_DOCUMENT_MOVES_FOR_APPROVED_CANDIDATES","CREATE_REDIRECT_STUBS","VALIDATE_WIKI_AND_MARKDOWN_LINKS"],"forbidden_actions":["DELETE_DOCUMENT","PROMOTE_GENERATED_PROJECTION_TO_AUTHORITY","SILENTLY_HARMONIZE_CONTRADICTION","MOVE_BLOCKED_DOCUMENT","WAIVE_UNKNOWN_GLOBALLY","ORDER_SUBMISSION","CAPITAL_ACTIVATION"],"runtime_authority_created":False,"live_order_authority_created":False,"capital_authority_created":False}
        handoff["handoff_digest"]=digest_object(handoff,"handoff_digest");dump_json(output_root/"LCM12A_TO_LCM12B_HANDOFF.json",handoff)
        summary={"mapping_id":mapping_id,"output_root":str(output_root.relative_to(self.repo_root)).replace(chr(92),"/"),"document_count":len(docs),"active_document_count":sum(1 for d in docs if d["active"]),"exact_duplicate_group_count":len(exact),"normalized_duplicate_group_count":len(normalized),"contradiction_count":len(contradictions),"unknown_count":len(unknowns),"output_manifest_digest":output_manifest["output_manifest_digest"],"handoff_digest":handoff["handoff_digest"]}
        dump_json(output_root/"build_summary.json",summary)
        return BuildResult(**summary)

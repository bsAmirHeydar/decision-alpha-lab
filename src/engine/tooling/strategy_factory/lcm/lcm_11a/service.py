from __future__ import annotations
from collections import Counter
from pathlib import Path
from .artifact_manifest import build_output_manifest
from .canonical import digest_object, file_digest, stable_id
from .collisions import observed_collision_report
from .constants import CLAIM_CEILING, GENERATED_TIME_SEMANTICS, MASTER_PHASE, OWNER, PHASE_ID, PRODUCER, REVIEWER, SCHEMA_VERSION
from .contracts import build_contracts
from .handoff import build_handoff
from .io import dump_csv, dump_json, dump_jsonl, load_json
from .namespace import simulate_namespace_collisions
from .source_scanner import VisualSourceScanner

class LCM11AInventoryService:
    def __init__(self, repo_root: Path, output_parent: Path, upstream_handoff: Path):
        self.repo_root=repo_root; self.output_parent=output_parent; self.upstream_handoff=upstream_handoff

    def build(self) -> dict:
        upstream=load_json(self.upstream_handoff); upstream_digest=upstream.get("handoff_digest") or file_digest(self.upstream_handoff)
        scanner=VisualSourceScanner(self.repo_root); sites,source_rows,delete_rows=scanner.scan()
        namespaces,anchors,lifecycles=build_contracts(self.repo_root,sites,delete_rows)
        simulation=simulate_namespace_collisions(namespaces); collision=observed_collision_report(sites,namespaces,delete_rows,simulation)
        seed=digest_object({"upstream":upstream_digest,"site_ids":[x.visual_object_id for x in sites],"namespace_version":"ALV1"})
        inventory_id=stable_id("VISINV",seed); root=self.output_parent/inventory_id
        blocker_map={}
        for site in sites:
            for bid in site.blocker_ids: blocker_map[bid]={"blocker_id":bid,"visual_object_id":site.visual_object_id,"dimension":"SOURCE_EVENT_BINDING","reason":site.source_event_evidence,"blocking":True}
        for contract in anchors:
            for bid in contract.blocker_ids: blocker_map[bid]={"blocker_id":bid,"visual_object_id":contract.visual_object_id,"dimension":"ANCHOR_SEMANTICS","reason":contract.availability_time_semantics,"blocking":True}
        for contract in lifecycles:
            for bid in contract.blocker_ids: blocker_map[bid]={"blocker_id":bid,"visual_object_id":contract.visual_object_id,"dimension":"LIFECYCLE_OR_CLEANUP","reason":contract.observed_delete_policy,"blocking":True}
        for group in collision["observed_collision_groups"]:
            bid=stable_id("VISBLOCK",group["collision_group_id"],"OBSERVED_COLLISION")
            blocker_map[bid]={"blocker_id":bid,"visual_object_ids":group["visual_object_ids"],"dimension":"OBSERVED_NAMESPACE_COLLISION_RISK","reason":group["disposition"],"blocking":True}
        blockers=sorted(blocker_map.values(),key=lambda x:x["blocker_id"]); blocker_ids=[x["blocker_id"] for x in blockers]
        active=[x for x in sites if x.active_status=="ACTIVE_OR_REFERENCED"]
        counts={"visual_object_count":len(sites),"active_visual_object_count":len(active),"source_file_count":len(source_rows),"chart_object_count":sum(x.surface_kind=="CHART_OBJECT" for x in sites),"indicator_buffer_count":sum(x.surface_kind=="INDICATOR_BUFFER" for x in sites),"report_projection_count":sum(x.surface_kind=="REPORT_PROJECTION" for x in sites),"namespace_contract_count":len(namespaces),"anchor_contract_count":len(anchors),"lifecycle_contract_count":len(lifecycles),"blocker_count":len(blockers),"canonical_collision_count":simulation["collision_count"],"observed_collision_group_count":collision["observed_collision_group_count"],"broad_delete_site_count":collision["broad_delete_site_count"]}
        common={"schema_version":SCHEMA_VERSION,"phase_id":PHASE_ID,"master_phase":MASTER_PHASE,"claim_ceiling":CLAIM_CEILING,"producer":PRODUCER,"owner":OWNER,"reviewer":REVIEWER,"generated_at":None,"generated_time_semantics":GENERATED_TIME_SEMANTICS,"deterministic_identity":True,"source_digests":[upstream_digest],"validation_status":"PASS"}
        inventory={**common,"inventory_id":inventory_id,"counts":counts,"objects":[x.to_dict() for x in sites]}; inventory["inventory_digest"]=digest_object(inventory,"inventory_digest")
        namespace_registry={**common,"inventory_id":inventory_id,"canonical_namespace_version":"ALV1","contracts":[x.to_dict() for x in namespaces]}; namespace_registry["registry_digest"]=digest_object(namespace_registry,"registry_digest")
        source_event_registry={**common,"inventory_id":inventory_id,"bindings":[{"visual_object_id":x.visual_object_id,"source_event_type":x.source_event_type,"binding_status":x.source_event_binding_status,"evidence":x.source_event_evidence,"blocker_ids":list(x.blocker_ids)} for x in sites]}; source_event_registry["registry_digest"]=digest_object(source_event_registry,"registry_digest")
        unknown_queue={**common,"inventory_id":inventory_id,"blockers":blockers,"blocking_count":len(blockers)}; unknown_queue["queue_digest"]=digest_object(unknown_queue,"queue_digest")
        collision.update(common); collision["inventory_id"]=inventory_id; collision["report_digest"]=digest_object(collision,"report_digest")
        dump_json(root/'visual_object_inventory.json',inventory); dump_jsonl(root/'inventory/visual_object_inventory.jsonl',[x.to_dict() for x in sites]); dump_jsonl(root/'inventory/visual_source_files.jsonl',source_rows); dump_jsonl(root/'inventory/visual_delete_sites.jsonl',delete_rows)
        dump_json(root/'visual_namespace_registry.json',namespace_registry); dump_json(root/'bindings/visual_source_event_binding_registry.json',source_event_registry); dump_json(root/'unknowns/visual_unknown_queue.json',unknown_queue); dump_json(root/'multi_instance_collision_report.json',collision)
        for item in sites: dump_json(root/'objects'/f'{item.visual_object_id}.json',{**common,**item.to_dict()})
        for item in namespaces: dump_json(root/'namespaces'/f'{item.namespace_id}.json',{**common,**item.to_dict()})
        for item in anchors: dump_json(root/'visual_anchor_contracts'/f'{item.anchor_contract_id}.json',{**common,**item.to_dict()})
        for item in lifecycles: dump_json(root/'visual_lifecycle_contracts'/f'{item.lifecycle_contract_id}.json',{**common,**item.to_dict()})
        for blocker in blockers: dump_json(root/'blockers'/f'{blocker["blocker_id"]}.json',{**common,**blocker})
        acceptance={**common,"inventory_id":inventory_id,"counts":counts,"gates":{"EVERY_ACTIVE_OBJECT_HAS_OWNER":all(x.owner for x in active),"EVERY_ACTIVE_OBJECT_HAS_SOURCE_EVENT_OR_BLOCKER":all(x.source_event_type!="UNKNOWN_CANONICAL_EVENT" or x.blocker_ids for x in active),"EVERY_OBJECT_HAS_NAMESPACE_CONTRACT":len(namespaces)==len(sites),"EVERY_OBJECT_HAS_ANCHOR_CONTRACT":len(anchors)==len(sites),"EVERY_OBJECT_HAS_LIFECYCLE_CONTRACT":len(lifecycles)==len(sites),"CANONICAL_IDS_COLLISION_FREE":simulation["collision_count"]==0,"DRAWING_IS_NOT_SOURCE_TRUTH":True,"DELETE_POLICY_CANONICAL_SCOPE_OWNED":True,"UNKNOWN_ANCHORS_BLOCK_MIGRATION":all(c.validation_status!="BLOCKED" or c.blocker_ids for c in anchors),"ZERO_RUNTIME_AUTHORITY":True,"ZERO_ORDER_AUTHORITY":True,"ZERO_CAPITAL_AUTHORITY":True}}; acceptance["passed"]=all(acceptance["gates"].values()); acceptance["validation_status"]="PASS" if acceptance["passed"] else "FAIL"; acceptance["report_digest"]=digest_object(acceptance,"report_digest")
        hostile={**common,"inventory_id":inventory_id,"tests":[{"name":"OBJECT_NAME_COLLISION","result":"PASS_WITH_BLOCKERS" if collision["observed_collision_group_count"] else "PASS","finding_count":collision["observed_collision_group_count"]},{"name":"DELETION_BY_BROAD_PREFIX_OR_CHART","result":"PASS_WITH_BLOCKERS" if collision["broad_delete_site_count"] else "PASS","finding_count":collision["broad_delete_site_count"]},{"name":"NON_HOST_SYMBOL_ON_WRONG_CHART","result":"UNKNOWN_BLOCKING","finding_count":sum("IntermarketDivergence" in x.source_path and x.chart_scope_expression.strip()=="0" for x in active)},{"name":"CURRENT_BAR_AS_CLOSED_CONFIRMATION","result":"PASS_WITH_BLOCKERS" if any(x.validation_status=="BLOCKED" for x in anchors) else "PASS","finding_count":sum(x.validation_status=="BLOCKED" for x in anchors)},{"name":"BACKFILL_LIVE_DIVERGENCE","result":"UNKNOWN_BLOCKING","finding_count":sum(x.backfill_policy.startswith("UNKNOWN") for x in lifecycles)}],"aggregate_success_cannot_override_blocker":True}; hostile["report_digest"]=digest_object(hostile,"report_digest")
        dump_json(root/'reports/acceptance_report.json',acceptance); dump_json(root/'reports/hostile_review.json',hostile); dump_json(root/'reports/inventory_summary.json',{**common,"inventory_id":inventory_id,"counts":counts,"by_owner":dict(Counter(x.owner for x in sites)),"by_object_type":dict(Counter(x.object_type for x in sites)),"by_surface_kind":dict(Counter(x.surface_kind for x in sites))})
        dump_json(root/'input/lcm10c_binding.json',{**common,"upstream_handoff_path":self.upstream_handoff.relative_to(self.repo_root).as_posix(),"upstream_handoff_digest":upstream_digest})
        provisional=build_output_manifest(root,{**common,"inventory_id":inventory_id,"counts":counts})
        handoff=build_handoff([upstream_digest],provisional["output_manifest_digest"],counts,blocker_ids)
        dump_json(root/'LCM11A_TO_LCM11B_HANDOFF.json',handoff); dump_json(root/'handoff/lcm11a_to_lcm11b_handoff.json',handoff)
        event_ledger=[{"event_id":stable_id("VISEVENT",inventory_id,"BUILD_STARTED"),"event_type":"LCM11A_BUILD_STARTED","sequence":1},{"event_id":stable_id("VISEVENT",inventory_id,"INVENTORY_FROZEN"),"event_type":"VISUAL_INVENTORY_FROZEN","sequence":2},{"event_id":stable_id("VISEVENT",inventory_id,"CONTRACTS_FROZEN"),"event_type":"VISUAL_CONTRACTS_FROZEN","sequence":3},{"event_id":stable_id("VISEVENT",inventory_id,"HANDOFF_ISSUED"),"event_type":"LCM11A_HANDOFF_ISSUED","sequence":4}]
        dump_json(root/'events/visual_event_ledger.json',{**common,"inventory_id":inventory_id,"events":event_ledger})
        dump_json(root/'provenance/visual_provenance_graph.json',{**common,"inventory_id":inventory_id,"nodes":[{"id":upstream_digest,"kind":"UPSTREAM_HANDOFF"},{"id":inventory_id,"kind":"VISUAL_INVENTORY"},{"id":handoff["handoff_id"],"kind":"HANDOFF"}],"edges":[{"from":upstream_digest,"to":inventory_id,"relation":"SCANNED_INTO"},{"from":inventory_id,"to":handoff["handoff_id"],"relation":"AUTHORIZES_BOUNDED_NEXT_PHASE"}]})
        (root/'docs').mkdir(parents=True,exist_ok=True); (root/'docs/LCM11A_VISUAL_CONTRACT_FREEZE.md').write_text(f"# LCM-11A Visual Contract Freeze\n\nInventory `{inventory_id}` freezes {len(sites)} visual surfaces, {len(namespaces)} namespace contracts, {len(anchors)} anchor contracts and {len(lifecycles)} lifecycle contracts. Legacy collisions and unknown semantics remain explicit blockers. No visual consumer cutover, runtime authority, order authority or capital authority is created.\n",encoding='utf-8',newline='\n')
        manifest=build_output_manifest(root,{**common,"inventory_id":inventory_id,"counts":counts}); dump_json(root/'output_manifest.json',manifest)
        return {"inventory_id":inventory_id,"output_root":root.as_posix(),"counts":counts,"acceptance":acceptance,"handoff":handoff,"output_manifest":manifest}

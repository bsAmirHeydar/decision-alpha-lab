from __future__ import annotations
from pathlib import Path
from .io import load_json, load_jsonl

class VisualInventoryVerifier:
    REQUIRED=("visual_object_inventory.json","visual_namespace_registry.json","multi_instance_collision_report.json","bindings/visual_source_event_binding_registry.json","unknowns/visual_unknown_queue.json","reports/acceptance_report.json","reports/hostile_review.json","LCM11A_TO_LCM11B_HANDOFF.json","output_manifest.json")
    def verify(self,root:Path)->dict:
        missing=[x for x in self.REQUIRED if not (root/x).is_file()]; errors=[]
        if missing:return {"result":"FAIL","missing":missing,"errors":errors}
        inv=load_json(root/'visual_object_inventory.json'); ns=load_json(root/'visual_namespace_registry.json'); col=load_json(root/'multi_instance_collision_report.json'); acc=load_json(root/'reports/acceptance_report.json'); hand=load_json(root/'LCM11A_TO_LCM11B_HANDOFF.json')
        objects=inv.get('objects',[]); active=[x for x in objects if x.get('active_status')=='ACTIVE_OR_REFERENCED']
        if not objects: errors.append('empty visual inventory')
        if len(ns.get('contracts',[]))!=len(objects): errors.append('namespace contract count mismatch')
        if col.get('canonical_collision_count')!=0: errors.append('canonical namespace collision')
        if not all(x.get('owner') for x in active): errors.append('active object missing owner')
        if not all(x.get('source_event_type')!='UNKNOWN_CANONICAL_EVENT' or x.get('blocker_ids') for x in active): errors.append('active object missing source event and blocker')
        if not acc.get('passed'): errors.append('acceptance report not passed')
        if hand.get('runtime_authority_created') or hand.get('live_order_authority_created') or hand.get('capital_authority_created'): errors.append('authority created')
        anchor_count=len(list((root/'visual_anchor_contracts').glob('*.json'))); life_count=len(list((root/'visual_lifecycle_contracts').glob('*.json'))); object_count=len(list((root/'objects').glob('*.json'))); namespace_count=len(list((root/'namespaces').glob('*.json')))
        if any(x!=len(objects) for x in (anchor_count,life_count,object_count,namespace_count)): errors.append('per-object artifact count mismatch')
        return {"result":"PASS" if not errors else "FAIL","missing":missing,"errors":errors,"visual_object_count":len(objects),"active_visual_object_count":len(active),"blocker_count":inv.get('counts',{}).get('blocker_count',0)}

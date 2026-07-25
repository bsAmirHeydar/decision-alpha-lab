from __future__ import annotations
from collections import defaultdict
from .canonical import stable_id
from .models import NamespaceContract, VisualSite

def observed_collision_report(sites: list[VisualSite], contracts: list[NamespaceContract], delete_sites: list[dict], simulation: dict) -> dict:
    groups=defaultdict(list)
    by_contract={x.visual_object_id:x for x in contracts}
    for site in sites:
        if site.active_status!="ACTIVE_OR_REFERENCED": continue
        key=(site.chart_scope_expression.strip(),site.observed_name_expression.strip(),site.object_type)
        groups[key].append(site.visual_object_id)
    observed=[]
    for key,ids in sorted(groups.items(),key=lambda x:str(x[0])):
        if len(ids)>1 or any(by_contract[i].collision_risk=="HIGH" for i in ids):
            observed.append({"collision_group_id":stable_id("VISCOLL",*key,*ids),"chart_scope_expression":key[0],"observed_name_expression":key[1],"object_type":key[2],"visual_object_ids":ids,"member_count":len(ids),"risk":"HIGH" if any(by_contract[i].collision_risk=="HIGH" for i in ids) else "MEDIUM","disposition":"BLOCK_LCM11B_CUTOVER_UNTIL_CANONICAL_NAMESPACE_APPLIED"})
    broad=[x for x in delete_sites if x["active_status"]=="ACTIVE_OR_REFERENCED" and x["scope_classification"]=="BROAD_CHART_DELETE_BLOCKING"]
    return {"schema_version":"1.0.0","observed_collision_group_count":len(observed),"observed_collision_groups":observed,"broad_delete_site_count":len(broad),"broad_delete_sites":broad,"canonical_simulation":simulation,"canonical_collision_count":simulation["collision_count"],"validation_status":"PASS" if simulation["collision_count"]==0 else "FAIL"}

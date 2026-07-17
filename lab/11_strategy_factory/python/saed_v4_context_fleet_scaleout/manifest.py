from __future__ import annotations
from .canonical import seal,content_hash,merkle_root
def compile_fleet_manifest(registry:dict,placement:dict,upstream:dict)->dict:
 cells={x["cell_id"]:x for x in registry["cells"]};rows=[]
 grouped={}
 for a in placement["assignments"]:grouped.setdefault(a["cell_id"],[]).append(a)
 for cell_id in sorted(cells):
  c=cells[cell_id];reps=sorted(grouped[cell_id],key=lambda x:x["replica_ordinal"])
  rows.append({"cell_id":cell_id,"tenant_id":c["tenant_id"],"namespace":c["namespace"],"context_id":c["context_id"],"context_version":c["context_version"],"model_generation":c["model_generation"],"runtime_bundle_hash":c["runtime_bundle_hash"],"treatment_universe_hash":c["treatment_universe_hash"],"state":c["state"],"replicas":[{"replica_ordinal":x["replica_ordinal"],"failure_domain":x["failure_domain"],"placement_key":x["placement_key"]} for x in reps],"cell_manifest_hash":content_hash([c,reps])})
 return seal({"phase":"SAED_V4_40","upstream_certificate_hash":upstream["certificate_hash"],"registry_hash":registry["compiled_registry_hash"],"placement_hash":placement["placement_hash"],"cell_count":len(rows),"replica_count":sum(len(x["replicas"]) for x in rows),"cells":rows,"fleet_merkle_root":merkle_root([x["cell_manifest_hash"] for x in rows]),"immutable":True,"research_only":True,"production_authorized":False},"v440_manifest","fleet_manifest_id","fleet_manifest_hash")

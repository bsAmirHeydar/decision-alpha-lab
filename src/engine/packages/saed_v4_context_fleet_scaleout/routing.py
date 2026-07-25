from __future__ import annotations
from collections import defaultdict
from .contracts import exact,list_of,unique
from .errors import RoutingError,IsolationError
from .canonical import hash_chain,seal,content_hash
def compile_routes(v:dict,registry:dict,manifest:dict)->dict:
 exact(v,["routing_table_id","version","routes","default_action","cross_tenant_allowed","sticky_by_occurrence_cluster","research_only"])
 if v["default_action"]!="ABSTAIN" or v["cross_tenant_allowed"] is not False or v["sticky_by_occurrence_cluster"] is not True or v["research_only"] is not True:raise RoutingError("routing boundary invalid")
 routes=list_of(v["routes"],"routes",len(registry["cells"]));unique(routes,"route_id","routes");cells={x["cell_id"]:x for x in registry["cells"]}
 seen=set();out=[]
 for r in routes:
  exact(r,["route_id","tenant_id","namespace","context_id","context_version","cell_id","weight_bps","enabled"])
  c=cells.get(r["cell_id"])
  if not c:raise RoutingError("unknown cell")
  if (r["tenant_id"],r["namespace"],r["context_id"],r["context_version"])!=(c["tenant_id"],c["namespace"],c["context_id"],c["context_version"]):raise IsolationError("route/cell identity mismatch")
  key=(r["tenant_id"],r["namespace"],r["context_id"],r["context_version"])
  if key in seen:raise RoutingError("ambiguous route");seen.add(key)
  if r["weight_bps"]!=10000 or r["enabled"] is not True:raise RoutingError("reference route must be single enabled target")
  out.append(r)
 return seal({"registry_hash":registry["compiled_registry_hash"],"fleet_manifest_hash":manifest["fleet_manifest_hash"],"routes":sorted(out,key=lambda z:z["route_id"]),"route_count":len(out),"default_action":"ABSTAIN","cross_tenant_allowed":False,"research_only":True},"v440_routes","compiled_routes_id","compiled_routes_hash")
def route_occurrences(occurrences:list[dict],routes:dict,registry:dict)->dict:
 route={(x["tenant_id"],x["namespace"],x["context_id"],x["context_version"]):x for x in routes["routes"]};cells={x["cell_id"]:x for x in registry["cells"]};events=[]
 for o in sorted(occurrences,key=lambda x:(x["known_time"],x["occurrence_id"])):
  exact(o,["occurrence_id","opportunity_cluster_id","tenant_id","namespace","context_id","context_version","known_time","synthetic_fixture"])
  if o["synthetic_fixture"] is not True:raise RoutingError("reference only accepts synthetic occurrence")
  r=route.get((o["tenant_id"],o["namespace"],o["context_id"],o["context_version"]))
  action="ROUTE" if r and cells[r["cell_id"]]["state"]=="QUALIFIED_REFERENCE" else "ABSTAIN"
  events.append({"occurrence_id":o["occurrence_id"],"known_time":o["known_time"],"tenant_id":o["tenant_id"],"cell_id":r["cell_id"] if action=="ROUTE" else "","action":action,"reason":"QUALIFIED_ROUTE" if action=="ROUTE" else "NO_ELIGIBLE_ROUTE","side_effects_allowed":False})
 chain=hash_chain(events,"v440_route_event")
 return seal({"compiled_routes_hash":routes["compiled_routes_hash"],"events":chain,"event_count":len(chain),"routed_count":sum(x["action"]=="ROUTE" for x in chain),"abstained_count":sum(x["action"]=="ABSTAIN" for x in chain),"future_suffix_used":False,"live_side_effects":0,"research_only":True},"v440_route_ledger","ledger_id","ledger_hash")

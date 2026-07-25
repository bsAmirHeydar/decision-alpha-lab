from __future__ import annotations
from collections import Counter,defaultdict
from .canonical import seal,content_hash
def build_observability(registry:dict,placement:dict,health:dict,routes:dict,rollout:dict,journal:dict)->dict:
 tenants=Counter(x["tenant_id"] for x in registry["cells"]);domains=Counter(x["failure_domain"] for x in placement["assignments"]);states=Counter(x["state"] for x in registry["cells"])
 rows=[]
 h={x["cell_id"]:x for x in health["rows"]}
 for c in registry["cells"]:
  rows.append({"cell_id":c["cell_id"],"tenant_id":c["tenant_id"],"state":c["state"],"health_status":h[c["cell_id"]]["status"],"replica_count":c["replica_count"],"route_present":any(r["cell_id"]==c["cell_id"] for r in routes["routes"]),"rollout_eligible":c["cell_id"] in rollout["eligible_cells"],"control_events":sum(e["cell_id"]==c["cell_id"] for e in journal["events"])})
 alerts=[]
 for r in rows:
  if r["health_status"]!="HEALTHY":alerts.append({"alert_type":"UNHEALTHY_CELL","cell_id":r["cell_id"],"severity":"HIGH","automatic_action":"QUARANTINE"})
  if not r["route_present"]:alerts.append({"alert_type":"MISSING_ROUTE","cell_id":r["cell_id"],"severity":"MEDIUM","automatic_action":"ABSTAIN"})
 return seal({"phase":"SAED_V4_40","cell_rows":sorted(rows,key=lambda z:z["cell_id"]),"tenant_counts":dict(sorted(tenants.items())),"domain_replica_counts":dict(sorted(domains.items())),"registry_state_counts":dict(sorted(states.items())),"alerts":sorted(alerts,key=lambda z:(z["severity"],z["cell_id"])),"fleet_health_ratio":round(health["healthy_count"]/len(rows),8),"unknown_cells":0,"live_order_side_effects":0,"research_only":True},"v440_observability","observability_id","observability_hash")

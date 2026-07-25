from __future__ import annotations
from collections import defaultdict
from .errors import PlacementError,QuotaError
from .canonical import content_hash,seal
def place_fleet(registry:dict,catalog:dict,quotas:dict)->dict:
 classes={x["class_id"]:x for x in catalog["classes"]};domains=catalog["failure_domains"]
 quota={x["tenant_id"]:x for x in quotas["tenant_quotas"]};usage=defaultdict(lambda:{"cells":0,"replicas":0,"cpu":0,"memory":0})
 assignments=[];domain_usage=defaultdict(int)
 for cell in registry["cells"]:
  rc=classes.get(cell["resource_class"])
  if not rc:raise PlacementError("unknown resource class")
  q=quota[cell["tenant_id"]];u=usage[cell["tenant_id"]];u["cells"]+=1;u["replicas"]+=cell["replica_count"];u["cpu"]+=rc["cpu_units"]*cell["replica_count"];u["memory"]+=rc["memory_mb"]*cell["replica_count"]
  if u["cells"]>q["max_cells"] or u["replicas"]>q["max_replicas"] or u["cpu"]>q["max_cpu_units"] or u["memory"]>q["max_memory_mb"]:raise QuotaError("tenant quota exceeded")
  chosen=[]
  for replica in range(cell["replica_count"]):
   options=sorted(domains,key=lambda d:(domain_usage[d["domain_id"]],d["domain_id"]))
   d=next((x for x in options if domain_usage[x["domain_id"]]+rc["cpu_units"]<=x["capacity_units"] and x["domain_id"] not in chosen),None)
   if d is None:raise PlacementError("no failure-domain capacity")
   chosen.append(d["domain_id"]);domain_usage[d["domain_id"]]+=rc["cpu_units"]
   assignments.append({"cell_id":cell["cell_id"],"replica_ordinal":replica,"tenant_id":cell["tenant_id"],"resource_class":cell["resource_class"],"failure_domain":d["domain_id"],"cpu_units":rc["cpu_units"],"memory_mb":rc["memory_mb"],"placement_key":content_hash([cell["cell_id"],replica,d["domain_id"]])})
 if len(registry["cells"])>quotas["global_max_cells"] or len(assignments)>quotas["global_max_replicas"]:raise QuotaError("global quota exceeded")
 return seal({"registry_hash":registry["compiled_registry_hash"],"catalog_hash":catalog["frozen_catalog_hash"],"quota_hash":quotas["frozen_quota_hash"],"assignments":assignments,"assignment_count":len(assignments),"domain_usage":dict(sorted(domain_usage.items())),"deterministic":True,"overcommit":False,"research_only":True},"v440_placement","placement_id","placement_hash")

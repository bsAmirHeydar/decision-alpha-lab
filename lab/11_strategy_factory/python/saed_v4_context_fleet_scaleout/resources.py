from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,number,sorted_unique_strings
from .errors import QuotaError
from .canonical import content_hash,seal
def freeze_resource_catalog(v:dict)->dict:
 exact(v,["catalog_id","version","classes","failure_domains","scheduler_capacity","overcommit_allowed","research_only"])
 if v["overcommit_allowed"] is not False or v["research_only"] is not True:raise QuotaError("resource boundary invalid")
 classes=list_of(v["classes"],"classes",3);unique(classes,"class_id","classes")
 for c in classes:
  exact(c,["class_id","cpu_units","memory_mb","disk_mb","max_replicas","priority","requires_accelerator"])
  for k in ["cpu_units","memory_mb","disk_mb","max_replicas","priority"]:integer(c[k],k,1)
 domains=list_of(v["failure_domains"],"failure_domains",4);unique(domains,"domain_id","failure_domains")
 for d in domains:
  exact(d,["domain_id","region","zone","capacity_units","healthy"]);integer(d["capacity_units"],"capacity_units",1)
  if d["healthy"] is not True:raise QuotaError("reference domains must begin healthy")
 integer(v["scheduler_capacity"],"scheduler_capacity",64)
 x=deepcopy(v);x["classes"]=sorted(classes,key=lambda z:z["class_id"]);x["failure_domains"]=sorted(domains,key=lambda z:z["domain_id"]);x["catalog_hash"]=content_hash(x);return seal(x,"v440_resources","frozen_catalog_id","frozen_catalog_hash")
def freeze_quotas(v:dict,registry:dict)->dict:
 exact(v,["quota_id","version","tenant_quotas","global_max_cells","global_max_replicas","global_max_cpu_units","global_max_memory_mb","hard_enforcement","research_only"])
 if v["hard_enforcement"] is not True or v["research_only"] is not True:raise QuotaError("hard quota required")
 qs=list_of(v["tenant_quotas"],"tenant_quotas",2);unique(qs,"tenant_id","tenant_quotas")
 if set(x["tenant_id"] for x in qs)!=set(registry["tenants"]):raise QuotaError("tenant quota coverage mismatch")
 for q in qs:
  exact(q,["tenant_id","max_cells","max_replicas","max_cpu_units","max_memory_mb","max_rollout_concurrency","max_route_rps"])
  for k in ["max_cells","max_replicas","max_cpu_units","max_memory_mb","max_rollout_concurrency","max_route_rps"]:integer(q[k],k,1)
 for k in ["global_max_cells","global_max_replicas","global_max_cpu_units","global_max_memory_mb"]:integer(v[k],k,1)
 return seal(deepcopy(v),"v440_quotas","frozen_quota_id","frozen_quota_hash")

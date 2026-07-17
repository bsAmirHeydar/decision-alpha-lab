from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,integer,enum,sha256,sorted_unique_strings
from .errors import RegistryError
from .canonical import content_hash,seal
STATES={"REGISTERED","QUALIFIED_REFERENCE","QUARANTINED","RETIRED"}
def compile_registry(v:dict)->dict:
 exact(v,["registry_id","version","created_at","cells","tenants","namespaces","immutable","research_only"])
 if v["immutable"] is not True or v["research_only"] is not True:raise RegistryError("registry must be immutable research-only")
 cells=list_of(v["cells"],"cells",64);unique(cells,"cell_id","cells")
 tenants=sorted_unique_strings(v["tenants"],"tenants",2);namespaces=sorted_unique_strings(v["namespaces"],"namespaces",2)
 out=[]
 for c in cells:
  exact(c,["cell_id","context_id","context_version","tenant_id","namespace","runtime_bundle_hash","model_generation","treatment_universe_hash","environment_id","state","known_time_cutoff","replica_count","resource_class","failure_domain_policy","baseline_cell_id","mutable"])
  if c["tenant_id"] not in tenants or c["namespace"] not in namespaces:raise RegistryError("unknown tenant or namespace")
  sha256(c["runtime_bundle_hash"],"runtime_bundle_hash");sha256(c["treatment_universe_hash"],"treatment_universe_hash")
  enum(c["state"],STATES,"state");integer(c["context_version"],"context_version",1);integer(c["model_generation"],"model_generation",1);integer(c["replica_count"],"replica_count",1,8)
  if c["mutable"] is not False:raise RegistryError("cell mutable")
  out.append(deepcopy(c))
 if len({(x["tenant_id"],x["context_id"],x["context_version"]) for x in out})!=len(out):raise RegistryError("duplicate context version per tenant")
 x=deepcopy(v);x["cells"]=sorted(out,key=lambda z:z["cell_id"]);x["registry_hash"]=content_hash(x["cells"]);return seal(x,"v440_registry","compiled_registry_id","compiled_registry_hash")
def registry_index(registry:dict)->dict:
 by_tenant={}
 for c in registry["cells"]:by_tenant.setdefault(c["tenant_id"],[]).append(c["cell_id"])
 rows=[{"tenant_id":k,"cell_ids":sorted(v),"cell_count":len(v)} for k,v in sorted(by_tenant.items())]
 return seal({"registry_hash":registry["compiled_registry_hash"],"tenant_rows":rows,"cell_count":len(registry["cells"]),"tenant_count":len(rows),"research_only":True},"v440_registry_index","index_id","index_hash")

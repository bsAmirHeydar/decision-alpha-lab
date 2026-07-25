from __future__ import annotations
from .errors import IsolationError
from .canonical import seal,content_hash
def build_isolation_matrix(registry:dict)->dict:
 rows=[]
 tenant_counts={}
 namespace_counts={}
 for cell in registry["cells"]:
  tenant_counts[cell["tenant_id"]]=tenant_counts.get(cell["tenant_id"],0)+1
  namespace_counts[cell["namespace"]]=namespace_counts.get(cell["namespace"],0)+1
  rows.append({"cell_id":cell["cell_id"],"tenant_id":cell["tenant_id"],"namespace":cell["namespace"],"allowed_scope_hash":content_hash([cell["tenant_id"],cell["namespace"]]),"cross_tenant_allowed":False,"cross_namespace_allowed":False})
 n=len(rows);same_scope_pairs=sum(v*v for v in tenant_counts.values())
 return seal({"registry_hash":registry["compiled_registry_hash"],"rows_hash":content_hash(rows),"row_count":len(rows),"possible_pair_count":n*n,"allowed_same_tenant_pairs":same_scope_pairs,"denied_cross_tenant_pairs":n*n-same_scope_pairs,"tenant_counts":dict(sorted(tenant_counts.items())),"namespace_counts":dict(sorted(namespace_counts.items())),"cross_tenant_allowed":False,"cross_namespace_allowed":False,"rows":rows,"research_only":True},"v440_isolation","matrix_id","matrix_hash")
def assert_route_isolated(source:dict,target:dict):
 if source["tenant_id"]!=target["tenant_id"] or source["namespace"]!=target["namespace"]:raise IsolationError("cross-boundary routing denied")

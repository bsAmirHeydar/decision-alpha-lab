from __future__ import annotations
from collections import defaultdict
from .canonical import seal,content_hash
from .errors import DependencyError
def build_dependency_graph(registry:dict,routes:dict)->dict:
 route_by_cell={x["cell_id"]:x for x in routes["routes"]};nodes=[];edges=[]
 for c in registry["cells"]:
  cid=c["cell_id"];items=[("CELL",cid),("CONTEXT",f"{c['context_id']}@{c['context_version']}"),("MODEL",f"{c['context_id']}#G{c['model_generation']}"),("RUNTIME",c["runtime_bundle_hash"]),("TREATMENT_UNIVERSE",c["treatment_universe_hash"]),("TENANT",c["tenant_id"]),("NAMESPACE",c["namespace"])]
  for typ,nid in items:nodes.append({"node_id":f"{typ}:{nid}","node_type":typ,"tenant_id":c["tenant_id"],"immutable":True})
  for typ,nid in items[1:]:edges.append({"source":f"CELL:{cid}","target":f"{typ}:{nid}","edge_type":"DEPENDS_ON","tenant_id":c["tenant_id"]})
  r=route_by_cell.get(cid)
  if r:
   nodes.append({"node_id":f"ROUTE:{r['route_id']}","node_type":"ROUTE","tenant_id":c["tenant_id"],"immutable":True});edges.append({"source":f"ROUTE:{r['route_id']}","target":f"CELL:{cid}","edge_type":"ROUTES_TO","tenant_id":c["tenant_id"]})
 # de-duplicate deterministic
 nd={x["node_id"]:x for x in nodes};ed={content_hash(x):x for x in edges}
 return seal({"registry_hash":registry["compiled_registry_hash"],"nodes":sorted(nd.values(),key=lambda x:x["node_id"]),"edges":sorted(ed.values(),key=lambda x:(x["source"],x["target"])),"node_count":len(nd),"edge_count":len(ed),"cross_tenant_edges":0,"immutable":True,"research_only":True},"v441_dependencies","graph_id","graph_hash")
def impact_for_cells(graph:dict,cell_ids:list[str])->dict:
 wanted={f"CELL:{x}" for x in cell_ids};edges=[x for x in graph["edges"] if x["source"] in wanted or x["target"] in wanted];tenants={x["tenant_id"] for x in edges}
 if len(tenants)>len(cell_ids) and len(cell_ids)==1:raise DependencyError("unexpected cross-tenant impact")
 nodes=sorted({x["source"] for x in edges}|{x["target"] for x in edges})
 return seal({"graph_hash":graph["graph_hash"],"cell_ids":sorted(cell_ids),"affected_nodes":nodes,"affected_edges":edges,"affected_node_count":len(nodes),"cross_tenant_impact":False,"research_only":True},"v441_impact","impact_id","impact_hash")

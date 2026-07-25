from __future__ import annotations
from copy import deepcopy
from .contracts import require_exact,require_list,require_unique,require_sha256
from .errors import SBOMError
from .canonical import content_hash,seal

def build_sbom(models:dict,datasets:dict,dependencies:dict,tools:dict,runtimes:dict,services:dict)->dict:
    components=[]
    for registry,id_field,ctype in [(models,"model_id","machine-learning-model"),(datasets,"dataset_id","data"),(dependencies,"dependency_id","library"),(tools,"tool_id","application"),(runtimes,"runtime_id","container"),(services,"service_id","service")]:
        for r in registry["records"]:
            components.append({"component_id":r[id_field],"component_type":ctype,"version":r.get("version",r.get("image_ref","pinned")),"content_hash":r["content_hash"],"supplier_id":r.get("supplier_id",r.get("owner_id",r.get("builder_id","unknown"))),"license_id":r.get("license_id","INTERNAL"),"immutable":True})
    require_unique(components,"component_id","sbom.components")
    body={"phase":"SAED_V4_35","format":"CycloneDX-inspired-closed-reference","spec_version":"1.5-reference","serial_number":"pending","components":sorted(components,key=lambda x:x["component_id"]),"component_count":len(components),"complete":True,"research_only":True}
    body["serial_number"]="urn:uuid:"+content_hash(body)[:32]; return seal(body,"v435_sbom","sbom_id","sbom_hash")

def dependency_graph(dependencies:dict,runtimes:dict,edges:list[dict])->dict:
    nodes={r["dependency_id"] for r in dependencies["records"]}|{r["runtime_id"] for r in runtimes["records"]}
    edges=require_list(edges,"dependency_edges",1); out=[]
    for e in edges:
        require_exact(e,["source_id","target_id","relation","optional"])
        if e["source_id"] not in nodes or e["target_id"] not in nodes or e["source_id"]==e["target_id"]: raise SBOMError("dependency edge invalid")
        out.append(deepcopy(e))
    out=sorted(out,key=lambda x:(x["source_id"],x["target_id"],x["relation"]));
    # cycle check
    adj={n:[] for n in nodes}
    for e in out: adj[e["source_id"]].append(e["target_id"])
    state={}
    def visit(n):
        if state.get(n)==1: raise SBOMError("dependency cycle")
        if state.get(n)==2:return
        state[n]=1
        for q in sorted(adj[n]):visit(q)
        state[n]=2
    for n in sorted(nodes):visit(n)
    return seal({"phase":"SAED_V4_35","nodes":sorted(nodes),"edges":out,"node_count":len(nodes),"edge_count":len(out),"acyclic":True,"transitive_closure_required":True,"research_only":True},"v435_depgraph","graph_id","graph_hash")

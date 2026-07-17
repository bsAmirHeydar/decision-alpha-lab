from __future__ import annotations
from dataclasses import dataclass
from .types import Reason

@dataclass(frozen=True,slots=True)
class DependencyEdge:
    source_artifact_id:str
    target_artifact_id:str
    dependency_type:str
    optional:bool=False
    interface_id:str|None=None
    def to_dict(self):
        out={"source_artifact_id":self.source_artifact_id,"target_artifact_id":self.target_artifact_id,"dependency_type":self.dependency_type,"optional":self.optional}
        if self.interface_id: out["interface_id"]=self.interface_id
        return out

class DependencyGraph:
    def __init__(self,policies): self.policy=policies.documents["dependency_policy"]
    def validate(self,descriptors:dict,edges:list[DependencyEdge])->list[Reason]:
        reasons=[]; allowed=set(self.policy["allowed_types"]); ranks=self.policy["layer_ranks"]
        graph={k:[] for k in descriptors}
        seen=set()
        for e in edges:
            key=(e.source_artifact_id,e.target_artifact_id,e.dependency_type)
            if key in seen: reasons.append(Reason("DUPLICATE_DEPENDENCY_EDGE","Duplicate dependency edge.",{"edge":list(key)})); continue
            seen.add(key)
            if e.dependency_type not in allowed: reasons.append(Reason("DEPENDENCY_TYPE_UNKNOWN","Unknown dependency type.",{"type":e.dependency_type}))
            if e.source_artifact_id==e.target_artifact_id: reasons.append(Reason("SELF_DEPENDENCY","Artifact cannot depend on itself.",{"artifact_id":e.source_artifact_id})); continue
            if e.source_artifact_id not in descriptors or e.target_artifact_id not in descriptors:
                reasons.append(Reason("DEPENDENCY_ENDPOINT_UNRESOLVED","Dependency endpoint is missing.",{"source":e.source_artifact_id,"target":e.target_artifact_id})); continue
            src=descriptors[e.source_artifact_id]; dst=descriptors[e.target_artifact_id]
            if ranks.get(src.layer,-1)<ranks.get(dst.layer,-1): reasons.append(Reason("DEPENDENCY_DIRECTION_VIOLATION","Dependency points outward across architectural layers.",{"source_layer":src.layer,"target_layer":dst.layer}))
            if src.identity.tenant_id!=dst.identity.tenant_id and e.dependency_type!="external_contract": reasons.append(Reason("CROSS_TENANT_DEPENDENCY_DENIED","Cross-tenant dependencies require external_contract type.",{}))
            if dst.metadata.get("visibility")=="PRIVATE" and src.identity.namespace!=dst.identity.namespace: reasons.append(Reason("PRIVATE_IMPLEMENTATION_DEPENDENCY","Cross-namespace dependency on private implementation is forbidden.",{}))
            graph[e.source_artifact_id].append(e.target_artifact_id)
        color={k:0 for k in graph}
        def visit(node,stack):
            color[node]=1
            for nxt in graph[node]:
                if color[nxt]==0: visit(nxt,stack+[node])
                elif color[nxt]==1: reasons.append(Reason("DEPENDENCY_CYCLE","Hard dependency cycle detected.",{"cycle":stack+[node,nxt]}))
            color[node]=2
        for n in sorted(graph):
            if color[n]==0: visit(n,[])
        return reasons

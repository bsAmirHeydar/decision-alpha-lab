from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from .canonical import digest_object
from .types import Reason

@dataclass(frozen=True,slots=True)
class LineageEdge:
    edge_id:str
    source_artifact_id:str
    target_artifact_id:str
    edge_type:str
    transformation_id:str|None
    recorded_at:datetime
    metadata:dict
    def to_dict(self):
        return {"edge_id":self.edge_id,"source_artifact_id":self.source_artifact_id,"target_artifact_id":self.target_artifact_id,"edge_type":self.edge_type,"transformation_id":self.transformation_id,"recorded_at":self.recorded_at.astimezone(timezone.utc).isoformat().replace("+00:00","Z"),"metadata":self.metadata}

class LineageGraph:
    def __init__(self,policies): self.policy=policies.documents["lineage_edge_types"]
    def validate(self,descriptors:dict,edges:list[LineageEdge])->list[Reason]:
        reasons=[]; specs=self.policy["edge_types"]; ids=set(); directed={k:[] for k in descriptors}
        for e in edges:
            if e.edge_id in ids: reasons.append(Reason("DUPLICATE_LINEAGE_EDGE_ID","Lineage edge IDs must be unique.",{"edge_id":e.edge_id}))
            ids.add(e.edge_id)
            if e.edge_type not in specs: reasons.append(Reason("LINEAGE_EDGE_TYPE_UNKNOWN","Unknown lineage edge type.",{"edge_type":e.edge_type})); continue
            if e.source_artifact_id not in descriptors or e.target_artifact_id not in descriptors: reasons.append(Reason("LINEAGE_ENDPOINT_UNRESOLVED","Lineage endpoint is missing.",{})); continue
            if specs[e.edge_type].get("requires_transformation") and not e.transformation_id: reasons.append(Reason("LINEAGE_TRANSFORMATION_MISSING","Lineage edge requires transformation identity.",{"edge_type":e.edge_type}))
            if specs[e.edge_type].get("acyclic",True): directed[e.source_artifact_id].append(e.target_artifact_id)
        color={k:0 for k in directed}
        def visit(n,path):
            color[n]=1
            for x in directed[n]:
                if color[x]==0: visit(x,path+[n])
                elif color[x]==1: reasons.append(Reason("LINEAGE_CYCLE","Derivation lineage must be acyclic.",{"cycle":path+[n,x]}))
            color[n]=2
        for n in sorted(directed):
            if color[n]==0: visit(n,[])
        return reasons

    @staticmethod
    def snapshot_digest(edges:list[LineageEdge])->str:
        return digest_object([e.to_dict() for e in sorted(edges,key=lambda x:x.edge_id)])

from __future__ import annotations
from collections import defaultdict,deque
from .models import LineageEdge
from .canonical import content_hash,merkle_root
from .errors import LineageCycleError,ImmutableConflict
class LineageGraph:
    def __init__(self): self._edges:dict[str,LineageEdge]={}; self._children=defaultdict(set); self._parents=defaultdict(set)
    def add(self,edge:LineageEdge)->str:
        if edge.edge_id in self._edges:
            if self._edges[edge.edge_id]!=edge: raise ImmutableConflict('lineage edge id conflict')
            return edge.edge_id
        if edge.parent_artifact_id==edge.child_artifact_id: raise LineageCycleError('self-cycle')
        self._children[edge.parent_artifact_id].add(edge.child_artifact_id); self._parents[edge.child_artifact_id].add(edge.parent_artifact_id)
        if self._reachable(edge.child_artifact_id,edge.parent_artifact_id):
            self._children[edge.parent_artifact_id].remove(edge.child_artifact_id); self._parents[edge.child_artifact_id].remove(edge.parent_artifact_id)
            raise LineageCycleError('lineage cycle detected')
        self._edges[edge.edge_id]=edge; return edge.edge_id
    def _reachable(self,start,target):
        q=deque([start]); seen=set()
        while q:
            n=q.popleft()
            if n==target:return True
            if n in seen:continue
            seen.add(n); q.extend(self._children[n])
        return False
    def ancestors(self,node:str)->set[str]:
        out=set(); q=deque(self._parents[node])
        while q:
            n=q.popleft()
            if n in out:continue
            out.add(n);q.extend(self._parents[n])
        return out
    def edges(self): return tuple(self._edges[k] for k in sorted(self._edges))
    def root_hash(self)->str: return merkle_root(content_hash(e.__dict__) for e in self.edges())

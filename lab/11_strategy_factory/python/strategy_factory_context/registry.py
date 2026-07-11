from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol
from strategy_factory_contracts.hashing import stable_id
from strategy_factory_contracts.records import AnatomyEvent, FeatureValue
from .descriptor import FeatureDescriptor
class FeatureGraphError(ValueError): pass
class FeatureNode(Protocol):
    descriptor: FeatureDescriptor
    def compute(self,event:AnatomyEvent,state:"ContextState")->FeatureValue: ...
@dataclass(slots=True)
class FeatureRegistry:
    _nodes:dict[str,FeatureNode]
    _order:tuple[str,...]=()
    _graph_hash:str=''
    def __init__(self):self._nodes={};self._order=();self._graph_hash=''
    def register(self,node:FeatureNode)->None:
        d=node.descriptor
        if d.feature_id in self._nodes:raise FeatureGraphError(f'duplicate feature owner: {d.feature_id}')
        self._nodes[d.feature_id]=node;self._order=();self._graph_hash=''
    def compile(self)->tuple[str,...]:
        if not self._nodes:raise FeatureGraphError('feature registry is empty')
        for node in self._nodes.values():
            for dep in node.descriptor.dependencies:
                if dep not in self._nodes:raise FeatureGraphError(f'missing feature dependency: {dep}')
        indegree={k:len(v.descriptor.dependencies) for k,v in self._nodes.items()};remaining=set(self._nodes);order=[]
        while remaining:
            ready=sorted(k for k in remaining if indegree[k]==0)
            if not ready:raise FeatureGraphError('feature dependency cycle detected')
            current=ready[0];remaining.remove(current);order.append(current)
            for k in remaining:
                if current in self._nodes[k].descriptor.dependencies:indegree[k]-=1
        self._order=tuple(order);canonical='|'.join(self._nodes[k].descriptor.canonical for k in self._order);self._graph_hash=stable_id('fdag',canonical);return self._order
    @property
    def order(self)->tuple[str,...]:
        if not self._order:return self.compile()
        return self._order
    @property
    def graph_hash(self)->str:
        if not self._graph_hash:self.compile()
        return self._graph_hash
    def node(self,feature_id:str)->FeatureNode:return self._nodes[feature_id]
    def descriptor(self,feature_id:str)->FeatureDescriptor:return self._nodes[feature_id].descriptor
    def validate_vector_fields(self,fields)->None:
        for f in fields:
            if f.feature_id not in self._nodes:raise FeatureGraphError(f'vector feature not registered: {f.feature_id}')
            if self.descriptor(f.feature_id).value_type is not f.expected_type:raise FeatureGraphError(f'vector feature type mismatch: {f.feature_id}')
from typing import TYPE_CHECKING
if TYPE_CHECKING:from .state import ContextState

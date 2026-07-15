from __future__ import annotations
from .canonical import content_hash
from .models import CostModel,CostBreakdown
from .errors import ContractError
class CostRegistry:
    def __init__(self,models:list[CostModel]):
        if not models:raise ContractError('empty cost registry')
        keys=[(m.model_id,m.exact_version) for m in models]
        if len(keys)!=len(set(keys)):raise ContractError('duplicate cost model')
        self._items={k:m for k,m in zip(keys,models)}
        self.registry_hash=content_hash([m.semantic_payload() for m in sorted(models,key=lambda x:(x.model_id,x.exact_version))])
    @classmethod
    def from_mapping(cls,x):return cls([CostModel.from_mapping(m) for m in x['models']])
    def resolve(self,model_id,version):
        try:return self._items[(model_id,version)]
        except KeyError as e:raise ContractError('unknown cost model') from e

def compute_cost(model:CostModel,risk_points:float,entry_spread:float,exit_spread:float)->CostBreakdown:
    if risk_points<=0:raise ContractError('risk_points must be positive')
    es=max(0.0,entry_spread)*model.spread_multiplier;xs=max(0.0,exit_spread)*model.spread_multiplier
    points=es+xs+model.entry_slippage_points+model.exit_slippage_points
    total_r=points/risk_points+model.commission_r+model.other_r
    return CostBreakdown(es,xs,model.entry_slippage_points,model.exit_slippage_points,model.commission_r,model.other_r,points,total_r,model.model_hash)

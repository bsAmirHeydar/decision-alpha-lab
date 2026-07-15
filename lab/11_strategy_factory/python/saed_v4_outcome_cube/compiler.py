from __future__ import annotations
from typing import Any
from .models import ContextSnapshot,ExecutionSpec
from .errors import ContractError

def _component(node:dict[str,Any],slot:str)->dict[str,Any]|None:
    items=[c for c in node.get('instantiated_components',[]) if c.get('slot')==slot]
    if len(items)>1: raise ContractError(f'duplicate component slot {slot}')
    return items[0] if items else None

def compile_spec(node:dict[str,Any],context:ContextSnapshot)->ExecutionSpec:
    action=node['action_class']; hashes=tuple(sorted(c['component_hash'] for c in node.get('instantiated_components',[])))
    if action in ('skip','abstain'):
        return ExecutionSpec(node['node_id'],node['node_hash'],action,context.direction,None,None,None,None,None,None,None,0,0.0,0.0,0.0,hashes)
    f=context.feature_map(); entry=_component(node,'entry'); stop=_component(node,'stop'); target=_component(node,'target'); exit_c=_component(node,'exit'); management=_component(node,'management'); trail=_component(node,'trail'); trigger=_component(node,'trigger')
    if not entry or not stop: raise ContractError('ordinary node requires entry and stop')
    ep=entry['parameters']; sp=stop['parameters']
    eref=str(ep['reference_feature']); sref=str(sp['reference_feature'])
    if eref not in f or sref not in f: raise ContractError('required reference feature missing')
    ebuf=float(ep.get('buffer_points',0)); sbuf=float(sp.get('buffer_points',0)); direction=context.direction
    entry_price=float(f[eref])+direction*ebuf; stop_price=float(f[sref])-direction*sbuf
    risk=(entry_price-stop_price)*direction
    if risk<=0: raise ContractError('non-positive initial risk')
    target_price=None
    if target:
        reward=float(target['parameters']['reward_r']);target_price=entry_price+direction*reward*risk
    ttl=int(ep.get('ttl_ms',0)); expiration=context.decision_time_ms+ttl if ttl>0 else context.decision_time_ms
    max_holding=int((exit_c or {'parameters':{}})['parameters'].get('maximum_holding_ms',0))
    partial=float((management or {'parameters':{}})['parameters'].get('quantity_fraction',0));partial_activation=float((management or {'parameters':{}})['parameters'].get('activation_r',0));trail_activation=float((trail or {'parameters':{}})['parameters'].get('activation_r',0))
    tref=top=None;texp=None
    if trigger:
        p=trigger['parameters'];tref=str(p.get('feature_ref'));top=str(p.get('operator'));texp=p.get('expected_value')
    return ExecutionSpec(node['node_id'],node['node_hash'],action,direction,tref,top,texp,entry_price,expiration,stop_price,target_price,max_holding,partial,partial_activation,trail_activation,hashes)

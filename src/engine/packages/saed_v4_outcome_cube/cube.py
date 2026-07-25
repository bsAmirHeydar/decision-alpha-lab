from __future__ import annotations
from typing import Any
from .authority import assert_evidence_role
from .canonical import content_hash,stable_id
from .compiler import compile_spec
from .costs import CostRegistry
from .exposure import build_exposure
from .models import ContextSnapshot,PriceObservation,OutcomePolicy,OutcomeCube
from .simulator import simulate
from .errors import ContractError,IntegrityError

def validate_upstream(lattice:dict[str,Any],handoff:dict[str,Any])->None:
    if handoff['phase']!='SAED_V4_07' or handoff['next_phase']!='SAED_V4_08':raise ContractError('invalid upstream handoff')
    if lattice['lattice_hash']!=handoff['lattice_hash']:raise IntegrityError('lattice hash does not match handoff')
    if lattice.get('selection_authority') or lattice.get('execution_authority'):raise ContractError('upstream lattice authority violation')
    if lattice.get('outcome_semantics')!='none':raise ContractError('upstream lattice already contains outcome semantics')

def build_cube(lattice:dict[str,Any],handoff:dict[str,Any],context:ContextSnapshot,observations:list[PriceObservation],policy:OutcomePolicy,cost_registry:CostRegistry,cost_model_id:str,cost_model_version:str)->OutcomeCube:
    validate_upstream(lattice,handoff);assert_evidence_role(context.evidence_role)
    if context.evidence_role not in policy.allowed_evidence_roles:raise ContractError('evidence role blocked by outcome policy')
    if len(lattice['nodes'])>policy.maximum_rows:raise ContractError('row budget exceeded')
    if policy.require_skip_and_abstain and not(lattice.get('contains_skip') and lattice.get('contains_abstain')):raise ContractError('mandatory Skip/Abstain absent')
    model=cost_registry.resolve(cost_model_id,cost_model_version)
    rows=[]
    for node in sorted(lattice['nodes'],key=lambda n:n['node_id']):
        spec=compile_spec(node,context);rows.append(simulate(spec,context,observations,policy,model))
    exposure=build_exposure(lattice['nodes'],rows)
    if policy.require_complete_exposure and not exposure['complete']:raise IntegrityError('incomplete outcome exposure')
    ordinary=sum(r.action_class=='ordinary' for r in rows);skip=sum(r.action_class=='skip' for r in rows);abstain=sum(r.action_class=='abstain' for r in rows)
    start=min((o.observed_at_ms for o in observations),default=context.decision_time_ms);end=max((o.observed_at_ms for o in observations),default=context.decision_time_ms)
    base={'phase':'SAED_V4_08','version':'1.0.0','context_snapshot_id':context.snapshot_id,'context_snapshot_hash':context.snapshot_hash,'source_lattice_id':lattice['lattice_id'],'source_lattice_hash':lattice['lattice_hash'],'source_handoff_hash':handoff['handoff_hash'],'policy_id':policy.policy_id,'policy_hash':policy.policy_hash,'cost_registry_hash':cost_registry.registry_hash,'evidence_role':context.evidence_role,'known_as_of':context.known_as_of,'decision_time_ms':context.decision_time_ms,'observation_window_start_ms':start,'observation_window_end_ms':end,'row_count':len(rows),'ordinary_row_count':ordinary,'skip_row_count':skip,'abstain_row_count':abstain,'complete_exposure':exposure['complete'],'selection_authority':False,'execution_authority':False,'ranking_semantics':'none','rows':[dict(r.semantic_payload(),row_id=r.row_id,row_hash=r.row_hash) for r in rows],'exposure_ledger':exposure,'limitations':['Counterfactual path outcomes are conditional on frozen path, cost and ambiguity policy.','Rows are not rankings, recommendations, capital allocations or live orders.','Real alpha, external reproduction, runtime parity and production authorization are not claimed.']}
    ch=content_hash(base);cid=stable_id('outcomecube',base)
    return OutcomeCube(cube_id=cid,cube_hash=ch,rows=tuple(rows),limitations=tuple(base['limitations']),exposure_ledger=exposure,**{k:v for k,v in base.items() if k not in ('rows','limitations','exposure_ledger')})

from __future__ import annotations
from .contracts import AdapterConfig,ModelIntake,CandidateSpec,Disclosure,DomainShiftPolicy,ComputeExposureBudget
from .errors import ContractError,IntegrityError

def validate_config(x): return AdapterConfig.from_mapping(x)
def validate_intakes(xs):
    out=tuple(ModelIntake.from_mapping(x) for x in xs); ids=[x.intake_id for x in out]
    if len(ids)!=len(set(ids)): raise ContractError('duplicate intake id')
    if not any(x.enabled for x in out): raise ContractError('no enabled intake')
    return out

def validate_candidates(xs,intakes):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs); ids=[x.candidate_id for x in out]; intake_by={x.intake_id:x for x in intakes}
    if len(ids)!=len(set(ids)): raise ContractError('duplicate candidate id')
    if not any(x.enabled for x in out): raise ContractError('no enabled candidate')
    for c in out:
        if c.intake_id not in intake_by or intake_by[c.intake_id].family!=c.family: raise ContractError('candidate intake binding mismatch')
    return out

def validate_disclosures(xs,intakes):
    out=tuple(Disclosure.from_mapping(x) for x in xs); ids=[x.disclosure_id for x in out]; intake_ids={x.intake_id for x in intakes}
    if len(ids)!=len(set(ids)) or {x.intake_id for x in out}!=intake_ids: raise ContractError('disclosure coverage mismatch')
    return out

def validate_domain_shift_policy(x): return DomainShiftPolicy.from_mapping(x)
def validate_budget(x): return ComputeExposureBudget.from_mapping(x)

def validate_upstream(handoff,registry,embeddings,compiled_graph,tournament):
    if handoff.get('phase')!='SAED_V4_13' or handoff.get('next_phase')!='SAED_V4_14': raise IntegrityError('wrong upstream handoff')
    if handoff.get('graph_checkpoint_registry_hash')!=registry.get('registry_hash'): raise IntegrityError('V4-13 registry hash mismatch')
    if handoff.get('compiled_graph_hash')!=compiled_graph.get('compiled_graph_hash'): raise IntegrityError('V4-13 compiled graph hash mismatch')
    if handoff.get('reference_champion_id')!=tournament.get('reference_champion_id'): raise IntegrityError('V4-13 champion mismatch')
    if handoff.get('reference_champion_id') not in {x['candidate_id'] for x in embeddings.get('candidates',[])}: raise IntegrityError('champion embedding missing')
    gates=handoff.get('entry_gates',{}); required={'frozen_upstream_binding_verified','known_time_graph_compilation_passed','future_suffix_forbidden','outcome_supervision_absent','deterministic_replay_passed','baseline_preserved','graph_registry_admitted'}
    if set(gates)!=required or not all(gates.values()): raise IntegrityError('V4-13 handoff gates not closed')
    auth=handoff.get('authority',{})
    if auth.get('read_frozen_graph_embeddings') is not True or auth.get('read_frozen_graph_registry') is not True or auth.get('build_reference_foundation_model_adapters') is not True: raise IntegrityError('V4-13 authority missing')
    forbidden=['mutate_v4_13_evidence','predict_outcomes','rank_treatments','select_treatment','allocate_risk','activate_runtime','send_order']
    if any(auth.get(k) is not False for k in forbidden): raise IntegrityError('upstream authority boundary widened')
    return {'phase':'SAED_V4_14','passed':True,'v4_13_handoff_hash':handoff['handoff_hash'],'v4_13_registry_hash':registry['registry_hash'],'v4_13_compiled_graph_hash':compiled_graph['compiled_graph_hash'],'v4_13_reference_champion_id':handoff['reference_champion_id'],'gate_count':len(required),'frozen':True}

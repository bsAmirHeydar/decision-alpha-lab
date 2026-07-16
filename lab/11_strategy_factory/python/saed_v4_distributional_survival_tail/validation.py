from __future__ import annotations
from .contracts import EventDefinitionRegistry,CensoringPolicy,DatasetSpec,ModelConfig,CandidateSpec,TailPolicy,ComputeExposureBudget
from .errors import ContractError,IntegrityError

def validate_event_registry(x):return EventDefinitionRegistry.from_mapping(x)
def validate_censoring_policy(x):return CensoringPolicy.from_mapping(x)
def validate_dataset_spec(x):return DatasetSpec.from_mapping(x)
def validate_model_config(x):return ModelConfig.from_mapping(x)
def validate_tail_policy(x):return TailPolicy.from_mapping(x)
def validate_budget(x):return ComputeExposureBudget.from_mapping(x)
def validate_candidates(xs):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs);ids=[x.candidate_id for x in out]
    if len(ids)!=len(set(ids)) or not any(x.enabled for x in out):raise ContractError('candidate identity or coverage failure')
    if sum(x.algorithm=='empirical_km_baseline' and x.enabled for x in out)!=1:raise ContractError('exactly one empirical/KM baseline required')
    return out

def validate_upstream(handoff,registry,fusion_outputs,aligned,integrity):
    if handoff.get('phase')!='SAED_V4_15' or handoff.get('next_phase')!='SAED_V4_16':raise IntegrityError('wrong V4-15 handoff')
    if handoff.get('fusion_checkpoint_registry_hash')!=registry.get('registry_hash'):raise IntegrityError('V4-15 registry hash mismatch')
    if handoff.get('aligned_view_set_hash')!=aligned.get('aligned_set_hash'):raise IntegrityError('V4-15 aligned view hash mismatch')
    if handoff.get('integrity_receipt_hash')!=integrity.get('receipt_hash'):raise IntegrityError('V4-15 integrity hash mismatch')
    champion=handoff.get('reference_champion_id')
    if champion!=registry.get('reference_champion_id') or champion not in {x.get('candidate_id') for x in fusion_outputs.get('items',[])}:raise IntegrityError('V4-15 champion binding failure')
    gates=handoff.get('entry_gates',{});required={'all_domain_subsets_bounded','all_foundation_subsets_bounded','baseline_preserved','deterministic_replay_passed','explicit_missingness_passed','frozen_upstream_binding_verified','fusion_registry_admitted','future_suffix_forbidden','known_time_alignment_passed','outcome_supervision_absent'}
    if set(gates)!=required or not all(gates.values()):raise IntegrityError('V4-15 entry gates not closed')
    auth=handoff.get('authority',{});allowed={'read_frozen_fusion_features','read_frozen_fusion_registry','build_reference_distributional_survival_tail_models'}
    if any(auth.get(k) is not True for k in allowed):raise IntegrityError('V4-15 read authority missing')
    forbidden={'mutate_v4_15_evidence','predict_outcomes','rank_treatments','select_treatment','allocate_risk','activate_runtime','send_order'}
    if any(auth.get(k) is not False for k in forbidden):raise IntegrityError('V4-15 authority widened')
    output=next(x for x in fusion_outputs['items'] if x['candidate_id']==champion)
    if output.get('production_eligible') or output.get('known_as_of')!=aligned.get('known_as_of'):raise IntegrityError('invalid frozen fusion output')
    return {'phase':'SAED_V4_16','passed':True,'v4_15_handoff_hash':handoff['handoff_hash'],'v4_15_registry_hash':registry['registry_hash'],'v4_15_fusion_hash':output['fusion_hash'],'v4_15_aligned_set_hash':aligned['aligned_set_hash'],'v4_15_integrity_receipt_hash':integrity['receipt_hash'],'reference_fusion_candidate_id':champion,'known_as_of':output['known_as_of'],'feature_dim':len(output['fused_embedding']),'frozen':True}

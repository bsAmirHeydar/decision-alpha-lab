from .contracts import FusionConfig,CandidateSpec,SupportPolicy,MissingnessPolicy,ComputeExposureBudget
from .errors import ContractError,IntegrityError

def validate_config(x): return FusionConfig.from_mapping(x)
def validate_candidates(xs):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs);ids=[x.candidate_id for x in out]
    if len(ids)!=len(set(ids)) or not any(x.enabled for x in out): raise ContractError('candidate identity/coverage failure')
    if sum(x.algorithm=='late_mean_baseline' and x.enabled for x in out)!=1: raise ContractError('exactly one enabled baseline required')
    return out

def validate_support_policy(x): return SupportPolicy.from_mapping(x)
def validate_missingness_policy(x): return MissingnessPolicy.from_mapping(x)
def validate_budget(x): return ComputeExposureBudget.from_mapping(x)

def validate_upstream(v414_handoff,v414_registry,v414_features,v414_tokens,v414_calibration,v414_domain,v414_tournament,v404_package,v404_handoff):
    if v414_handoff.get('phase')!='SAED_V4_14' or v414_handoff.get('next_phase')!='SAED_V4_15': raise IntegrityError('wrong V4-14 handoff')
    if v414_handoff.get('foundation_checkpoint_registry_hash')!=v414_registry.get('registry_hash'): raise IntegrityError('V4-14 registry hash mismatch')
    if v414_handoff.get('source_token_sequence_hash')!=v414_tokens.get('token_sequence_hash'): raise IntegrityError('V4-14 token hash mismatch')
    if v414_handoff.get('calibration_report_hash')!=v414_calibration.get('report_hash') or v414_handoff.get('domain_shift_report_hash')!=v414_domain.get('report_hash'): raise IntegrityError('V4-14 diagnostic hash mismatch')
    if v414_handoff.get('reference_champion_id')!=v414_tournament.get('reference_champion_id'): raise IntegrityError('V4-14 champion mismatch')
    if v414_handoff.get('reference_champion_id') not in {x['candidate_id'] for x in v414_features.get('items',[])}: raise IntegrityError('V4-14 champion feature missing')
    gates=v414_handoff.get('entry_gates',{});required={'baseline_preserved','deterministic_replay_passed','fail_closed_fallback_verified','foundation_registry_admitted','frozen_v4_13_binding_verified','future_suffix_forbidden','known_time_tokenization_passed','model_intake_closed','outcome_supervision_absent','pretraining_contamination_reviewed','supply_chain_attested'}
    if set(gates)!=required or not all(gates.values()): raise IntegrityError('V4-14 entry gates not closed')
    auth=v414_handoff.get('authority',{});allowed={'read_frozen_foundation_features','read_frozen_foundation_registry','build_reference_multimodal_fusion'}
    if any(auth.get(k) is not True for k in allowed): raise IntegrityError('V4-14 read authority missing')
    forbidden={'mutate_v4_14_evidence','predict_outcomes','rank_treatments','select_treatment','allocate_risk','activate_runtime','send_order','invoke_remote_model','load_unapproved_external_weights'}
    if any(auth.get(k) is not False for k in forbidden): raise IntegrityError('V4-14 authority widened')
    if v404_handoff.get('phase')!='SAED_V4_04' or v404_handoff.get('package_hash')!=v404_package.get('package_hash'): raise IntegrityError('V4-04 package heritage mismatch')
    if v404_package.get('known_as_of')!=v414_tokens.get('known_as_of'): raise IntegrityError('known-time alignment mismatch')
    if v404_package.get('compatibility',{}).get('status')!='compatible': raise IntegrityError('V4-04 view package incompatible')
    return {'phase':'SAED_V4_15','passed':True,'v4_14_handoff_hash':v414_handoff['handoff_hash'],'v4_14_registry_hash':v414_registry['registry_hash'],'v4_14_token_sequence_hash':v414_tokens['token_sequence_hash'],'v4_04_package_hash':v404_package['package_hash'],'known_as_of':v414_tokens['known_as_of'],'foundation_candidate_count':len(v414_features['items']),'domain_view_count':len(v404_package['views']),'frozen':True}

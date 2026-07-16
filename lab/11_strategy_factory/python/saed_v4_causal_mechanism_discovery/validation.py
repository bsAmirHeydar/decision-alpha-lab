from __future__ import annotations
from .contracts import VariableRegistry,EnvironmentRegistry,GraphConstraints,DiscoveryConfig,CandidateSpec,ComputeExposureBudget
from .errors import ContractError,IntegrityError

def validate_variable_registry(x):return VariableRegistry.from_mapping(x)
def validate_environment_registry(x):return EnvironmentRegistry.from_mapping(x)
def validate_graph_constraints(x):return GraphConstraints.from_mapping(x)
def validate_discovery_config(x):return DiscoveryConfig.from_mapping(x)
def validate_budget(x):return ComputeExposureBudget.from_mapping(x)
def validate_candidates(xs):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs);ids=[x.candidate_id for x in out]
    if len(ids)!=len(set(ids)) or not any(x.enabled for x in out):raise ContractError('candidate identity or coverage failure')
    if sum(x.algorithm=='correlation_baseline' and x.enabled for x in out)!=1:raise ContractError('exactly one correlation baseline required')
    return out

def validate_upstream(handoff,dataset,checkpoint_registry,integrity,tail_cal,time_cal):
    if handoff.get('phase')!='SAED_V4_16' or handoff.get('next_phase')!='SAED_V4_17':raise IntegrityError('wrong V4-16 handoff')
    if handoff.get('survival_dataset_hash')!=dataset.get('dataset_hash'):raise IntegrityError('V4-16 dataset hash mismatch')
    if handoff.get('model_checkpoint_registry_hash')!=checkpoint_registry.get('registry_hash'):raise IntegrityError('V4-16 registry hash mismatch')
    if handoff.get('integrity_receipt_hash')!=integrity.get('receipt_hash'):raise IntegrityError('V4-16 integrity mismatch')
    if handoff.get('tail_calibration_report_hash')!=tail_cal.get('report_hash') or handoff.get('time_calibration_report_hash')!=time_cal.get('report_hash'):raise IntegrityError('V4-16 calibration binding failure')
    gates=handoff.get('entry_gates',{});required={'baseline_preserved','censoring_audited','competing_risk_simplex_verified','deterministic_replay_passed','distribution_calibration_bounded','event_registry_frozen','future_suffix_forbidden','known_time_dataset_passed','quantile_crossing_eliminated','tail_stress_suite_passed','upstream_v4_15_binding_verified'}
    if set(gates)!=required or not all(gates.values()):raise IntegrityError('V4-16 entry gates not closed')
    auth=handoff.get('authority',{})
    if auth.get('read_frozen_distributional_survival_tail_evidence') is not True or auth.get('build_reference_causal_mechanism_discovery') is not True:raise IntegrityError('V4-16 read authority missing')
    for key in ['mutate_v4_16_evidence','assert_causality','rank_treatments','select_treatment','allocate_risk','sign_promotion','activate_runtime','send_order']:
        if auth.get(key) is not False:raise IntegrityError('V4-16 authority widened')
    if not dataset.get('synthetic_only') or dataset.get('protected_evidence_exposures')!=0 or not dataset.get('known_time_ordered'):raise IntegrityError('upstream evidence role invalid')
    return {'phase':'SAED_V4_17','passed':True,'v4_16_handoff_hash':handoff['handoff_hash'],'v4_16_dataset_hash':dataset['dataset_hash'],'v4_16_registry_hash':checkpoint_registry['registry_hash'],'v4_16_integrity_receipt_hash':integrity['receipt_hash'],'v4_16_tail_calibration_hash':tail_cal['report_hash'],'v4_16_time_calibration_hash':time_cal['report_hash'],'reference_v4_16_champion_id':handoff['reference_champion_id'],'row_count':dataset['row_count'],'feature_dim':dataset['feature_dim'],'synthetic_only':True,'frozen':True}

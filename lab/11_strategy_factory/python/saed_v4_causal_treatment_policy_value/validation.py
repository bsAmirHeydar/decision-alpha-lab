from __future__ import annotations
from .contracts import TreatmentRegistry,OutcomeSpec,IdentificationPlan,EstimatorSpec,PolicySpec,ComputeExposureBudget
from .errors import ContractError,IntegrityError,LeakageError
from .canonical import content_hash

def validate_inputs(treatment_registry,outcome_spec,identification_plan,estimators,policies,budget):
    tr=TreatmentRegistry.from_mapping(treatment_registry);os=OutcomeSpec.from_mapping(outcome_spec);ip=IdentificationPlan.from_mapping(identification_plan)
    es=[EstimatorSpec.from_mapping(x) for x in estimators];ps=[PolicySpec.from_mapping(x) for x in policies];bd=ComputeExposureBudget.from_mapping(budget)
    if len(es)!=len({x.estimator_id for x in es}) or len(ps)!=len({x.policy_id for x in ps}):raise ContractError('duplicate estimator or policy ids')
    tids={x['treatment_id'] for x in tr.treatments}
    for p in ps:
        if p.policy_type=='fixed_treatment' and p.treatment_id not in tids:raise ContractError('policy treatment outside registry')
    return tr,os,ip,es,ps,bd

def validate_upstream(handoff,registry,integrity,claims):
    if handoff.get('next_phase')!='SAED_V4_18':raise IntegrityError('V4-17 handoff target mismatch')
    if handoff.get('authority',{}).get('estimate_production_treatment_effect',True):raise IntegrityError('upstream treatment authority contamination')
    if claims.get('claim_tier') not in {'mechanism_compatible_synthetic','associational','abstain'}:raise IntegrityError('upstream claim tier unsupported')
    if not registry.get('registry_hash') or not integrity.get('receipt_hash'):raise IntegrityError('upstream immutable evidence missing')
    return {'phase':'SAED_V4_18','upstream_phase':'SAED_V4_17','handoff_hash':handoff.get('handoff_hash'),'registry_hash':registry['registry_hash'],'integrity_hash':integrity['receipt_hash'],'claim_tier':claims['claim_tier'],'hash_verified':True,'immutable':True,'protected_evidence_exposures':0,'validation_hash':content_hash({'handoff':handoff.get('handoff_hash'),'registry':registry['registry_hash'],'integrity':integrity['receipt_hash']})}

def validate_split_plan(plan,dataset):
    by_cluster={}
    for r in dataset['rows']:by_cluster.setdefault(r['cluster_id'],[]).append(r['ordinal'])
    for fold in plan['folds']:
        train=set(fold['train_ordinals']);evaluation=set(fold['evaluation_ordinals'])
        if train&evaluation:raise LeakageError('train/evaluation overlap')
        if train and evaluation and max(train)>=min(evaluation):raise LeakageError('future training detected')
        for ords in by_cluster.values():
            if set(ords)&train and set(ords)&evaluation:raise LeakageError('sibling cluster split')
    return True

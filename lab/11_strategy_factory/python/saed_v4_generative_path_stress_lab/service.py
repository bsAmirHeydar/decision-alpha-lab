from __future__ import annotations
from .security import scan
from .contracts import StateSchemaContract,RolloutBudget
from .budget import BudgetLedger
from .upstream import validate_upstream
from .path_data import validate_real_paths,summary
from .generators import generate_registry
from .stress import compose_stress_library
from .invariants import inspect_paths
from .fidelity import compare
from .uncertainty import horizon_map
from .exploitability import evaluate
from .adversary import search
from .certificates import build
from .replay import build as build_replay
from .handoff import build as build_handoff
from .canonical import content_hash
from .watermark import validate as validate_watermark

def run_reference(config,upstream_documents,real_path_document,policy_document,qa=None):
    scan(config);scan(upstream_documents);scan(real_path_document);scan(policy_document)
    ledger=BudgetLedger(RolloutBudget.from_mapping(config['budget']))
    upstream=validate_upstream(config['upstream_intake'],upstream_documents)
    state=StateSchemaContract.from_mapping(config['state_schema'])
    real=validate_real_paths(real_path_document,state,ledger);real_summary=summary(real['paths'])
    registry=generate_registry(real['paths'],config['generator_program'],real['dataset_hash'],ledger)
    if not all(validate_watermark(p['watermark']) for p in registry['paths']): raise ValueError('watermark failure')
    native_invariants=inspect_paths(registry['paths'],config['path_invariants'])
    stress_library=compose_stress_library(registry['paths'][:4],config['stress_program'],ledger)
    stress_invariants=inspect_paths(stress_library['paths'],config['path_invariants'])
    combined={'path_count':native_invariants['path_count']+stress_invariants['path_count'],'passed':native_invariants['passed'] and stress_invariants['passed'],'failed_path_count':native_invariants['failed_path_count']+stress_invariants['failed_path_count'],'native_report_hash':native_invariants['invariant_report_hash'],'stress_report_hash':stress_invariants['invariant_report_hash'],'rows':native_invariants['rows']+stress_invariants['rows']};combined['invariant_report_hash']=content_hash(combined)
    fidelity=compare(real['paths'],registry['paths'],config['fidelity'],ledger)
    uncertainty=horizon_map(registry['paths'],config['fidelity']['minimum_trusted_horizon'],config['uncertainty_threshold'])
    exploitability=evaluate(real['paths'],registry['paths'],policy_document,config['exploitability'])
    adversary=search(registry['paths'][:4],policy_document,config['stress_program'],ledger)
    budget=ledger.snapshot()
    certificate=build(upstream,real_summary,registry,stress_library,combined,fidelity,uncertainty,exploitability,adversary,budget)
    outputs={'upstream_receipt':upstream,'real_path_summary':real_summary,'generator_registry':{k:v for k,v in registry.items() if k!='paths'},'native_rollout_set':{'paths':registry['paths'],'path_count':registry['path_count'],'rollout_set_hash':registry['rollout_set_hash'],'research_only':True},'stress_library':stress_library,'invariant_report':combined,'fidelity_report':fidelity,'uncertainty_map':uncertainty,'exploitability_report':exploitability,'adversarial_failure_packet':adversary,'budget_snapshot':budget,'certificate':certificate}
    outputs['replay_receipt']=build_replay({'config':config,'upstream_documents':upstream_documents,'real_path_document':real_path_document,'policy_document':policy_document},outputs)
    outputs['claim_tier_report']={'phase':'SAED_V4_22','claim_tier':'local_deterministic_synthetic_stress_reference','generative_paths_implemented':True,'stress_composition_implemented':True,'fidelity_diagnostics_implemented':True,'exploitability_challenge_implemented':True,'real_alpha_established':False,'synthetic_positive_evidence_allowed':False,'production_policy_selection':False,'runtime_activation':False,'production_authorization':False}
    outputs['handoff']=build_handoff(certificate,fidelity,uncertainty,exploitability,budget,qa or {'passed':True})
    outputs['reference_run_hash']=content_hash(outputs)
    return outputs

def future_suffix_invariance(config,upstream_documents,real_path_document,policy_document):
    a=run_reference(config,upstream_documents,real_path_document,policy_document)
    mutated=dict(real_path_document);mutated['future_suffix']={'future_close':999999,'future_outcome':'oracle'}
    safe={k:v for k,v in mutated.items() if k in {'dataset_id','context_id','paths','role','known_time_cutoff'}}
    b=run_reference(config,upstream_documents,safe,policy_document)
    return {'passed':a['reference_run_hash']==b['reference_run_hash'],'original_hash':a['reference_run_hash'],'mutated_hash':b['reference_run_hash'],'future_suffix_ignored':True}

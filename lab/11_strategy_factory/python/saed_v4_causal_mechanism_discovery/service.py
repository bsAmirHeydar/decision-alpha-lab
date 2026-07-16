from __future__ import annotations
from .validation import *
from .dataset import build as build_dataset,ground_truth_graph
from .graph import association_baseline,temporal_candidate,graph_metrics
from .structural import fit_equations,residual_independence
from .invariance import audit as invariance_audit
from .identification import backdoor_audit,frontdoor_audit,temporal_audit,acyclicity_audit
from .orthogonal import reference_score
from .falsification import negative_controls,environment_permutation,hidden_confounder_sensitivity,edge_reversal_stress,future_suffix_audit,fail_closed_audit
from .transport import support_report
from .claims import tier,claim_ledger
from .budget import enforce
from .tournament import candidate_metrics,select
from .checkpoint import build as build_checkpoints,registry as build_registry
from .integrity import receipt as integrity_receipt
from .replay import receipt as replay_receipt
from .provenance import build as provenance_build
from .security import sbom,incident_template
from .authority import boundary_record
from .handoff import build as handoff_build
from .canonical import content_hash

def build_reference_bundle(handoff,v416_dataset,v416_registry,v416_integrity,v416_tail_cal,v416_time_cal,variable_registry_map,environment_registry_map,graph_constraints_map,config_map,candidate_maps,budget_map):
    upstream=validate_upstream(handoff,v416_dataset,v416_registry,v416_integrity,v416_tail_cal,v416_time_cal)
    vr=validate_variable_registry(variable_registry_map);er=validate_environment_registry(environment_registry_map);gc=validate_graph_constraints(graph_constraints_map);cfg=validate_discovery_config(config_map);candidates=validate_candidates(candidate_maps);budget=validate_budget(budget_map)
    dataset=build_dataset(upstream,v416_dataset,vr,er,cfg);truth=ground_truth_graph(vr)
    baseline=association_baseline(dataset,vr,gc,cfg);temporal=temporal_candidate(dataset,vr,gc,cfg)
    ci={'phase':'SAED_V4_17','test_count':temporal['test_count'],'tests':temporal['tests']};ci['report_hash']=content_hash(ci)
    equations=fit_equations(dataset,temporal['graph']);residuals=residual_independence(dataset,equations);invariance=invariance_audit(dataset,temporal['graph'],er,cfg)
    temporal_a=temporal_audit(temporal['graph'],gc);acyclic=acyclicity_audit(temporal['graph']);backdoor=backdoor_audit(temporal['graph'],vr.treatment_proxy_id,vr.outcome_proxy_id,vr);frontdoor=frontdoor_audit(temporal['graph'],vr.treatment_proxy_id,vr.outcome_proxy_id)
    orth=reference_score(dataset,vr.treatment_proxy_id,vr.outcome_proxy_id,['context_state','structure_state','liquidity_state','execution_friction'])
    neg=negative_controls(dataset,vr,cfg);env_perm=environment_permutation(dataset,temporal['graph'],cfg.seed);hidden=hidden_confounder_sensitivity(dataset,orth,cfg);reversal=edge_reversal_stress(temporal['graph'],gc);future=future_suffix_audit(dataset);fail=fail_closed_audit();transport=support_report(dataset,vr)
    gm=graph_metrics(temporal['graph'],truth);claim=tier(gm,invariance,neg,temporal_a,acyclic)
    metrics=candidate_metrics(candidates,baseline['graph'],temporal['graph'],truth,invariance,neg,graph_metrics);tournament=select(metrics)
    checkpoints=build_checkpoints(metrics,tournament,dataset['dataset_hash'],upstream['v4_16_handoff_hash']);registry=build_registry(checkpoints,tournament)
    ledger=enforce(budget,dataset,vr,candidates,temporal['test_count'],cfg.bootstrap_replicates,6)
    integrity=integrity_receipt(upstream,dataset,registry,claim,ledger)
    hashes={'dataset':dataset['dataset_hash'],'truth_graph':truth['graph_hash'],'baseline':baseline['report_hash'],'temporal_graph':temporal['report_hash'],'invariance':invariance['report_hash'],'negative_controls':neg['report_hash'],'claim':claim['report_hash'],'registry':registry['registry_hash'],'integrity':integrity['receipt_hash']}
    replay=replay_receipt(hashes);provenance=provenance_build(upstream['v4_16_handoff_hash'],dataset['dataset_hash'],registry['registry_hash']);handoff18=handoff_build(upstream,vr,er,dataset,registry,integrity,claim,backdoor,frontdoor)
    return {'upstream_validation':upstream,'variable_registry':variable_registry_map,'environment_registry':environment_registry_map,'graph_constraints':graph_constraints_map,'causal_benchmark_dataset':dataset,'ground_truth_graph':truth,'association_baseline':baseline,'temporal_candidate_graph':temporal,'conditional_independence_audit':ci,'structural_equations':equations,'residual_independence_audit':residuals,'invariant_mechanism_report':invariance,'temporal_precedence_audit':temporal_a,'acyclicity_audit':acyclic,'backdoor_audit':backdoor,'frontdoor_audit':frontdoor,'orthogonal_score_report':orth,'negative_control_audit':neg,'environment_permutation':env_perm,'hidden_confounder_sensitivity':hidden,'edge_reversal_stress':reversal,'future_suffix_audits':future,'fail_closed_audits':fail,'transport_support_report':transport,'claim_tier_report':claim,'candidate_metrics':metrics,'tournament':tournament,'candidate_checkpoints':checkpoints,'checkpoint_registry':registry,'compute_exposure_ledger':ledger,'integrity_receipt':integrity,'replay_receipt':replay,'provenance':provenance,'handoff':handoff18,'claim_ledger':claim_ledger(),'sbom':sbom(),'incident_template':incident_template(),'authority_boundary':boundary_record()}

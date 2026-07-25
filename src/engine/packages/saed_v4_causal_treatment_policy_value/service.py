from __future__ import annotations
from .validation import validate_inputs,validate_upstream,validate_split_plan
from .authority import boundary_record
from .dataset import build_synthetic_dataset
from .splits import build_chronological_cluster_folds,audit_splits
from .crossfit import cross_fit
from .propensity import propensity_diagnostics
from .outcome import nuisance_diagnostics
from .overlap import overlap_audit
from .effects import estimate_ate,fit_cate_models,subgroup_effects
from .policies import compile_assignments
from .policy_value import evaluate_policy_values,negative_control_policy_value
from .sensitivity import propensity_clip_sensitivity,hidden_confounder_sensitivity,cost_stress,environment_transport
from .ranking import rank_treatments
from .benchmarks import estimator_scorecard
from .audits import future_suffix_audit,fail_closed_audits
from .budget import enforce
from .tournament import run_tournament
from .claims import tier_claims
from .checkpoint import build_checkpoints
from .security import security_posture
from .integrity import build_integrity_receipt
from .replay import build_replay_receipt
from .provenance import build_provenance
from .handoff import build_handoff
from .canonical import content_hash

def build_reference_bundle(v417_handoff,v417_registry,v417_integrity,v417_claims,treatment_registry,outcome_spec,identification_plan,estimators,policies,budget):
    tr,os,ip,es,ps,bd=validate_inputs(treatment_registry,outcome_spec,identification_plan,estimators,policies,budget)
    upstream=validate_upstream(v417_handoff,v417_registry,v417_integrity,v417_claims)
    tids=[x['treatment_id'] for x in tr.treatments];dataset,truth=build_synthetic_dataset(tids,480,6);split=build_chronological_cluster_folds(dataset,ip);validate_split_plan(split,dataset);split_audit=audit_splits(dataset,split)
    cf=cross_fit(dataset,split,tids,ip.propensity_clip,0.02);prop=propensity_diagnostics(cf['predictions'],tids,ip.overlap_floor);nuis=nuisance_diagnostics(cf);overlap=overlap_audit(cf,ip.overlap_floor,ip.min_effective_sample_size)
    ate=estimate_ate(cf,tr.baseline_treatment_id);cate=fit_cate_models(cf,tr.baseline_treatment_id,0.03);subgroups=subgroup_effects(cf,cate)
    catalog=compile_assignments(cf,[p.__dict__ for p in ps],cate,ip.overlap_floor);values=evaluate_policy_values(cf,catalog,'policy_skip_all');negative=negative_control_policy_value(cf,catalog)
    psens=propensity_clip_sensitivity(cf,catalog,'policy_skip_all',[0.01,0.03,0.05,0.08,0.12]);hsens=hidden_confounder_sensitivity(values,[0.0,0.03,0.06,0.10,0.15,0.25]);cost=cost_stress(cf,catalog,'policy_skip_all',[1.0,1.25,1.5,2.0]);transport=environment_transport(cf,catalog)
    ranking=rank_treatments(ate);scorecard=estimator_scorecard(cf,ate,tr.baseline_treatment_id);future_audit=future_suffix_audit(dataset,split);fail_audit=fail_closed_audits(overlap,negative,boundary_record());ledger=enforce(bd,dataset,tr,es,ps,ip.cross_fit_folds,64,len(psens['runs'])+len(hsens['runs'])+len(cost['runs'])+transport['environment_count'])
    tournament=run_tournament(values,overlap,negative,psens,'policy_manual_rule','policy_skip_all');claims=tier_claims(upstream,overlap,negative,tournament);checkpoint=build_checkpoints(tournament,values,claims)
    bundle={'upstream_validation':upstream,'authority_boundary':boundary_record(),'treatment_registry':treatment_registry,'outcome_spec':outcome_spec,'identification_plan':identification_plan,'estimator_catalog':estimators,'policy_specs':policies,'compute_budget':budget,'synthetic_treatment_dataset':dataset,'synthetic_ground_truth':truth,'split_plan':split,'split_audit':split_audit,'crossfit_predictions':cf,'propensity_report':prop,'nuisance_report':nuis,'overlap_report':overlap,'ate_report':ate,'cate_report':cate,'subgroup_report':subgroups,'policy_catalog':catalog,'policy_value_report':values,'negative_control_report':negative,'propensity_sensitivity':psens,'hidden_confounder_sensitivity':hsens,'cost_stress':cost,'transport_report':transport,'treatment_ranking':ranking,'estimator_scorecard':scorecard,'future_suffix_audit':future_audit,'fail_closed_audits':fail_audit,'compute_exposure_ledger':ledger,'tournament':tournament,'candidate_checkpoints':checkpoint['checkpoints'],'checkpoint_registry':checkpoint['registry'],'claim_tier_report':claims,'security_posture':security_posture()}
    integrity=build_integrity_receipt(bundle);bundle['integrity_receipt']=integrity;bundle['replay_receipt']=build_replay_receipt(bundle)
    bundle['provenance']=build_provenance({'v417_handoff':v417_handoff['handoff_hash'],'v417_registry':v417_registry['registry_hash'],'v417_integrity':v417_integrity['receipt_hash']},{k:content_hash(v) for k,v in bundle.items() if k not in {'synthetic_ground_truth','crossfit_predictions'}})
    bundle['handoff']=build_handoff(checkpoint['registry'],claims,upstream,integrity,tournament)
    return bundle

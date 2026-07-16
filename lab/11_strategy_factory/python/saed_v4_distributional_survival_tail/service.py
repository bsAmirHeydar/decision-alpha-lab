from __future__ import annotations
from .validation import validate_upstream,validate_event_registry,validate_censoring_policy,validate_dataset_spec,validate_model_config,validate_candidates,validate_tail_policy,validate_budget
from .dataset import build as build_dataset
from .censoring import audit as censoring_audit,ipcw
from .risksets import build as build_risksets
from .survival import build_predictions as build_survival
from .distributional import build_predictions as build_distributional
from .tails import summarize as summarize_tails,calibration as tail_calibration
from .calibration import time_calibration,distribution_calibration
from .diagnostics import quantile_crossing,competing_risk_simplex
from .perturbation import future_suffix_audits,fail_closed_audits,stress_suite
from .metrics import evaluate
from .budget import enforce
from .tournament import run as run_tournament
from .checkpoint import make as make_checkpoint
from .registry import build as build_registry
from .integrity import receipt as integrity_receipt
from .replay import receipt as replay_receipt
from .provenance import build as build_provenance
from .handoff import build as build_handoff
from .claims import claim_ledger
from .security import sbom,incident_template
from .authority import boundary_record
from .canonical import content_hash

def build_reference_bundle(v415_handoff,v415_registry,v415_fusion_outputs,v415_aligned,v415_integrity,event_registry_doc,censoring_policy_doc,dataset_spec_doc,model_config_doc,candidate_docs,tail_policy_doc,budget_doc):
    upstream=validate_upstream(v415_handoff,v415_registry,v415_fusion_outputs,v415_aligned,v415_integrity)
    event_registry=validate_event_registry(event_registry_doc);censoring=validate_censoring_policy(censoring_policy_doc);spec=validate_dataset_spec(dataset_spec_doc);config=validate_model_config(model_config_doc);candidates=validate_candidates(candidate_docs);tail_policy=validate_tail_policy(tail_policy_doc);budget=validate_budget(budget_doc)
    dataset=build_dataset(upstream,v415_fusion_outputs,spec,event_registry,censoring);censor_audit=censoring_audit(dataset,event_registry,censoring);risksets=build_risksets(dataset,event_registry,config);weights=ipcw(dataset,config,censoring)
    survival=build_survival(candidates,dataset,event_registry,config);distribution=build_distributional(candidates,dataset,config);tail_summary=summarize_tails(dataset,config);tail_cal=tail_calibration(distribution,dataset,config);time_cal=time_calibration(survival,dataset);dist_cal=distribution_calibration(distribution,dataset);crossing=quantile_crossing(distribution);simplex=competing_risk_simplex(survival)
    metrics=evaluate(candidates,dataset,distribution,survival,tail_cal,config);baseline_id=next(c.candidate_id for c in candidates if c.algorithm=='empirical_km_baseline' and c.enabled);tournament=run_tournament(metrics,baseline_id);stress=stress_suite(dataset,distribution,metrics,event_registry,config);future=future_suffix_audits(dataset,distribution,survival);failclosed=fail_closed_audits(event_registry,config,tail_policy);ledger=enforce(dataset,candidates,config,budget,len(stress))
    metric_by={x['candidate_id']:x for x in metrics['rows']};checkpoints=[make_checkpoint(c,metric_by[c.candidate_id],tournament,upstream,dataset) for c in candidates if c.enabled];registry=build_registry(checkpoints,tournament)
    core={'upstream_validation':upstream,'event_definition_registry':event_registry.__dict__,'censoring_policy':censoring.__dict__,'survival_dataset':dataset,'censoring_audit':censor_audit,'risk_set_ledger':risksets,'ipcw_weights':weights,'survival_predictions':survival,'distributional_predictions':distribution,'tail_risk_summaries':tail_summary,'tail_calibration_report':tail_cal,'time_calibration_report':time_cal,'distribution_calibration_report':dist_cal,'quantile_crossing_audit':crossing,'competing_risk_simplex_audit':simplex,'candidate_metrics':metrics,'stress_tests':stress,'future_suffix_audits':future,'fail_closed_audits':failclosed,'compute_exposure_ledger':ledger,'tournament':tournament,'candidate_checkpoints':checkpoints,'checkpoint_registry':registry}
    integrity=integrity_receipt(core);provenance=build_provenance(upstream,dataset,tournament,registry);handoff=build_handoff(upstream,event_registry,censoring,dataset,tournament,registry,integrity,tail_cal,time_cal)
    bundle={**core,'integrity_receipt':integrity,'replay_receipt':replay_receipt(core,core),'provenance':provenance,'handoff':handoff,'claim_ledger':claim_ledger(),'sbom':sbom(),'incident_template':incident_template(),'authority_boundary':boundary_record()};bundle['bundle_hash']=content_hash(bundle);return bundle

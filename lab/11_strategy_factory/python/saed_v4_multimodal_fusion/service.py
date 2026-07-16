from __future__ import annotations
from .validation import validate_config,validate_candidates,validate_support_policy,validate_missingness_policy,validate_budget,validate_upstream
from .alignment import build as build_alignment
from .support import audit as support_audit
from .fusion import fuse
from .missingness import domain_subset_matrix,foundation_subset_matrix,dropout_plan
from .diagnostics import disagreement,ablation,attribution,permutation
from .perturbation import future_suffix_audit,fail_closed_audits
from .budget import enforce
from .evaluation import evaluate
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

def build_reference_bundle(v414_handoff,v414_registry,v414_features,v414_tokens,v414_calibration,v414_domain,v414_tournament,v404_package,v404_handoff,config_doc,candidate_docs,support_policy_doc,missingness_policy_doc,budget_doc):
    config=validate_config(config_doc);candidates=validate_candidates(candidate_docs);policy=validate_support_policy(support_policy_doc);missing_policy=validate_missingness_policy(missingness_policy_doc);budget=validate_budget(budget_doc)
    upstream=validate_upstream(v414_handoff,v414_registry,v414_features,v414_tokens,v414_calibration,v414_domain,v414_tournament,v404_package,v404_handoff)
    aligned=build_alignment(v404_package,v414_features,v414_domain,v414_calibration,config);envelopes=aligned['domain_views']+aligned['foundation_views']
    dm=domain_subset_matrix(aligned['domain_views'],config);fm=foundation_subset_matrix(aligned['foundation_views']);drop=dropout_plan(envelopes,config,missing_policy);ledger=enforce(candidates,dm,fm,drop,aligned,budget)
    supports=[];outputs=[];perms=[];failclosed=[]
    for c in candidates:
        if not c.enabled:continue
        sup=support_audit(envelopes,config,c,policy);out=fuse(c,envelopes,sup,config);supports.append(sup);outputs.append(out)
        perms.append(permutation(c,envelopes,sup,lambda es,s:fuse(c,es,s,config)))
        failclosed.append(fail_closed_audits(envelopes,config,c,policy,lambda es:support_audit(es,config,c,policy),lambda es,s:fuse(c,es,s,config)))
    metrics=evaluate(outputs,dm,fm);baseline_id=next(c.candidate_id for c in candidates if c.algorithm=='late_mean_baseline' and c.enabled);tournament=run_tournament(metrics,baseline_id)
    metric_by={x['candidate_id']:x for x in metrics['rows']};support_by={x['candidate_id']:x for x in supports};output_by={x['candidate_id']:x for x in outputs};cand_by={x.candidate_id:x for x in candidates}
    checkpoints=[make_checkpoint(cand_by[cid],output_by[cid],metric_by[cid],support_by[cid],aligned) for cid in output_by];registry=build_registry(checkpoints,tournament)
    champion=cand_by[tournament['reference_champion_id']];champion_output=output_by[champion.candidate_id]
    ab=ablation(champion,envelopes,champion_output,config,lambda es:support_audit(es,config,champion,policy),lambda es,s:fuse(champion,es,s,config))
    future=[future_suffix_audit(v,config,v404_package['known_as_of']) for v in v404_package['views']]
    core={'upstream_validation':upstream,'aligned_view_set':aligned,'domain_subset_matrix':dm,'foundation_subset_matrix':fm,'dropout_plan':drop,'compute_exposure_ledger':ledger,'support_audits':supports,'fusion_outputs':outputs,'disagreement_report':disagreement(outputs),'ablation_report':ab,'attribution_report':attribution(outputs),'permutation_reports':perms,'future_suffix_audits':future,'fail_closed_audits':failclosed,'candidate_metrics':metrics,'tournament':tournament,'candidate_checkpoints':checkpoints,'checkpoint_registry':registry}
    integ=integrity_receipt(core);prov=build_provenance(upstream,aligned,tournament,registry);handoff=build_handoff(upstream,aligned,tournament,registry,integ,dm,fm)
    bundle={**core,'integrity_receipt':integ,'replay_receipt':replay_receipt(core,core),'provenance':prov,'handoff':handoff,'claim_ledger':claim_ledger(),'sbom':sbom(),'incident_template':incident_template(),'authority_boundary':boundary_record()};bundle['bundle_hash']=content_hash(bundle);return bundle

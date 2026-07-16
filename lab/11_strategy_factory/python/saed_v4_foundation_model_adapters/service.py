from __future__ import annotations
from .validation import validate_config,validate_intakes,validate_candidates,validate_disclosures,validate_domain_shift_policy,validate_budget,validate_upstream
from .intake import decide_all
from .supply_chain import attest
from .contamination import audit as contamination_audit
from .tokenization import compile_token_sequence
from .budget import enforce
from .adapters import run_adapter
from .calibration import calibrate
from .domain_shift import assess
from .objectives import evaluate
from .perturbation import future_suffix_audit,fail_closed_audit
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
from .canonical import content_hash,stable_id

def _report(name,rows):
    doc={'phase':'SAED_V4_14','report_type':name,'rows':rows,'row_count':len(rows),'all_passed':all((r.get('supported',True) and r.get('quantile_monotonic',True)) for r in rows),'production_evidence':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('fmreport',doc);return doc

def build_reference_bundle(v413_handoff,v413_registry,v413_embeddings,v413_graph,v413_tournament,adapter_config_doc,intake_docs,candidate_docs,disclosure_docs,domain_policy_doc,budget_doc):
    config=validate_config(adapter_config_doc);intakes=validate_intakes(intake_docs);candidates=validate_candidates(candidate_docs,intakes);disclosures=validate_disclosures(disclosure_docs,intakes);policy=validate_domain_shift_policy(domain_policy_doc);budget=validate_budget(budget_doc)
    upstream=validate_upstream(v413_handoff,v413_registry,v413_embeddings,v413_graph,v413_tournament)
    decisions=decide_all(intakes,disclosures);decision_by={x['intake_id']:x for x in decisions};intake_by={x.intake_id:x for x in intakes}
    attestations=[attest(i,decision_by[i.intake_id]) for i in intakes];attest_by={x['intake_id']:x for x in attestations}
    contamination=contamination_audit(intakes,disclosures,decisions,v413_graph['known_as_of'])
    seq=compile_token_sequence(v413_graph,v413_embeddings,v413_handoff['reference_champion_id'],config)
    ledger=enforce(seq,candidates,budget,decisions)
    features=[];calibrations=[];domains=[];metrics=[];future=[];failclosed=[];checkpoints=[]
    for c in candidates:
        if not c.enabled or decision_by[c.intake_id]['decision']!='admit_reference': continue
        f=run_adapter(seq,config,c);cal=calibrate(f,seq,c);dom=assess(seq,f,c,policy);ev=evaluate(seq,f,cal,dom,c,config)
        features.append(f);calibrations.append(cal);domains.append(dom);metrics.append(ev);future.append(future_suffix_audit(v413_graph,v413_embeddings,v413_handoff['reference_champion_id'],config,c));failclosed.append(fail_closed_audit(c,decision_by[c.intake_id],dom));checkpoints.append(make_checkpoint(c,f,ev,cal,dom,decision_by[c.intake_id],attest_by[c.intake_id],seq))
    baseline_id=next(c.candidate_id for c in candidates if c.family=='native_linear_baseline' and c.enabled)
    tournament=run_tournament(metrics,baseline_id);registry=build_registry(checkpoints,tournament);domain_report=_report('domain_shift',domains);calibration_report=_report('calibration',calibrations)
    core={'upstream_validation':upstream,'intake_decisions':decisions,'supply_chain_attestations':attestations,'contamination_audit':contamination,'token_sequence':seq,'compute_exposure_ledger':ledger,'adapter_features':features,'calibration_report':calibration_report,'domain_shift_report':domain_report,'candidate_metrics':metrics,'future_suffix_audits':future,'fail_closed_audits':failclosed,'candidate_checkpoints':checkpoints,'tournament':tournament,'checkpoint_registry':registry}
    integ=integrity_receipt(core);prov=build_provenance(upstream,seq,tournament,registry,decisions);handoff=build_handoff(upstream,seq,tournament,registry,integ,domain_report,calibration_report)
    bundle={**core,'integrity_receipt':integ,'replay_receipt':replay_receipt(core,core),'provenance':prov,'handoff':handoff,'claim_ledger':claim_ledger(),'sbom':sbom(),'incident_template':incident_template(),'authority_boundary':boundary_record()}
    bundle['bundle_hash']=content_hash(bundle);return bundle

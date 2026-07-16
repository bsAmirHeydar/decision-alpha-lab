from __future__ import annotations
from .canonical import content_hash,stable_id
from .authority import authority_boundary

def build(upstream,real_summary,registry,stress_library,invariants,fidelity,uncertainty,exploitability,adversary,budget):
    passed=invariants['passed'] and exploitability['passed'] and budget['hidden_evaluation_queries']==0 and budget['protected_evidence_exposures']==0
    out={'phase':'SAED_V4_22','certificate_id':'','upstream_intake_hash':upstream['intake_hash'],'real_summary_hash':real_summary['summary_hash'],'generator_registry_hash':registry['generator_registry_hash'],'rollout_set_hash':registry['rollout_set_hash'],'stress_library_hash':stress_library['stress_library_hash'],'invariant_report_hash':invariants['invariant_report_hash'],'fidelity_report_hash':fidelity['fidelity_report_hash'],'uncertainty_map_hash':uncertainty['uncertainty_map_hash'],'exploitability_report_hash':exploitability['exploitability_report_hash'],'adversarial_failure_packet_hash':adversary['adversarial_failure_packet_hash'],'budget_ledger_hash':budget['ledger_hash'],'accepted_for_synthetic_stress_falsification':passed,'positive_alpha_evidence':False,'promotion_authority':False,'runtime_executable':False,'production_authority':False,'research_only':True,'authority_boundary':authority_boundary()}
    out['certificate_id']=stable_id('generative_stress_certificate',out);out['certificate_hash']=content_hash(out);return out

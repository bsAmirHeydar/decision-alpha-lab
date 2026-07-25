from __future__ import annotations
from .canonical import content_hash,stable_id
from .authority import boundary_record

def build_certificate(upstream,scenario_set,ambiguity_set,allocation_universe,optimization_report,adversary_report,stability_report,budget_snapshot):
    authority=boundary_record();decision=optimization_report['decision']
    body={'phase':'SAED_V4_21','context_id':scenario_set['context_id'],'upstream_intake_hash':upstream['intake_hash'],'selection_certificate_hash':upstream['certificate_hash'],'scenario_set_hash':scenario_set['scenario_set_hash'],'ambiguity_set_hash':ambiguity_set['ambiguity_set_hash'],'allocation_universe_hash':allocation_universe['allocation_universe_hash'],'optimization_report_hash':optimization_report['optimization_report_hash'],'adversary_report_hash':adversary_report['adversary_report_hash'],'stability_report_hash':stability_report['stability_report_hash'],'budget_ledger_hash':budget_snapshot['ledger_hash'],'decision':decision,'research_only':True,'runtime_executable':False,'decision_authority':False,'risk_allocation_authority':False,'promotion_authority':False,'execution_authority':False,'production_authority':False,'authority_hash':content_hash(authority)}
    body['certificate_id']=stable_id('robust_certificate',body);body['certificate_hash']=content_hash(body);return body

def verify_certificate(c):
    if not c.get('research_only') or any(c.get(k) for k in ['runtime_executable','decision_authority','risk_allocation_authority','promotion_authority','execution_authority','production_authority']):return False
    h=c.get('certificate_hash');return h==content_hash({k:v for k,v in c.items() if k!='certificate_hash'})

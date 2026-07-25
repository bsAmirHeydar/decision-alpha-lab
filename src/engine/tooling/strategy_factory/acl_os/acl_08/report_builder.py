from __future__ import annotations
from collections import Counter
from typing import Any
from .canonical import with_digest
from .policies import CLAIM_CEILING

def candidate_report(report_id:str,decision:dict[str,Any],gate_doc:dict[str,Any])->dict[str,Any]:
    gates=[{'gate_id':g['gate_id'],'status':g['status'],'reason_codes':g['reason_codes'],'metrics':g.get('metrics',{}),'gate_result_digest':g['gate_result_digest']} for g in gate_doc['gates']]
    return with_digest({'schema_version':'1.0.0','report_id':report_id,'setup_id':decision['setup_id'],'candidate_id':decision['candidate_id'],'lane':decision['lane'],'origin':decision['origin'],'decision_id':decision['decision_id'],'decision_status':decision['decision_status'],'reason_codes':decision['reason_codes'],'gate_summary':decision['gate_summary'],'gates':gates,'source_decision_digest':decision['decision_digest'],'source_candidate_gate_digest':gate_doc['candidate_gate_digest'],'reporting_eligible':decision['decision_status']=='VALIDATION_ELIGIBLE_FOR_REPORTING','diagnostic_selectable':False if decision['lane']=='DIAGNOSTIC' else None,'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'candidate_report_digest')

def build_batch_report(report_id:str,bundle:dict[str,Any],candidate_reports:list[dict[str,Any]],reported_at:str,blocks:list[str])->dict[str,Any]:
    decisions=bundle['decisions']; status_counts=dict(Counter(x['decision_status'] for x in decisions['decisions']))
    gate_counts=Counter(g['status'] for c in candidate_reports for g in c['gates'])
    unknown_gates=Counter(g['gate_id'] for c in candidate_reports for g in c['gates'] if g['status']=='UNKNOWN')
    limitations=[]
    if status_counts.get('VALIDATION_ELIGIBLE_FOR_REPORTING',0)==0: limitations.append('No candidate is validation-eligible for reporting in the reference evidence.')
    if unknown_gates: limitations.append('Required validation evidence remains unknown for one or more candidates.')
    limitations += ['Reference evidence is synthetic and does not establish market edge.','Execution economics, prospective evidence and independent replication are not established.','This report has no promotion, order or capital authority.']
    body={'schema_version':'1.0.0','report_id':report_id,'report_type':'ACL08_BATCH_REPORT','reported_at':reported_at,'validation_id':bundle['handoff']['validation_id'],'run_id':bundle['handoff']['run_id'],'batch_id':bundle['handoff']['batch_id'],'source_claim_ceiling':bundle['handoff']['claim_ceiling'],'claim_ceiling':CLAIM_CEILING,'report_blocks':blocks,'candidate_count':len(candidate_reports),'decision_counts':status_counts,'gate_status_counts':dict(gate_counts),'unknown_gate_frequency':dict(sorted(unknown_gates.items())),'candidate_report_digests':[x['candidate_report_digest'] for x in candidate_reports],'baseline_count':sum(x['decision_status']=='BASELINE_REFERENCE_ONLY' for x in candidate_reports),'diagnostic_count':sum(x['lane']=='DIAGNOSTIC' for x in candidate_reports),'reporting_eligible_count':status_counts.get('VALIDATION_ELIGIBLE_FOR_REPORTING',0),'limitations':limitations,'required_next_evidence':sorted(unknown_gates),'decision_semantics_mutated':False,'diagnostic_evidence_segregated':True,'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
    return with_digest(body,'batch_report_digest')

def build_executive_summary(report:dict[str,Any],reported_at:str)->dict[str,Any]:
    eligible=report['reporting_eligible_count']
    answer='No candidate is validation-eligible for reporting in the reference evidence.' if eligible==0 else f'{eligible} candidate(s) are validation-eligible for reporting; none are promoted.'
    findings=[answer,f"Decision distribution: {report['decision_counts']}",f"Unknown validation evidence remains in {len(report['unknown_gate_frequency'])} gate categories.",'Diagnostic evidence remains non-selectable and baselines remain non-promotable.','No alpha, execution or capital claim is authorized.']
    return with_digest({'schema_version':'1.0.0','report_id':report['report_id'],'reported_at':reported_at,'answer_first':answer,'key_findings':findings,'decision_counts':report['decision_counts'],'limitations':report['limitations'],'claim_ceiling':report['claim_ceiling'],'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False},'executive_summary_digest')

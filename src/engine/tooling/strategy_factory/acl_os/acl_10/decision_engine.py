from __future__ import annotations
from collections import Counter
from typing import Any
from .canonical import stable_id, with_digest

def _target_state(subject:dict[str,Any], evaluation:dict[str,Any]) -> tuple[str,list[str]]:
    if subject['diagnostic']: return 'DIAGNOSTIC_QUARANTINED',['DIAGNOSTIC_LANE_NON_SELECTABLE']
    if subject['baseline']: return 'BASELINE_REFERENCE_ONLY',['BASELINE_NOT_PROMOTABLE']
    if subject['experience_class']=='NEGATIVE_VALIDATION': return 'VALIDATION_FAILED_ARCHIVED',['VALIDATION_FAILED']
    if evaluation['promotion_review_eligible']: return 'PROMOTION_REVIEW_ELIGIBLE',['ALL_PROMOTION_REVIEW_PREREQUISITES_SATISFIED']
    reasons=sorted({r['reason_code'] for r in evaluation['results'] if r['status'] in {'UNSATISFIED','UNKNOWN'}})
    return 'RESEARCH_HOLD',reasons or ['PROMOTION_PREREQUISITES_NOT_SATISFIED']
def build_decisions(subject_bundle:dict[str,Any], matrix:dict[str,Any], policy:dict[str,Any], evaluated_at:str) -> tuple[dict[str,Any],dict[str,Any]]:
    eval_by={e['subject_id']:e for e in matrix['evaluations']}; decisions=[]; attempts=[]
    for subject in subject_bundle['subjects']:
        evaluation=eval_by[subject['subject_id']]; state,reasons=_target_state(subject,evaluation)
        dbody={'schema_version':'1.0.0','state_decision_id':stable_id('PROMDEC',subject['subject_id'],evaluation['evaluation_digest']),'subject_id':subject['subject_id'],'experience_id':subject['experience_id'],'source_subject_digest':subject['subject_digest'],'prerequisite_evaluation_digest':evaluation['evaluation_digest'],'current_state':state,'reason_codes':reasons,'evaluated_at':evaluated_at,'promotion_review_eligible':state=='PROMOTION_REVIEW_ELIGIBLE','promotion_executed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        decision=with_digest(dbody,'state_decision_digest'); decisions.append(decision)
        if state in {'BASELINE_REFERENCE_ONLY','DIAGNOSTIC_QUARANTINED','VALIDATION_FAILED_ARCHIVED'}: status='NOT_APPLICABLE'
        elif state=='PROMOTION_REVIEW_ELIGIBLE': status='ALLOWED_NOT_EXECUTED'
        else: status='DENIED'
        abody={'schema_version':'1.0.0','transition_attempt_id':stable_id('TRANSATT',decision['state_decision_id']),'subject_id':subject['subject_id'],'transition_id':'RESEARCH_HOLD_TO_PROMOTION_REVIEW','status':status,'reason_codes':reasons,'state_decision_digest':decision['state_decision_digest'],'transition_executed':False}
        attempts.append(with_digest(abody,'transition_attempt_digest'))
    counts=dict(sorted(Counter(d['current_state'] for d in decisions).items()))
    body={'schema_version':'1.0.0','decision_count':len(decisions),'state_counts':counts,'promotion_review_eligible_count':sum(1 for d in decisions if d['promotion_review_eligible']),'promotion_executed_count':0,'decisions':[{'state_decision_id':d['state_decision_id'],'subject_id':d['subject_id'],'current_state':d['current_state'],'state_decision_digest':d['state_decision_digest']} for d in decisions],'promotion_execution_allowed':False,'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
    bundle=with_digest(body,'decision_bundle_digest')
    tbody={'schema_version':'1.0.0','attempt_count':len(attempts),'allowed_not_executed_count':sum(1 for x in attempts if x['status']=='ALLOWED_NOT_EXECUTED'),'denied_count':sum(1 for x in attempts if x['status']=='DENIED'),'not_applicable_count':sum(1 for x in attempts if x['status']=='NOT_APPLICABLE'),'attempts':[{'transition_attempt_id':x['transition_attempt_id'],'subject_id':x['subject_id'],'status':x['status'],'transition_attempt_digest':x['transition_attempt_digest']} for x in attempts]}
    return bundle, with_digest(tbody,'attempt_bundle_digest'), decisions, attempts

from __future__ import annotations
from typing import Any
from .canonical import stable_id, with_digest
PRIMARY = ['SOURCE_INTEGRITY','REPORTING_ELIGIBILITY','VALIDATED_EVIDENCE','NON_DIAGNOSTIC','NON_BASELINE','PROSPECTIVE_EVIDENCE','INDEPENDENT_REPLICATION','EXECUTION_ECONOMICS','OOD_AND_ABSTENTION']
def _result(prerequisite_id:str,status:str,reason_code:str,evidence_refs:list[str]) -> dict[str,Any]:
    body={'schema_version':'1.0.0','prerequisite_id':prerequisite_id,'status':status,'reason_code':reason_code,'evidence_refs':evidence_refs}
    return with_digest(body,'result_digest')
def evaluate_subject(subject:dict[str,Any], bundle:dict[str,Any], policy:dict[str,Any]) -> dict[str,Any]:
    refs=[subject['subject_digest'],bundle['binding']['binding_digest']]
    results=[]
    results.append(_result('SOURCE_INTEGRITY','SATISFIED','UPSTREAM_INTEGRITY_VERIFIED',refs))
    if subject['diagnostic']:
        results.extend([
            _result('REPORTING_ELIGIBILITY','UNSATISFIED','DIAGNOSTIC_NOT_REPORTING_ELIGIBLE',refs),
            _result('VALIDATED_EVIDENCE','UNSATISFIED','DIAGNOSTIC_NOT_VALIDATION_ELIGIBLE',refs),
            _result('NON_DIAGNOSTIC','UNSATISFIED','DIAGNOSTIC_LANE_QUARANTINED',refs),
            _result('NON_BASELINE','NOT_APPLICABLE','DIAGNOSTIC_LANE',refs),
        ])
    elif subject['baseline']:
        results.extend([
            _result('REPORTING_ELIGIBILITY','UNSATISFIED','BASELINE_NOT_REPORTING_ELIGIBLE',refs),
            _result('VALIDATED_EVIDENCE','UNSATISFIED','BASELINE_NOT_PROMOTABLE',refs),
            _result('NON_DIAGNOSTIC','SATISFIED','NON_DIAGNOSTIC_SOURCE',refs),
            _result('NON_BASELINE','UNSATISFIED','BASELINE_REFERENCE_ONLY',refs),
        ])
    elif subject['reporting_eligible']:
        results.extend([
            _result('REPORTING_ELIGIBILITY','SATISFIED','ACL07_REPORTING_ELIGIBLE',refs),
            _result('VALIDATED_EVIDENCE','SATISFIED','ACL07_VALIDATED_EVIDENCE',refs),
            _result('NON_DIAGNOSTIC','SATISFIED','NON_DIAGNOSTIC_SOURCE',refs),
            _result('NON_BASELINE','SATISFIED','NON_BASELINE_SOURCE',refs),
        ])
    else:
        results.extend([
            _result('REPORTING_ELIGIBILITY','UNSATISFIED','REPORTING_ELIGIBILITY_NOT_ESTABLISHED',refs),
            _result('VALIDATED_EVIDENCE','UNSATISFIED','VALIDATED_EVIDENCE_NOT_ESTABLISHED',refs),
            _result('NON_DIAGNOSTIC','SATISFIED','NON_DIAGNOSTIC_SOURCE',refs),
            _result('NON_BASELINE','SATISFIED','NON_BASELINE_SOURCE',refs),
        ])
    if subject['diagnostic'] or subject['baseline']:
        for pid in ['PROSPECTIVE_EVIDENCE','INDEPENDENT_REPLICATION','EXECUTION_ECONOMICS','OOD_AND_ABSTENTION']:
            results.append(_result(pid,'NOT_APPLICABLE','SOURCE_CLASS_NON_PROMOTABLE',refs))
    else:
        results.extend([
            _result('PROSPECTIVE_EVIDENCE','UNKNOWN','PROSPECTIVE_EVIDENCE_MISSING',refs),
            _result('INDEPENDENT_REPLICATION','UNKNOWN','INDEPENDENT_REPLICATION_MISSING',refs),
            _result('EXECUTION_ECONOMICS','UNKNOWN','EXECUTION_ECONOMICS_MISSING',refs),
            _result('OOD_AND_ABSTENTION','UNKNOWN','OOD_AND_ABSTENTION_EVIDENCE_MISSING',refs),
        ])
    satisfied=all(r['status']=='SATISFIED' for r in results if r['prerequisite_id'] in PRIMARY)
    body={'schema_version':'1.0.0','evaluation_id':stable_id('PREEVAL',subject['subject_id'],policy['policy_digest']),'subject_id':subject['subject_id'],'transition_id':'RESEARCH_HOLD_TO_PROMOTION_REVIEW','results':results,'all_required_satisfied':satisfied,'unknown_blocks_promotion':policy['unknown_blocks_promotion'],'promotion_review_eligible':satisfied}
    return with_digest(body,'evaluation_digest')
def build_matrix(subject_bundle:dict[str,Any], bundle:dict[str,Any], policy:dict[str,Any]) -> dict[str,Any]:
    evaluations=[evaluate_subject(subject,bundle,policy) for subject in subject_bundle['subjects']]
    body={'schema_version':'1.0.0','memory_run_id':bundle['memory_run']['memory_run_id'],'evaluation_count':len(evaluations),'eligible_count':sum(1 for e in evaluations if e['promotion_review_eligible']),'evaluations':evaluations}
    return with_digest(body,'matrix_digest')

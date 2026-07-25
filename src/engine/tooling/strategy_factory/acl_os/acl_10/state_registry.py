from __future__ import annotations
from .canonical import digest_object, with_digest
from .errors import PolicyError
STATES = [
 {'state_id':'RESEARCH_HOLD','category':'NON_PROMOTIONAL','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'VALIDATION_FAILED_ARCHIVED','category':'NON_PROMOTIONAL_TERMINAL','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'BASELINE_REFERENCE_ONLY','category':'REFERENCE_ONLY','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'DIAGNOSTIC_QUARANTINED','category':'QUARANTINE','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'PROMOTION_REVIEW_ELIGIBLE','category':'REVIEW_ONLY','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'PAPER_CANDIDATE','category':'FUTURE_DECLARED','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'SHADOW_CANDIDATE','category':'FUTURE_DECLARED','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'MICRO_LIVE_CANDIDATE','category':'FUTURE_DECLARED','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'CHAMPION','category':'FUTURE_DECLARED','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'SUSPENDED','category':'CONTROL','runtime_eligible':False,'capital_eligible':False},
 {'state_id':'RETIRED','category':'TERMINAL','runtime_eligible':False,'capital_eligible':False},
]
TRANSITIONS = [
 {'transition_id':'RESEARCH_HOLD_TO_PROMOTION_REVIEW','from_state':'RESEARCH_HOLD','to_state':'PROMOTION_REVIEW_ELIGIBLE','prerequisites':['SOURCE_INTEGRITY','REPORTING_ELIGIBILITY','VALIDATED_EVIDENCE','NON_DIAGNOSTIC','NON_BASELINE','PROSPECTIVE_EVIDENCE','INDEPENDENT_REPLICATION','EXECUTION_ECONOMICS','OOD_AND_ABSTENTION']},
 {'transition_id':'PROMOTION_REVIEW_TO_PAPER','from_state':'PROMOTION_REVIEW_ELIGIBLE','to_state':'PAPER_CANDIDATE','prerequisites':['HUMAN_APPROVAL','SECURITY_CLEARANCE','RUNTIME_PARITY_PLAN']},
 {'transition_id':'PAPER_TO_SHADOW','from_state':'PAPER_CANDIDATE','to_state':'SHADOW_CANDIDATE','prerequisites':['PAPER_EVIDENCE','HUMAN_APPROVAL','SECURITY_CLEARANCE']},
 {'transition_id':'SHADOW_TO_MICRO_LIVE','from_state':'SHADOW_CANDIDATE','to_state':'MICRO_LIVE_CANDIDATE','prerequisites':['SHADOW_EVIDENCE','BROKER_QUALIFICATION','RUNTIME_PARITY','HUMAN_APPROVAL']},
 {'transition_id':'MICRO_LIVE_TO_CHAMPION','from_state':'MICRO_LIVE_CANDIDATE','to_state':'CHAMPION','prerequisites':['MICRO_LIVE_EVIDENCE','CAPITAL_COMMITTEE_APPROVAL','SURVEILLANCE_READY']},
 {'transition_id':'ANY_TO_SUSPENDED','from_state':'*','to_state':'SUSPENDED','prerequisites':['REVOCATION_TRIGGER']},
 {'transition_id':'ANY_TO_RETIRED','from_state':'*','to_state':'RETIRED','prerequisites':['RETIREMENT_DECISION']},
]
PREREQUISITES = [
 {'prerequisite_id':'SOURCE_INTEGRITY','evidence_class':'UPSTREAM_INTEGRITY','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'REPORTING_ELIGIBILITY','evidence_class':'ACL07_DECISION','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'VALIDATED_EVIDENCE','evidence_class':'ACL07_DECISION','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'NON_DIAGNOSTIC','evidence_class':'LANE_CLASSIFICATION','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'NON_BASELINE','evidence_class':'ORIGIN_CLASSIFICATION','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'PROSPECTIVE_EVIDENCE','evidence_class':'PROSPECTIVE','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'INDEPENDENT_REPLICATION','evidence_class':'REPLICATION','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'EXECUTION_ECONOMICS','evidence_class':'ECONOMICS','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'OOD_AND_ABSTENTION','evidence_class':'OOD','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'HUMAN_APPROVAL','evidence_class':'APPROVAL','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'SECURITY_CLEARANCE','evidence_class':'SECURITY','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'RUNTIME_PARITY_PLAN','evidence_class':'RUNTIME_PLAN','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'PAPER_EVIDENCE','evidence_class':'PAPER','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'SHADOW_EVIDENCE','evidence_class':'SHADOW','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'BROKER_QUALIFICATION','evidence_class':'BROKER','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'RUNTIME_PARITY','evidence_class':'PARITY','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'MICRO_LIVE_EVIDENCE','evidence_class':'MICRO_LIVE','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'CAPITAL_COMMITTEE_APPROVAL','evidence_class':'CAPITAL_APPROVAL','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'SURVEILLANCE_READY','evidence_class':'SURVEILLANCE','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'REVOCATION_TRIGGER','evidence_class':'CONTROL','unknown_behavior':'BLOCK'},
 {'prerequisite_id':'RETIREMENT_DECISION','evidence_class':'CONTROL','unknown_behavior':'BLOCK'},
]
def state_registry_snapshot() -> dict:
    body={'schema_version':'1.0.0','registry_id':'ACL10_STATE_REGISTRY_V1','closed_registry':True,'states':STATES}
    return with_digest(body,'registry_digest')
def transition_registry_snapshot() -> dict:
    body={'schema_version':'1.0.0','registry_id':'ACL10_TRANSITION_REGISTRY_V1','closed_registry':True,'transitions':TRANSITIONS}
    return with_digest(body,'registry_digest')
def prerequisite_registry_snapshot() -> dict:
    body={'schema_version':'1.0.0','registry_id':'ACL10_PREREQUISITE_REGISTRY_V1','closed_registry':True,'prerequisites':PREREQUISITES}
    return with_digest(body,'registry_digest')
def validate_registries(state:dict, transition:dict, prerequisite:dict) -> None:
    if state != state_registry_snapshot() or transition != transition_registry_snapshot() or prerequisite != prerequisite_registry_snapshot(): raise PolicyError('ACL10_REGISTRY_DRIFT')
    state_ids={x['state_id'] for x in state['states']}; prereq_ids={x['prerequisite_id'] for x in prerequisite['prerequisites']}
    if len(state_ids)!=len(state['states']) or len(prereq_ids)!=len(prerequisite['prerequisites']): raise PolicyError('ACL10_REGISTRY_DUPLICATE')
    for item in transition['transitions']:
        if item['from_state']!='*' and item['from_state'] not in state_ids: raise PolicyError('ACL10_TRANSITION_FROM_UNKNOWN')
        if item['to_state'] not in state_ids: raise PolicyError('ACL10_TRANSITION_TO_UNKNOWN')
        if not set(item['prerequisites']).issubset(prereq_ids): raise PolicyError('ACL10_TRANSITION_PREREQUISITE_UNKNOWN')

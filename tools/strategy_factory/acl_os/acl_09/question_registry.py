from __future__ import annotations
from .canonical import with_digest
from .errors import PolicyError
ENTRIES=[
 {'question_id':'SCHEDULE_INDEPENDENT_REPLICATION','target_gate':'INDEPENDENT_REPLICATION','cost_units':28,'information_gain':10,'risk_reduction':10,'decision_relevance':10,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'RUN_PROSPECTIVE_SHADOW_EVALUATION','target_gate':'PROSPECTIVE_EVIDENCE','cost_units':24,'information_gain':10,'risk_reduction':9,'decision_relevance':10,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'COLLECT_EXECUTION_COST_EVIDENCE','target_gate':'EXECUTION_ECONOMICS','cost_units':14,'information_gain':9,'risk_reduction':10,'decision_relevance':9,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'BUILD_OOD_AND_ABSTENTION_EVIDENCE','target_gate':'OOD_AND_ABSTENTION','cost_units':16,'information_gain':8,'risk_reduction':9,'decision_relevance':8,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'COLLECT_TAIL_PATH_EVIDENCE','target_gate':'DISTRIBUTIONAL_ROBUSTNESS','cost_units':12,'information_gain':8,'risk_reduction':8,'decision_relevance':8,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'ADD_TEMPORAL_HOLDOUT_EVIDENCE','target_gate':'TEMPORAL_GENERALIZATION','cost_units':10,'information_gain':8,'risk_reduction':7,'decision_relevance':8,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'COLLECT_SIGNIFICANCE_EVIDENCE','target_gate':'STATISTICAL_SIGNIFICANCE','cost_units':8,'information_gain':7,'risk_reduction':6,'decision_relevance':7,'requires_new_batch':True,'requires_human_approval':True},
 {'question_id':'REDUCE_OR_REFREEZE_TESTING_FAMILY','target_gate':'MULTIPLE_TESTING','cost_units':6,'information_gain':5,'risk_reduction':8,'decision_relevance':7,'requires_new_batch':True,'requires_human_approval':True},
]
def registry_snapshot()->dict:
    return with_digest({'schema_version':'1.0.0','registry_id':'ACL09_RESEARCH_QUESTION_REGISTRY_V1','closed_world':True,'entries':ENTRIES},'registry_digest')
def validate_registry(doc:dict)->dict:
    expected=registry_snapshot()
    if doc!=expected: raise PolicyError('ACL09_RESEARCH_QUESTION_REGISTRY_NOT_CANONICAL')
    return doc
def by_id(doc:dict)->dict: return {x['question_id']:x for x in doc['entries']}

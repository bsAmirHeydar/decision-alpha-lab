from __future__ import annotations
from .canonical import stable_id, with_digest

def build_provenance(promotion_run_id:str,binding:dict,policy:dict,subject_bundle:dict,matrix:dict,decision_bundle:dict,runtime_manifest:dict,events:dict) -> dict:
    nodes=[
      {'node_id':'ACL09_HANDOFF','artifact_type':'ACL09_TO_ACL10','digest':binding['handoff_digest']},
      {'node_id':'ACL09_MEMORY','artifact_type':'MEMORY_INDEX','digest':binding['memory_index_digest']},
      {'node_id':'ACL09_PLAN','artifact_type':'PLAN_PORTFOLIO','digest':binding['plan_portfolio_digest']},
      {'node_id':'ACL10_POLICY','artifact_type':'PROMOTION_POLICY','digest':policy['policy_digest']},
      {'node_id':'ACL10_SUBJECTS','artifact_type':'SOURCE_SUBJECT_BUNDLE','digest':subject_bundle['subject_bundle_digest']},
      {'node_id':'ACL10_PREREQUISITES','artifact_type':'PREREQUISITE_MATRIX','digest':matrix['matrix_digest']},
      {'node_id':'ACL10_DECISIONS','artifact_type':'PROMOTION_DECISION_BUNDLE','digest':decision_bundle['decision_bundle_digest']},
      {'node_id':'ACL10_RUNTIME','artifact_type':'RUNTIME_CANDIDATE_MANIFEST','digest':runtime_manifest['runtime_candidate_manifest_digest']},
      {'node_id':'ACL10_EVENTS','artifact_type':'PROMOTION_EVENT_LEDGER','digest':events['ledger_digest']},
    ]
    edges=[
      {'from':'ACL09_HANDOFF','relation':'BINDS','to':'ACL09_MEMORY'}, {'from':'ACL09_HANDOFF','relation':'BINDS','to':'ACL09_PLAN'},
      {'from':'ACL09_MEMORY','relation':'PROJECTED_AS','to':'ACL10_SUBJECTS'}, {'from':'ACL10_POLICY','relation':'GOVERNS','to':'ACL10_PREREQUISITES'},
      {'from':'ACL10_SUBJECTS','relation':'EVALUATED_BY','to':'ACL10_PREREQUISITES'}, {'from':'ACL10_PREREQUISITES','relation':'DETERMINES','to':'ACL10_DECISIONS'},
      {'from':'ACL10_DECISIONS','relation':'BOUNDS','to':'ACL10_RUNTIME'}, {'from':'ACL10_DECISIONS','relation':'RECORDED_IN','to':'ACL10_EVENTS'}]
    body={'schema_version':'1.0.0','graph_id':stable_id('PROMPROV',promotion_run_id),'promotion_run_id':promotion_run_id,'nodes':nodes,'edges':edges,'reaches_acl07_validation':True,'reaches_acl09_memory':True,'source_memory_mutated':False,'source_decisions_mutated':False,'promotion_executed':False,'runtime_generation_authority_granted':False,'live_order_authority_granted':False,'capital_authority_granted':False}
    return with_digest(body,'graph_digest')

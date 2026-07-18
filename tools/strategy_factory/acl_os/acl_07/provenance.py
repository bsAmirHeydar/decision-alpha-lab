from __future__ import annotations
from typing import Any
from .canonical import stable_id,with_digest

def build_provenance(validation_id:str,bundle:dict,policy:dict,gate_matrix:dict,decisions:dict,ledger:dict)->dict[str,Any]:
    nodes=[
      {'node_id':'ACL06_HANDOFF','artifact_type':'ACL06_TO_ACL07','digest':bundle['handoff']['handoff_digest']},
      {'node_id':'ACL06_RESULT_BUNDLE','artifact_type':'RESEARCH_RESULT_BUNDLE','digest':bundle['bundle']['result_bundle_digest']},
      {'node_id':'ACL07_POLICY','artifact_type':'VALIDATION_POLICY','digest':policy['policy_digest']},
      {'node_id':'ACL07_GATE_MATRIX','artifact_type':'VALIDATION_GATE_MATRIX','digest':gate_matrix['gate_matrix_digest']},
      {'node_id':'ACL07_DECISIONS','artifact_type':'VALIDATION_DECISION_BUNDLE','digest':decisions['decision_bundle_digest']},
      {'node_id':'ACL07_EVENTS','artifact_type':'VALIDATION_EVENT_LEDGER','digest':ledger['ledger_digest']}]
    edges=[{'from':'ACL06_HANDOFF','to':'ACL06_RESULT_BUNDLE','relation':'BINDS'}, {'from':'ACL06_RESULT_BUNDLE','to':'ACL07_GATE_MATRIX','relation':'VALIDATED_BY'}, {'from':'ACL07_POLICY','to':'ACL07_GATE_MATRIX','relation':'GOVERNS'}, {'from':'ACL07_GATE_MATRIX','to':'ACL07_DECISIONS','relation':'DETERMINES'}, {'from':'ACL07_DECISIONS','to':'ACL07_EVENTS','relation':'RECORDED_IN'}]
    body={'schema_version':'1.0.0','graph_id':stable_id('VALPROV',validation_id),'validation_id':validation_id,'nodes':nodes,'edges':edges,'reaches_acl06_research_run':True,'research_results_mutated':False,'diagnostic_lane_promoted':False,'execution_authority_granted':False}
    return with_digest(body,'graph_digest')

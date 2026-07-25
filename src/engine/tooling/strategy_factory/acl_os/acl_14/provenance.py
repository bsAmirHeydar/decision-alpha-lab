from __future__ import annotations
from .canonical import stable_id,with_digest
def build(binding:dict,req:dict,contract:dict,readiness:dict,decision:dict,execution:dict)->dict:
    nodes=[
      {'node_id':'ACL13_HANDOFF','artifact_type':'ACL13_TO_ACL14','digest':binding['acl13_handoff_digest']},
      {'node_id':'PILOT_REQUEST','artifact_type':'PILOT_REQUEST','digest':req['pilot_request_digest']},
      {'node_id':'PILOT_CONTRACT','artifact_type':'FIRST_REAL_CONTEXT_PILOT_CONTRACT','digest':contract['pilot_contract_digest']},
      {'node_id':'READINESS_MATRIX','artifact_type':'PILOT_READINESS_MATRIX','digest':readiness['readiness_matrix_digest']},
      {'node_id':'READINESS_DECISION','artifact_type':'PILOT_READINESS_DECISION','digest':decision['pilot_readiness_decision_digest']},
      {'node_id':'EXECUTION_MANIFEST','artifact_type':'EMPTY_PILOT_EXECUTION_MANIFEST','digest':execution['pilot_execution_manifest_digest']},
    ]
    edges=[{'from':'ACL13_HANDOFF','to':'PILOT_REQUEST'},{'from':'PILOT_REQUEST','to':'PILOT_CONTRACT'},{'from':'PILOT_CONTRACT','to':'READINESS_MATRIX'},{'from':'READINESS_MATRIX','to':'READINESS_DECISION'},{'from':'READINESS_DECISION','to':'EXECUTION_MANIFEST'}]
    return with_digest({'schema_version':'1.0.0','graph_id':stable_id('ACL14PROV',req['pilot_request_id'],length=28),'nodes':nodes,'edges':edges,'reaches_acl13_assessment':True,'synthetic_reference_reused_as_real':False,'prospective_evidence_invented':False,'pilot_execution_materialized':False,'validation_evidence_invented':False,'runtime_authority_created':False,'live_order_authority_created':False,'capital_authority_created':False},'graph_digest')

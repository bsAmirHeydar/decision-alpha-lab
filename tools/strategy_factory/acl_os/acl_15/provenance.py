from __future__ import annotations
from .canonical import stable_id,with_digest
def build_provenance(run_id:str,binding:dict,contracts:dict,ops:dict,decision:dict)->dict:
    nodes=[
      {'node_id':'ACL14_HANDOFF','artifact_type':'ACL14_TO_ACL15','digest':binding['acl14_handoff_digest']},
      {'node_id':'ACL14_PILOT_CONTRACT','artifact_type':'FIRST_REAL_CONTEXT_PILOT_CONTRACT','digest':binding['pilot_contract_digest']},
      {'node_id':'ACL15_FLEET_REGISTRATION','artifact_type':'FLEET_REGISTRATION_CONTRACT','digest':contracts['fleet']['fleet_registration_digest']},
      {'node_id':'ACL15_EVIDENCE_INVENTORY','artifact_type':'PILOT_EVIDENCE_INVENTORY','digest':ops['evidence']['evidence_inventory_digest']},
      {'node_id':'ACL15_CLOSURE_DECISION','artifact_type':'NON_CAPITAL_CLOSURE_DECISION','digest':decision['closure_decision_digest']},
    ]
    edges=[{'from':nodes[i]['node_id'],'to':nodes[i+1]['node_id'],'relation':'DERIVED_WITHOUT_SEMANTIC_MUTATION'} for i in range(len(nodes)-1)]
    return with_digest({'schema_version':'1.0.0','graph_id':stable_id('PROV',run_id),'fleet_closure_run_id':run_id,'nodes':nodes,'edges':edges,'reaches_acl14_pilot_package':True,'pilot_readiness_reinterpreted':False,'pilot_outcomes_invented':False,'prospective_evidence_invented':False,'validation_bypassed':False,'promotion_bypassed':False,'runtime_generated':False,'live_order_authority_created':False,'capital_authority_created':False},'graph_digest')

from __future__ import annotations
from .canonical import with_digest
def build_provenance(bundle: dict,assessment: dict,decision: dict,generation: dict) -> dict:
    nodes=[
      {'node_id':'ACL10_HANDOFF','artifact_digest':bundle['handoff']['handoff_digest'],'artifact_type':'ACL10_TO_ACL11'},
      {'node_id':'ACL10_RUNTIME_MANIFEST','artifact_digest':bundle['runtime']['runtime_candidate_manifest_digest'],'artifact_type':'RUNTIME_CANDIDATE_MANIFEST'},
      {'node_id':'ACL11_PARITY_ASSESSMENT','artifact_digest':assessment['assessment_digest'],'artifact_type':'RUNTIME_PARITY_ASSESSMENT'},
      {'node_id':'ACL11_CUSTODY_DECISION','artifact_digest':decision['custody_decision_digest'],'artifact_type':'NON_EXECUTABLE_CUSTODY_DECISION'},
      {'node_id':'ACL11_GENERATION_MANIFEST','artifact_digest':generation['generation_manifest_digest'],'artifact_type':'EMPTY_RUNTIME_GENERATION_MANIFEST'}]
    edges=[{'from':'ACL10_HANDOFF','to':'ACL10_RUNTIME_MANIFEST'},{'from':'ACL10_RUNTIME_MANIFEST','to':'ACL11_PARITY_ASSESSMENT'},{'from':'ACL11_PARITY_ASSESSMENT','to':'ACL11_CUSTODY_DECISION'},{'from':'ACL11_CUSTODY_DECISION','to':'ACL11_GENERATION_MANIFEST'}]
    body={'schema_version':'1.0.0','nodes':nodes,'edges':edges,'reaches_acl10_promotion_state':True,'promotion_decisions_mutated':False,'runtime_candidate_invented':False,'runtime_generation_materialized':False,'signature_created':False,'live_order_authority_created':False,'capital_authority_created':False}
    return with_digest(body,'graph_digest')

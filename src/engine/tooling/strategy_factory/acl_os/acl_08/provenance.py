from __future__ import annotations
from .canonical import stable_id,with_digest
def build_provenance(report_id:str,bundle:dict,policy:dict,batch:dict,experience:dict,ledger:dict)->dict:
    nodes=[
      {'node_id':'ACL07_HANDOFF','artifact_type':'ACL07_TO_ACL08','digest':bundle['handoff']['handoff_digest']},
      {'node_id':'ACL07_DECISIONS','artifact_type':'VALIDATION_DECISION_BUNDLE','digest':bundle['decisions']['decision_bundle_digest']},
      {'node_id':'ACL07_GATES','artifact_type':'VALIDATION_GATE_MATRIX','digest':bundle['matrix']['gate_matrix_digest']},
      {'node_id':'ACL08_POLICY','artifact_type':'REPORT_POLICY','digest':policy['policy_digest']},
      {'node_id':'ACL08_REPORT','artifact_type':'BATCH_REPORT','digest':batch['batch_report_digest']},
      {'node_id':'ACL08_EXPERIENCE','artifact_type':'EXPERIENCE_BUNDLE','digest':experience['experience_bundle_digest']},
      {'node_id':'ACL08_EVENTS','artifact_type':'REPORT_EVENT_LEDGER','digest':ledger['ledger_digest']},
    ]
    edges=[
      {'from':'ACL07_HANDOFF','relation':'BINDS','to':'ACL07_DECISIONS'},
      {'from':'ACL07_HANDOFF','relation':'BINDS','to':'ACL07_GATES'},
      {'from':'ACL07_DECISIONS','relation':'PROJECTED_WITHOUT_REINTERPRETATION','to':'ACL08_REPORT'},
      {'from':'ACL07_GATES','relation':'PROJECTED_WITHOUT_REINTERPRETATION','to':'ACL08_REPORT'},
      {'from':'ACL08_POLICY','relation':'GOVERNS','to':'ACL08_REPORT'},
      {'from':'ACL08_REPORT','relation':'YIELDS_NON_PROMOTIONAL','to':'ACL08_EXPERIENCE'},
      {'from':'ACL08_EXPERIENCE','relation':'RECORDED_IN','to':'ACL08_EVENTS'},
    ]
    return with_digest({'schema_version':'1.0.0','graph_id':stable_id('REPPROV',report_id),'report_id':report_id,'nodes':nodes,'edges':edges,'reaches_acl07_validation':True,'validation_decisions_mutated':False,'diagnostic_lane_promoted':False,'execution_authority_granted':False},'graph_digest')

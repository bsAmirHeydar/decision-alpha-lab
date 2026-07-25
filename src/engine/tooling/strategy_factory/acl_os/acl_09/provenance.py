from __future__ import annotations
from .canonical import with_digest,stable_id
def build_provenance(memory_run_id:str,bundle:dict,memory_policy:dict,planner_policy:dict,equivalence:dict,index:dict,portfolio:dict,ledger:dict)->dict:
    nodes=[
      {'node_id':'ACL08_HANDOFF','artifact_type':'ACL08_TO_ACL09','digest':bundle['handoff']['handoff_digest']},
      {'node_id':'ACL08_REPORT','artifact_type':'BATCH_REPORT','digest':bundle['batch']['batch_report_digest']},
      {'node_id':'ACL08_EXPERIENCE','artifact_type':'EXPERIENCE_BUNDLE','digest':bundle['experience']['experience_bundle_digest']},
      {'node_id':'ACL09_MEMORY_POLICY','artifact_type':'MEMORY_POLICY','digest':memory_policy['policy_digest']},
      {'node_id':'ACL09_PLANNER_POLICY','artifact_type':'PLANNER_POLICY','digest':planner_policy['policy_digest']},
      {'node_id':'ACL09_EQUIVALENCE','artifact_type':'DUPLICATE_EQUIVALENCE_REPORT','digest':equivalence['equivalence_report_digest']},
      {'node_id':'ACL09_MEMORY','artifact_type':'MEMORY_INDEX','digest':index['memory_index_digest']},
      {'node_id':'ACL09_PLAN','artifact_type':'PLAN_PORTFOLIO','digest':portfolio['portfolio_digest']},
      {'node_id':'ACL09_EVENTS','artifact_type':'MEMORY_EVENT_LEDGER','digest':ledger['ledger_digest']},
    ]
    edges=[
      {'from':'ACL08_HANDOFF','relation':'BINDS','to':'ACL08_REPORT'},
      {'from':'ACL08_HANDOFF','relation':'BINDS','to':'ACL08_EXPERIENCE'},
      {'from':'ACL08_EXPERIENCE','relation':'CLASSIFIED_BY','to':'ACL09_EQUIVALENCE'},
      {'from':'ACL09_MEMORY_POLICY','relation':'GOVERNS','to':'ACL09_MEMORY'},
      {'from':'ACL09_EQUIVALENCE','relation':'CONTROLS_ADMISSION','to':'ACL09_MEMORY'},
      {'from':'ACL09_MEMORY','relation':'BOUNDS_SOURCES_FOR','to':'ACL09_PLAN'},
      {'from':'ACL09_PLANNER_POLICY','relation':'GOVERNS','to':'ACL09_PLAN'},
      {'from':'ACL09_PLAN','relation':'RECORDED_IN','to':'ACL09_EVENTS'},
    ]
    return with_digest({'schema_version':'1.0.0','graph_id':stable_id('MEMPROV',memory_run_id),'memory_run_id':memory_run_id,'nodes':nodes,'edges':edges,'reaches_acl07_validation':True,'source_decisions_mutated':False,'diagnostic_memory_selectable':False,'research_execution_authority_granted':False,'execution_authority_granted':False},'graph_digest')

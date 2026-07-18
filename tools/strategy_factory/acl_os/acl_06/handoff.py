from .canonical import with_digest
from .policies import CLAIM_CEILING,HANDOFF_OUT

def build_acl07_handoff(run,result_bundle,dag,receipts,accounting,object_index,events,provenance):
    body={'schema_version':'1.0.0','handoff_type':HANDOFF_OUT,'run_id':run['run_id'],'batch_id':run['batch_id'],'research_run_digest':run['research_run_digest'],'dag_digest':dag['dag_digest'],'result_bundle_digest':result_bundle['result_bundle_digest'],'task_receipt_set_digest':receipts['receipt_set_digest'],'resource_accounting_digest':accounting['accounting_digest'],'object_index_digest':object_index['object_index_digest'],'event_ledger_digest':events['ledger_digest'],'provenance_graph_digest':provenance['graph_digest'],'claim_ceiling':CLAIM_CEILING,'required_acl07_actions':['VERIFY_RESEARCH_EVIDENCE','APPLY_UNIFIED_VALIDATION_GATES','ISSUE_NON_PROMOTIONAL_VALIDATION_DECISION'],'forbidden_acl07_actions':['MUTATE_RESEARCH_RESULTS','MUTATE_FROZEN_BATCH','PROMOTE_DIAGNOSTIC_LANE','INFER_ALPHA_WITHOUT_GATES','AUTHORIZE_EXECUTION','ACTIVATE_CAPITAL'],'live_order_submission_allowed':False,'capital_activation_allowed':False}
    return with_digest(body,'handoff_digest')

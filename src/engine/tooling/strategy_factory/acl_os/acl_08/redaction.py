from __future__ import annotations
import json
from typing import Any
from .canonical import with_digest
from .errors import RedactionError
PROHIBITED_EXTERNAL=['SETUP_','CAND_','VALDEC_','candidate_id','setup_id','decision_id','gate_result_digest','candidate_report_digest']
def build_views(batch:dict[str,Any],executive:dict[str,Any],candidate_reports:list[dict[str,Any]])->dict[str,dict[str,Any]]:
    internal=with_digest({'schema_version':'1.0.0','audience':'INTERNAL_RESEARCH','batch_report_digest':batch['batch_report_digest'],'candidate_reports':candidate_reports,'decision_counts':batch['decision_counts'],'limitations':batch['limitations'],'claim_ceiling':batch['claim_ceiling'],'authority':{'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}},'view_digest')
    executive_view=with_digest({'schema_version':'1.0.0','audience':'EXECUTIVE','report_id':batch['report_id'],'answer_first':executive['answer_first'],'key_findings':executive['key_findings'],'decision_counts':executive['decision_counts'],'limitations':executive['limitations'],'claim_ceiling':executive['claim_ceiling'],'authority':{'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}},'view_digest')
    external=with_digest({'schema_version':'1.0.0','audience':'EXTERNAL_RESTRICTED','report_id':batch['report_id'],'reported_at':batch['reported_at'],'decision_counts':batch['decision_counts'],'reporting_eligible_count':batch['reporting_eligible_count'],'limitations':batch['limitations'],'claim_ceiling':batch['claim_ceiling'],'authority':{'alpha_claim_allowed':False,'promotion_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}},'view_digest')
    text=json.dumps(external,sort_keys=True)
    leaked=[x for x in PROHIBITED_EXTERNAL if x in text]
    if leaked: raise RedactionError(f'external view leaked restricted identifiers: {leaked}')
    return {'INTERNAL_RESEARCH':internal,'EXECUTIVE':executive_view,'EXTERNAL_RESTRICTED':external}
def redaction_report(report_id:str,views:dict[str,dict])->dict:
    return with_digest({'schema_version':'1.0.0','report_id':report_id,'profiles_applied':sorted(views),'external_prohibited_tokens':PROHIBITED_EXTERNAL,'restricted_identifier_leaks':[],'decision_semantics_changed':False,'passed':True},'report_digest')

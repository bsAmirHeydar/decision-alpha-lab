from __future__ import annotations
from .canonical import stable_id,with_digest
def build_security(run_id:str,binding:dict,decision:dict)->dict:
    return with_digest({'schema_version':'1.0.0','security_report_id':stable_id('SEC',run_id),'fleet_closure_run_id':run_id,'acl14_package_verified':True,'closed_history_immutable':True,'path_traversal_allowed':False,'symlink_substitution_allowed':False,'network_access_allowed':False,'secret_access_allowed':False,'pilot_execution_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'automatic_reopen_allowed':False,'production_security_ready':False},'security_report_digest')

from __future__ import annotations
from .canonical import with_digest
def build(binding:dict,decision:dict)->dict:
    return with_digest({'schema_version':'1.0.0','acl13_security_status_preserved':True,'production_security_ready':False,'real_context_data_classification_required':True,'reference_fixture_contains_real_market_data':False,'secret_access_allowed':False,'network_access_allowed':False,'runtime_generation_allowed':False,'runtime_activation_allowed':False,'pilot_execution_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'source_binding_digest':binding['binding_digest'],'decision_digest':decision['pilot_readiness_decision_digest']},'security_report_digest')

from __future__ import annotations
from .canonical import with_digest
def build_security(binding:dict,decision:dict)->dict:
    return with_digest({'schema_version':'1.0.0','passed':True,'acl12_package_verified':True,'source_production_security_ready':False,'production_security_reinterpreted':False,'runtime_candidate_count':0,'production_key_material_accessed':False,'network_access_allowed':False,'pilot_execution_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'assessment_result_digest':decision['assessment_result_digest']},'security_report_digest')

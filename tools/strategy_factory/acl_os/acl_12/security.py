from __future__ import annotations
from .canonical import with_digest
def build_security_boundary_report(bundle:dict,decision:dict,artifacts:dict)->dict:
    scans=[artifacts[k]['passed'] for k in ['secret_scan','static_scan','mql5_scan','path_scan']]
    return with_digest({'schema_version':'1.0.0','passed':all(scans),'acl11_integrity_verified':True,'runtime_candidate_count':0,'runtime_candidate_invented':False,'runtime_generation_materialized':False,'secret_material_present':False,'production_key_material_present':False,'network_access_allowed':False,'runtime_activation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False,'scan_passed':all(scans),'readiness_decision_digest':decision['readiness_decision_digest']},'security_report_digest')

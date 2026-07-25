from __future__ import annotations
from .canonical import stable_id,with_digest
def build_reports(run_id:str,binding:dict,contracts:dict,ops:dict,decision:dict,registries:dict,closed_at:str)->dict:
    report=with_digest({'schema_version':'1.0.0','report_id':stable_id('FLEETREPORT',run_id),'fleet_closure_run_id':run_id,'closed_at':closed_at,'claim_ceiling':'FLEET_OPERATIONS_AND_CLOSURE_REFERENCE_ONLY','section_registry_digest':registries['report']['registry_digest'],'sections':[
      {'section_id':'IDENTITY_AND_SCOPE','facts':{'fleet_id':contracts['fleet']['fleet_id'],'pilot_run_id':binding['pilot_run_id']}},
      {'section_id':'UPSTREAM_PILOT_STATUS','facts':{'pilot_readiness_state':binding['pilot_readiness_state'],'pilot_executed':False,'prospective_evidence_present':False}},
      {'section_id':'FLEET_REGISTRATION','facts':{'status':contracts['fleet']['fleet_status'],'package_count':1}},
      {'section_id':'LIFECYCLE_OWNERSHIP','facts':{'role_count':len(contracts['ownership']['roles']),'self_approval_allowed':False}},
      {'section_id':'RETENTION','facts':{'status':ops['retention_status']['status'],'deletion_allowed':False}},
      {'section_id':'SURVEILLANCE','facts':{'status':ops['surveillance_status']['status'],'production_monitoring_active':False}},
      {'section_id':'EVIDENCE_INVENTORY','facts':{'pilot_design_present':True,'pilot_outcomes_present':False,'prospective_rows':0}},
      {'section_id':'CLOSURE_DECISION','facts':{'state':decision['state'],'decision':decision['decision']}},
      {'section_id':'REOPEN_AND_MIGRATION','facts':{'allowed_reopen_actions':contracts['reopen']['allowed_actions'],'automatic_reopen_allowed':False}},
      {'section_id':'SECURITY_AND_AUTHORITY','facts':{'runtime_generation_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}},
      {'section_id':'RESIDUAL_RISK','facts':{'real_pilot_not_run':True,'validation_not_performed':True,'production_security_not_proven':True}},
      {'section_id':'FINAL_PROGRAM_STATUS','facts':{'reference_program_closed':True,'production_program_closed':False}},
    ],'pilot_outcome_claimed':False,'prospective_evidence_claimed':False,'validation_claimed':False,'alpha_claimed':False,'runtime_claimed':False,'capital_claimed':False},'fleet_closure_report_digest')
    executive=with_digest({'schema_version':'1.0.0','executive_brief_id':stable_id('EXECBRIEF',run_id),'fleet_closure_run_id':run_id,'answer_first':'The ACL reference lifecycle is closed as a governed, non-capital, non-executed package. Reopening requires new authorized real evidence.','key_facts':['ACL-14 package integrity verified','pilot design preserved','zero prospective outcomes','fleet ownership, retention and surveillance contracts registered','reference lifecycle closed without validation, runtime, orders or capital'],'closure_state':decision['state'],'allowed_next_action':'AUTHOR_NEW_REAL_CONTEXT_PILOT_PACKAGE','production_readiness_claimed':False},'executive_brief_digest')
    residual=with_digest({'schema_version':'1.0.0','risk_report_id':stable_id('RISKS',run_id),'fleet_closure_run_id':run_id,'risks':[{'risk_id':'REAL_PILOT_NOT_EXECUTED','status':'OPEN','blocks':'PROSPECTIVE_EVIDENCE'},{'risk_id':'VALIDATION_NOT_PERFORMED','status':'OPEN','blocks':'PROMOTION'},{'risk_id':'RUNTIME_PARITY_NOT_PROVEN','status':'OPEN','blocks':'RUNTIME'},{'risk_id':'PRODUCTION_SECURITY_NOT_PROVEN','status':'OPEN','blocks':'PRODUCTION'},{'risk_id':'BROKER_AND_CAPITAL_BOUNDARY_UNTESTED','status':'OPEN','blocks':'LIVE_CAPITAL'}],'automatic_risk_acceptance_allowed':False},'residual_risk_report_digest')
    return {'report':report,'executive':executive,'residual':residual}

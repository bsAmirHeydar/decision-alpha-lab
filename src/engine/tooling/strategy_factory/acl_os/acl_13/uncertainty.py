from __future__ import annotations
from .canonical import with_digest
def build_uncertainty(req:dict,binding:dict,support:dict,baselines:dict)->dict:
    gaps=[
      {'gap_id':'REAL_CONTEXT_DATA','status':'MISSING' if req.get('synthetic_reference_data') else 'PRESENT','blocks_validation':True,'next_action':'REPLACE_SYNTHETIC_FIXTURE_WITH_APPROVED_REAL_CONTEXT_INPUT'},
      {'gap_id':'PROSPECTIVE_EVIDENCE','status':'MISSING','blocks_validation':True,'next_action':'RUN_PRECOMMITTED_PROSPECTIVE_PILOT'},
      {'gap_id':'INDEPENDENT_REPLICATION','status':'MISSING','blocks_validation':True,'next_action':'REPLICATE_ON_INDEPENDENT_PERIOD_OR_LAB'},
      {'gap_id':'EXECUTION_ECONOMICS','status':'MISSING','blocks_validation':True,'next_action':'COLLECT_BROKER_AND_FILL_EVIDENCE'},
      {'gap_id':'PRODUCTION_SECURITY','status':'UNKNOWN','blocks_validation':False,'next_action':'CLOSE_ACL12_PRODUCTION_SECURITY_BLOCKERS'},
      {'gap_id':'RUNTIME_PARITY','status':'MISSING','blocks_validation':True,'next_action':'PRODUCE_METAEDITOR_AND_STRATEGY_TESTER_PARITY_EVIDENCE'},
      {'gap_id':'SAMPLE_SUPPORT','status':'LIMITED','blocks_validation':True,'next_action':'INCREASE_MATURE_OCCURRENCE_SUPPORT'}]
    limitations=['Reference observations are synthetic.','Circular-shift baselines are descriptive, not inferential validation.','Declared setup families are bounded examples, not discovered alpha.','No prospective, independent, execution-economics or runtime-parity evidence exists.','ACL-12 explicitly reports production security not ready.']
    body={'schema_version':'1.0.0','gap_count':len(gaps),'gaps':gaps,'limitations':limitations,'unknown_count':sum(1 for g in gaps if g['status']=='UNKNOWN'),'missing_count':sum(1 for g in gaps if g['status']=='MISSING'),'triage_support_limited':not support['support_sufficient_for_validation'],'random_baseline_descriptive_only':baselines['descriptive_only'],'production_security_ready':False,'validation_claim_allowed':False,'alpha_claim_allowed':False}
    return with_digest(body,'uncertainty_report_digest')

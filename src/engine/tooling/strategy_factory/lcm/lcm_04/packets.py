from __future__ import annotations
from .canonical import content_id,digest_object
from .case_catalog import required_cases

def packet(identity,profile):
    if identity['protected_platform_asset']:
        status='EXCLUDED_PROTECTED_PLATFORM';reason=['PROTECTED_PLATFORM_NOT_LEGACY_CHARACTERIZATION_TARGET']
    elif identity['security_sensitive'] or identity['identity_status']=='SECURITY_REVIEW_BLOCKED':
        status='BLOCKED_SECURITY_REVIEW';reason=['SECURITY_REVIEW_REQUIRED','HUMAN_OWNER_PENDING']
    elif identity['owner_resolution_status']!='HUMAN_APPROVED':
        status='BLOCKED_OWNER_APPROVAL';reason=['HUMAN_SEMANTIC_OWNER_APPROVAL_PENDING','CODE_OWNER_APPROVAL_PENDING']
    else:
        status='READY_FOR_INSTRUMENTATION';reason=[]
    cases=required_cases(profile)
    material={'identity_id':identity['identity_id'],'identity_digest':identity['identity_digest'],'profile_digest':profile['profile_digest'],'case_types':cases}
    out={'schema_version':'1.0.0','packet_id':content_id('CHARPACKET',material),'identity_id':identity['identity_id'],
         'identity_kind':identity['identity_kind'],'family_candidate':identity['family_candidate'],
         'source_artifact_path':identity['source_artifact_path'],'source_artifact_sha256':identity['source_artifact_sha256'],
         'identity_digest':identity['identity_digest'],'identity_status':identity['identity_status'],
         'owner_resolution_status':identity['owner_resolution_status'],'protected_platform_asset':identity['protected_platform_asset'],
         'security_sensitive':identity['security_sensitive'],'packet_status':status,
         'legacy_execution_allowed':status=='READY_FOR_INSTRUMENTATION','source_mutation_allowed':False,
         'required_case_types':cases,'required_case_count':len(cases),'static_profile_digest':profile['profile_digest'],
         'blocking_reason_codes':reason,'observed_behavior_captured':False,'intended_correction_registered':False,
         'packet_digest':None}
    out['packet_digest']=digest_object(out,'packet_digest');return out

def priority(packet,profile):
    kind_weight={'CONTEXT':0,'SETUP':5,'VISUALIZER':10,'TREATMENT':20,'ADAPTER':30,'ENGINE':40,'SUPPORT_ARTIFACT':60}.get(packet['identity_kind'],70)
    status_weight={'READY_FOR_INSTRUMENTATION':0,'BLOCKED_OWNER_APPROVAL':20,'BLOCKED_SECURITY_REVIEW':60,'EXCLUDED_PROTECTED_PLATFORM':90}[packet['packet_status']]
    score=min(100,kind_weight+status_weight+profile['characterization_risk_score']//4)
    out={'packet_id':packet['packet_id'],'identity_id':packet['identity_id'],'identity_kind':packet['identity_kind'],
         'family_candidate':packet['family_candidate'],'packet_status':packet['packet_status'],
         'risk_score':profile['characterization_risk_score'],'queue_priority_score':score,
         'owner_review_required':packet['owner_resolution_status']!='HUMAN_APPROVED',
         'security_review_required':packet['security_sensitive'],
         'legacy_execution_allowed':packet['legacy_execution_allowed'],'priority_digest':None}
    out['priority_digest']=digest_object(out,'priority_digest');return out

def instrumentation_plan(packet,profile):
    points=['CASE_ENTRY','INPUT_ACCEPTANCE','STATE_BEFORE_AFTER','CASE_EXIT']
    caps=profile['capabilities']
    if caps['timeframe_api'] or caps['current_bar'] or caps['closed_bar']: points+=['BAR_SELECTION','BAR_CLOSURE','DATA_AVAILABILITY']
    if caps['drawing_api']: points+=['DRAWING_CREATE','DRAWING_UPDATE','DRAWING_DELETE']
    if caps['order_api']: points+=['DRY_REQUEST_INTENT','REQUEST_CANCELLATION','REQUEST_REJECTION']
    if caps['global_state'] or caps['timer_api']: points+=['STATE_PERSIST','STATE_RESTORE','TIMER_EVENT']
    if caps['session_api'] or caps['wall_clock']: points+=['SESSION_RESOLUTION','TIMEZONE_RESOLUTION']
    out={'schema_version':'1.0.0','plan_id':content_id('INSTRPLAN',{'p':packet['packet_digest'],'points':sorted(set(points))}),
         'packet_id':packet['packet_id'],'identity_id':packet['identity_id'],'mode':'PLAN_ONLY_NO_SOURCE_MUTATION',
         'emission_points':sorted(set(points)),'normalized_trace_required':True,'raw_journal_required':True,
         'broker_submission_allowed':False,'source_patch_materialized':False,'legacy_execution_allowed':packet['legacy_execution_allowed'],
         'plan_digest':None};out['plan_digest']=digest_object(out,'plan_digest');return out

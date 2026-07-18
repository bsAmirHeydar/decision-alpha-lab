from __future__ import annotations
from .canonical import with_digest
def assess_completeness(req:dict,binding:dict)->dict:
    checks=[('EXACT_CONTEXT_IDENTITY',bool(req.get('context_id') and req.get('context_version'))),('DECLARED_OWNER',bool(req.get('owner_roles'))),('DOCTRINE_SUMMARY',bool(req.get('doctrine_summary','').strip())),('KNOWN_TIME_CONTRACT',req.get('known_time_contract',{}).get('future_data_allowed') is False),('ASSESSMENT_CUT',bool(req.get('assessment_cut_at'))),('OBSERVATIONS_PRESENT',bool(req.get('observations'))),('SETUP_FAMILIES_DECLARED',bool(req.get('declared_setup_families'))),('SECURITY_PACKAGE_BOUND',bool(binding.get('binding_digest'))),('PRODUCTION_SECURITY_DISCLOSED',binding.get('production_security_ready') is False),('RUNTIME_CANDIDATE_COUNT_DISCLOSED',binding.get('runtime_candidate_count')==0)]
    results=[{'check_id':i,'status':'PASS' if ok else 'FAIL','required':True} for i,ok in checks]
    passed=sum(1 for x in results if x['status']=='PASS')
    return with_digest({'schema_version':'1.0.0','check_count':len(results),'passed_count':passed,'failed_count':len(results)-passed,'completeness_ratio':passed/len(results),'results':results,'triage_input_complete':passed==len(results)},'completeness_report_digest')

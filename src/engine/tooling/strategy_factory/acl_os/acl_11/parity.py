from __future__ import annotations
from .canonical import stable_id,with_digest
from .policies import PARITY_STATUSES
def _result(req: dict,status: str,reason: str,evidence: list[str]) -> dict:
    assert status in PARITY_STATUSES
    return with_digest({'schema_version':'1.0.0','requirement_id':req['requirement_id'],'status':status,'reason_code':reason,'evidence_refs':evidence,'unknown_blocks_runtime':True},'result_digest')
def assess(bundle: dict,registry: dict,assessed_at: str) -> dict:
    count=bundle['runtime']['runtime_candidate_count']; results=[]; base=[bundle['binding']['binding_digest'],bundle['runtime']['runtime_candidate_manifest_digest']]
    for req in registry['requirements']:
        rid=req['requirement_id']
        if rid=='SOURCE_PROMOTION_PACKAGE_INTEGRITY': status,reason='SATISFIED','ACL10_PACKAGE_INTEGRITY_VERIFIED'
        elif rid=='RUNTIME_CANDIDATE_PRESENT': status,reason=('SATISFIED','RUNTIME_CANDIDATE_PRESENT') if count>0 else ('UNSATISFIED','NO_RUNTIME_CANDIDATES')
        elif count==0: status,reason='NOT_APPLICABLE','NO_RUNTIME_CANDIDATES_PARITY_NOT_RUN'
        else: status,reason='UNKNOWN','REQUIRED_RUNTIME_PARITY_EVIDENCE_MISSING'
        results.append(_result(req,status,reason,base))
    body={'schema_version':'1.0.0','assessment_id':stable_id('PARITY',bundle['handoff']['promotion_run_id'],registry['registry_digest']),'promotion_run_id':bundle['handoff']['promotion_run_id'],'assessed_at':assessed_at,'runtime_candidate_count':count,'results':results,'status_counts':{s:sum(1 for x in results if x['status']==s) for s in sorted(PARITY_STATUSES)},'all_hard_requirements_satisfied':all(x['status']=='SATISFIED' for x in results),'runtime_generation_allowed':False}
    return with_digest(body,'assessment_digest')

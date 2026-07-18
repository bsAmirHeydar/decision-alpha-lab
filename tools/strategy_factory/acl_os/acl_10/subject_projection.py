from __future__ import annotations
from typing import Any
from .canonical import stable_id, with_digest

def project_subjects(bundle: dict[str,Any]) -> dict[str,Any]:
    entries=bundle['entries']; quarantines=bundle['quarantines']; subjects=[]
    for decision in sorted(bundle['decisions'], key=lambda x:x['experience_id']):
        target=decision['target_memory_identity']; status=decision['admission_status']
        if status=='QUARANTINED_DIAGNOSTIC':
            source=quarantines[target]; experience_class='DIAGNOSTIC_EXCLUSION'; source_digest=source['quarantine_digest']; source_kind='DIAGNOSTIC_QUARANTINE'
        else:
            source=entries[target]; experience_class=source['experience_class']; source_digest=source['memory_entry_digest']; source_kind='MEMORY_ENTRY'
        body={'schema_version':'1.0.0','subject_id':stable_id('PROMSUB',decision['experience_id'],decision['admission_decision_digest']),'experience_id':decision['experience_id'],'admission_decision_id':decision['admission_decision_id'],'admission_status':status,'target_memory_identity':target,'source_kind':source_kind,'source_digest':source_digest,'experience_class':experience_class,'reporting_eligible':experience_class=='REPORTABLE_EVIDENCE','diagnostic':experience_class=='DIAGNOSTIC_EXCLUSION','baseline':experience_class=='BASELINE_REFERENCE'}
        subjects.append(with_digest(body,'subject_digest'))
    bundle_body={'schema_version':'1.0.0','memory_run_id':bundle['memory_run']['memory_run_id'],'subject_count':len(subjects),'subjects':subjects}
    return with_digest(bundle_body,'subject_bundle_digest')

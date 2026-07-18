from .canonical import with_digest
REASONS={
 'ACL07_BUNDLE_VERIFIED':'ACL-07 validation package passed integrity verification.',
 'DECISIONS_PRESERVED_EXACTLY':'All decision status and reason-code semantics are preserved.',
 'NO_REPORTING_ELIGIBLE_CANDIDATE':'No candidate is eligible for reportable evidence under ACL-07.',
 'EVIDENCE_INSUFFICIENT_RECORDED':'Insufficient evidence is captured as unknown, not as failure or alpha.',
 'BASELINE_RECORDED_AS_REFERENCE':'Baseline remains a comparator and is not promotable.',
 'DIAGNOSTIC_RECORDED_NON_SELECTABLE':'Diagnostic evidence remains segregated and non-selectable.',
 'VALIDATION_FAILURE_CAPTURED':'Validation failure is captured as negative knowledge.',
 'REPORTABLE_EVIDENCE_NON_PROMOTIONAL':'Reportable evidence is still non-promotional.',
 'AUDIENCE_REDACTION_APPLIED':'Audience view was generated under the closed redaction profile.',
 'NO_PREVIOUS_REPORT':'No previous report package was supplied for diffing.',
 'NO_MATERIAL_CHANGE':'The compared report package has no material semantic change.',
 'MATERIAL_CHANGE_DETECTED':'The compared report package differs in material evidence.',
 'UNKNOWN_GATES_REQUIRE_MORE_EVIDENCE':'One or more required gates remain UNKNOWN.',
 'REPORTING_HAS_NO_EXECUTION_AUTHORITY':'Reporting output cannot authorize orders or capital.',
}
def registry()->dict: return with_digest({'schema_version':'1.0.0','registry_id':'ACL08_REASON_CODES_V1','entries':[{'reason_code':k,'meaning':v} for k,v in sorted(REASONS.items())]},'registry_digest')

from __future__ import annotations
from .canonical import with_digest
def build_evidence_bundle(binding:dict,artifacts:dict,control_matrix:dict,threat_assessment:dict,risk_register:dict)->dict:
    refs=[binding['binding_digest'],control_matrix['assessment_digest'],threat_assessment['assessment_digest'],risk_register['register_digest']]
    refs.extend([artifacts[k][next(x for x in artifacts[k] if x.endswith('_digest'))] for k in ['secret_scan','static_scan','mql5_scan','path_scan','sbom','recall','operator','key_custody','incident','revocation']])
    body={'schema_version':'1.0.0','evidence_bundle_id':'ACL12_SECURITY_EVIDENCE_BUNDLE_V1','evidence_refs':sorted(set(refs)),'evidence_count':len(set(refs)),'reference_only':True,'production_security_evidence_complete':False,'external_scan_attestations_present':False,'production_key_attestation_present':False}
    return with_digest(body,'evidence_bundle_digest')

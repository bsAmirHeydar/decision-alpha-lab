from __future__ import annotations
from .canonical import with_digest
def build_key_custody_interface(signing_plan:dict)->dict:
    return with_digest({'schema_version':'1.0.0','interface_id':'ACL12_KEY_CUSTODY_INTERFACE_V1','signing_mode':signing_plan['signing_mode'],'input_key_material_present':False,'production_key_material_present':False,'production_key_access_allowed':False,'key_export_allowed':False,'signature_creation_allowed':False,'required_provider_classes':['HSM_OR_MANAGED_KMS','DETACHED_SIGNER','REVOCATION_REGISTRY'],'provider_connected':False,'rotation_evidence_present':False,'zeroization_evidence_present':False,'reason_code':'REFERENCE_MODE_PRODUCTION_KEY_ACCESS_DENIED'},'interface_digest')

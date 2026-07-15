from __future__ import annotations
from .canonical import content_hash, stable_id
from .checkpoint import validate_checkpoint
from .errors import RegistryError

def build_checkpoint_registry(checkpoint:dict,dossier:dict,contamination_audit:dict,membership_audit:dict,control_comparison:dict)->dict:
    validate_checkpoint(checkpoint)
    reasons=[]
    if not contamination_audit['passed']: reasons.append('contamination_audit_failed')
    if not membership_audit['passed']: reasons.append('membership_audit_failed')
    if not dossier['accepted_for_reference_registry']: reasons.append('representation_dossier_rejected')
    status='admitted_reference_synthetic' if not reasons else 'rejected'
    entry={"checkpoint_id":checkpoint['checkpoint_id'],"checkpoint_hash":checkpoint['checkpoint_hash'],"status":status,"reasons":reasons,"evidence_scope":"synthetic_reference","runtime_authority":False,"promotion_authority":False,"dossier_hash":dossier['dossier_hash'],"contamination_audit_hash":contamination_audit['audit_hash'],"membership_audit_hash":membership_audit['audit_hash'],"control_comparison_hash":control_comparison['comparison_hash']}
    payload={"phase":"SAED_V4_11","entries":[entry],"entry_count":1,"immutable":True,"admitted_count":int(status.startswith('admitted')),"rejected_count":int(status=='rejected'),"baseline_preserved":True}
    payload['registry_id']=stable_id('checkpointregistry',payload);payload['registry_hash']=content_hash(payload);return payload

def admitted_checkpoint_hash(registry:dict)->str:
    admitted=[x for x in registry['entries'] if x['status']=='admitted_reference_synthetic']
    if len(admitted)!=1: raise RegistryError('exactly one admitted reference checkpoint required')
    return admitted[0]['checkpoint_hash']

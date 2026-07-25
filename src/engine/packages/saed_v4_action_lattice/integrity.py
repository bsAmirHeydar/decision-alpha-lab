from __future__ import annotations
from typing import Any
from .canonical import content_hash,stable_id,merkle_root

def build_integrity_receipt(*,package:dict[str,Any],handoff:dict[str,Any],policy:dict[str,Any],registry:dict[str,Any],request:dict[str,Any],result:dict[str,Any],lattice:dict[str,Any])->dict[str,Any]:
    hashes={'source_package_hash':package['package_hash'],'source_handoff_hash':handoff['handoff_hash'],'policy_hash':policy['policy_hash'],'domain_registry_hash':registry['registry_hash'],'request_hash':request['request_hash'],'solver_result_hash':result['solver_result_hash'],'lattice_hash':lattice['lattice_hash']}
    root=merkle_root(hashes.values());seed={**hashes,'lineage_root':root}
    return {'receipt_id':stable_id('latticeintegrity',seed),'receipt_hash':content_hash(seed),**seed,'verification_status':'verified_reference','external_reproduction':False,'metaeditor_compile':False,'production_authorization':False}

def verify_integrity_receipt(receipt:dict[str,Any])->bool:
    keys=('source_package_hash','source_handoff_hash','policy_hash','domain_registry_hash','request_hash','solver_result_hash','lattice_hash')
    root=merkle_root(receipt[k] for k in keys)
    seed={k:receipt[k] for k in keys};seed['lineage_root']=root
    return root==receipt['lineage_root'] and content_hash(seed)==receipt['receipt_hash']

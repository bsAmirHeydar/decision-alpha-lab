from __future__ import annotations
from .canonical import content_hash,merkle_root,stable_id

def build_receipt(cube)->dict:
    payload={'cube_id':cube.cube_id,'cube_hash':cube.cube_hash,'row_count':cube.row_count,'row_merkle_root':merkle_root(r.row_hash for r in cube.rows),'source_lattice_hash':cube.source_lattice_hash,'context_snapshot_hash':cube.context_snapshot_hash,'policy_hash':cube.policy_hash,'cost_registry_hash':cube.cost_registry_hash,'complete_exposure':cube.complete_exposure,'selection_authority':False,'execution_authority':False}
    payload['receipt_id']=stable_id('cubeintegrity',payload);payload['receipt_hash']=content_hash(payload);return payload

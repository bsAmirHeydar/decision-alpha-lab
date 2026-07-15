from __future__ import annotations
from .canonical import content_hash
from .errors import IntegrityError

def validate_cube(cube)->None:
    payload=cube.semantic_payload();observed=content_hash(payload)
    if observed!=cube.cube_hash:raise IntegrityError('cube hash mismatch')
    if cube.row_count!=len(cube.rows):raise IntegrityError('row count mismatch')
    if len({r.node_id for r in cube.rows})!=len(cube.rows):raise IntegrityError('duplicate node rows')
    if cube.selection_authority or cube.execution_authority or cube.ranking_semantics!='none':raise IntegrityError('authority violation')
    if not cube.complete_exposure:raise IntegrityError('incomplete exposure')

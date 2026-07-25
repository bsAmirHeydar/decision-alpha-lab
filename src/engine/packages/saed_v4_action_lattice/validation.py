from __future__ import annotations
from typing import Any
from .authority import assert_safe_authority
from .canonical import content_hash
from .errors import ContractError, IntegrityError
from .graph import validate_atomic_edges,validate_dag

def validate_upstream(package:dict[str,Any],handoff:dict[str,Any])->None:
    if handoff.get('next_phase')!='SAED_V4_07': raise ContractError('wrong upstream handoff target')
    if package.get('package_hash')!=handoff.get('package_hash'): raise IntegrityError('package/handoff hash mismatch')
    if package.get('package_id')!=handoff.get('package_id'): raise IntegrityError('package/handoff id mismatch')
    auth=handoff.get('authority',{})
    if not auth.get('solve_bounded_action_lattice') or auth.get('select_treatment') or auth.get('send_order'): raise ContractError('invalid inherited authority')

def validate_solver_result(result:dict[str,Any])->None:
    expected=content_hash({k:v for k,v in result.items() if k!='solver_result_hash'})
    if result['solver_result_hash']!=expected: raise IntegrityError('solver result hash mismatch')
    if result['candidate_count']!=result['feasible_count']+result['pruned_count']: raise ContractError('candidate accounting mismatch')
    if result['selection_authority'] or result['execution_authority']: raise ContractError('authority leak')

def validate_lattice(lattice:dict[str,Any])->None:
    expected=content_hash({k:v for k,v in lattice.items() if k!='lattice_hash'})
    if lattice['lattice_hash']!=expected: raise IntegrityError('lattice hash mismatch')
    if lattice['node_count']!=len(lattice['nodes']) or lattice['edge_count']!=len(lattice['edges']): raise ContractError('lattice count mismatch')
    if not lattice['contains_skip'] or not lattice['contains_abstain']: raise ContractError('mandatory fallback absent')
    validate_atomic_edges(lattice['nodes'],lattice['edges']);validate_dag(lattice['nodes'],lattice['edges'])

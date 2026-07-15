from __future__ import annotations
from typing import Any
from .authority import authority_boundary,assert_safe_authority
from .budget import BudgetMeter
from .canonical import content_hash,stable_id,merkle_root
from .domains import load_domains
from .errors import ContractError,IntegrityError
from .graph import validate_dag
from .lattice import build_lattice,lattice_payload
from .models import LatticePolicy
from .solver import enumerate_candidates
from .validation import validate_lattice,validate_solver_result,validate_upstream

class ActionLatticeService:
    """Deterministic bounded SAED V4-07 solver. It never scores, selects, sizes or executes an action."""
    def solve(self,*,package:dict[str,Any],handoff:dict[str,Any],policy_document:dict[str,Any],domain_registry:dict[str,Any],request:dict[str,Any])->dict[str,Any]:
        validate_upstream(package,handoff);policy=LatticePolicy.from_mapping(policy_document);assert_safe_authority(policy_document['authority'])
        if package['evidence_role'] not in policy.allowed_evidence_roles: raise ContractError('Evidence Role not allowed')
        if request['source_package_hash']!=package['package_hash'] or request['source_handoff_hash']!=handoff['handoff_hash']: raise IntegrityError('request lineage mismatch')
        if request['policy_hash']!=policy.policy_hash or request['domain_registry_hash']!=domain_registry['registry_hash']: raise IntegrityError('request policy/domain hash mismatch')
        expected_request_hash=content_hash({k:v for k,v in request.items() if k not in ('request_hash','request_id')})
        if request['request_hash']!=expected_request_hash or request['request_id']!=stable_id('solverrequest',{k:v for k,v in request.items() if k not in ('request_hash','request_id')}): raise IntegrityError('request identity mismatch')
        meter=BudgetMeter(policy.budget);feasible,pruned,domains=enumerate_candidates(package,domain_registry,policy,meter)
        pruning_records=[]
        for c in pruned:
            seed={'candidate_id':c['candidate_id'],'candidate_hash':c['candidate_hash'],'failed_constraints':c['failed_constraints']}
            pruning_records.append({'record_id':stable_id('prune',seed),'record_hash':content_hash(seed),**seed,'reason_code':'STRUCTURAL_CONSTRAINT_VIOLATION'})
        pruning_records=sorted(pruning_records,key=lambda r:r['record_id'])
        pruning_seed={'record_hashes':[r['record_hash'] for r in pruning_records],'record_count':len(pruning_records)}
        pruning={'ledger_id':stable_id('pruningledger',pruning_seed),'ledger_hash':content_hash(pruning_seed),**pruning_seed,'records':pruning_records}
        seed={'source_package_hash':package['package_hash'],'source_handoff_hash':handoff['handoff_hash'],'policy_hash':policy.policy_hash,'domain_registry_hash':domain_registry['registry_hash'],'request_hash':request['request_hash'],'candidate_hashes':sorted(c['candidate_hash'] for c in feasible+pruned),'pruning_ledger_hash':pruning['ledger_hash']}
        result={'solver_result_id':stable_id('solverresult',seed),'solver_result_hash':'','source_package_id':package['package_id'],'source_package_hash':package['package_hash'],'source_handoff_id':handoff['handoff_id'],'source_handoff_hash':handoff['handoff_hash'],'policy_id':policy.policy_id,'policy_hash':policy.policy_hash,'domain_registry_id':domain_registry['registry_id'],'domain_registry_hash':domain_registry['registry_hash'],'request_id':request['request_id'],'request_hash':request['request_hash'],'evidence_role':package['evidence_role'],'known_as_of':package['known_as_of'],'candidate_count':len(feasible)+len(pruned),'feasible_count':len(feasible),'pruned_count':len(pruned),'feasible_candidates':feasible,'pruning_ledger':pruning,'domain_ids':[d.domain_id for d in domains],'domain_hashes':[d.domain_hash for d in domains],'budget_ledger':{},'authority':authority_boundary(),'selection_authority':False,'execution_authority':False,'limitations':['Reference deterministic bounded solver only.','No outcome, preference, ranking, model, capital, runtime or execution authority.','Deferred feature predicates remain unresolved until V4-08 path evaluation.']}
        nodes,edges=build_lattice(feasible);meter.set_nodes(len(nodes));meter.set_edges(len(edges));result['budget_ledger']=meter.to_dict();result['solver_result_hash']=content_hash({k:v for k,v in result.items() if k!='solver_result_hash'});validate_solver_result(result)
        lattice=lattice_payload(nodes,edges,result);order=validate_dag(nodes,edges);lattice['topological_order']=order;lattice['lattice_hash']=content_hash({k:v for k,v in lattice.items() if k!='lattice_hash'});validate_lattice(lattice)
        return {'solver_result':result,'action_lattice':lattice}

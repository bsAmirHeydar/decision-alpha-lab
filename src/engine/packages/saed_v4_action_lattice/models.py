from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .canonical import content_hash, stable_id
from .errors import ContractError, DomainError

@dataclass(frozen=True)
class ParameterDomain:
    domain_name: str
    exact_version: str
    program_id: str
    parameter_ref: str
    value_type: str
    ordered_values: tuple[Any,...]
    include_source_value: bool
    monotonic_semantics: str
    description: str
    @classmethod
    def from_mapping(cls, x: Mapping[str,Any]) -> 'ParameterDomain':
        required=('domain_name','exact_version','program_id','parameter_ref','value_type','ordered_values','include_source_value','monotonic_semantics','description')
        missing=[k for k in required if k not in x]
        if missing: raise DomainError(f'domain missing fields: {missing}')
        values=tuple(x['ordered_values'])
        if not values or len(values)!=len({str(v) for v in values}): raise DomainError('domain values must be finite, non-empty and unique')
        if len(values)>64: raise DomainError('domain cardinality exceeds hard safety bound')
        if x['monotonic_semantics']!='structural_only': raise DomainError('only structural_only monotonic semantics are permitted')
        return cls(*(x[k] if k!='ordered_values' else values for k in required))
    def semantic_payload(self) -> dict[str,Any]:
        return {'domain_name':self.domain_name,'exact_version':self.exact_version,'program_id':self.program_id,'parameter_ref':self.parameter_ref,'value_type':self.value_type,'ordered_values':list(self.ordered_values),'include_source_value':self.include_source_value,'monotonic_semantics':self.monotonic_semantics,'description':self.description}
    @property
    def domain_id(self)->str: return stable_id('domain',self.semantic_payload())
    @property
    def domain_hash(self)->str: return content_hash(self.semantic_payload())

@dataclass(frozen=True)
class SolverBudget:
    maximum_candidates:int
    maximum_feasible_nodes:int
    maximum_edges:int
    maximum_constraint_evaluations:int
    maximum_domains_per_program:int
    maximum_values_per_domain:int
    deterministic_partition_count:int
    operation_budget:int
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'SolverBudget':
        keys=('maximum_candidates','maximum_feasible_nodes','maximum_edges','maximum_constraint_evaluations','maximum_domains_per_program','maximum_values_per_domain','deterministic_partition_count','operation_budget')
        try: obj=cls(*(int(x[k]) for k in keys))
        except KeyError as e: raise ContractError(f'budget missing field {e.args[0]}') from e
        if min(obj.__dict__.values())<=0: raise ContractError('all budget values must be positive')
        return obj

@dataclass(frozen=True)
class LatticePolicy:
    policy_name:str
    exact_version:str
    require_skip:bool
    require_abstain:bool
    require_source_value_in_domain:bool
    require_adjacent_atomic_edges:bool
    permit_deferred_feature_constraints:bool
    allowed_evidence_roles:tuple[str,...]
    prohibited_identifier_tokens:tuple[str,...]
    budget:SolverBudget
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'LatticePolicy':
        return cls(str(x['policy_name']),str(x['exact_version']),bool(x['require_skip']),bool(x['require_abstain']),bool(x['require_source_value_in_domain']),bool(x['require_adjacent_atomic_edges']),bool(x['permit_deferred_feature_constraints']),tuple(sorted(x['allowed_evidence_roles'])),tuple(sorted(x['prohibited_identifier_tokens'])),SolverBudget.from_mapping(x['budget']))
    def semantic_payload(self)->dict[str,Any]:
        return {'policy_name':self.policy_name,'exact_version':self.exact_version,'require_skip':self.require_skip,'require_abstain':self.require_abstain,'require_source_value_in_domain':self.require_source_value_in_domain,'require_adjacent_atomic_edges':self.require_adjacent_atomic_edges,'permit_deferred_feature_constraints':self.permit_deferred_feature_constraints,'allowed_evidence_roles':list(self.allowed_evidence_roles),'prohibited_identifier_tokens':list(self.prohibited_identifier_tokens),'budget':self.budget.__dict__}
    @property
    def policy_id(self)->str:return stable_id('latticepolicy',self.semantic_payload())
    @property
    def policy_hash(self)->str:return content_hash(self.semantic_payload())

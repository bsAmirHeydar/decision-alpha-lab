from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping
from .errors import ContractError

@dataclass(frozen=True)
class Predicate:
    feature_ref: str
    operator: str
    expected: Any
    missing_policy: str = "fail_rule"
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"Predicate":
        obj=cls(str(x['feature_ref']),str(x['operator']),x.get('expected'),str(x.get('missing_policy','fail_rule')))
        if obj.missing_policy not in {'fail_rule','match_only_missing','fail_program'}: raise ContractError('invalid missing_policy')
        return obj

@dataclass(frozen=True)
class Rule:
    rule_id: str
    priority: int
    predicates: tuple[Predicate,...]
    action_node_id: str
    reason_code: str
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"Rule":
        obj=cls(str(x['rule_id']),int(x['priority']),tuple(Predicate.from_mapping(p) for p in x['predicates']),str(x['action_node_id']),str(x['reason_code']))
        if not obj.rule_id or not obj.action_node_id or not obj.reason_code: raise ContractError('rule identity/action/reason required')
        return obj

@dataclass(frozen=True)
class ManualProgram:
    program_name: str
    exact_version: str
    evidence_role: str
    rules: tuple[Rule,...]
    fallback_node_id: str
    authoring_basis: str
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->"ManualProgram":
        obj=cls(str(x['program_name']),str(x['exact_version']),str(x['evidence_role']),tuple(Rule.from_mapping(r) for r in x['rules']),str(x['fallback_node_id']),str(x['authoring_basis']))
        if obj.evidence_role not in {'development','training','validation'}: raise ContractError('manual program evidence role forbidden')
        priorities=[r.priority for r in obj.rules]
        if len(priorities)!=len(set(priorities)): raise ContractError('duplicate rule priority')
        return obj

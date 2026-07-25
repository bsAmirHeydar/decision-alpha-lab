from __future__ import annotations
from typing import Any
from .models import ParameterDomain, LatticePolicy
from .references import component_value
from .errors import DomainError

def load_domains(registry: dict[str,Any]) -> tuple[ParameterDomain,...]:
    allowed={'registry_name','exact_version','source_package_id','source_package_hash','domains','limitations','registry_id','registry_hash'}
    unknown=set(registry)-allowed
    if unknown: raise DomainError(f'unknown domain registry fields: {sorted(unknown)}')
    domains=tuple(ParameterDomain.from_mapping(x) for x in registry['domains'])
    refs=[(d.program_id,d.parameter_ref) for d in domains]
    if len(refs)!=len(set(refs)): raise DomainError('duplicate program/parameter domain')
    return tuple(sorted(domains,key=lambda d:(d.program_id,d.parameter_ref)))

def validate_domains(package:dict[str,Any], domains:tuple[ParameterDomain,...], policy:LatticePolicy)->None:
    programs={p['program_id']:p for p in package['programs']}
    counts={}
    for d in domains:
        if d.program_id not in programs: raise DomainError(f'unknown program in domain: {d.program_id}')
        program=programs[d.program_id]
        low=(d.domain_name+' '+d.parameter_ref).lower()
        if any(t in low for t in policy.prohibited_identifier_tokens): raise DomainError(f'prohibited domain token: {d.parameter_ref}')
        try:
            source=component_value(program['components'],d.parameter_ref)
        except Exception as exc:
            raise DomainError(f'invalid governed parameter reference: {d.parameter_ref}') from exc
        if len(d.ordered_values)>policy.budget.maximum_values_per_domain: raise DomainError('domain value budget exceeded')
        if policy.require_source_value_in_domain and str(source) not in {str(v) for v in d.ordered_values}: raise DomainError(f'source value absent from domain: {d.parameter_ref}')
        counts[d.program_id]=counts.get(d.program_id,0)+1
        if counts[d.program_id]>policy.budget.maximum_domains_per_program: raise DomainError('domain count budget exceeded')

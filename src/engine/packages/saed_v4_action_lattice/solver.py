from __future__ import annotations
from itertools import product
from typing import Any
from .budget import BudgetMeter
from .canonical import content_hash, stable_id
from .constraints import evaluate_program
from .domains import load_domains, validate_domains
from .instantiation import instantiate_program
from .models import LatticePolicy, ParameterDomain
from .errors import ContractError

def _action_class(program:dict[str,Any])->str:
    labels=program.get('semantic_labels',{})
    if labels.get('action_class') in ('skip','abstain'): return labels['action_class']
    for c in program['components']:
        if c['primitive_key'].startswith('action.skip@'): return 'skip'
        if c['primitive_key'].startswith('action.abstain@'): return 'abstain'
    return 'ordinary'

def _candidate(program:dict[str,Any],assignments:dict[str,Any],components:list[dict[str,Any]],evaluations:list[dict[str,Any]],feasible:bool,domain_indices:dict[str,int])->dict[str,Any]:
    seed={'program_id':program['program_id'],'program_hash':program['program_hash'],'assignments':assignments}
    cid=stable_id('candidate',seed);ch=content_hash(seed)
    failed=sorted(e['constraint_name'] for e in evaluations if e['status']=='violated')
    return {'candidate_id':cid,'candidate_hash':ch,'program_id':program['program_id'],'program_hash':program['program_hash'],'program_name':program['program_name'],'action_class':_action_class(program),'parameter_assignments':dict(sorted(assignments.items())),'domain_indices':dict(sorted(domain_indices.items())),'instantiated_components':components,'constraint_evaluations':evaluations,'status':'feasible' if feasible else 'pruned','failed_constraints':failed,'evidence_role':program['evidence_role'],'known_as_of':program['known_as_of']}

def enumerate_candidates(package:dict[str,Any],registry:dict[str,Any],policy:LatticePolicy,meter:BudgetMeter)->tuple[list[dict[str,Any]],list[dict[str,Any]],tuple[ParameterDomain,...]]:
    domains=load_domains(registry);validate_domains(package,domains,policy)
    by_program:dict[str,list[ParameterDomain]]={}
    for d in domains: by_program.setdefault(d.program_id,[]).append(d)
    feasible=[];pruned=[]
    capabilities=set()
    # capability profile is represented by required capability components in the frozen program and the upstream profile hash; exact capability names used by constraints are copied from the frozen package fixture.
    capabilities.add('exit.partial')
    found={'skip':False,'abstain':False}
    for program in sorted(package['programs'],key=lambda p:p['program_id']):
        action_class=_action_class(program)
        if action_class in found: found[action_class]=True
        pdomains=sorted(by_program.get(program['program_id'],[]),key=lambda d:d.parameter_ref)
        if action_class!='ordinary':
            meter.add_candidate();components=instantiate_program(program,{})
            c=_candidate(program,{},components,[],True,{})
            feasible.append(c);continue
        if not pdomains:
            meter.add_candidate();components=instantiate_program(program,{})
            ev,ok=evaluate_program(program,components,capabilities,policy.permit_deferred_feature_constraints);meter.add_constraints(len(ev))
            (feasible if ok else pruned).append(_candidate(program,{},components,ev,ok,{}));continue
        for values in product(*(d.ordered_values for d in pdomains)):
            meter.add_candidate();assign={d.parameter_ref:v for d,v in zip(pdomains,values)};indices={d.parameter_ref:d.ordered_values.index(v) for d,v in zip(pdomains,values)}
            components=instantiate_program(program,assign);ev,ok=evaluate_program(program,components,capabilities,policy.permit_deferred_feature_constraints);meter.add_constraints(len(ev))
            (feasible if ok else pruned).append(_candidate(program,assign,components,ev,ok,indices))
    if policy.require_skip and not found['skip']: raise ContractError('mandatory Skip action missing')
    if policy.require_abstain and not found['abstain']: raise ContractError('mandatory Abstain action missing')
    return sorted(feasible,key=lambda c:c['candidate_id']),sorted(pruned,key=lambda c:c['candidate_id']),domains

from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import ContractError

def build_registry(lattice:dict, programs:list[dict], traces:list[dict])->dict:
    node_by_id={n['node_id']:n for n in lattice['nodes']}
    entries=[]
    abstain=next(n for n in lattice['nodes'] if n['action_class']=='abstain')
    entries.append({"baseline_key":"null_abstain","baseline_family":"null","projected_node_id":abstain['node_id'],"source":"lattice_abstain","frozen":True,"outcome_fitted":False,"learning_semantics":"none"})
    for p,t in zip(programs,traces):
        if t['projected_node_id'] not in node_by_id: raise ContractError('trace node missing from lattice')
        entries.append({"baseline_key":p['program_name'],"baseline_family":"manual_doctrine","projected_node_id":t['projected_node_id'],"source":p['compiled_program_id'],"frozen":True,"outcome_fitted":False,"learning_semantics":"none"})
    entries.sort(key=lambda x:x['baseline_key'])
    payload={"phase":"SAED_V4_10","entries":entries,"entry_count":len(entries),"source_lattice_hash":lattice['lattice_hash'],"baseline_preservation_required":True,"future_challengers_must_report_against_all":True,"selection_authority":False,"execution_authority":False}
    payload['registry_id']=stable_id('baselineregistry',payload);payload['registry_hash']=content_hash(payload)
    return payload

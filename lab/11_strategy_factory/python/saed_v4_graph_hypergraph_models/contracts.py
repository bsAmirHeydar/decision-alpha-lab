from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
from .errors import ContractError

ARCHITECTURES={'relation_mean_baseline','relational_gcn','graph_attention','hypergraph_diffusion','temporal_graph_memory','heterogeneous_graph_fusion'}
OBJECTIVES={'masked_node_reconstruction','relation_type_prediction','hyperedge_membership','temporal_consistency','sequence_state_alignment'}

@dataclass(frozen=True)
class GraphSpec:
    exact_version:str; input_dim:int; hidden_dim:int; output_dim:int; layers:int; max_nodes:int; max_hyperedges:int; max_clique_degree:int; known_time_only:bool; frozen_upstream:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'GraphSpec':
        required={'exact_version','input_dim','hidden_dim','output_dim','layers','max_nodes','max_hyperedges','max_clique_degree','known_time_only','frozen_upstream'}
        if set(x)!=required: raise ContractError(f'graph spec fields mismatch: {sorted(set(x)^required)}')
        o=cls(str(x['exact_version']),int(x['input_dim']),int(x['hidden_dim']),int(x['output_dim']),int(x['layers']),int(x['max_nodes']),int(x['max_hyperedges']),int(x['max_clique_degree']),bool(x['known_time_only']),bool(x['frozen_upstream']))
        if min(o.input_dim,o.hidden_dim,o.output_dim,o.layers,o.max_nodes,o.max_hyperedges,o.max_clique_degree)<1: raise ContractError('invalid graph dimensions or budgets')
        if not o.known_time_only or not o.frozen_upstream: raise ContractError('known_time_only and frozen_upstream must be true')
        return o

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; architecture:str; seed:int; hidden_dim:int; output_dim:int; layers:int; dropout:float; enabled:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'CandidateSpec':
        required={'candidate_id','architecture','seed','hidden_dim','output_dim','layers','dropout','enabled'}
        if set(x)!=required: raise ContractError(f'candidate fields mismatch: {sorted(set(x)^required)}')
        o=cls(str(x['candidate_id']),str(x['architecture']),int(x['seed']),int(x['hidden_dim']),int(x['output_dim']),int(x['layers']),float(x['dropout']),bool(x['enabled']))
        if o.architecture not in ARCHITECTURES: raise ContractError(f'unknown architecture {o.architecture}')
        if min(o.hidden_dim,o.output_dim,o.layers)<1 or not 0.0<=o.dropout<1.0: raise ContractError('invalid candidate parameters')
        return o

@dataclass(frozen=True)
class ObjectiveSpec:
    name:str; weight:float; train_only:bool; outcome_free:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'ObjectiveSpec':
        required={'name','weight','train_only','outcome_free'}
        if set(x)!=required: raise ContractError(f'objective fields mismatch: {sorted(set(x)^required)}')
        o=cls(str(x['name']),float(x['weight']),bool(x['train_only']),bool(x['outcome_free']))
        if o.name not in OBJECTIVES or o.weight<=0 or not o.outcome_free: raise ContractError('invalid or unsafe objective')
        return o

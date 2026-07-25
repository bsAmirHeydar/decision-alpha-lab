from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping,Sequence
from .errors import ContractError

ARCHITECTURES={'ema_recurrent','causal_convolution','diagonal_ssm','selective_ssm','local_causal_attention','hybrid_ssm_attention'}
RESET_REASONS={'context_boundary','root_context_change','domain_change','session_boundary','gap_threshold','explicit_restart','corrupt_state'}

@dataclass(frozen=True)
class SequenceSpec:
    exact_version:str; input_dim:int; state_dim:int; max_context_steps:int; local_attention_window:int; chunk_size:int; gap_reset_seconds:int; causal:bool; frozen_encoder:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'SequenceSpec':
        required={'exact_version','input_dim','state_dim','max_context_steps','local_attention_window','chunk_size','gap_reset_seconds','causal','frozen_encoder'}
        if set(x)!=required: raise ContractError(f'sequence spec fields mismatch: {sorted(set(x)^required)}')
        obj=cls(str(x['exact_version']),int(x['input_dim']),int(x['state_dim']),int(x['max_context_steps']),int(x['local_attention_window']),int(x['chunk_size']),int(x['gap_reset_seconds']),bool(x['causal']),bool(x['frozen_encoder']))
        if obj.input_dim<1 or obj.state_dim<2 or obj.max_context_steps<2 or obj.local_attention_window<1 or obj.chunk_size<1 or obj.gap_reset_seconds<1: raise ContractError('invalid sequence dimensions or limits')
        if not obj.causal or not obj.frozen_encoder: raise ContractError('causal and frozen_encoder must be true')
        return obj

@dataclass(frozen=True)
class CandidateSpec:
    candidate_id:str; architecture:str; seed:int; state_dim:int; context_steps:int; enabled:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'CandidateSpec':
        required={'candidate_id','architecture','seed','state_dim','context_steps','enabled'}
        if set(x)!=required: raise ContractError(f'candidate fields mismatch: {sorted(set(x)^required)}')
        obj=cls(str(x['candidate_id']),str(x['architecture']),int(x['seed']),int(x['state_dim']),int(x['context_steps']),bool(x['enabled']))
        if obj.architecture not in ARCHITECTURES: raise ContractError(f'unknown architecture {obj.architecture}')
        if obj.state_dim<2 or obj.context_steps<2: raise ContractError('invalid candidate dimensions')
        return obj

@dataclass(frozen=True)
class SequencePoint:
    record_id:str; context_id:str; root_context_id:str; domain_id:str; event_time:str; known_time:str; split:str; vector:tuple[float,...]; token_hash:str

@dataclass(frozen=True)
class SequenceExample:
    sequence_id:str; root_context_id:str; domain_id:str; split:str; points:tuple[SequencePoint,...]; source_hash:str

@dataclass(frozen=True)
class ResetPolicy:
    reset_on_context_boundary:bool; reset_on_root_change:bool; reset_on_domain_change:bool; reset_on_session_boundary:bool; gap_reset_seconds:int; restart_requires_snapshot_hash:bool; fail_closed_on_corruption:bool
    @classmethod
    def from_mapping(cls,x:Mapping[str,Any])->'ResetPolicy':
        required={'reset_on_context_boundary','reset_on_root_change','reset_on_domain_change','reset_on_session_boundary','gap_reset_seconds','restart_requires_snapshot_hash','fail_closed_on_corruption'}
        if set(x)!=required: raise ContractError(f'reset policy fields mismatch: {sorted(set(x)^required)}')
        obj=cls(bool(x['reset_on_context_boundary']),bool(x['reset_on_root_change']),bool(x['reset_on_domain_change']),bool(x['reset_on_session_boundary']),int(x['gap_reset_seconds']),bool(x['restart_requires_snapshot_hash']),bool(x['fail_closed_on_corruption']))
        if obj.gap_reset_seconds<1 or not obj.restart_requires_snapshot_hash or not obj.fail_closed_on_corruption: raise ContractError('unsafe reset policy')
        return obj

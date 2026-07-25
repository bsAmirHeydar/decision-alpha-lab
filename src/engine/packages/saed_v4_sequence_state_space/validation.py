from __future__ import annotations
from .contracts import SequenceSpec,CandidateSpec,ResetPolicy
from .errors import ContractError,IntegrityError

def validate_sequence_spec(x): return SequenceSpec.from_mapping(x)
def validate_candidates(xs):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs)
    ids=[x.candidate_id for x in out]
    if len(ids)!=len(set(ids)): raise ContractError('duplicate candidate id')
    if not any(x.enabled for x in out): raise ContractError('no enabled candidates')
    return out

def validate_reset_policy(x): return ResetPolicy.from_mapping(x)

def validate_upstream(handoff,tokenizer,checkpoint,registry):
    expected={
      'tokenizer_hash':tokenizer.get('tokenizer_hash'),'encoder_checkpoint_hash':checkpoint.get('checkpoint_hash'),
      'checkpoint_registry_hash':registry.get('registry_hash')}
    for key,value in expected.items():
        if handoff.get(key)!=value: raise IntegrityError(f'upstream {key} mismatch')
    gates=handoff.get('entry_gates',{})
    required={'baseline_registry_preserved','contamination_audit_passed','deterministic_replay_passed','future_suffix_forbidden','membership_audit_passed','outcome_supervision_absent','reference_checkpoint_admitted'}
    if not required.issubset(gates) or not all(gates[k] is True for k in required): raise IntegrityError('upstream entry gate not closed')
    auth=handoff.get('authority',{})
    if auth.get('read_frozen_encoder') is not True or auth.get('build_reference_sequence_state_space_challengers') is not True: raise IntegrityError('handoff does not grant V4-12 research authority')
    return {'passed':True,'verified_hashes':expected,'gate_count':len(required),'frozen':True}

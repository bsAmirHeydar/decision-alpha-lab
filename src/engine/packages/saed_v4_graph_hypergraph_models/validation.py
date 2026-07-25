from __future__ import annotations
from .contracts import GraphSpec,CandidateSpec,ObjectiveSpec
from .errors import ContractError,IntegrityError

def validate_graph_spec(x): return GraphSpec.from_mapping(x)
def validate_candidates(xs):
    out=tuple(CandidateSpec.from_mapping(x) for x in xs);ids=[x.candidate_id for x in out]
    if len(ids)!=len(set(ids)): raise ContractError('duplicate candidate id')
    if not any(x.enabled for x in out): raise ContractError('no enabled candidate')
    return out

def validate_objectives(xs):
    out=tuple(ObjectiveSpec.from_mapping(x) for x in xs);names=[x.name for x in out]
    if len(names)!=len(set(names)): raise ContractError('duplicate objective')
    return out

def validate_upstream(v405_graph,v405_receipt,v412_handoff,v412_registry,v412_distillation):
    if v405_receipt.get('graph_hash')!=v405_graph.get('graph_hash'): raise IntegrityError('V4-05 graph receipt mismatch')
    if v412_handoff.get('sequence_checkpoint_registry_hash')!=v412_registry.get('registry_hash'): raise IntegrityError('V4-12 registry mismatch')
    if v412_handoff.get('distillation_hash')!=v412_distillation.get('distillation_hash'): raise IntegrityError('V4-12 distillation mismatch')
    gates=v412_handoff.get('entry_gates',{})
    required={'baseline_preserved','causal_sequence_compilation_passed','frozen_v4_11_binding_verified','future_suffix_forbidden','outcome_supervision_absent','restart_snapshot_parity_passed','streaming_batch_parity_passed'}
    if not required.issubset(gates) or not all(gates[k] is True for k in required): raise IntegrityError('V4-12 handoff gates not closed')
    auth=v412_handoff.get('authority',{})
    if auth.get('read_frozen_sequence_states') is not True or auth.get('build_reference_graph_hypergraph_challengers') is not True: raise IntegrityError('V4-12 handoff authority missing')
    return {'passed':True,'v4_05_graph_hash':v405_graph['graph_hash'],'v4_12_registry_hash':v412_registry['registry_hash'],'v4_12_distillation_hash':v412_distillation['distillation_hash'],'gate_count':len(required),'frozen':True}

from __future__ import annotations
import re
from .authority import assert_reference_authority
from .errors import ContractError, LeakageError, IntegrityError
from .models import CorpusRecord, TrainingConfig
from .canonical import content_hash

FORBIDDEN_SUBSTRINGS={
 "outcome_cube","execution_twin","benchmark_result","protected_final","prospective",
 "shadow","live_fill","net_r","gross_r","mfe","mae","exit_price","exit_reason",
 "treatment_rank","policy_value","target_return","realized_pnl"
}
ALLOWED_ARTIFACT_CLASSES={"multimodal_view_package","semantic_temporal_hypergraph","action_lattice_descriptors"}

def scan_forbidden(value, path='$'):
    if isinstance(value,dict):
        for k,v in value.items():
            scan_forbidden(k,path+'.<key>');scan_forbidden(v,path+'.'+str(k))
    elif isinstance(value,(list,tuple)):
        for i,v in enumerate(value): scan_forbidden(v,f'{path}[{i}]')
    elif isinstance(value,str):
        low=value.lower()
        hits=sorted(x for x in FORBIDDEN_SUBSTRINGS if x in low)
        if hits: raise LeakageError(f"forbidden token(s) {hits} at {path}")

def validate_v4_10_handoff(handoff:dict, corpus_manifest:dict)->None:
    if handoff.get('phase')!='SAED_V4_10' or handoff.get('next_phase')!='SAED_V4_11': raise ContractError('wrong handoff phase')
    if handoff.get('pretraining_corpus_manifest_hash')!=corpus_manifest.get('manifest_hash'): raise IntegrityError('corpus manifest hash mismatch')
    gates=handoff.get('entry_gates',{})
    required=['baseline_frozen','manual_program_replayable','self_supervised_corpus_boundary_frozen','outcomes_excluded_from_pretraining_inputs','future_suffix_forbidden']
    if not all(gates.get(x) is True for x in required): raise ContractError('V4-10 entry gates not closed')
    if handoff.get('authority',{}).get('build_self_supervised_pretraining_reference') is not True: raise ContractError('reference pretraining not granted')
    if handoff.get('authority',{}).get('use_outcomes_as_pretraining_inputs') is not False: raise LeakageError('outcome inputs not denied')

def validate_upstream_manifest(manifest:dict)->None:
    if manifest.get('target_phase')!='SAED_V4_11' or manifest.get('self_supervised_only') is not True: raise ContractError('invalid upstream corpus manifest')
    if manifest.get('future_suffix_allowed') is not False: raise LeakageError('future suffix allowed')
    classes={x.get('artifact_class') for x in manifest.get('included_artifacts',[])}
    if not classes or not classes<=ALLOWED_ARTIFACT_CLASSES: raise LeakageError(f'non-allowlisted artifact classes: {sorted(classes-ALLOWED_ARTIFACT_CLASSES)}')
    if any(x in classes for x in manifest.get('prohibited_input_artifact_classes',[])): raise LeakageError('prohibited artifact class included')
    if not set(manifest.get('forbidden_objectives',[])) >= {'outcome_prediction','treatment_ranking','policy_value','live_fill_prediction'}: raise ContractError('forbidden objective denylist incomplete')

def validate_records(records:list[dict])->list[CorpusRecord]:
    objs=[CorpusRecord.from_mapping(x) for x in records]
    ids=[x.record_id for x in objs]
    if len(ids)!=len(set(ids)): raise ContractError('duplicate record_id')
    for raw in records: scan_forbidden(raw)
    return objs

def validate_training_config(config:dict)->TrainingConfig:
    scan_forbidden(config)
    return TrainingConfig.from_mapping(config)

def validate_content_hash(document:dict, hash_field:str)->None:
    actual=document.get(hash_field)
    payload={k:v for k,v in document.items() if k!=hash_field}
    if actual!=content_hash(payload): raise IntegrityError(f'{hash_field} mismatch')

def validate_authority(boundary:dict)->None:
    assert_reference_authority(boundary.get('capabilities',{}))

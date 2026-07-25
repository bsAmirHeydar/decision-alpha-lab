from __future__ import annotations
from .authority import assert_reference_authority
from .errors import ContractError, LeakageError
from .feature_space import validate_feature_ref
from .models import ManualProgram

OUTCOME_FIELDS={'net_r','gross_r','adjusted_net_r','fill_probability','fill_fraction','mfe_r','mae_r','exit_reason','status'}

def validate_upstream(view_package:dict,lattice:dict,twin:dict)->None:
    if view_package.get('evidence_role') not in {'development','training','validation'}: raise ContractError('view role forbidden')
    if lattice.get('selection_authority') or lattice.get('execution_authority'): raise ContractError('lattice authority drift')
    if twin.get('ranking_semantics')!='none': raise ContractError('twin ranking semantics drift')
    if not twin.get('complete_exposure'): raise ContractError('execution twin exposure incomplete')
    assert_reference_authority(twin.get('authority',{}))

def validate_program(program:ManualProgram,registry:dict,lattice:dict)->None:
    node_ids={n['node_id'] for n in lattice['nodes']}
    if program.fallback_node_id not in node_ids: raise ContractError('unknown fallback node')
    action={n['node_id']:n['action_class'] for n in lattice['nodes']}
    if action[program.fallback_node_id] not in {'abstain','skip'}: raise ContractError('fallback must be abstain or skip')
    for rule in program.rules:
        if rule.action_node_id not in node_ids: raise ContractError(f'unknown node: {rule.action_node_id}')
        if action[rule.action_node_id] != 'ordinary': raise ContractError('rule action must be ordinary')
        for p in rule.predicates: validate_feature_ref(p.feature_ref,registry)

def validate_corpus_manifest(manifest:dict)->None:
    prohibited=set(manifest['prohibited_input_artifact_classes'])
    included={x['artifact_class'] for x in manifest['included_artifacts']}
    if included & prohibited: raise LeakageError('prohibited artifact class included in pretraining corpus')
    if not manifest['self_supervised_only'] or manifest['label_semantics']!='none': raise LeakageError('corpus is not self-supervised-only')

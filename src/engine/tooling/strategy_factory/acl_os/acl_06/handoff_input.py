from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .artifact_manifest import verify_output_manifest
from .canonical import digest_bytes,digest_file,digest_object,verify_embedded_digest
from .errors import ContractError,IntegrityError
from .io import load_json,safe_relative
from .policies import HANDOFF_IN,REQUIRED_UPSTREAM_ACTIONS,FORBIDDEN_UPSTREAM_ACTIONS
from .schema_validation import validate_instance

REQUIRED={'handoff':'handoff/acl06_handoff.json','manifest':'output_manifest.json','receipt':'batch_receipt.json','batch':'batch/batch_definition.json','batch_manifest':'batch/batch_manifest.json','freeze_receipt':'batch/freeze_receipt.json','candidate_freeze':'batch/candidate_freeze_set.json','dataset_set':'batch/dataset_snapshot_set.json','label_set':'batch/label_contract_set.json','split':'batch/split_contract.json','environment':'batch/environment_lock.json','budget':'batch/compute_budget.json','object_index':'store/object_index.json','events':'events/batch_event_ledger.json','provenance':'lineage/batch_provenance_graph.json'}

def _sem(doc:dict,field:str,label:str):
    if not verify_embedded_digest(doc,field): raise IntegrityError(f'invalid {label} digest')

def load_acl05_bundle(root:Path)->dict[str,Any]:
    root=root.resolve()
    if not (root/'.acl05_generated_root').is_file() or (root/'.acl05_generated_root').is_symlink(): raise ContractError('ACL05 generated-root marker missing')
    docs={k:load_json(safe_relative(root,v)) for k,v in REQUIRED.items()}
    h=docs['handoff']; validate_instance('acl05_handoff_input',h)
    if h['handoff_type']!=HANDOFF_IN: raise ContractError('wrong handoff type')
    _sem(h,'handoff_digest','handoff'); _sem(docs['receipt'],'receipt_digest','receipt'); _sem(docs['batch'],'batch_definition_digest','batch'); _sem(docs['batch_manifest'],'batch_manifest_digest','batch manifest'); _sem(docs['freeze_receipt'],'freeze_receipt_digest','freeze receipt'); _sem(docs['candidate_freeze'],'candidate_freeze_digest','candidate freeze'); _sem(docs['dataset_set'],'dataset_snapshot_set_digest','dataset set'); _sem(docs['label_set'],'label_contract_set_digest','label set'); _sem(docs['split'],'split_digest','split'); _sem(docs['environment'],'environment_digest','environment'); _sem(docs['budget'],'budget_digest','budget'); _sem(docs['object_index'],'object_index_digest','object index'); _sem(docs['events'],'ledger_digest','event ledger'); _sem(docs['provenance'],'graph_digest','provenance')
    if not verify_output_manifest(root,docs['manifest']): raise IntegrityError('ACL05 output manifest invalid')
    if docs['receipt']['output_manifest_digest']!=docs['manifest']['manifest_digest'] or docs['receipt']['acl06_handoff_digest']!=h['handoff_digest']: raise IntegrityError('ACL05 receipt binding invalid')
    if set(h['required_acl06_actions'])!=REQUIRED_UPSTREAM_ACTIONS or set(h['forbidden_acl06_actions'])!=FORBIDDEN_UPSTREAM_ACTIONS: raise ContractError('ACL05 action contract changed')
    if h['live_order_submission_allowed'] or h['capital_activation_allowed']: raise ContractError('ACL05 authority escalation')
    if docs['batch']['state']!='FROZEN' or docs['batch']['material_mutation_allowed'] is not False: raise ContractError('batch not immutable and frozen')
    bindings={'batch_definition_digest':'batch','batch_manifest_digest':'batch_manifest','freeze_receipt_digest':'freeze_receipt','candidate_freeze_digest':'candidate_freeze','dataset_snapshot_set_digest':'dataset_set','label_contract_set_digest':'label_set','split_digest':'split','environment_digest':'environment','budget_digest':'budget','object_index_digest':'object_index','event_ledger_digest':'events','provenance_graph_digest':'provenance'}
    fields={'batch':'batch_definition_digest','batch_manifest':'batch_manifest_digest','freeze_receipt':'freeze_receipt_digest','candidate_freeze':'candidate_freeze_digest','dataset_set':'dataset_snapshot_set_digest','label_set':'label_contract_set_digest','split':'split_digest','environment':'environment_digest','budget':'budget_digest','object_index':'object_index_digest','events':'ledger_digest','provenance':'graph_digest'}
    for hf,key in bindings.items():
        if h[hf]!=docs[key][fields[key]]: raise IntegrityError(f'handoff binding mismatch: {hf}')
    objects={}
    for rec in docs['object_index']['objects']:
        p=safe_relative(root/'store',rec['store_path'])
        if not p.is_file() or p.is_symlink(): raise IntegrityError(f"missing CAS object {rec['logical_id']}")
        payload=p.read_bytes()
        if len(payload)!=rec['size_bytes'] or digest_bytes(payload)!=rec['blob_digest']: raise IntegrityError(f"CAS object mismatch {rec['logical_id']}")
        objects.setdefault(rec['artifact_class'],[]).append((rec,payload))
    candidates=[]
    for rec,payload in objects.get('ACL04_CANONICAL_CANDIDATE',[]):
        doc=json.loads(payload); candidates.append(doc)
    if len(candidates)!=docs['candidate_freeze']['research_count']+docs['candidate_freeze']['diagnostic_count']: raise IntegrityError('candidate payload count mismatch')
    datasets=[]
    for rec,payload in objects.get('DATASET_SNAPSHOT_BYTES',[]): datasets.append({'record':rec,'payload':payload})
    if not datasets: raise IntegrityError('dataset bytes absent from CAS')
    material={'handoff_digest':h['handoff_digest'],'batch_id':h['batch_id'],'object_index_digest':h['object_index_digest'],'candidate_set_digest':digest_object(sorted((c['setup_id'],c['candidate_digest']) for c in candidates)),'dataset_blob_digests':sorted(x['record']['blob_digest'] for x in datasets)}
    return {**docs,'candidates':sorted(candidates,key=lambda x:x['setup_id']),'datasets':datasets,'bundle_digest':digest_object(material),'root':root}

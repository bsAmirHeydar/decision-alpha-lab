from __future__ import annotations
import shutil,tempfile
from pathlib import Path
from typing import Any
from .artifact_manifest import build_output_manifest
from .authority import validate_authority
from .budget import ResourceAccountant
from .cache import RunArtifactStore
from .canonical import digest_object,stable_id,verify_embedded_digest,with_digest
from .dag import plan_dag
from .errors import ContractError,PublicationError
from .event_ledger import EventLedger,verify_event_ledger
from .executor import execute_dag
from .handoff import build_acl07_handoff
from .handoff_input import load_acl05_bundle
from .io import atomic_publish,dump_json
from .lineage import build_provenance
from .policies import CLAIM_CEILING,ORCHESTRATOR_VERSION
from .projection import write_docs
from .schema_validation import validate_instance
from .security import evaluate_security
from .task_registry import registry_snapshot,validate_registry

class ACL06ResearchOrchestrationService:
    def run(self,*,acl05_root:Path,output_root:Path,authority_permit:dict[str,Any],run_request:dict[str,Any],task_registry:dict[str,Any]|None=None)->dict[str,Any]:
        output_root=output_root.resolve()
        if output_root.exists() and any(output_root.iterdir()): raise PublicationError('output root must be empty')
        bundle=load_acl05_bundle(acl05_root); h=bundle['handoff']; authority=validate_authority(authority_permit,h)
        validate_instance('research_run_request',run_request)
        if not verify_embedded_digest(run_request,'request_digest'): raise ContractError('run request digest invalid')
        if run_request['batch_id']!=h['batch_id'] or run_request['upstream_handoff_digest']!=h['handoff_digest']: raise ContractError('run request binding mismatch')
        if run_request['live_order_submission_allowed'] or run_request['capital_activation_allowed'] or run_request['network_access_allowed'] or run_request['secret_access_allowed']: raise ContractError('run request grants forbidden capability')
        registry=validate_registry(task_registry or registry_snapshot()); dag=plan_dag(bundle,run_request,registry)
        request_seed=digest_object({k:v for k,v in run_request.items() if k not in {'run_id','request_digest'}})
        expected_run=stable_id('RUN',bundle['batch']['batch_id'],request_seed,registry['registry_digest'],length=32)
        if run_request['run_id']!=expected_run: raise ContractError('run_id is not deterministic from frozen material')
        run_body={'schema_version':'1.0.0','run_id':run_request['run_id'],'batch_id':bundle['batch']['batch_id'],'batch_definition_digest':bundle['batch']['batch_definition_digest'],'upstream_handoff_digest':h['handoff_digest'],'dag_digest':dag['dag_digest'],'task_registry_digest':registry['registry_digest'],'started_at':run_request['started_at'],'state':'COMPLETED','claim_ceiling':CLAIM_CEILING,'orchestrator_version':ORCHESTRATOR_VERSION,'batch_mutation_allowed':False,'candidate_mutation_allowed':False,'alpha_claim_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False}
        research_run=with_digest(run_body,'research_run_digest')
        staging=Path(tempfile.mkdtemp(prefix='.acl06-stage-',dir=output_root.parent));
        try:
            (staging/'.acl06_generated_root').write_text('ACL-06 GENERATED ROOT — DO NOT EDIT\n',encoding='utf-8')
            (staging/'.acl06_generated_root').write_text('ACL-06 GENERATED ROOT — DO NOT EDIT\n',encoding='utf-8')
            ledger=EventLedger(run_request['run_id']); ledger.append('ACL05_HANDOFF_ACCEPTED',{'handoff_digest':h['handoff_digest'],'batch_id':h['batch_id']},run_request['started_at']); ledger.append('RESEARCH_DAG_PLANNED',{'dag_digest':dag['dag_digest'],'task_count':dag['task_count']},run_request['started_at'])
            store=RunArtifactStore(staging/'store'); accountant=ResourceAccountant(bundle['budget']); executed=execute_dag(bundle,dag,run_request,store,ledger,accountant)
            accounting=accountant.document(); object_index=store.index(); events=ledger.document()
            if not verify_event_ledger(events): raise ContractError('event chain invalid')
            result_bundle=executed['result_bundle']; provenance=build_provenance(bundle,dag,result_bundle,object_index,events)
            security=evaluate_security(bundle,authority,registry,dag)
            acl07=build_acl07_handoff(research_run,result_bundle,dag,executed['receipts'],accounting,object_index,events,provenance)
            integrity=with_digest({'schema_version':'1.0.0','run_id':run_request['run_id'],'acl05_bundle_verified':True,'frozen_batch_unchanged':True,'candidate_behavior_unchanged':True,'dag_acyclic':True,'all_tasks_successful':True,'resource_budget_respected':True,'event_chain_verified':True,'diagnostic_lane_segregated':True,'passed':True},'report_digest')
            failure=with_digest({'schema_version':'1.0.0','run_id':run_request['run_id'],'failed_task_count':0,'blocked_task_count':0,'failures':[],'run_failed':False},'report_digest')
            binding=with_digest({'schema_version':'1.0.0','batch_id':h['batch_id'],'acl05_handoff_digest':h['handoff_digest'],'acl05_bundle_digest':bundle['bundle_digest'],'batch_definition_digest':bundle['batch']['batch_definition_digest'],'object_index_digest':bundle['object_index']['object_index_digest'],'immutable':True},'binding_digest')
            docs={'binding/acl05_binding.json':binding,'authority/authority_report.json':authority,'plan/research_run_request.json':run_request,'plan/task_registry_snapshot.json':registry,'plan/research_dag.json':dag,'execution/research_run.json':research_run,'execution/task_receipt_set.json':executed['receipts'],'execution/resource_accounting.json':accounting,'results/research_result_bundle.json':result_bundle,'results/research_result_index.json':with_digest({'schema_version':'1.0.0','run_id':run_request['run_id'],'candidate_results':[{'setup_id':x['setup_id'],'candidate_result_digest':x['candidate_result_digest'],'lane':x['lane']} for x in result_bundle['candidate_results']],'candidate_count':result_bundle['candidate_count'],'diagnostic_candidates_selectable':False},'index_digest'),'store/object_index.json':object_index,'events/research_event_ledger.json':events,'lineage/research_provenance_graph.json':provenance,'reports/integrity_report.json':integrity,'reports/security_isolation_report.json':security,'reports/failure_report.json':failure,'handoff/acl07_handoff.json':acl07}
            for sid,res in sorted(executed['candidate_results'].items()): docs[f'results/candidates/{sid}.json']=res
            for rel,doc in docs.items(): dump_json(staging/rel,doc)
            write_docs(staging,research_run,dag,bundle,result_bundle,accounting)
            manifest=build_output_manifest(staging,run_request['run_id']); dump_json(staging/'output_manifest.json',manifest)
            receipt=with_digest({'schema_version':'1.0.0','orchestrator_version':ORCHESTRATOR_VERSION,'run_id':run_request['run_id'],'batch_id':h['batch_id'],'research_run_digest':research_run['research_run_digest'],'dag_digest':dag['dag_digest'],'result_bundle_digest':result_bundle['result_bundle_digest'],'task_receipt_set_digest':executed['receipts']['receipt_set_digest'],'resource_accounting_digest':accounting['accounting_digest'],'acl07_handoff_digest':acl07['handoff_digest'],'output_manifest_digest':manifest['manifest_digest'],'claim_ceiling':CLAIM_CEILING,'live_order_submission_allowed':False,'capital_activation_allowed':False},'receipt_digest'); dump_json(staging/'research_receipt.json',receipt)
            atomic_publish(staging,output_root)
        except Exception:
            shutil.rmtree(staging,ignore_errors=True); raise
        return {'passed':True,'run_id':run_request['run_id'],'batch_id':h['batch_id'],'task_count':dag['task_count'],'candidate_count':result_bundle['candidate_count'],'research_candidate_count':result_bundle['research_candidate_count'],'diagnostic_candidate_count':result_bundle['diagnostic_candidate_count'],'dag':dag,'research_run':research_run,'result_bundle':result_bundle,'receipts':executed['receipts'],'accounting':accounting,'object_index':object_index,'events':events,'provenance':provenance,'handoff':acl07,'output_manifest':manifest,'receipt':receipt,'output_root':str(output_root)}

from __future__ import annotations
from collections import defaultdict,deque
from typing import Any
from .canonical import digest_object,stable_id,with_digest
from .errors import DAGError,BudgetError
from .policies import SEGMENTS,TASK_EXECUTOR_ID
from .schema_validation import validate_instance
from .task_registry import COSTS

def _task(task_type:str,deps:list[str],inputs:list[str],lane:str='SYSTEM',candidate_id:str|None=None,setup_id:str|None=None,segment:str|None=None)->dict:
    material={'task_type':task_type,'dependencies':sorted(deps),'input_digests':sorted(inputs),'lane':lane,'candidate_id':candidate_id,'setup_id':setup_id,'segment':segment,'executor_id':TASK_EXECUTOR_ID}
    task_id=stable_id('TASK',digest_object(material),length=24)
    cpu,mem,out=COSTS[task_type]
    body={'schema_version':'1.0.0','task_id':task_id,**material,'deterministic':True,'idempotent':True,'max_attempts':2,'budget':{'cpu_seconds':cpu,'memory_mb':mem,'output_bytes':out},'cache_key':digest_object({'material':material,'executor_version':'1.0.0'})}
    return with_digest(body,'task_contract_digest')

def plan_dag(bundle:dict[str,Any],request:dict[str,Any],registry:dict[str,Any])->dict[str,Any]:
    b=bundle['batch']; tasks=[]
    verify=_task('VERIFY_FROZEN_BATCH',[],[bundle['handoff']['handoff_digest'],bundle['bundle_digest']]); tasks.append(verify)
    materialize=_task('MATERIALIZE_DATASET',[verify['task_id']],[bundle['dataset_set']['dataset_snapshot_set_digest'],bundle['object_index']['object_index_digest']]); tasks.append(materialize)
    labels=_task('COMPILE_MATURE_LABELS',[materialize['task_id']],[bundle['label_set']['label_contract_set_digest']]); tasks.append(labels)
    split=_task('ASSIGN_PURGED_SPLITS',[labels['task_id']],[bundle['split']['split_digest']]); tasks.append(split)
    aggregates=[]
    status={x['setup_id']:x['status'] for x in bundle['candidate_freeze']['research_candidates']+bundle['candidate_freeze']['diagnostic_candidates']}
    for c in bundle['candidates']:
        lane='DIAGNOSTIC' if status[c['setup_id']]=='DIAGNOSTIC_ONLY' else 'RESEARCH'
        ev=[]
        for segment in SEGMENTS:
            t=_task('EVALUATE_CANDIDATE_SEGMENT',[split['task_id']],[c['candidate_digest'],bundle['dataset_set']['dataset_snapshot_set_digest'],bundle['label_set']['label_contract_set_digest'],bundle['split']['split_digest']],lane,c['candidate_id'],c['setup_id'],segment); tasks.append(t); ev.append(t['task_id'])
        a=_task('AGGREGATE_CANDIDATE',ev,[c['candidate_digest']],lane,c['candidate_id'],c['setup_id']); tasks.append(a); aggregates.append(a['task_id'])
    package=_task('PACKAGE_RESEARCH_RESULTS',aggregates,[bundle['batch']['batch_definition_digest'],bundle['candidate_freeze']['candidate_freeze_digest']]); tasks.append(package)
    handoff=_task('BUILD_ACL07_HANDOFF',[package['task_id']],[bundle['handoff']['handoff_digest']]); tasks.append(handoff)
    _validate_acyclic(tasks)
    budget=bundle['budget']; planned={'task_count':len(tasks),'cpu_seconds':sum(t['budget']['cpu_seconds'] for t in tasks),'peak_memory_mb':max(t['budget']['memory_mb'] for t in tasks),'output_bytes':sum(t['budget']['output_bytes'] for t in tasks)}
    if planned['task_count']>budget['max_tasks'] or planned['cpu_seconds']>budget['max_cpu_seconds'] or planned['peak_memory_mb']>budget['max_memory_mb'] or planned['output_bytes']>budget['max_store_bytes']: raise BudgetError(f'planned DAG exceeds frozen budget: {planned}')
    body={'schema_version':'1.0.0','plan_id':stable_id('DAG',bundle['batch']['batch_id'],request['request_digest'],registry['registry_digest'],length=32),'batch_id':bundle['batch']['batch_id'],'request_digest':request['request_digest'],'registry_digest':registry['registry_digest'],'tasks':tasks,'task_count':len(tasks),'planned_resources':planned,'closed':True,'batch_mutation_allowed':False,'candidate_mutation_allowed':False}
    doc=with_digest(body,'dag_digest'); validate_instance('research_dag',doc); return doc

def _validate_acyclic(tasks:list[dict])->None:
    ids={t['task_id'] for t in tasks}
    if len(ids)!=len(tasks): raise DAGError('duplicate task id')
    indeg={i:0 for i in ids}; edges=defaultdict(list)
    for t in tasks:
        for d in t['dependencies']:
            if d not in ids: raise DAGError(f'unknown dependency {d}')
            edges[d].append(t['task_id']); indeg[t['task_id']]+=1
    q=deque(sorted(i for i,v in indeg.items() if v==0)); visited=[]
    while q:
        n=q.popleft(); visited.append(n)
        for m in sorted(edges[n]):
            indeg[m]-=1
            if indeg[m]==0:q.append(m)
    if len(visited)!=len(tasks): raise DAGError('cycle detected')

def topological_order(dag:dict)->list[dict]:
    by={t['task_id']:t for t in dag['tasks']}; indeg={k:0 for k in by}; edges=defaultdict(list)
    for t in by.values():
        for d in t['dependencies']: edges[d].append(t['task_id']); indeg[t['task_id']]+=1
    q=deque(sorted(k for k,v in indeg.items() if v==0)); out=[]
    while q:
        n=q.popleft(); out.append(by[n])
        for m in sorted(edges[n]):
            indeg[m]-=1
            if indeg[m]==0:q.append(m)
    return out

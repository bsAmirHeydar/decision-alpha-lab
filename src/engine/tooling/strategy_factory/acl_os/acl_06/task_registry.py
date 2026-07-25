from __future__ import annotations
from typing import Any,Callable
from .canonical import digest_object,with_digest
from .errors import ContractError
from .policies import TASK_TYPES,TASK_EXECUTOR_ID
from .schema_validation import validate_instance

COSTS={
 'VERIFY_FROZEN_BATCH':(1,32,2048),'MATERIALIZE_DATASET':(2,64,8192),'COMPILE_MATURE_LABELS':(2,64,8192),'ASSIGN_PURGED_SPLITS':(1,32,4096),
 'EVALUATE_CANDIDATE_SEGMENT':(3,64,8192),'AGGREGATE_CANDIDATE':(1,32,4096),'PACKAGE_RESEARCH_RESULTS':(2,64,16384),'BUILD_ACL07_HANDOFF':(1,32,4096)}

def registry_snapshot()->dict[str,Any]:
    entries=[]
    for t in TASK_TYPES:
        cpu,mem,out=COSTS[t]
        entries.append({'task_type':t,'executor_id':TASK_EXECUTOR_ID,'deterministic':True,'idempotent':True,'max_attempts':2,'cpu_seconds_budget':cpu,'memory_mb_budget':mem,'output_bytes_budget':out,'network_access_allowed':False,'secret_access_allowed':False,'live_order_submission_allowed':False,'capital_activation_allowed':False})
    return with_digest({'schema_version':'1.0.0','registry_id':'ACL06_TASK_REGISTRY_V1','closed_world':True,'entries':entries},'registry_digest')
def validate_registry(doc:dict[str,Any])->dict[str,Any]:
    validate_instance('task_registry',doc)
    expected=registry_snapshot()
    if doc!=expected: raise ContractError('task registry differs from closed-world reference')
    return doc

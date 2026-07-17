from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id

STEP_DEFINITIONS=(
 ("FREEZE_SOURCE",()),
 ("VALIDATE_PREREQUISITES",("FREEZE_SOURCE",)),
 ("COMPILE_DETECTOR_IR",("VALIDATE_PREREQUISITES",)),
 ("COMPILE_OCCURRENCE_IR",("VALIDATE_PREREQUISITES",)),
 ("COMPILE_KNOWN_TIME_IR",("VALIDATE_PREREQUISITES",)),
 ("COMPILE_FEATURE_BINDING_IR",("VALIDATE_PREREQUISITES",)),
 ("EMIT_ADAPTER_CONTRACTS",("COMPILE_KNOWN_TIME_IR","COMPILE_FEATURE_BINDING_IR")),
 ("COMPILE_GOLDEN_REPLAY",("COMPILE_DETECTOR_IR","COMPILE_OCCURRENCE_IR","COMPILE_KNOWN_TIME_IR")),
 ("RUN_GOLDEN_REPLAY",("COMPILE_GOLDEN_REPLAY",)),
 ("EMIT_GENERATED_SCHEMAS",("COMPILE_DETECTOR_IR","COMPILE_OCCURRENCE_IR","COMPILE_KNOWN_TIME_IR","COMPILE_FEATURE_BINDING_IR")),
 ("BUILD_ONBOARDING_REPORT",("RUN_GOLDEN_REPLAY","EMIT_ADAPTER_CONTRACTS","EMIT_GENERATED_SCHEMAS")),
 ("EMIT_ACL04_HANDOFF",("BUILD_ONBOARDING_REPORT",)),
 ("FINALIZE_RECEIPT",("EMIT_ACL04_HANDOFF",)),
)

def build_compiler_plan(context_id:str,context_version:str,source_digest:str,compiler_version:str)->dict[str,Any]:
    steps=[]
    for order,(name,deps) in enumerate(STEP_DEFINITIONS,1):
        steps.append({"step_id":stable_id("CSTEP",context_id,context_version,name),"name":name,"order":order,"depends_on":[stable_id("CSTEP",context_id,context_version,d) for d in deps],"idempotent":True,"side_effect_scope":"DECLARED_OUTPUT_ROOT_ONLY"})
    body={"schema_version":"1.0.0","context_id":context_id,"context_version":context_version,"source_digest":source_digest,"compiler_version":compiler_version,"steps":steps,"claim_ceiling":"CONTEXT_COMPILATION_REFERENCE_ONLY"}
    return {**body,"plan_digest":digest_object(body)}

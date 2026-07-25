from __future__ import annotations
from typing import Any
from .canonical import digest_object

def _closed(required:list[str],properties:dict[str,Any])->dict[str,Any]:
    return {"$schema":"https://json-schema.org/draft/2020-12/schema","type":"object","additionalProperties":False,"required":required,"properties":properties}

def generated_schemas(context_id:str)->dict[str,dict[str,Any]]:
    string={"type":"string","minLength":1}; digest={"type":"string","pattern":"^sha256:[0-9a-f]{64}$"}
    return {
      "detector_event.schema.json":_closed(["event","known_time","decision_time"],{"event":string,"known_time":{"type":"string","format":"date-time"},"decision_time":{"type":"string","format":"date-time"},"guard_result":{"type":["boolean","null"]}}),
      "occurrence_identity.schema.json":_closed(["context_id","context_version","anchor_time","direction","subject_key"],{"context_id":{"const":context_id},"context_version":string,"anchor_time":{"type":"string","format":"date-time"},"direction":{"enum":["LONG","SHORT","NEUTRAL","UNKNOWN"]},"subject_key":string}),
      "feature_record.schema.json":_closed(["context_id","known_time","values","missingness","freshness_ms"],{"context_id":{"const":context_id},"known_time":{"type":"string","format":"date-time"},"values":{"type":"object"},"missingness":{"type":"object"},"freshness_ms":{"type":"object"}}),
      "compiler_receipt.schema.json":_closed(["context_id","source_digest","plan_digest","output_manifest_digest","claim_ceiling"],{"context_id":{"const":context_id},"source_digest":digest,"plan_digest":digest,"output_manifest_digest":digest,"claim_ceiling":{"const":"CONTEXT_COMPILATION_REFERENCE_ONLY"}}),
    }

def build_schema_index(context_id:str)->dict[str,Any]:
    schemas=generated_schemas(context_id)
    entries=[]
    for name,schema in sorted(schemas.items()): entries.append({"name":name,"schema_digest":digest_object(schema)})
    body={"schema_version":"1.0.0","context_id":context_id,"entries":entries,"closed_schema_required":True}
    return {**body,"schema_index_digest":digest_object(body)}

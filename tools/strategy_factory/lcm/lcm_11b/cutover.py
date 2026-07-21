from __future__ import annotations
from .canonical import stable_id,digest_object

def cutover_record(obj,contract,eligibility):
    eligible=eligibility["reference_harness_cutover_allowed"]
    value={"cutover_record_id":stable_id("VISCUT",obj["visual_object_id"]),"visual_object_id":obj["visual_object_id"],"visualizer_id":contract.visualizer_id,"legacy_source_path":obj["source_path"],"legacy_function_name":obj["function_name"],"cutover_state":"REFERENCE_HARNESS_CUTOVER_ACTIVE" if eligible else "BLOCKED_EXPLICIT","consumer_adapter_state":"ENABLED_REFERENCE_ONLY" if eligible else "DISABLED_BLOCKED","production_source_mutation_performed":False,"legacy_source_deleted":False,"rollback_path":"DISABLE_LCM11B_REFERENCE_ADAPTER_AND_RETAIN_LEGACY_SOURCE","reversible":True,"runtime_authority":False,"order_authority":False,"capital_authority":False,"blocking_reasons":eligibility["blocking_reasons"]}
    value["cutover_digest"]=digest_object(value,"cutover_digest");return value

def adapter_record(obj,contract,eligibility):
    value={"adapter_id":stable_id("VISADP",obj["visual_object_id"]),"visual_object_id":obj["visual_object_id"],"visualizer_id":contract.visualizer_id,"adapter_type":"LEGACY_EVENT_TO_CANONICAL_PROJECTION_REFERENCE","enabled":eligibility["reference_harness_cutover_allowed"],"enabled_scope":"LCM11B_REFERENCE_HARNESS_ONLY","source_mutation_allowed":False,"domain_state_mutation_allowed":False,"runtime_authority":False,"order_authority":False,"capital_authority":False,"blocking_reasons":eligibility["blocking_reasons"]};value["adapter_digest"]=digest_object(value,"adapter_digest");return value

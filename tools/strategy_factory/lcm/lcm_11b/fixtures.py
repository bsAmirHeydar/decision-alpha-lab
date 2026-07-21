from __future__ import annotations
from .canonical import stable_id,digest_object

def fixture_record(obj,event,projection,eligibility):
    v={"fixture_id":stable_id("VISFIX",obj["visual_object_id"],event.event_id),"visual_object_id":obj["visual_object_id"],"fixture_kind":"CONTRACT_GOLDEN_VISUAL_FIXTURE","event":event.to_dict(),"expected_projection":projection.to_dict(),"legacy_comparison_status":"ELIGIBLE" if eligibility["reference_harness_cutover_allowed"] else "BLOCKED","blocking_reasons":eligibility["blocking_reasons"],"screenshot_claimed":False,"semantic_fixture":True}
    v["fixture_digest"]=digest_object(v,"fixture_digest");return v

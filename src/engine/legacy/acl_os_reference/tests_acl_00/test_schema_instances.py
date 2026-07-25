from __future__ import annotations
import json
from referencing import Registry,Resource
from jsonschema import Draft202012Validator
from tools.strategy_factory.acl_os.common import REPO_ROOT,load_json
from tools.strategy_factory.acl_os.acl_00.service import ACL00ControlPlane

SCHEMAS=REPO_ROOT/"registry"/"acl_os"/"acl_00"/"schemas"/"v1"
FIX=REPO_ROOT/"lab"/"11_strategy_factory"/"acl_os"/"fixtures"/"acl_00"

def registry():
    out=Registry()
    for path in SCHEMAS.glob("*.schema.json"):
        obj=load_json(path); out=out.with_resource(obj["$id"],Resource.from_contents(obj))
    return out

def validator(name):
    schema=load_json(SCHEMAS/name)
    return Draft202012Validator(schema,registry=registry())

def test_valid_evaluation_bundle_schema():
    obj=load_json(FIX/"valid_semantic_transition.json")
    assert not list(validator("evaluation_bundle.schema.json").iter_errors(obj))

def test_unknown_bundle_field_rejected():
    obj=load_json(FIX/"valid_semantic_transition.json"); obj["bypass"]=True
    assert list(validator("evaluation_bundle.schema.json").iter_errors(obj))

def test_decision_instance_schema(valid_bundle):
    decision=ACL00ControlPlane().evaluate(valid_bundle,valid_bundle.request.requested_at).to_dict()
    errors=list(validator("transition_decision.schema.json").iter_errors(decision)); assert not errors,errors

def test_decision_schema_forbids_live_authority(valid_bundle):
    decision=ACL00ControlPlane().evaluate(valid_bundle,valid_bundle.request.requested_at).to_dict(); decision["live_order_submission_allowed"]=True
    assert list(validator("transition_decision.schema.json").iter_errors(decision))

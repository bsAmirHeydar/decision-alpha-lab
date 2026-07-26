from __future__ import annotations
import json
from pathlib import Path
import pytest,yaml
from jsonschema import Draft202012Validator
from src.engine.tooling.strategy_factory.acl_os.common import REPO_ROOT,load_json
from src.engine.tooling.strategy_factory.acl_os.acl_00.catalogs import PolicyBundle,CATALOG_ROOT
from src.engine.tooling.strategy_factory.acl_os.acl_00.types import Actor,ArtifactRef,TransitionRequest

SCHEMAS=REPO_ROOT/"registry"/"acl_os"/"acl_00"/"schemas"/"v1"

def test_schema_count_and_meta_schema_validity():
    files=list(SCHEMAS.glob("*.schema.json")); assert len(files)>=12
    for p in files: Draft202012Validator.check_schema(load_json(p))

@pytest.mark.parametrize("name",["lifecycle_transitions","authority_roles","separation_of_duties","evidence_requirements","approval_policy","security_hook_policy","waiver_policy","claim_ceiling_bindings","reason_codes","action_catalog"])
def test_required_policy_document(name): assert (CATALOG_ROOT/f"{name}.yaml").is_file()

def test_policy_digest_is_deterministic(): assert PolicyBundle.load().digest==PolicyBundle.load().digest

def test_transition_references_resolve():
    b=PolicyBundle.load()
    for key,spec in b.documents["lifecycle_transitions"]["transitions"].items():
        assert spec["evidence_policy"] in b.documents["evidence_requirements"]["policies"]
        assert spec["approval_policy"] in b.documents["approval_policy"]["policies"]
        assert spec["security_policy"] in b.documents["security_hook_policy"]["policies"]

def test_actor_rejects_unknown_field():
    with pytest.raises(ValueError): Actor.from_dict({"actor_id":"USR_X","roles":["AUDITOR"],"tenant_id":"TEN_X","bad":1})

def test_transition_rejects_unknown_field(valid_bundle):
    obj=valid_bundle.request.to_dict(); obj["surprise"]=True
    with pytest.raises(ValueError): TransitionRequest.from_dict(obj)

def test_artifact_roundtrip():
    x=ArtifactRef("CTX_X","1.0.0","sha256:"+"a"*64,"contexts/x"); assert ArtifactRef.from_dict(x.to_dict())==x

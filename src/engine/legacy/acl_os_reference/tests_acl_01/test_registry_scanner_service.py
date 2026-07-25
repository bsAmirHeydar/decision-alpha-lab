import json
from pathlib import Path
from tools.strategy_factory.acl_os.acl_01.scanner import RepositoryScanner
from tools.strategy_factory.acl_os.acl_01.service import ACL01RepositoryControlPlane

def test_snapshot_deterministic(registry): assert registry.digest==registry.digest

def test_scanner_clean(registry,descriptor,permit_factory,tmp_path):
    assert not registry.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id))
    out=RepositoryScanner(registry,tmp_path).scan(); assert out["passed"]

def test_scanner_detects_drift(registry,descriptor,permit_factory,tmp_path):
    assert not registry.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id)); (tmp_path/descriptor.canonical_path).write_text("drift",encoding="utf-8")
    out=RepositoryScanner(registry,tmp_path).scan(); assert not out["passed"]

def test_service_claim_ceiling(registry,tmp_path):
    out=ACL01RepositoryControlPlane(tmp_path,registry.policies,registry).validate(); assert out["live_order_submission_allowed"] is False and out["capital_activation_allowed"] is False

def test_descriptor_sidecar_divergence(registry,descriptor,permit_factory,tmp_path):
    assert not registry.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id))
    side=tmp_path/"bad.artifact.json"; obj=descriptor.to_dict(); obj["owner_id"]="OWNER_OTHER"; side.write_text(json.dumps(obj),encoding="utf-8")
    out=RepositoryScanner(registry,tmp_path).scan(); assert any(x["code"]=="DESCRIPTOR_REGISTRY_DIVERGENCE" for x in out["findings"])


def test_service_registration_checks_missing_bytes(registry,descriptor,permit_factory,tmp_path):
    (tmp_path/descriptor.canonical_path).unlink()
    cp=ACL01RepositoryControlPlane(tmp_path,registry.policies,registry)
    reasons=cp.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id))
    assert any(x.code=="ARTIFACT_FILE_MISSING" for x in reasons)

def test_bootstrap_registry_is_self_consistent():
    from tools.strategy_factory.acl_os.acl_01.bootstrap_registry import build
    from tools.strategy_factory.acl_os.common import REPO_ROOT
    reg=build(REPO_ROOT)
    assert reg.artifacts and reg.schemas and not reg.validate_graphs()
    assert all(d.identity.namespace=="acl-os" for d in reg.artifacts.values())

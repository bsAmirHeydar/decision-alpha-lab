from dataclasses import replace
from tools.strategy_factory.acl_os.acl_01.locator import ArtifactLocator
from tools.strategy_factory.acl_os.acl_01.types import RegistryStatus

def setup(registry,descriptor,permit_factory):
    assert not registry.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id))

def test_exact_resolution(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); out=ArtifactLocator(registry,tmp_path).resolve(descriptor.identity.artifact_id)
    assert out.status.value=="RESOLVED" and out.verified_digest

def test_base_range_resolution(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); out=ArtifactLocator(registry,tmp_path).resolve(descriptor.identity.base_id,"^1.0.0")
    assert out.descriptor.identity.artifact_id==descriptor.identity.artifact_id

def test_digest_drift_fails(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); (tmp_path/descriptor.canonical_path).write_text("mutated",encoding="utf-8")
    out=ArtifactLocator(registry,tmp_path).resolve(descriptor.identity.artifact_id)
    assert out.status.value=="INTEGRITY_FAILURE"

def test_missing_file_fails(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); (tmp_path/descriptor.canonical_path).unlink()
    out=ArtifactLocator(registry,tmp_path).resolve(descriptor.identity.artifact_id)
    assert out.status.value=="NOT_FOUND"

def test_quarantined_not_resolved(registry,descriptor,permit_factory,tmp_path):
    q=replace(descriptor,status=RegistryStatus.QUARANTINED); setup(registry,q,permit_factory)
    assert ArtifactLocator(registry,tmp_path).resolve(q.identity.artifact_id).status.value=="NOT_FOUND"

def test_alias_resolution(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); assert not registry.register_alias("context:latest",descriptor.identity.artifact_id,permit_factory("REGISTER_ALIAS",subject=descriptor.identity.artifact_id))
    assert ArtifactLocator(registry,tmp_path).resolve("context:latest").descriptor.identity.artifact_id==descriptor.identity.artifact_id

def test_alias_cycle_detected(registry):
    registry.aliases={"a":"b","b":"a"}; target,reasons=registry.resolve_alias("a"); assert target is None and reasons[0].code=="ALIAS_CYCLE"


def test_base_without_constraint_denied(registry,descriptor,permit_factory,tmp_path):
    setup(registry,descriptor,permit_factory); out=ArtifactLocator(registry,tmp_path).resolve(descriptor.identity.base_id)
    assert out.status.value=="NOT_FOUND" and any(x.code=="BASE_ID_VERSION_CONSTRAINT_REQUIRED" for x in out.reasons)

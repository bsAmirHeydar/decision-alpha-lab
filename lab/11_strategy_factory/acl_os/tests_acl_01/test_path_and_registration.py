from dataclasses import replace
from tools.strategy_factory.acl_os.acl_01.types import ArtifactMutability

def test_register_valid_artifact(registry,descriptor,permit_factory):
    assert registry.register_artifact(descriptor,permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id))==[]
    assert descriptor.identity.artifact_id in registry.artifacts

def test_duplicate_artifact_rejected(registry,descriptor,permit_factory):
    permit=permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id); assert not registry.register_artifact(descriptor,permit)
    assert any(x.code=="ARTIFACT_ID_ALREADY_REGISTERED" for x in registry.register_artifact(descriptor,permit))

def test_zone_mismatch(registry,descriptor,permit_factory):
    bad=replace(descriptor,zone="generated")
    reasons=registry.register_artifact(bad,permit_factory("REGISTER_ARTIFACT",subject=bad.identity.artifact_id))
    assert any(x.code=="PATH_ZONE_MISMATCH" for x in reasons)

def test_generated_requires_provenance(registry,descriptor,permit_factory):
    bad=replace(descriptor,zone="generated",canonical_path="lab/11_strategy_factory/generated/alpha/research/generated_projection/x/1.0.0/x.md",mutability=ArtifactMutability.GENERATED)
    reasons=registry.register_artifact(bad,permit_factory("REGISTER_ARTIFACT",subject=bad.identity.artifact_id))
    assert any(x.code=="GENERATED_PROVENANCE_MISSING" for x in reasons)

def test_unregistered_owner_fails(registry,descriptor,permit_factory):
    bad=replace(descriptor,owner_id="OWNER_UNKNOWN")
    reasons=registry.register_artifact(bad,permit_factory("REGISTER_ARTIFACT",subject=bad.identity.artifact_id))
    assert any(x.code=="OWNER_NOT_REGISTERED" for x in reasons)

def test_unregistered_schema_fails(registry,descriptor,permit_factory):
    bad=replace(descriptor,schema_id="schema:missing:1")
    reasons=registry.register_artifact(bad,permit_factory("REGISTER_ARTIFACT",subject=bad.identity.artifact_id))
    assert any(x.code=="SCHEMA_NOT_REGISTERED" for x in reasons)

def test_invalid_permit_action_fails(registry,descriptor,permit_factory):
    reasons=registry.register_artifact(descriptor,permit_factory("REGISTER_SCHEMA",subject=descriptor.identity.artifact_id))
    assert any(x.code=="ACL00_ACTION_MISMATCH" for x in reasons)

def test_live_authority_permit_fails(registry,descriptor,permit_factory):
    from dataclasses import replace
    p=replace(permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id),capital_activation_allowed=True)
    reasons=registry.register_artifact(descriptor,p)
    assert any(x.code=="ILLEGAL_LIVE_AUTHORITY_CLAIM" for x in reasons)


def test_alias_collision_is_atomic(registry,descriptor,permit_factory):
    registry.aliases["collision"]="other"
    from dataclasses import replace
    d=replace(descriptor,aliases=("collision",))
    reasons=registry.register_artifact(d,permit_factory("REGISTER_ARTIFACT",subject=d.identity.artifact_id))
    assert reasons and d.identity.artifact_id not in registry.artifacts

def test_wrong_acl00_policy_digest_fails(registry,descriptor,permit_factory):
    from dataclasses import replace
    permit=replace(permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id),policy_digest="sha256:"+"f"*64)
    reasons=registry.register_artifact(descriptor,permit)
    assert any(x.code=="ACL00_POLICY_DIGEST_MISMATCH" for x in reasons)

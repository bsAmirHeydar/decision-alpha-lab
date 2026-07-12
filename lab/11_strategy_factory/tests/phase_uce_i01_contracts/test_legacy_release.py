from strategy_factory_contracts_v3.enums import IdentityKind
from strategy_factory_contracts_v3.legacy_bridge import bridge_sf01
from strategy_factory_contracts_v3.release import ArtifactDigest,build_release_manifest
from strategy_factory_contracts_v3.schema import SchemaDescriptor,SchemaId,SchemaRegistry,SemanticVersion
from strategy_factory_contracts_v3.time_model import UtcInstant

def test_sf01_bridge_preserves_both_identities():
    legacy=SchemaId("alpha_lab.strategy_factory","anatomy_event",SemanticVersion(1,0,0))
    identity,record=bridge_sf01(legacy_contract_id="sf01",legacy_schema=legacy,legacy_entity_id="evt_42",legacy_payload={"x":1},target_kind=IdentityKind.CONTEXT_OCCURRENCE,semantic_namespace="exp0017.context",semantic_version="1.0.0",owner_id="exp0017",bridged_at=UtcInstant(100,"bridge"))
    assert record.legacy_entity_id=="evt_42"
    assert record.v3_entity_id==identity.stable_id
    assert record.legacy_payload_sha256 in identity.dimensions.values()

def test_release_manifest_is_order_stable():
    descriptor=SchemaDescriptor(SchemaId("alpha_lab.ucee","x",SemanticVersion(3,0,0)),"owner",("a",))
    schemas=SchemaRegistry((descriptor,))
    a=ArtifactDigest("b.json","a"*64,"application/json",2)
    b=ArtifactDigest("a.json","b"*64,"application/json",1)
    left=build_release_manifest(release_id="ucee-contracts-3.0.0",created_at=UtcInstant(1,"release"),schemas=schemas,artifacts=(a,b))
    right=build_release_manifest(release_id="ucee-contracts-3.0.0",created_at=UtcInstant(1,"release"),schemas=schemas,artifacts=(b,a))
    assert left.manifest_sha256==right.manifest_sha256

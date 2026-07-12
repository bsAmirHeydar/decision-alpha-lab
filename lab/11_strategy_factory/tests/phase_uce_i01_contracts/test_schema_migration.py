import pytest
from strategy_factory_contracts_v3.enums import MigrationMode
from strategy_factory_contracts_v3.errors import MigrationError,SchemaError
from strategy_factory_contracts_v3.migration import MigrationEdge,MigrationRegistry
from strategy_factory_contracts_v3.schema import SchemaDescriptor,SchemaId,SchemaRegistry,SemanticVersion
from strategy_factory_contracts_v3.time_model import UtcInstant

def make_registry():
    v300=SchemaDescriptor(SchemaId("alpha_lab.ucee","sample",SemanticVersion(3,0,0)),"owner",("a",))
    v310=SchemaDescriptor(SchemaId("alpha_lab.ucee","sample",SemanticVersion(3,1,0)),"owner",("a","b"))
    return SchemaRegistry((v300,v310)),v300,v310

def test_exact_resolution_and_unknown_version_rejection():
    registry,v300,_=make_registry()
    assert registry.resolve_exact(v300.schema_id).semantic_hash==v300.semantic_hash
    with pytest.raises(SchemaError) as error:registry.resolve_exact("alpha_lab.ucee/sample@3.0.1")
    assert error.value.code=="unknown_exact_schema"
    with pytest.raises(SchemaError):registry.require_supported_major("alpha_lab.ucee","sample",4)

def test_migration_records_source_and_destination_hashes():
    registry,v300,v310=make_registry()
    edge=MigrationEdge("sample_300_to_310",v300.schema_id,v310.schema_id,v300.semantic_hash,v310.semantic_hash,MigrationMode.LOSSLESS,lambda row:{**row,"b":0})
    migrations=MigrationRegistry(registry,(edge,))
    migrated,evidence=migrations.migrate({"a":7},v300.schema_id,v310.schema_id,applied_at=UtcInstant(100,"migration"))
    assert migrated=={"a":7,"b":0}
    assert evidence.source_payload_sha256!=evidence.destination_payload_sha256
    assert evidence.migration_path==("sample_300_to_310",)

def test_cross_family_and_non_monotonic_migrations_rejected():
    registry,v300,v310=make_registry()
    with pytest.raises(MigrationError):
        MigrationEdge("bad",v310.schema_id,v300.schema_id,v310.semantic_hash,v300.semantic_hash,MigrationMode.LOSSLESS,lambda row:row)

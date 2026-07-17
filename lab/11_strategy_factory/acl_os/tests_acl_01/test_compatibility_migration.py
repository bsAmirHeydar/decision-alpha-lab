from dataclasses import replace
from tools.strategy_factory.acl_os.acl_01.compatibility import CompatibilityRequirement
from tools.strategy_factory.acl_os.acl_01.migrations import MigrationPlan

def test_compatible_provider(registry,descriptor,permit_factory):
    registry.artifacts[descriptor.identity.artifact_id]=descriptor
    req=CompatibilityRequirement("consumer",descriptor.identity.base_id,"^1.0.0","context.read","^1.0.0","INTERNAL")
    got,reasons=registry.compat.resolve(req,registry.artifacts); assert got==descriptor and not reasons

def test_security_downgrade_denied(registry,descriptor):
    registry.artifacts[descriptor.identity.artifact_id]=descriptor
    req=CompatibilityRequirement("consumer",descriptor.identity.base_id,"*","context.read","*","SECRET")
    got,reasons=registry.compat.resolve(req,registry.artifacts); assert got is None and reasons[0].code=="NO_COMPATIBLE_PROVIDER"

def test_breaking_schema_requires_major(registry,descriptor):
    new=replace(descriptor,identity=replace(descriptor.identity,version="1.1.0",artifact_id=descriptor.identity.artifact_id.replace("@1.0.0","@1.1.0"),digest="sha256:"+"3"*64),metadata=descriptor.metadata|{"schema_semver":"1.1.0","breaking_change":True})
    assert any(x.code=="BREAKING_SCHEMA_WITHOUT_MAJOR" for x in registry.compat.validate_schema_evolution(descriptor,new))

def test_valid_migration(registry):
    p=MigrationPlan("MIG_1","al://alpha/x/context_contract/x","1.0.0","2.0.0","al://alpha/x/migration/up@1.0.0","al://alpha/x/migration/down@1.0.0","IDEMP_1",True,True,False,"DEC_1")
    assert not registry.migration_registry.validate([p])

def test_irreversible_migration_denied(registry):
    p=MigrationPlan("MIG_1","al://alpha/x/context_contract/x","1.0.0","2.0.0","up","down","IDEMP_1",True,True,True,"DEC_1")
    assert any(x.code=="IRREVERSIBLE_MIGRATION_DENIED" for x in registry.migration_registry.validate([p]))

def test_migration_requires_dry_run(registry):
    p=MigrationPlan("MIG_1","al://alpha/x/context_contract/x","1.0.0","2.0.0","up","down","IDEMP_1",False,True,False,"DEC_1")
    assert any(x.code=="MIGRATION_DRY_RUN_REQUIRED" for x in registry.migration_registry.validate([p]))

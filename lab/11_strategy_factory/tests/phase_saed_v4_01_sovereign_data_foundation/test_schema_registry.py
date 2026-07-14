import pytest
from saed_v4_data_foundation.schema_registry import SchemaRegistry
from saed_v4_data_foundation.errors import ImmutableConflict,ContractError
S={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','additionalProperties':False,'properties':{'x':{'type':'integer'}},'required':['x']}
def test_register_validate(): r=SchemaRegistry(); r.register('x','1',S); r.validate('x','1',{'x':1})
def test_unknown_rejected():
 r=SchemaRegistry(); r.register('x','1',S)
 with pytest.raises(ContractError): r.validate('x','1',{'x':1,'y':2})
def test_open_schema_rejected():
 r=SchemaRegistry()
 with pytest.raises(ContractError): r.register('x','1',{'type':'object','properties':{}})
def test_idempotent():
 r=SchemaRegistry(); a=r.register('x','1',S); b=r.register('x','1',dict(S)); assert a==b
def test_conflict():
 r=SchemaRegistry(); r.register('x','1',S)
 with pytest.raises(ImmutableConflict): r.register('x','1',{**S,'required':[]})
def test_migration_declaration():
 r=SchemaRegistry();r.register('x','1',S);r.register('x','2',S);r.declare_migration('x','1','2','a'*64);assert r.migration_hash('x','1','2')=='a'*64
def test_registry_hash_stable():
 a=SchemaRegistry();b=SchemaRegistry();a.register('x','1',S);b.register('x','1',S);assert a.registry_hash()==b.registry_hash()

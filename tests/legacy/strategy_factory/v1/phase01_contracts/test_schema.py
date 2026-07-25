import pytest
from strategy_factory_contracts import SchemaIdentity, Compatibility
from strategy_factory_contracts.validation import ContractValidationError

def test_schema_canonical():
    schema = SchemaIdentity("alpha_lab.strategy_factory","anatomy_event",1,0,0)
    assert schema.canonical == "alpha_lab.strategy_factory/anatomy_event@1.0.0"

def test_schema_major_breaks_compatibility():
    producer = SchemaIdentity("alpha_lab.strategy_factory","anatomy_event",2,0,0)
    consumer = SchemaIdentity("alpha_lab.strategy_factory","anatomy_event",1,9,0)
    assert producer.compatibility_with(consumer) == Compatibility.INCOMPATIBLE

def test_invalid_identifier_rejected():
    with pytest.raises(ContractValidationError):
        SchemaIdentity("bad namespace","x",1,0,0)

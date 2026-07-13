import pytest
from fp_i01_compatibility.models import DependencyPin,AdapterDescriptor
from fp_i01_compatibility.enums import *
from fp_i01_compatibility.errors import CompatibilityError

def test_dependency_pin_forbids_mutation():
    with pytest.raises(CompatibilityError,match='read-only'):
        DependencyPin('D','O',SourceContext.EXP0017,ReuseMode.ADAPTER,'x',('*.mqh',),1,'a'*64,'HASH_PINNED',True)

def test_adapter_forbids_authority():
    with pytest.raises(CompatibilityError,match='authority'):
        AdapterDescriptor('A','1.0.0',SourceContext.EXP0017,'T',AdapterFamily.TIME,ReuseMode.ADAPTER,'D',('x',),('y',),(),False,('ORDER',))

def test_descriptor_hash_changes_with_semantic_delta():
    a=AdapterDescriptor('A','1.0.0',SourceContext.EXP0017,'T',AdapterFamily.TIME,ReuseMode.ADAPTER,'D',('x',),('y',),('one',))
    b=AdapterDescriptor('A','1.0.0',SourceContext.EXP0017,'T',AdapterFamily.TIME,ReuseMode.ADAPTER,'D',('x',),('y',),('two',))
    assert a.descriptor_hash!=b.descriptor_hash

import pytest
from saed_v4_data_foundation.lineage import LineageGraph
from saed_v4_data_foundation.models import LineageEdge
from saed_v4_data_foundation.enums import LineageEdgeType
from saed_v4_data_foundation.errors import LineageCycleError
H='a'*64
def e(a,b): return LineageEdge(a,b,LineageEdgeType.DERIVED_FROM,'t','1',H)
def test_add_and_ancestors():
 g=LineageGraph();g.add(e('a','b'));g.add(e('b','c'));assert g.ancestors('c')=={'a','b'}
def test_self_cycle():
 with pytest.raises(LineageCycleError): LineageGraph().add(e('a','a'))
def test_indirect_cycle():
 g=LineageGraph();g.add(e('a','b'));g.add(e('b','c'))
 with pytest.raises(LineageCycleError): g.add(e('c','a'))
def test_root_deterministic():
 a=LineageGraph();b=LineageGraph();a.add(e('a','b'));a.add(e('b','c'));b.add(e('b','c'));b.add(e('a','b'));assert a.root_hash()==b.root_hash()
def test_idempotent_edge():
 g=LineageGraph();x=e('a','b');assert g.add(x)==g.add(x)

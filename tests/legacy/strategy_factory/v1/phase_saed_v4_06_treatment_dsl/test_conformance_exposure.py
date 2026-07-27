from .helpers import build,graph,handoff,sources
from saed_v4_treatment_dsl.catalog import institutional_capability_profile,institutional_policy,institutional_registry
from saed_v4_treatment_dsl.conformance import run_conformance
def test_conformance_is_order_invariant():
 r=run_conformance(graph=graph(),handoff=handoff(),registry=institutional_registry(),policy=institutional_policy(),capability_profile=institutional_capability_profile(),sources=sources());assert r['ordering_invariant'];assert not r['selection_authority'];assert not r['runtime_authority'];assert not r['order_authority']

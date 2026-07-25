import pytest
from strategy_factory_treatments_v3 import *
def test_catalog_contains_50_exact_version_atoms():
 c=build_default_catalog(); assert c.atom_count==50
 assert [len(r.all()) for r in c.registries()]==[8,8,7,10,8,9]
 assert len({a.descriptor.definition_id for r in c.registries() for a in r.all()})==50
def test_registry_is_frozen_and_exact_version_only():
 c=build_default_catalog()
 with pytest.raises(RegistryError): c.entry.register(ImmediateMarketEntry())
 with pytest.raises(RegistryError): c.entry.resolve('entry.immediate_market','9.9.9')
def test_parameter_packet_identity_changes_with_behavior():
 a=FixedDistanceStop(); x,_=a.invoke(reference_context(),{'distance_points':'100'}); y,_=a.invoke(reference_context(),{'distance_points':'101'})
 assert x.invocation_id!=y.invocation_id and x.parameters.packet_id!=y.parameters.packet_id
def test_manual_and_ai_provenance_share_same_contract():
 a=FixedRTarget(); c=reference_context()
 m,_=a.invoke(c,provenance={'source':'manual'}); ai,_=a.invoke(c,provenance={'source':'ai_search'})
 assert m.descriptor_definition_id==ai.descriptor_definition_id
 assert m.invocation_id!=ai.invocation_id

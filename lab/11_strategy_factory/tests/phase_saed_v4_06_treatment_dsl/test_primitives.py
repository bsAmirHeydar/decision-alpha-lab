import pytest
from saed_v4_treatment_dsl.catalog import institutional_registry
from saed_v4_treatment_dsl.enums import PrimitiveKind

def test_skip_and_abstain_are_first_class():
 r=institutional_registry(); fam={(x.kind.value,x.family) for x in r.primitives}; assert ('action','skip') in fam; assert ('action','abstain') in fam
@pytest.mark.parametrize('kind',[x.value for x in PrimitiveKind])
def test_registry_covers_primitive_kind(kind):
 assert any(x.kind.value==kind for x in institutional_registry().primitives)
@pytest.mark.parametrize('primitive',institutional_registry().primitives,ids=lambda x:x.primitive_id)
def test_primitive_ids_hash_stably(primitive):
 assert primitive.definition_id.startswith('dslprim_'); assert len(primitive.definition_hash)==64
@pytest.mark.parametrize('primitive',institutional_registry().primitives,ids=lambda x:x.primitive_id)
def test_primitive_parameters_are_unique(primitive):
 names=[x.name for x in primitive.parameters]; assert len(names)==len(set(names))

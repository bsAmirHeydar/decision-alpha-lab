import pytest
from saed_v4_context_twin.models import OntologyTerm,OntologyRelation
from saed_v4_context_twin.ontology import OntologyGraph
from saed_v4_context_twin.enums import RelationKind
from saed_v4_context_twin.errors import OntologyError

def t(i):return OntologyTerm(i,i,'d','n')
def test_ancestors():
 g=OntologyGraph([t('a'),t('b'),t('c')]);g.add_relation(OntologyRelation('a','b',RelationKind.IS_A));g.add_relation(OntologyRelation('b','c',RelationKind.IS_A));assert g.ancestors('a')==('b','c')
def test_unknown_term():
 with pytest.raises(OntologyError):OntologyGraph([t('a')],[OntologyRelation('a','x',RelationKind.IS_A)])
def test_cycle():
 g=OntologyGraph([t('a'),t('b')]);g.add_relation(OntologyRelation('a','b',RelationKind.IS_A))
 with pytest.raises(OntologyError):g.add_relation(OntologyRelation('b','a',RelationKind.IS_A))
def test_duplicate_idempotent():
 r=OntologyRelation('a','b',RelationKind.RELATED_TO);g=OntologyGraph([t('a'),t('b')],[r]);g.add_relation(r);assert len(g.relations)==1

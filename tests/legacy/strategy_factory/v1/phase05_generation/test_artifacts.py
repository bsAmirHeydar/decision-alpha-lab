import pytest
from strategy_factory_generation import ArtifactCatalog,ArtifactEntry
def test_catalog_add_seal():
    c=ArtifactCatalog();c.add(ArtifactEntry('a1','run/x.jsonl','application/jsonl','schema'));c.seal('a1',3,100,'hash');assert c.get('a1').sealed and len(c)==1

def test_catalog_duplicate_rejected():
    c=ArtifactCatalog();c.add(ArtifactEntry('a1','x','t','s'))
    with pytest.raises(ValueError):c.add(ArtifactEntry('a1','y','t','s'))

def test_catalog_path_traversal_rejected():
    with pytest.raises(ValueError):ArtifactCatalog().add(ArtifactEntry('a','../x','t','s'))

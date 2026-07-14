import pytest
from saed_v4_data_foundation.retention import RetentionPolicy
from saed_v4_data_foundation.enums import RetentionClass,ArtifactKind,DataRole
from saed_v4_data_foundation.errors import AccessDenied,ImmutableConflict,IntegrityViolation
from saed_v4_data_foundation.migration import MigrationRegistry
from saed_v4_data_foundation.catalog import ArtifactCatalog
from saed_v4_data_foundation.models import ArtifactDescriptor
from saed_v4_data_foundation.canonical import content_hash
H='a'*64
def test_retention_elapsed(): assert RetentionPolicy(RetentionClass.RESEARCH,1).deletable('2026-01-01T00:00:00Z','2026-01-03T00:00:00Z')
def test_permanent_not_deletable(): assert not RetentionPolicy(RetentionClass.PERMANENT,0).deletable('2026-01-01T00:00:00Z','2030-01-01T00:00:00Z')
def test_legal_hold():
 with pytest.raises(AccessDenied): RetentionPolicy(RetentionClass.RESEARCH,0,True).require_deletable('2026-01-01T00:00:00Z','2030-01-01T00:00:00Z')
def test_migration():
 r=MigrationRegistry();r.register('x','1','2',lambda d:{'x':d['x']+1},H);out,src,dig=r.migrate('x','1','2',{'x':1});assert out=={'x':2} and src==H
def test_migration_hash_mismatch():
 r=MigrationRegistry();r.register('x','1','2',lambda d:{'x':2},H)
 with pytest.raises(IntegrityViolation):r.migrate('x','1','2',{'x':1},'0'*64)
def art(h=H):return ArtifactDescriptor('a',ArtifactKind.DATASET_SNAPSHOT,'1',h,'s','1',DataRole.DEVELOPMENT)
def test_catalog_idempotent():
 c=ArtifactCatalog();assert c.register(art())==c.register(art())
def test_catalog_conflict():
 c=ArtifactCatalog();c.register(art())
 with pytest.raises(ImmutableConflict):c.register(art('b'*64))

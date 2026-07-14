import pytest
from dataclasses import replace
from helpers import golden_sources,sv
from saed_v4_multimodal_views.source_frame import SourceFrame
from saed_v4_multimodal_views.errors import SourceConflictError

def test_identical_duplicate_is_idempotent():
 x=golden_sources()[0];f=SourceFrame((x,x));assert len(f.all())==1
def test_conflicting_duplicate_rejected():
 x=golden_sources()[0];y=replace(x,value=x.value+1)
 with pytest.raises(SourceConflictError):SourceFrame((x,y))
def test_bad_quality_rejected():
 with pytest.raises(SourceConflictError):SourceFrame((sv('x','y',1,quality=1.1),))
def test_bad_source_hash_rejected():
 x=replace(golden_sources()[0],source_hash='bad')
 with pytest.raises(SourceConflictError):SourceFrame((x,))

import pytest
from saed_v4_event_model.registry import EventStreamRegistry,ProjectionRegistry
from saed_v4_event_model.errors import RegistryError,AuthorityError
from dataclasses import replace

def test_manifest_identity_order_independent(stream_nq):
    x=replace(stream_nq,subject_ids=tuple(reversed(stream_nq.subject_ids)),accepted_kinds=tuple(reversed(stream_nq.accepted_kinds)))
    assert x.semantic_hash==stream_nq.semantic_hash

def test_exact_version_rebind_rejected(stream_nq):
    r=EventStreamRegistry();r.register(stream_nq)
    with pytest.raises(RegistryError):r.register(replace(stream_nq,source_priority=999))

def test_forbidden_authority_rejected(stream_nq):
    from saed_v4_event_model.models import EventAuthorityBoundary
    r=EventStreamRegistry()
    with pytest.raises(AuthorityError):r.register(replace(stream_nq,authority=EventAuthorityBoundary(send_order=True)))

def test_projection_duplicate_field_rejected(projection_def):
    r=ProjectionRegistry()
    from dataclasses import replace
    with pytest.raises(RegistryError):r.register(replace(projection_def,fields=(projection_def.fields[0],projection_def.fields[0])))

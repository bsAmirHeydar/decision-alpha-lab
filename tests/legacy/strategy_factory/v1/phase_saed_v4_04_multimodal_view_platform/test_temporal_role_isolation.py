import pytest
from dataclasses import replace
from .helpers import service_and_specs,request,golden_sources,KT,ET
from saed_v4_multimodal_views.enums import EvidenceRole
from saed_v4_multimodal_views.errors import MissingnessError,ViewBuildError

def test_future_known_source_not_visible():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');src=[replace(x,known_time='2026-01-06T00:00:00Z') if x.path=='bid' else x for x in golden_sources()]
 with pytest.raises(MissingnessError):service.build_view(price,request(src))
def test_future_event_source_not_visible():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');src=[replace(x,event_time='2026-01-06T00:00:00Z',known_time='2026-01-06T00:00:01Z') if x.path=='bid' else x for x in golden_sources()]
 with pytest.raises(MissingnessError):service.build_view(price,request(src))
def test_cross_role_source_rejected_as_unavailable():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');src=[replace(x,evidence_role=EvidenceRole.LOCKED_FINAL) if x.path=='bid' else x for x in golden_sources()]
 with pytest.raises(MissingnessError):service.build_view(price,request(src))
def test_request_role_must_be_allowed():
 service,specs=service_and_specs();s=replace(specs[0],evidence_roles=(EvidenceRole.DEVELOPMENT,))
 with pytest.raises(ViewBuildError):service.build_view(s,request(role=EvidenceRole.LOCKED_FINAL))
def test_irrelevant_future_suffix_does_not_change_view_hash():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');a=service.build_view(price,request());extra=replace(golden_sources()[0],namespace='unused',path='future_noise',value=999,event_time='2026-01-06T00:00:00Z',known_time='2026-01-06T00:00:01Z');b=service.build_view(price,request(golden_sources()+(extra,)));assert a.view_hash==b.view_hash

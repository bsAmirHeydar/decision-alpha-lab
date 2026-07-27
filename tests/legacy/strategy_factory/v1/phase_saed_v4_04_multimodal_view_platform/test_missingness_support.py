import pytest
from dataclasses import replace
from .helpers import service_and_specs,request,golden_sources
from saed_v4_multimodal_views.enums import ViewStatus,MissingnessPolicy
from saed_v4_multimodal_views.errors import MissingnessError

def without(path):return tuple(x for x in golden_sources() if x.path!=path)
def test_missing_prohibited_feature_fails():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view')
 with pytest.raises(MissingnessError):service.build_view(price,request(without('bid')))
def test_missing_unknown_required_yields_unknown():
 service,specs=service_and_specs();htf=next(s for s in specs if s.view_name=='higher_timeframe_view');v=service.build_view(htf,request(without('htf_alignment')));assert v.status==ViewStatus.UNKNOWN;assert 'htf_alignment' in v.support.missing_features
def test_explicit_default_is_masked():
 service,specs=service_and_specs();anc=next(s for s in specs if s.view_name=='context_ancestry_view');v=service.build_view(anc,request(without('parent_context_id')));f=next(x for x in v.features if x.feature_id=='parent_context_id');assert f.value=='none' and f.mask==1 and f.missing
def test_optional_missing_degrades_view():
 service,specs=service_and_specs();liq=next(s for s in specs if s.view_name=='liquidity_view');v=service.build_view(liq,request(without('quote_rate')));assert v.status==ViewStatus.DEGRADED
def test_stale_required_degrades_or_quarantines():
 service,specs=service_and_specs();price=next(s for s in specs if s.view_name=='price_view');src=[]
 for x in golden_sources():src.append(replace(x,event_time='2026-01-05T14:00:00Z') if x.path in {'bid','ask'} else x)
 v=service.build_view(price,request(src));assert v.status in {ViewStatus.DEGRADED,ViewStatus.QUARANTINED}

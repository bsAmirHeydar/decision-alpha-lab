import pytest
from dataclasses import replace
from .helpers import service_and_specs,request,golden_sources
from saed_v4_multimodal_views.diff import diff_views
from saed_v4_multimodal_views.integrity import build_integrity_receipt,verify_integrity
from saed_v4_multimodal_views.errors import ReplayError,IntegrityError

def test_view_replay_passes():
 service,specs=service_and_specs();s=specs[0];v=service.build_view(s,request());r=service.replayer.replay(s,request(),v.view_hash);assert r.status=='pass'
def test_view_replay_mismatch_fails():
 service,specs=service_and_specs();s=specs[0]
 with pytest.raises(ReplayError):service.replayer.replay(s,request(),'0'*64)
def test_view_diff_finds_changed_feature():
 service,specs=service_and_specs();s=specs[0];a=service.build_view(s,request());src=[replace(x,value=19999.0) if x.path=='bid' else x for x in golden_sources()];b=service.build_view(s,request(src));d=diff_views(a,b);assert {'bid','mid','spread'}<=set(d.changed_features)
def test_integrity_receipt_passes():
 service,specs=service_and_specs();vs=[service.build_view(s,request()) for s in specs];p=service.build_package(vs,'1.0.0',tuple(s.view_name for s in specs if s.required_view));r=build_integrity_receipt(p);assert verify_integrity(p,r)
def test_integrity_tamper_fails():
 service,specs=service_and_specs();vs=[service.build_view(s,request()) for s in specs];p=service.build_package(vs,'1.0.0',tuple(s.view_name for s in specs if s.required_view));r=build_integrity_receipt(p);bad=replace(p,package_hash='0'*64)
 with pytest.raises(IntegrityError):verify_integrity(bad,r)

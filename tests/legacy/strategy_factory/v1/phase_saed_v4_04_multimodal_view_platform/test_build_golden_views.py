from .helpers import service_and_specs,request
from saed_v4_multimodal_views.enums import ViewStatus,CompatibilityStatus

def test_all_golden_views_build():
 service,specs=service_and_specs();views=[service.build_view(s,request()) for s in specs];assert len(views)==10;assert all(v.view_hash for v in views)
def test_required_golden_views_complete():
 service,specs=service_and_specs();views=[service.build_view(s,request()) for s in specs if s.required_view];assert all(v.status==ViewStatus.COMPLETE for v in views)
def test_price_mid_and_spread():
 service,specs=service_and_specs();v=service.build_view(next(s for s in specs if s.view_name=='price_view'),request());m={x.feature_id:x.value for x in v.features};assert m['mid']==20000.25;assert m['spread']==0.5
def test_time_age_features():
 service,specs=service_and_specs();v=service.build_view(next(s for s in specs if s.view_name=='time_view'),request());m={x.feature_id:x.value for x in v.features};assert m['seconds_since_context_start']==1800.0
def test_package_compatible():
 service,specs=service_and_specs();views=[service.build_view(s,request()) for s in specs];p=service.build_package(views,'1.0.0',tuple(s.view_name for s in specs if s.required_view));assert p.compatibility.status==CompatibilityStatus.COMPATIBLE;assert len(p.missingness_vector)==sum(len(v.features) for v in views)
def test_package_order_invariant():
 service,specs=service_and_specs();views=[service.build_view(s,request()) for s in specs];a=service.build_package(views,'1.0.0',tuple(s.view_name for s in specs if s.required_view));b=service.build_package(reversed(views),'1.0.0',tuple(reversed([s.view_name for s in specs if s.required_view])));assert a.package_hash==b.package_hash

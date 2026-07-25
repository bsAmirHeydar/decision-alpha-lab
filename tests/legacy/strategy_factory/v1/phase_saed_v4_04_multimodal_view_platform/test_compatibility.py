from dataclasses import replace
from helpers import service_and_specs,request
from saed_v4_multimodal_views.compatibility import assess_compatibility
from saed_v4_multimodal_views.enums import CompatibilityStatus,ViewStatus

def views():
 service,specs=service_and_specs();return service,specs,[service.build_view(s,request()) for s in specs]
def test_missing_required_view_incompatible():
 service,specs,vs=views();required=tuple(s.view_name for s in specs if s.required_view);p=service.build_package([v for v in vs if v.view_name!='price_view'],'1.0.0',required);assert p.compatibility.status==CompatibilityStatus.INCOMPATIBLE;assert 'price_view' in p.compatibility.missing_required_views
def test_boundary_mismatch_incompatible():
 service,specs,vs=views();bad=replace(vs[0],known_as_of='2026-01-05T14:31:00Z');c=assess_compatibility((bad,vs[1]),());assert c.status==CompatibilityStatus.INCOMPATIBLE
def test_role_mismatch_incompatible():
 from saed_v4_multimodal_views.enums import EvidenceRole
 service,specs,vs=views();bad=replace(vs[0],evidence_role=EvidenceRole.LOCKED_FINAL);c=assess_compatibility((bad,vs[1]),());assert c.status==CompatibilityStatus.INCOMPATIBLE
def test_degraded_view_degrades_compatible_package():
 service,specs,vs=views();bad=replace(vs[0],status=ViewStatus.DEGRADED);c=assess_compatibility((bad,vs[1]),());assert c.status==CompatibilityStatus.DEGRADED

from helpers import service_and_specs,request
from saed_v4_multimodal_views.integrity import build_integrity_receipt
from saed_v4_multimodal_views.handoff import build_handoff
from saed_v4_multimodal_views.telemetry import telemetry

def package():
 service,specs=service_and_specs();vs=[service.build_view(s,request()) for s in specs];return service.build_package(vs,'1.0.0',tuple(s.view_name for s in specs if s.required_view))
def test_handoff_is_bounded():
 p=package();h=build_handoff(p,build_integrity_receipt(p));assert h['next_phase']=='SAED_V4_05';assert h['authority']['construct_temporal_hypergraph'];assert not h['authority']['train_model'];assert not h['authority']['select_treatment'];assert not h['authority']['send_order']
def test_telemetry_counts_views():
 t=telemetry(package());assert t['view_count']==10;assert t['complete_views']==10;assert t['missing_feature_count']==0

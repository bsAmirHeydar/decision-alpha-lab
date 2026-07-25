import hashlib
from saed_v4_multimodal_views.catalog import institutional_view_catalog
from saed_v4_multimodal_views.models import SourceValue,ViewBuildRequest
from saed_v4_multimodal_views.enums import EvidenceRole
from saed_v4_multimodal_views.service import MultimodalViewService
TWIN='twin_golden';ET='2026-01-05T14:30:00Z';KT='2026-01-05T14:30:01Z'
def sv(ns,path,value,event_time=ET,known_time=KT,quality=1.0,role=EvidenceRole.DEVELOPMENT,artifact=None,conflict=False):
 artifact=artifact or f'artifact_{ns}'
 return SourceValue(ns,path,value,event_time,known_time,quality,role,artifact,hashlib.sha256(artifact.encode()).hexdigest(),(f'lineage_{ns}',),conflict)
def golden_sources():
 return (
 sv('projection','bid',20000.0),sv('projection','ask',20000.5),sv('projection','last_trade_price',20000.25),sv('projection','previous_trade_price',19999.75,'2026-01-05T14:29:58Z'),sv('projection','reference_touch_count',2),sv('projection','last_event_marker',1),sv('projection','related_symbol_score',0.65,'2026-01-05T14:29:59Z'),sv('projection','quote_rate',42.0),sv('projection','trade_rate',12.0),sv('projection','gap_count',0),sv('projection','session_boundary_recent',False),
 sv('twin','lifecycle_state','valid'),sv('twin','twin_state','observing'),sv('twin','context_fresh',True),sv('twin','support_score',0.96),sv('twin','context_start_time','2026-01-05T14:00:00Z','2026-01-05T14:00:00Z'),sv('twin','htf_alignment',0.8),sv('twin','htf_phase','bullish'),sv('twin','htf_fresh',True),sv('twin','context_family','F2'),sv('twin','parent_context_id','ctx_parent'),sv('twin','generation_depth',2),sv('twin','transition_code_1',1),sv('twin','transition_code_2',3),
 sv('static','hour_utc',14),sv('static','weekday_utc',0),sv('static','cross_market_state','confirming'),sv('static','liquidity_state','normal'),sv('static','session_id','new_york'),sv('static','session_open',True),sv('static','minutes_from_open',0),
 sv('execution','spread_points',0.5),sv('execution','estimated_slippage_points',0.1),sv('execution','latency_ms',25.0),sv('execution','broker_state','normal'),sv('approved_treatment','descriptor_id','treatment_approved_001'),sv('approved_treatment','payoff_profile','P3'),sv('approved_treatment','entry_mechanism','breakout'),sv('approved_treatment','path_dependent',True))
def service_and_specs():
 service=MultimodalViewService();specs=institutional_view_catalog(TWIN)
 for s in specs:service.register_specification(s)
 return service,specs
def request(sources=None,known_as_of=KT,event_as_of=ET,role=EvidenceRole.DEVELOPMENT,rid='test'):
 return ViewBuildRequest(TWIN,known_as_of,event_as_of,role,tuple(sources or golden_sources()),rid)

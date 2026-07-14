from fp_i10_indicator import *
from fp_i10_indicator.enums import *

def test_init_creates_snapshot(config,modules):
 e=IndicatorEngine(); s=e.initialize(config=config,chart_id=1,terminal_instance_id='T',modules=modules,now_m1=1783900800000); assert s.sequence==0 and e.initialized
def test_timer_ready(engine,ready_state): assert engine.timer(now_m1=1783900860000,upstream_state=ready_state).health.overall is HealthState.READY
def test_calculate_incremental(engine,ready_state):
 before=engine.cursor.last_processed_m1; s=engine.calculate(target_closed_m1=before+60000,upstream_state=ready_state); assert s.last_processed_m1==before+60000
def test_duplicate_calculate_no_work(engine,ready_state):
 t=engine.cursor.last_processed_m1; count=engine.counters['processed_minutes']; engine.calculate(target_closed_m1=t,upstream_state=ready_state); assert engine.counters['processed_minutes']==count
def test_chart_event_does_not_replace_snapshot(engine):
 h=engine.snapshot.snapshot_hash; engine.chart_event(now_m1=engine.snapshot.generated_utc_ms,event_id=1,sparam='x'); assert engine.snapshot.snapshot_hash==h
def test_deinit_stops(engine):
 head=engine.deinitialize(now_m1=engine.snapshot.generated_utc_ms); assert head and engine.lifecycle is LifecycleState.STOPPED and not engine.initialized
def test_event_chain_valid(engine): assert engine.event_chain.validate()

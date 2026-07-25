from fp_i10_indicator.channels import *
from fp_i10_indicator.enums import *
from fp_i10_indicator.constants import *

def frame(enabled=True): return project_buffers(health=HealthState.READY,lifecycle=LifecycleState.READY,data_readiness=DataReadiness.READY,active_ww_direction=ActiveWWDirection.BULLISH,confirmed_signal_count=7,allowed_signal_count=3,suppressed_by_ww_count=2,suppressed_by_quota_count=2,quota_winner_signal_id='S',ledger_event_count=22,source_revision_sequence=5,generated_utc_ms=60000,enabled=enabled)
def test_exact_buffer_count(): assert len(frame().values)==BUFFER_COUNT
def test_mapping_names(): assert tuple(n for _,n in buffer_mapping())==BUFFER_NAMES
def test_values_semantics():
 f=frame(); assert f.values[0]==2.0 and f.values[3]==1.0 and f.values[8]==1.0 and f.values[9]==22.0
def test_disabled_still_deterministic(): assert frame(False).available is False and len(frame(False).values)==BUFFER_COUNT
def test_frame_hash_changes(): assert frame(True).frame_hash!=frame(False).frame_hash

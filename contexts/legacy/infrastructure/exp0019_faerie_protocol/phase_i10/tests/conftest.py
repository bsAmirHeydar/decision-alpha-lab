import sys
from pathlib import Path
import pytest
PH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PH/'python'))
from fp_i10_indicator import *
from fp_i10_indicator.canonical import canonical_sha256
from fp_i10_indicator.enums import ModuleStatus

NOW=1783900800000
@pytest.fixture
def config(): return build_config(context_epoch='FP-EPOCH-1',primary_symbol='ES',secondary_symbol='NQ',host_timeframe_minutes=5,history_days=5,max_incremental_minutes=10080)
@pytest.fixture
def modules(): return tuple(UpstreamModuleDescriptor(p,v,canonical_sha256({'phase':p,'version':v}),'NONE',ModuleStatus.READY,()) for p,v in EXPECTED_UPSTREAM)
@pytest.fixture
def ready_state(): return {'data_readiness':DataReadiness.READY,'history_ready':True,'source_revision_id':'REV-1','source_revision_sequence':1,'active_ww_direction':ActiveWWDirection.BULLISH,'confirmed_signal_count':7,'allowed_signal_count':3,'suppressed_by_ww_count':2,'suppressed_by_quota_count':2,'quota_winner_signal_id':'FPSIG-WINNER','ledger_event_count':22}
@pytest.fixture
def engine(config,modules,ready_state):
 e=IndicatorEngine(); e.initialize(config=config,chart_id=101,terminal_instance_id='TERM-A',modules=modules,now_m1=NOW); e.timer(now_m1=NOW,upstream_state=ready_state); return e

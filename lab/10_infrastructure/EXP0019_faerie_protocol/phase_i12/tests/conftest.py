import sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'python'
sys.path.insert(0,str(P))
import pytest
from fp_i12_operator import *
@pytest.fixture
def items():
 def it(i,kind='CONFIRMED_SIGNAL',relation='AL',direction='BULLISH',state='CONFIRMED',disposition='QUOTA_WINNER',session='N',symbol='ES',time=100,historical=False):
  return OperatorItem(f'SIG-{i}',f'OBJ-{i}',kind,relation,direction,state,disposition,session,symbol,time,historical,(),sha256({'i':i}))
 return (it(1),it(2,relation='WW',direction='BEARISH',disposition='SUPPRESSED_BY_WW',symbol='NQ',time=110),it(3,relation='LN',state='INVALIDATED',disposition='BLOCKED',session='L',time=90,historical=True),it(4,kind='WW_CONTEXT',relation='WW',direction='BULLISH',disposition='OBSERVED',session='W',time=120))
@pytest.fixture
def config():
 return OperatorConfig('INSTANCE-1','FP19::INSTANCE-1::',PanelConfig(),FilterConfig(),AlertConfig(channels=(AlertChannel.LOG,),startup_watermark=50),ExportConfig(enabled=True),open_decision_state='UNSET')
@pytest.fixture
def snapshot(items):
 s=OperatorSnapshot('SNAP-1',130,'REV-1',OperatorHealth.READY,'READY','BULLISH','SIG-1',42,7,items,'UNSET','')
 return s

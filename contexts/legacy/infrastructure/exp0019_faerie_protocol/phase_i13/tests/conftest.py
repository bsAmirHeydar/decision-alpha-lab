from tools.repository_paths import find_repository_root
from pathlib import Path
import sys,hashlib,pytest
ROOT=find_repository_root(__file__)
for phase,pkg in [('phase_i13','fp_i13_release'),('phase_i12','fp_i12_operator'),('phase_i11','fp_i11_visual'),('phase_i10','fp_i10_indicator')]:
    p=ROOT/'contexts/legacy/infrastructure/exp0019_faerie_protocol'/phase/'python'
    if p.exists():sys.path.insert(0,str(p))
from fp_i13_release import *

def h(x):return hashlib.sha256(str(x).encode()).hexdigest()
@pytest.fixture
def config_hash():return h('fp-i13-config')
@pytest.fixture
def instance(config_hash):return build_instance_identity(101,'/terminal/a','PAIR-ES-NQ','FP-EPOCH-1',config_hash)
@pytest.fixture
def fixture(config_hash):
    events=[];seq=1
    for day in range(4):
      for rel in ('AL','AN','LN','NA','NL','NN','WW'):
        sid=f'SIG-{day}-{rel}'
        events.append(ReplayEvent(seq,1_700_000_000+seq,ReplayEventType.SEMANTIC_UPSERT,sid,h((sid,'semantic')),'REV-1',rel,False,()));seq+=1
        events.append(ReplayEvent(seq,1_700_000_000+seq,ReplayEventType.VISUAL_FACT,sid,h((sid,'visual')),'REV-1','CONFIRMED',False,()));seq+=1
        events.append(ReplayEvent(seq,1_700_000_000+seq,ReplayEventType.ALERT_FACT,sid,h((sid,'alert')),'REV-1','SIGNAL_CONFIRMED',day<2,()));seq+=1
        events.append(ReplayEvent(seq,1_700_000_000+seq,ReplayEventType.EXPORT_FACT,sid,h((sid,'export')),'REV-1','AUDIT',False,()));seq+=1
    events.append(ReplayEvent(seq,1_700_100_000,ReplayEventType.HEALTH_FACT,'HEALTH-1',h('ready'),'REV-1','READY',False,()))
    return ReplayFixture('FIXTURE-I13-GOLDEN',config_hash,5,tuple(events),'REV-1','four-day relation and WW replay')

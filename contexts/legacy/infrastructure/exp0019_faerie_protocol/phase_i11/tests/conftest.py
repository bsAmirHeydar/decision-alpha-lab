import sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'python';sys.path.insert(0,str(P))
import pytest
from fp_i11_visual import *
def h(x): return canonical_sha256(x)
@pytest.fixture
def cfg(): return ProjectionConfig('INST-1','FP19::INST-1::',VisualMode.STANDARD,30,500)
@pytest.fixture
def layout(): return LayoutContext(90,110,1000,.25,6)
@pytest.fixture
def snapshot():
 return VisualSnapshot('SNAP-1','REV-1',1_000_000,
  windows=(WindowFact('WIN-A','A',100_000,200_000,105,95,SemanticState.COMPLETE,h('wa')),WindowFact('WIN-N','N',200_000,300_000,108,96,SemanticState.ACTIVE,h('wn'))),
  references=(ReferenceFact('REF-H','ES','HIGH',105,200_000,500_000,SemanticState.FRESH,h('rh')),ReferenceFact('REF-L','NQ','LOW',95,200_000,500_000,SemanticState.HUNTER_SEEN,h('rl'))),
  hunts=(HuntFact('HUNT-1','ES','HIGH',300_000,105,'HUNTER',h('h1')),HuntFact('HUNT-2','NQ','LOW',360_000,95,'PROTECTED',h('h2'))),
  signals=(SignalFact('SIG-1','AL','BEARISH','ES','NQ',300_000,420_000,105,95,SemanticState.CONFIRMED,SignalDisposition.QUOTA_WINNER,h('s1')),SignalFact('SIG-2','AN','BULLISH','NQ','ES',360_000,480_000,95,105,SemanticState.CONFIRMED,SignalDisposition.SUPPRESSED_BY_WW,h('s2'),('FP_WW_DIRECTION_MISMATCH',))),
  ww_contexts=(WWFact('WW-1','BEARISH',0,604_800_000,SemanticState.CONFIRMED,'ES','NQ',h('ww')),),
  health=HealthFact('HLTH-1','READY','FP READY',1_000_000,h('health')))

from __future__ import annotations
from fp_i03_time.contracts import TimeKernelConfig
from .contracts import M1Bar,SymbolPairSpec,SymbolSpec,SynchronizerConfig
from .enums import BarFinality,ExpectedMinutePolicy

def golden_pair():
    return SymbolPairSpec('FP-CONTEXT-001','FP-PAIR-ES-NQ',SymbolSpec('ES',('ES','US500'),0.25,2),SymbolSpec('NQ',('NQ','USTEC'),0.25,2))
def golden_config():
    tc=TimeKernelConfig();return SynchronizerConfig(pair_id='FP-PAIR-ES-NQ',expected_minute_policy=ExpectedMinutePolicy.ALL_REQUESTED_MINUTES,calendar_config_hash=tc.config_hash)
def bar(symbol,minute,price,sequence=0,revision='R1',received_offset=60_000,finality=BarFinality.CLOSED):
    return M1Bar(symbol,minute,price,price+0.5,price-0.5,price+0.25,10,0,1,finality,'GOLDEN',sequence,revision,minute+received_offset)
def golden_bars(start,minutes=5):
    out=[]
    for i in range(minutes):
        minute=start+i*60_000;out += [bar('ES',minute,5000+i,2*i),bar('NQ',minute,20000+i,2*i+1)]
    return tuple(out)

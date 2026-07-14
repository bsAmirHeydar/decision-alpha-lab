from pathlib import Path
import sys,hashlib,pytest
PH=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PH/'python'))
from fp_i14_diagnostic import *

def h(x): return hashlib.sha256(str(x).encode()).hexdigest()
@pytest.fixture
def config_hash(): return h('fp-i14-config')
@pytest.fixture
def facts():
    types=[TraceEventType.CONFIG,TraceEventType.TIME,TraceEventType.DATA,TraceEventType.WINDOW,TraceEventType.REFERENCE,TraceEventType.HUNT,TraceEventType.CANDIDATE,TraceEventType.CONFIRMATION,TraceEventType.SIGNAL,TraceEventType.WW_CONTEXT,TraceEventType.DIRECTION_GATE,TraceEventType.LEDGER,TraceEventType.QUOTA,TraceEventType.BUFFER,TraceEventType.VISUAL,TraceEventType.ALERT,TraceEventType.EXPORT,TraceEventType.HEALTH]
    out=[]
    for i,t in enumerate(types,1):
        state='QUOTA_WINNER' if t==TraceEventType.QUOTA else ('READY' if t==TraceEventType.HEALTH else 'CONFIRMED')
        out.append(SemanticFact(i,1_700_000_000_000+i*60_000,t,f'SEM-{i}',{'i':i,'type':t.value},state,'WW' if t==TraceEventType.WW_CONTEXT else 'AL','BULLISH','NYDAY:N',0 if t==TraceEventType.BUFFER else -1,float(i),()))
    return tuple(out)
@pytest.fixture
def manifests(config_hash): return {p:build_manifest(p,config_hash) for p in ProductKind}
@pytest.fixture
def runs(manifests,facts): return {p:build_run(manifests[p],'FIX-I14',adapt_facts(p,manifests[p],facts)) for p in ProductKind}

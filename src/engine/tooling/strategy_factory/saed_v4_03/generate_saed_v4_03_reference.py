from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__)
sys.path.insert(0,str(ROOT/'src/engine/packages'))
from saed_v4_event_model.conformance import manifest,event,projection
from saed_v4_event_model.models import EventBatch
from saed_v4_event_model.canonical import content_hash
from saed_v4_event_model.service import ContinuousTimeEventService
from saed_v4_event_model.integrity import build_integrity_receipt
from saed_v4_event_model.handoff import build_v4_04_handoff
EX=ROOT/'examples/legacy/strategy_factory/saed_v4_03'
OUT=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_03'
OUT.mkdir(parents=True,exist_ok=True)
s=ContinuousTimeEventService();ms=[]
for name in ['golden_stream_nq.json','golden_stream_es.json']:
    m=manifest(json.loads((EX/name).read_text()));s.register_stream(m);ms.append(m)
for m,name in zip(ms,['golden_events_nq.json','golden_events_es.json']):
    evs=tuple(event(x) for x in json.loads((EX/name).read_text()))
    s.append(EventBatch(name,m.stream_id,m.exact_version,evs,content_hash([x.envelope_hash for x in evs])))
d=projection(json.loads((EX/'golden_projection_definition.json').read_text()))
s.register_projection(d)
p=s.project(d.projection_name,d.exact_version,'2026-01-02T14:31:00Z','2026-01-02T14:30:03Z')
r=build_integrity_receipt(d.twin_id,s.journal.journal_root(),s.streams.all(),s.watermarks.all_states(),p)
h=build_v4_04_handoff('c'*64,ms,p,r,['fixture only','V4-04 not implemented','MetaEditor compile pending'])
def conv(x):
    if hasattr(x,'value'):return x.value
    if hasattr(x,'__dict__'):return {k:conv(v) for k,v in x.__dict__.items()}
    if isinstance(x,tuple):return [conv(v) for v in x]
    if isinstance(x,dict):return {k:conv(v) for k,v in x.items()}
    return x
for name,obj in [('GOLDEN_EVENT_PROJECTION.json',p),('EVENT_INTEGRITY_RECEIPT.json',r),('V4_03_TO_V4_04_HANDOFF.json',h)]:
    (OUT/name).write_text(json.dumps(conv(obj),indent=2,sort_keys=True)+'\n')
print(p.state_hash)

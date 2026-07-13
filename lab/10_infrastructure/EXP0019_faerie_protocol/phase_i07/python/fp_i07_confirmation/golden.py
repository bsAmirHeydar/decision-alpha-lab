from __future__ import annotations
from fp_i02_kernel.enums import RelationCode,PriceSide,Direction
from fp_i06_relations.contracts import RawDivergenceCandidate
from fp_i06_relations.enums import CandidateState
from .canonical import canonical_sha256,stable_id
from .contracts import ConfirmationConfig,HostBar
from .enums import HostTimeframe,ClosePairState
from .timeframe import timeframe_seconds
from .projection import project_candidate
from .engine import admit_candidate,finalize
from .observation import observe_close

def candidate(first=1_700_000_000_000,deadline=None):
    first=first-first%60_000;deadline=deadline or first+3_600_000
    material={"relation":"AL","side":"HIGH","hunter":"ES","protected":"NQ","hunt":first,"deadline":deadline}
    return RawDivergenceCandidate(stable_id("FPCAND",material,32),"FPSIDE-AL-HIGH","FPREL-AL",RelationCode.AL,Direction.BEARISH,PriceSide.HIGH,"ES","NQ",first,"FPHUNT-ES",CandidateState.RAW_ACTIVE,0,None,"",deadline,"REV-1","FP_HRC_RAW_CANDIDATE_CREATED",canonical_sha256(material))
def config(tf=HostTimeframe.M5): return ConfirmationConfig("FP-CONTEXT-001","PAIR-ES-NQ","ES",tf,timeframe_seconds(tf))
def host_bar(c,tf=HostTimeframe.M5,close_offset=300_000,coverage=True,closed=True):
    close=c.first_hunt_minute_utc_ms-c.first_hunt_minute_utc_ms%close_offset+close_offset
    if close<=c.first_hunt_minute_utc_ms:close+=close_offset
    op=close-close_offset
    material={"symbol":"ES","tf":tf,"open":op,"close":close,"coverage":coverage}
    return HostBar(stable_id("FPBAR",material,24),"ES",tf,op,close,100,102,99,101,closed,close,coverage,canonical_sha256([op,close]),"REV-1",canonical_sha256(material))
def golden_case(state=ClosePairState.HUNTER_ONLY,tf=HostTimeframe.M5):
    c=candidate();cfg=config(tf);bar=host_bar(c,tf,timeframe_seconds(tf)*1000);proj=project_candidate(c,(bar,),cfg);pending,admit=admit_candidate(c,proj,"REV-1",c.first_hunt_minute_utc_ms);obs=observe_close(c,bar,state,bar.close_utc_ms,"REV-1");result,event=finalize(pending,bar,obs,cfg);return c,cfg,bar,proj,pending,obs,result,(admit,event)

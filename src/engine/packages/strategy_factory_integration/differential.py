from __future__ import annotations
from .enums import DifferentialStatus
from .hashing import canonical_hash, stable_id
from .models import CanonicalAnatomyEvent, DifferentialRecord, DifferentialReport, LegacyDivergenceCandidate
from .mapper import map_candidate
from .models import AdapterConfig

def compare(case_id: str, legacy: tuple[LegacyDivergenceCandidate,...], canonical: tuple[CanonicalAnatomyEvent,...], config: AdapterConfig, known_time_ms: int) -> DifferentialReport:
    expected={map_candidate(c,config,known_time_ms)[0].event_id:(c,map_candidate(c,config,known_time_ms)[0]) for c in legacy}
    actual={e.event_id:e for e in canonical}
    records=[]; matched=missing=extra=mismatch=0
    for event_id,(candidate,expected_event) in expected.items():
        actual_event=actual.get(event_id)
        if actual_event is None:
            status=DifferentialStatus.MISSING_CANONICAL; fields=("event_id",); missing+=1; ch=""
        else:
            fields=tuple(name for name in ("symbol","reference_symbol","direction","reference_price","invalidation_price","timeframe_seconds","market_event_cluster_id","source_hash") if getattr(actual_event,name)!=getattr(expected_event,name))
            if fields: status=DifferentialStatus.FIELD_MISMATCH; mismatch+=1
            else: status=DifferentialStatus.MATCH; matched+=1
            ch=canonical_hash(actual_event,"sf20cp")
        records.append(DifferentialRecord(stable_id("sf20diff",f"{case_id}|{candidate.divergence_id}|{event_id}|{status.value}"),candidate.divergence_id,event_id,status,fields,candidate.payload_hash,ch,known_time_ms))
    for event_id,event in actual.items():
        if event_id in expected: continue
        extra+=1
        records.append(DifferentialRecord(stable_id("sf20diff",f"{case_id}|extra|{event_id}"),"",event_id,DifferentialStatus.EXTRA_CANONICAL,("event_id",),"",canonical_hash(event,"sf20cp"),known_time_ms))
    passed=missing==0 and extra==0 and mismatch==0 and matched==len(legacy)
    rid=canonical_hash({"case_id":case_id,"records":records,"passed":passed},"sf20report")
    return DifferentialReport(rid,case_id,len(legacy),len(canonical),matched,missing,extra,mismatch,tuple(records),passed)

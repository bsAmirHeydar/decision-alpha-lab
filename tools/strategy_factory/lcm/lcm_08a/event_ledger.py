from __future__ import annotations
from .canonical import content_id, digest_object


def build(portfolio_id: str, source_handoff_digest: str, issued_at: str):
    event_types=["UPSTREAM_BOUND","PORTFOLIO_RECONSTRUCTED","RISK_ASSESSED","DEPENDENCIES_BOUND","WAVES_ASSIGNED","PILOT_EVALUATED","PILOT_SELECTED","HOSTILE_REVIEW_COMPLETED","HANDOFF_ISSUED"]
    events=[]; previous=None
    for index,event_type in enumerate(event_types,1):
        event={"event_id":content_id("LCM08AEVT",[portfolio_id,index,event_type]),"sequence":index,"event_type":event_type,"portfolio_id":portfolio_id,"issued_at":issued_at,"previous_event_digest":previous,"source_handoff_digest":source_handoff_digest,"event_digest":None}
        event["event_digest"]=digest_object(event,"event_digest");previous=event["event_digest"];events.append(event)
    ledger={"schema_version":"1.0.0","ledger_id":content_id("LCM08ALEDGER",portfolio_id),"events":events,"head_digest":previous,"ledger_digest":None}
    ledger["ledger_digest"]=digest_object(ledger,"ledger_digest")
    return ledger

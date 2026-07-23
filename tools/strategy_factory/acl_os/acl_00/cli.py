from __future__ import annotations
import argparse,json
from datetime import datetime,timezone
from pathlib import Path
from .audit import AuditLedger
from .io import load_bundle
from .service import ACL00ControlPlane

def main()->int:
    ap=argparse.ArgumentParser(prog="acl00",description="ACL-00 unified authority control plane")
    sub=ap.add_subparsers(dest="command",required=True)
    ev=sub.add_parser("evaluate"); ev.add_argument("bundle",type=Path); ev.add_argument("--commit",action="store_true"); ev.add_argument("--ledger",type=Path); ev.add_argument("--as-of",dest="as_of")
    vr=sub.add_parser("verify-ledger"); vr.add_argument("ledger",type=Path)
    ns=ap.parse_args()
    if ns.command=="verify-ledger":
        ledger=AuditLedger(ns.ledger); print(json.dumps({"passed":ledger.verify(),"events":len(ledger.events),"head":ledger.head},indent=2,sort_keys=True)); return 0
    as_of=datetime.fromisoformat(ns.as_of.replace("Z","+00:00")) if ns.as_of else datetime.now(timezone.utc)
    ledger=AuditLedger(ns.ledger) if ns.ledger else AuditLedger(); cp=ACL00ControlPlane(audit_ledger=ledger); decision=cp.evaluate(load_bundle(ns.bundle),as_of,commit=ns.commit); print(json.dumps(decision.to_dict(),indent=2,sort_keys=True)); return 0 if decision.decision.value=="ALLOW" else 2
if __name__=="__main__": raise SystemExit(main())

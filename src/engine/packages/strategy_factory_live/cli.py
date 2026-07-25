from __future__ import annotations
import argparse, json
from dataclasses import asdict
from pathlib import Path
from .examples import reference_bundle
from .broker import DeterministicDryRunBroker
from .coordinator import LiveExecutionCoordinator
from .enums import LiveMode

def main() -> int:
    parser=argparse.ArgumentParser(description="Strategy Factory Phase 18 live-safety conformance utilities")
    parser.add_argument("--reference-preflight",action="store_true")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    if args.reference_preflight:
        release,auth,policy,intent,account,quote=reference_bundle()
        engine=LiveExecutionCoordinator("sf18-reference",LiveMode.DRY_RUN,release,auth,policy,DeterministicDryRunBroker())
        result=engine.submit(intent,account,quote,quote.time_utc_msc)
        payload={"decision":int(result.decision),"reason":int(result.reject_reason),"request_id":result.request_id,
                 "ledger_valid":engine.ledger.validate_chain(),"report":asdict(engine.report(quote.time_utc_msc+1))}
        text=json.dumps(payload,indent=2,default=int,sort_keys=True)
        if args.output: args.output.write_text(text+"\n",encoding="utf-8")
        else: print(text)
    return 0

if __name__=="__main__": raise SystemExit(main())

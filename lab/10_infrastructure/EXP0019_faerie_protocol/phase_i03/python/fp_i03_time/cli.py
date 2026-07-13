from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from fp_i02_kernel.canonical import canonical_value
from .calendar import snapshot
from .conformance import run_conformance
from .golden import golden_vector_material
from .time_math import epoch_ms


def main(argv=None) -> int:
    parser=argparse.ArgumentParser(prog="fp-i03")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("conformance")
    sub.add_parser("vectors")
    snap=sub.add_parser("snapshot");snap.add_argument("utc_iso")
    args=parser.parse_args(argv)
    if args.command=="conformance":payload=run_conformance()
    elif args.command=="vectors":payload=golden_vector_material()
    else:
        dt=datetime.fromisoformat(args.utc_iso.replace("Z","+00:00"))
        payload=snapshot(epoch_ms(dt.astimezone(timezone.utc)))
    print(json.dumps(canonical_value(payload),indent=2,sort_keys=True))
    return 0 if args.command!="conformance" or payload["passed"] else 1

if __name__=="__main__":raise SystemExit(main())

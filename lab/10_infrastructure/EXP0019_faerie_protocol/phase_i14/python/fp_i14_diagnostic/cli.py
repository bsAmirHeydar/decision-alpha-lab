from __future__ import annotations
import argparse,json
from pathlib import Path
from .canonical import primitive

def main(argv=None):
    ap=argparse.ArgumentParser(description='FP-I14 diagnostic trace utility')
    ap.add_argument('trace',type=Path);args=ap.parse_args(argv)
    lines=[json.loads(x) for x in args.trace.read_text(encoding='utf-8').splitlines() if x.strip()]
    print(json.dumps({'records':len(lines),'path':str(args.trace)},indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())

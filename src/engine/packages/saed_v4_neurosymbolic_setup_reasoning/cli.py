from __future__ import annotations
import argparse,json
from pathlib import Path

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-19');p.add_argument('--root',default='.');p.add_argument('--summary',action='store_true');a=p.parse_args(argv)
    root=Path(a.root);status=json.loads((root/'releases/history/strategy_factory/program/status/SAED_V4_19.json').read_text(encoding='utf-8'))
    print(json.dumps(status if a.summary else {'phase':status['phase'],'status':status['implementation_status'],'next_phase':status['next_phase']},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())

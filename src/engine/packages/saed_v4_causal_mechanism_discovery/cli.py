from __future__ import annotations
from tools.repository_paths import find_repository_root
import argparse,json
from pathlib import Path

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-17');sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('status');sub.add_parser('authority');sub.add_parser('handoff')
    args=p.parse_args(argv);root=find_repository_root(__file__)
    mapping={'status':'releases/history/strategy_factory/program/status/SAED_V4_17.json','authority':'releases/history/strategy_factory/artifacts/saed_v4_17/AUTHORITY_BOUNDARY.JSON','handoff':'releases/history/strategy_factory/artifacts/saed_v4_17/V4_17_TO_V4_18_HANDOFF.JSON'}
    print(json.dumps(json.loads((root/mapping[args.command]).read_text(encoding='utf-8')),indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())

from __future__ import annotations
import argparse,json
from pathlib import Path

def main(argv=None):
    p=argparse.ArgumentParser(prog='saed-v4-18');p.add_argument('--artifact-root',default='lab/11_strategy_factory/artifacts/saed_v4_18');p.add_argument('--summary',action='store_true');a=p.parse_args(argv)
    root=Path(a.artifact_root);status=json.loads((root/'GOLDEN_CLAIM_TIER_REPORT.JSON').read_text(encoding='utf-8'));tour=json.loads((root/'GOLDEN_POLICY_TOURNAMENT.JSON').read_text(encoding='utf-8'));handoff=json.loads((root/'V4_18_TO_V4_19_HANDOFF.JSON').read_text(encoding='utf-8'))
    print(json.dumps({'phase':'SAED_V4_18','claim_tier':status['claim_tier'],'reference_policy_id':tour['reference_champion_id'],'next_phase':handoff['next_phase'],'production_authority':False},indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())

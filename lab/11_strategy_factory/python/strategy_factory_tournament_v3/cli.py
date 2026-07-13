from __future__ import annotations
import argparse,json
from dataclasses import asdict
from .golden import golden_run
from .canonical import canonical_json
from .registry import capability_manifest

def main(argv=None):
 p=argparse.ArgumentParser(prog='strategy-factory-tournament-v3');p.add_argument('command',choices=('golden','capabilities'));p.add_argument('--pretty',action='store_true');ns=p.parse_args(argv)
 if ns.command=='capabilities':data=capability_manifest()
 else:
  inv,contexts,occ,t,a,freeze,report,plan,paper,decision=golden_run();data={'inventory':asdict(inv),'freeze_hash':freeze.freeze_hash,'report_hash':report.report_hash,'paper_report_hash':paper.report_hash,'decision':asdict(decision)}
 print(json.dumps(data,indent=2,sort_keys=True) if ns.pretty else canonical_json(data));return 0
if __name__=='__main__':raise SystemExit(main())

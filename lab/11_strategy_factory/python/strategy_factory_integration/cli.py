from __future__ import annotations
import argparse, json
from dataclasses import asdict
from pathlib import Path
from .differential import compare
from .fixtures import reference_candidates, reference_config
from .manifest import build_manifest, default_migration_waves
from .mapper import map_candidate

def main(argv=None)->int:
    p=argparse.ArgumentParser(prog="strategy-factory-integration")
    p.add_argument("command",choices=("golden","manifest","waves"))
    p.add_argument("--output",type=Path)
    ns=p.parse_args(argv)
    cfg=reference_config(); now=1783795000000
    if ns.command=="golden":
        events=tuple(map_candidate(c,cfg,now)[0] for c in reference_candidates())
        payload={"events":[asdict(e) for e in events],"differential":asdict(compare("reference",reference_candidates(),events,cfg,now))}
    elif ns.command=="manifest": payload=asdict(build_manifest(cfg,"sf20-reference-run","generation-reference","legacy_source_reference",now))
    else: payload={"waves":[asdict(x) for x in default_migration_waves()]}
    text=json.dumps(payload,indent=2,default=lambda x:getattr(x,"value",str(x)))+"\n"
    if ns.output: ns.output.write_text(text,encoding="utf-8")
    else: print(text,end="")
    return 0
if __name__=="__main__": raise SystemExit(main())

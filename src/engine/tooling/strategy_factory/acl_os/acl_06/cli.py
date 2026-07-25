from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_json
from .replay import verify_research_run
from .service import ACL06ResearchOrchestrationService
from .task_registry import registry_snapshot

def main(argv=None)->int:
    p=argparse.ArgumentParser(description='ACL-06 deterministic research DAG orchestrator'); sub=p.add_subparsers(dest='command',required=True)
    r=sub.add_parser('run-reference'); r.add_argument('--acl05-root',type=Path,required=True); r.add_argument('--fixture-root',type=Path,required=True); r.add_argument('--output-root',type=Path,required=True)
    v=sub.add_parser('verify'); v.add_argument('--run-root',type=Path,required=True); a=p.parse_args(argv)
    if a.command=='verify':
        x=verify_research_run(a.run_root); print(json.dumps(x,indent=2,sort_keys=True)); return 0 if x['passed'] else 2
    x=ACL06ResearchOrchestrationService().run(acl05_root=a.acl05_root,output_root=a.output_root,authority_permit=load_json(a.fixture_root/'authority_permit.json'),run_request=load_json(a.fixture_root/'research_run_request.json'),task_registry=registry_snapshot())
    print(json.dumps({k:v for k,v in x.items() if k not in {'dag','research_run','result_bundle','receipts','accounting','object_index','events','provenance','handoff','output_manifest','receipt'}},indent=2,sort_keys=True)); return 0
if __name__=='__main__': raise SystemExit(main())

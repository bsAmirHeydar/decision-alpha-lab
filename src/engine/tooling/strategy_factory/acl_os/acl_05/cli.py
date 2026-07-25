from __future__ import annotations
import argparse, json
from pathlib import Path
from .io import load_json
from .replay import verify_frozen_batch
from .service import ACL05ImmutableBatchService

def main(argv=None) -> int:
    p=argparse.ArgumentParser(description="ACL-05 immutable batch compiler")
    sub=p.add_subparsers(dest="command",required=True)
    b=sub.add_parser("build-reference"); b.add_argument("--acl04-root",type=Path,required=True); b.add_argument("--fixture-root",type=Path,required=True); b.add_argument("--output-root",type=Path,required=True)
    v=sub.add_parser("verify"); v.add_argument("--batch-root",type=Path,required=True)
    args=p.parse_args(argv)
    if args.command=="verify":
        result=verify_frozen_batch(args.batch_root); print(json.dumps(result,indent=2,sort_keys=True)); return 0 if result["passed"] else 2
    f=args.fixture_root
    svc=ACL05ImmutableBatchService(); result=svc.build(acl04_root=args.acl04_root,output_root=args.output_root,fixture_root=f,authority_permit=load_json(f/"authority_permit.json"),batch_request=load_json(f/"batch_request.json"),dataset_documents=[load_json(f/"dataset_snapshot.json")],label_documents=[load_json(f/"label_forward_direction.json"),load_json(f/"label_path_diagnostic.json")],split_contract=load_json(f/"split_contract.json"),environment_lock=load_json(f/"environment_lock.json"),compute_budget=load_json(f/"compute_budget.json"))
    print(json.dumps({k:v for k,v in result.items() if k not in {"batch","candidate_freeze","search_freeze","dataset_set","label_set","split","environment","budget","object_index","event_ledger","provenance","batch_manifest","freeze_receipt","handoff","output_manifest","receipt"}},indent=2,sort_keys=True)); return 0

if __name__=="__main__": raise SystemExit(main())

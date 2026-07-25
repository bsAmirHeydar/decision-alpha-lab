from __future__ import annotations
import argparse,json
from pathlib import Path
from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schemas
from .service import LCM12ADocumentationAuthorityService
from .static_validation import validate_module
from .verify import verify_package

def main(argv=None):
    parser=argparse.ArgumentParser();sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("build");p.add_argument("--repo-root",default=".");p.add_argument("--upstream-handoff",required=True);p.add_argument("--output-parent",required=True)
    p=sub.add_parser("verify-package");p.add_argument("--mapping-root",required=True)
    p=sub.add_parser("verify-patch");p.add_argument("--repo-root",default=".");p.add_argument("--hash-ledger",required=True)
    p=sub.add_parser("validate-schemas");p.add_argument("--schema-root",required=True)
    p=sub.add_parser("static-validate");p.add_argument("--module-root",required=True)
    p=sub.add_parser("qa");p.add_argument("--mapping-root",required=True);p.add_argument("--schema-root",required=True);p.add_argument("--module-root",required=True)
    p=sub.add_parser("verify-installation");p.add_argument("--repo-root",default=".");p.add_argument("--mapping-root",required=True);p.add_argument("--patch-index",required=True)
    args=parser.parse_args(argv);errors=[];result=None
    if args.command=="build":result=LCM12ADocumentationAuthorityService(Path(args.repo_root)).build(Path(args.upstream_handoff),Path(args.output_parent)).to_dict()
    elif args.command=="verify-package":errors=verify_package(Path(args.mapping_root))
    elif args.command=="verify-patch":errors=verify_hash_ledger(Path(args.repo_root),Path(args.hash_ledger))
    elif args.command=="validate-schemas":errors=validate_schemas(Path(args.schema_root))
    elif args.command=="static-validate":errors=validate_module(Path(args.module_root))
    elif args.command=="qa":errors=run_qa(Path(args.mapping_root),Path(args.schema_root),Path(args.module_root))
    elif args.command=="verify-installation":
        root=Path(args.repo_root);paths=[x.strip() for x in Path(args.patch_index).read_text(encoding="utf-8").splitlines() if x.strip()];errors=[f"MISSING:{p}" for p in paths if not (root/p).is_file()];errors.extend(verify_package(Path(args.mapping_root)))
    payload=result or {"passed":not errors,"errors":errors};print(json.dumps(payload,indent=2,sort_keys=True));return 0 if not errors else 1
if __name__=="__main__":raise SystemExit(main())

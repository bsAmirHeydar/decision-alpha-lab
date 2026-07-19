from __future__ import annotations
import argparse,json
from pathlib import Path
from .qa import run as run_qa
from .schema_validation import validate_schema_directory
from .static_validation import scan_module
from .verify import verify_installation,verify_package
def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("verify-package"); a.add_argument("--freeze-root",type=Path,required=True)
    a=s.add_parser("verify-installation"); a.add_argument("--repo-root",type=Path,required=True); a.add_argument("--freeze-root",type=Path,required=True); a.add_argument("--patch-index",type=Path,required=True)
    a=s.add_parser("qa"); a.add_argument("--repo-root",type=Path,required=True); a.add_argument("--freeze-root",type=Path,required=True)
    a=s.add_parser("validate-schemas"); a.add_argument("--schema-root",type=Path,required=True)
    a=s.add_parser("static-validate"); a.add_argument("--module-root",type=Path,required=True)
    args=p.parse_args()
    if args.cmd=="verify-package":out=verify_package(args.freeze_root)
    elif args.cmd=="verify-installation":out=verify_installation(args.repo_root,args.freeze_root,args.patch_index)
    elif args.cmd=="qa":out=run_qa(args.repo_root,args.freeze_root)
    elif args.cmd=="validate-schemas":out=validate_schema_directory(args.schema_root)
    else:out=scan_module(args.module_root)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__":main()

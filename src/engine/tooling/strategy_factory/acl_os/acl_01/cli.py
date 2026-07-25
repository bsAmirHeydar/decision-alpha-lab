from __future__ import annotations
import argparse,json
from pathlib import Path
from .io import load_registry
from .policies import PolicyBundle
from .service import ACL01RepositoryControlPlane
from ..common import REPO_ROOT


def parser():
    p=argparse.ArgumentParser(prog="acl01",description="ACL-01 repository identity and locator reference CLI")
    p.add_argument("--registry",type=Path,required=True); p.add_argument("--repo-root",type=Path,default=REPO_ROOT)
    sp=p.add_subparsers(dest="command",required=True)
    v=sp.add_parser("validate")
    r=sp.add_parser("resolve"); r.add_argument("ref"); r.add_argument("--version-constraint"); r.add_argument("--no-verify",action="store_true")
    sp.add_parser("scan"); sp.add_parser("snapshot")
    return p


def main(argv=None)->int:
    args=parser().parse_args(argv); policies=PolicyBundle.load(); reg=load_registry(args.registry,policies); cp=ACL01RepositoryControlPlane(args.repo_root,policies,reg)
    if args.command=="validate": out=cp.validate()
    elif args.command=="resolve": out=cp.resolve(args.ref,args.version_constraint,not args.no_verify).to_dict()
    elif args.command=="scan": out=cp.scan()
    else: out=reg.snapshot()|{"registry_digest":reg.digest}
    print(json.dumps(out,indent=2,sort_keys=True)); return 0 if out.get("passed",out.get("status") in {"RESOLVED",None}) else 1
if __name__=="__main__": raise SystemExit(main())

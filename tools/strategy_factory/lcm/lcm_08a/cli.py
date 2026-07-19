from __future__ import annotations
import argparse
import json
from pathlib import Path
from .qa import run as qa_run
from .schema_validation import validate as validate_schemas
from .service import RunConfig, run
from .verify import verify_installation, verify_package


def main(argv=None):
    parser=argparse.ArgumentParser(prog='python -m tools.strategy_factory.lcm.lcm_08a.cli')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('build');p.add_argument('--repo-root',required=True);p.add_argument('--destination',required=True);p.add_argument('--issued-at',default='2026-07-19T00:00:00Z')
    p=sub.add_parser('verify-package');p.add_argument('--portfolio-root',required=True)
    p=sub.add_parser('verify-installation');p.add_argument('--repo-root',required=True);p.add_argument('--portfolio-root',required=True);p.add_argument('--patch-index',required=True)
    p=sub.add_parser('qa');p.add_argument('--repo-root',required=True);p.add_argument('--portfolio-root',required=True)
    p=sub.add_parser('validate-schemas');p.add_argument('--schema-root',required=True)
    args=parser.parse_args(argv)
    if args.command=='build': result={'portfolio_root':str(run(RunConfig(Path(args.repo_root),Path(args.destination),args.issued_at)))}
    elif args.command=='verify-package': result=verify_package(Path(args.portfolio_root))
    elif args.command=='verify-installation': result=verify_installation(Path(args.repo_root),Path(args.portfolio_root),Path(args.patch_index))
    elif args.command=='qa': result=qa_run(Path(args.repo_root),Path(args.portfolio_root))
    else: result=validate_schemas(Path(args.schema_root))
    print(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2))
    if result.get('passed') is False or result.get('qa_passed') is False or result.get('installation_passed') is False:return 1
    return 0

if __name__=='__main__':raise SystemExit(main())

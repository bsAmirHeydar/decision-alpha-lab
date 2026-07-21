from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from .patch_verify import verify_hash_ledger
from .schema_validation import validate_schema_catalog
from .static_validation import validate_python
from .verify import ClosureVerifier
from .qa import run_qa

def main(argv=None):
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('verify-patch');q.add_argument('--repo-root',required=True);q.add_argument('--hash-ledger',required=True)
    q=sp.add_parser('validate-schemas');q.add_argument('--schema-root',required=True)
    q=sp.add_parser('static-validate');q.add_argument('--module-root',required=True)
    q=sp.add_parser('verify-package');q.add_argument('--closure-root',required=True)
    q=sp.add_parser('verify-installation');q.add_argument('--repo-root',required=True);q.add_argument('--closure-root',required=True);q.add_argument('--patch-index',required=True)
    q=sp.add_parser('qa');q.add_argument('--repo-root',required=True);q.add_argument('--closure-root',required=True);q.add_argument('--schema-root',required=True);q.add_argument('--module-root',required=True)
    a=p.parse_args(argv)
    if a.cmd=='verify-patch':r=verify_hash_ledger(Path(a.repo_root),Path(a.hash_ledger))
    elif a.cmd=='validate-schemas':r=validate_schema_catalog(Path(a.schema_root))
    elif a.cmd=='static-validate':r=validate_python(Path(a.module_root))
    elif a.cmd=='verify-package':r=ClosureVerifier().verify(Path(a.closure_root))
    elif a.cmd=='verify-installation':
        paths=[x.strip() for x in Path(a.patch_index).read_text(encoding='utf-8').splitlines() if x.strip()];missing=[x for x in paths if not (Path(a.repo_root)/x).is_file()];r={'result':'PASS' if not missing and ClosureVerifier().verify(Path(a.closure_root))['result']=='PASS' else 'FAIL','missing':missing}
    else:r=run_qa(Path(a.repo_root),Path(a.closure_root),Path(a.schema_root),Path(a.module_root))
    print(json.dumps(r,indent=2,sort_keys=True));return 0 if r['result']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

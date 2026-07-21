from __future__ import annotations
import argparse,json
from pathlib import Path
from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schema_catalog
from .service import LCM11AInventoryService
from .static_validation import validate_python
from .verify import VisualInventoryVerifier

def main(argv=None):
    p=argparse.ArgumentParser();sp=p.add_subparsers(dest='cmd',required=True)
    q=sp.add_parser('build');q.add_argument('--repo-root',required=True);q.add_argument('--output-parent',required=True);q.add_argument('--upstream-handoff',required=True)
    q=sp.add_parser('verify-patch');q.add_argument('--repo-root',required=True);q.add_argument('--hash-ledger',required=True)
    q=sp.add_parser('validate-schemas');q.add_argument('--schema-root',required=True)
    q=sp.add_parser('static-validate');q.add_argument('--module-root',required=True)
    q=sp.add_parser('verify-package');q.add_argument('--inventory-root',required=True)
    q=sp.add_parser('verify-installation');q.add_argument('--repo-root',required=True);q.add_argument('--inventory-root',required=True);q.add_argument('--patch-index',required=True)
    q=sp.add_parser('qa');q.add_argument('--repo-root',required=True);q.add_argument('--inventory-root',required=True);q.add_argument('--schema-root',required=True);q.add_argument('--module-root',required=True)
    a=p.parse_args(argv)
    if a.cmd=='build': r=LCM11AInventoryService(Path(a.repo_root),Path(a.output_parent),Path(a.upstream_handoff)).build(); r={'result':'PASS',**r}
    elif a.cmd=='verify-patch': r=verify_hash_ledger(Path(a.repo_root),Path(a.hash_ledger))
    elif a.cmd=='validate-schemas': r=validate_schema_catalog(Path(a.schema_root))
    elif a.cmd=='static-validate': r=validate_python(Path(a.module_root))
    elif a.cmd=='verify-package': r=VisualInventoryVerifier().verify(Path(a.inventory_root))
    elif a.cmd=='verify-installation':
        paths=[x.strip() for x in Path(a.patch_index).read_text(encoding='utf-8').splitlines() if x.strip()];missing=[x for x in paths if not (Path(a.repo_root)/x).is_file()];package=VisualInventoryVerifier().verify(Path(a.inventory_root));r={'result':'PASS' if not missing and package['result']=='PASS' else 'FAIL','missing':missing,'package':package}
    else:r=run_qa(Path(a.repo_root),Path(a.inventory_root),Path(a.schema_root),Path(a.module_root))
    print(json.dumps(r,indent=2,sort_keys=True));return 0 if r.get('result')=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())

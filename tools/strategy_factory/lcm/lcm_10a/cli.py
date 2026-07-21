from __future__ import annotations
import argparse, json
from pathlib import Path
from .patch_verify import verify_hash_ledger
from .qa import run as run_qa
from .schema_validation import validate_schema_directory
from .service import LCM10ATreatmentExecutionInventoryService
from .static_validation import scan_module
from .verify import verify_installation, verify_package

def main() -> None:
    p=argparse.ArgumentParser(prog='lcm10a');s=p.add_subparsers(dest='command',required=True)
    b=s.add_parser('build');b.add_argument('--repo-root',type=Path,required=True);b.add_argument('--output-root',type=Path,required=True)
    v=s.add_parser('verify-package');v.add_argument('--inventory-root',type=Path,required=True)
    i=s.add_parser('verify-installation');i.add_argument('--repo-root',type=Path,required=True);i.add_argument('--inventory-root',type=Path,required=True);i.add_argument('--patch-index',type=Path,required=True)
    q=s.add_parser('qa');q.add_argument('--repo-root',type=Path,required=True);q.add_argument('--inventory-root',type=Path,required=True)
    h=s.add_parser('verify-patch');h.add_argument('--repo-root',type=Path,required=True);h.add_argument('--hash-ledger',type=Path,required=True)
    sc=s.add_parser('validate-schemas');sc.add_argument('--schema-root',type=Path,required=True)
    st=s.add_parser('static-validate');st.add_argument('--module-root',type=Path,required=True)
    a=p.parse_args()
    if a.command=='build': out=LCM10ATreatmentExecutionInventoryService().build(a.repo_root,a.output_root)
    elif a.command=='verify-package': out=verify_package(a.inventory_root)
    elif a.command=='verify-installation': out=verify_installation(a.repo_root,a.inventory_root,a.patch_index)
    elif a.command=='qa': out=run_qa(a.repo_root,a.inventory_root)
    elif a.command=='verify-patch': out=verify_hash_ledger(a.repo_root,a.hash_ledger)
    elif a.command=='validate-schemas': out=validate_schema_directory(a.schema_root)
    else: out=scan_module(a.module_root)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()

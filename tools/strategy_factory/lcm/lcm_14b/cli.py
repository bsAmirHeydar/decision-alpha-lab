from __future__ import annotations
import argparse,sys
from pathlib import Path
from .patch_verify import verify_hash_ledger
from .qa import run_qa
from .schema_validation import validate_schema_directory
from .static_validation import static_validate
from .verify import verify_package
def main(argv=None):
 p=argparse.ArgumentParser(); s=p.add_subparsers(dest='command',required=True)
 x=s.add_parser('verify-patch');x.add_argument('--repo-root',required=True);x.add_argument('--hash-ledger',required=True)
 x=s.add_parser('validate-schemas');x.add_argument('--schema-root',required=True)
 x=s.add_parser('static-validate');x.add_argument('--module-root',required=True)
 x=s.add_parser('verify-package');x.add_argument('--quarantine-root',required=True)
 x=s.add_parser('verify-installation');x.add_argument('--repo-root',required=True);x.add_argument('--quarantine-root',required=True);x.add_argument('--patch-index',required=True)
 x=s.add_parser('qa');x.add_argument('--quarantine-root',required=True);x.add_argument('--schema-root',required=True);x.add_argument('--module-root',required=True)
 a=p.parse_args(argv)
 if a.command=='verify-patch': e=verify_hash_ledger(Path(a.repo_root),Path(a.hash_ledger))
 elif a.command=='validate-schemas': e=validate_schema_directory(Path(a.schema_root))
 elif a.command=='static-validate': e=static_validate(Path(a.module_root))
 elif a.command=='verify-package': e=verify_package(Path(a.quarantine_root))
 elif a.command=='verify-installation':
  e=verify_package(Path(a.quarantine_root)); idx=[z.strip() for z in Path(a.patch_index).read_text(encoding='utf-8-sig').splitlines() if z.strip()];e += ['INDEX_MISSING:'+z for z in idx if not (Path(a.repo_root)/z).is_file()]
 else:e=run_qa(Path(a.quarantine_root),Path(a.schema_root),Path(a.module_root))
 if e:print('\n'.join(e));return 1
 print('PASS');return 0
if __name__=='__main__':sys.exit(main())

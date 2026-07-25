from __future__ import annotations
import argparse,json
from pathlib import Path
from .service import LCM10BTreatmentBoundaryService
from .verify import verify_package
from .patch_verify import verify_patch
from .qa import run_qa
from .schema_validation import validate_schema_directory
from .static_validation import scan_module

def main(argv=None):
 p=argparse.ArgumentParser();s=p.add_subparsers(dest="command",required=True)
 b=s.add_parser("build");b.add_argument("--repo-root",default=".");b.add_argument("--output-root",required=True)
 v=s.add_parser("verify-package");v.add_argument("--package-root",required=True)
 q=s.add_parser("qa");q.add_argument("--repo-root",default=".");q.add_argument("--package-root",required=True);q.add_argument("--schema-root",required=True);q.add_argument("--module-root",required=True)
 vp=s.add_parser("verify-patch");vp.add_argument("--repo-root",default=".");vp.add_argument("--hash-ledger",required=True)
 vs=s.add_parser("validate-schemas");vs.add_argument("--schema-root",required=True)
 st=s.add_parser("static-validate");st.add_argument("--module-root",required=True)
 i=s.add_parser("verify-installation");i.add_argument("--repo-root",default=".");i.add_argument("--package-root",required=True);i.add_argument("--patch-index",required=True)
 a=p.parse_args(argv)
 if a.command=="build":r=LCM10BTreatmentBoundaryService().build(Path(a.repo_root),Path(a.output_root))
 elif a.command=="verify-package":r=verify_package(Path(a.package_root))
 elif a.command=="qa":r=run_qa(Path(a.repo_root),Path(a.package_root),Path(a.schema_root),Path(a.module_root))
 elif a.command=="verify-patch":r=verify_patch(Path(a.repo_root),Path(a.hash_ledger))
 elif a.command=="validate-schemas":r=validate_schema_directory(Path(a.schema_root))
 elif a.command=="static-validate":r=scan_module(Path(a.module_root))
 else:
  paths=[x.strip() for x in Path(a.patch_index).read_text(encoding="utf-8").splitlines() if x.strip()];missing=[x for x in paths if not (Path(a.repo_root)/x).is_file()];r={"passed":not missing,"path_count":len(paths),"missing":missing,"package":verify_package(Path(a.package_root))}
 print(json.dumps(r,indent=2,sort_keys=True));return 0 if r.get("passed") else 1
if __name__=="__main__":raise SystemExit(main())

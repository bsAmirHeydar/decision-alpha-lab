import argparse,json
from pathlib import Path
from .service import RunConfig,run
from .verify import verify_package
from .qa import run as qa_run

def main():
    p=argparse.ArgumentParser();s=p.add_subparsers(dest="command",required=True)
    b=s.add_parser("build");b.add_argument("--repo-root",required=True);b.add_argument("--destination",required=True)
    v=s.add_parser("verify-package");v.add_argument("--shared-engine-root",required=True)
    q=s.add_parser("qa");q.add_argument("--repo-root",required=True);q.add_argument("--shared-engine-root",required=True)
    i=s.add_parser("verify-installation");i.add_argument("--repo-root",required=True);i.add_argument("--shared-engine-root",required=True);i.add_argument("--patch-index",required=True)
    a=p.parse_args()
    if a.command=="build":r={"passed":True,"output":str(run(RunConfig(Path(a.repo_root),Path(a.destination))))}
    elif a.command=="verify-package":r=verify_package(Path(a.shared_engine_root))
    elif a.command=="qa":r=qa_run(Path(a.repo_root),Path(a.shared_engine_root))
    else:
        idx=[x.strip() for x in Path(a.patch_index).read_text(encoding="utf-8-sig").splitlines() if x.strip()];missing=[x for x in idx if not (Path(a.repo_root)/x).exists()];r={"passed":not missing,"indexed_path_count":len(idx),"missing":missing,"package":verify_package(Path(a.shared_engine_root))}
    print(json.dumps(r,indent=2,sort_keys=True));raise SystemExit(0 if r.get("passed") else 1)
if __name__=="__main__":main()

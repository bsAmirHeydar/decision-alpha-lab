import argparse, json
from pathlib import Path
from .service import RunConfig, run
from .verify import verify_package
from .qa import run as qa_run

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--repo-root", required=True)
    build.add_argument("--destination", required=True)
    verify = sub.add_parser("verify-package")
    verify.add_argument("--framework-root", required=True)
    qa = sub.add_parser("qa")
    qa.add_argument("--repo-root", required=True)
    qa.add_argument("--framework-root", required=True)
    install = sub.add_parser("verify-installation")
    install.add_argument("--repo-root", required=True)
    install.add_argument("--framework-root", required=True)
    install.add_argument("--patch-index", required=True)
    args = parser.parse_args()
    if args.command == "build":
        output = run(RunConfig(Path(args.repo_root), Path(args.destination)))
        result = {"passed": True, "output": str(output)}
    elif args.command == "verify-package":
        result = verify_package(Path(args.framework_root))
    elif args.command == "qa":
        result = qa_run(Path(args.repo_root), Path(args.framework_root))
    else:
        index = [x.strip() for x in Path(args.patch_index).read_text(encoding="utf-8-sig").splitlines() if x.strip()]
        missing = [x for x in index if not (Path(args.repo_root) / x).exists()]
        result = {"passed": not missing, "indexed_path_count": len(index), "missing": missing, "package": verify_package(Path(args.framework_root))}
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("passed") else 1)

if __name__ == "__main__":
    main()

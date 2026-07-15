from __future__ import annotations
import argparse
from .aggregation import build_summary
from .handoff import build_v4_10_handoff
from .integrity import build_integrity_receipt
from .serialization import write_json
from .service import build_from_files


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="saed-v4-execution-twin")
    sub = parser.add_subparsers(dest="command", required=True)
    build = sub.add_parser("build")
    build.add_argument("--cube", required=True); build.add_argument("--handoff", required=True); build.add_argument("--profile", required=True); build.add_argument("--output", required=True)
    build.add_argument("--receipt"); build.add_argument("--summary"); build.add_argument("--next-handoff")
    args = parser.parse_args(argv)
    twin = build_from_files(args.cube, args.handoff, args.profile); write_json(args.output, twin)
    if args.receipt: write_json(args.receipt, build_integrity_receipt(twin))
    if args.summary: write_json(args.summary, build_summary(twin))
    if args.next_handoff: write_json(args.next_handoff, build_v4_10_handoff(twin))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
from pathlib import Path

from tools.consolidation.uc04w1b.cutover_candidate import build_cutover_candidate
from tools.consolidation.uc04w1b.native_review import review_native_receipt
from tools.consolidation.uc04w1b.records import materialize_records
from tools.consolidation.uc04w1b.verify import verify
from tools.consolidation.uc04w1b.contracts import write_json


def main() -> int:
    parser = argparse.ArgumentParser(description="UC04-W1B native qualification tooling.")
    sub = parser.add_subparsers(dest="command", required=True)

    materialize = sub.add_parser("materialize-records")
    materialize.add_argument("--repo-root", default=".")

    check = sub.add_parser("verify")
    check.add_argument("--repo-root", default=".")

    review = sub.add_parser("review-native")
    review.add_argument("--repo-root", default=".")
    review.add_argument("--receipt", required=True)
    review.add_argument("--output", default="")

    candidate = sub.add_parser("build-cutover-candidate")
    candidate.add_argument("--repo-root", default=".")
    candidate.add_argument("--receipt", required=True)
    candidate.add_argument("--review", required=True)
    candidate.add_argument("--output-root", default="")

    args = parser.parse_args()
    if args.command == "materialize-records":
        materialize_records(Path(args.repo_root))
        return 0
    if args.command == "verify":
        errors = verify(Path(args.repo_root))
        if errors:
            for error in errors:
                print(error)
            return 1
        return 0
    if args.command == "review-native":
        receipt = Path(args.receipt)
        document = review_native_receipt(Path(args.repo_root), receipt)
        output = Path(args.output) if args.output else receipt.parent / "independent_native_review.json"
        write_json(output, document)
        return 0
    if args.command == "build-cutover-candidate":
        build_cutover_candidate(
            Path(args.repo_root),
            Path(args.receipt),
            Path(args.review),
            Path(args.output_root) if args.output_root else None,
        )
        return 0
    raise AssertionError(args.command)

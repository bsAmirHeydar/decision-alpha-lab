from __future__ import annotations

import argparse
import json
from pathlib import Path

from .config import load_activation_config
from .pipeline import RTHPTrainActivationPipeline, verify_run_root


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="rthp-train", description="Context-owned RTHP train activation over existing Strategy Factory engines.")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-config", help="Validate source and activation configuration without materializing or training.")
    validate.add_argument("--config", required=True)

    run = sub.add_parser("run", help="Materialize RTHP, freeze the batch, and train mature tasks with existing engines.")
    run.add_argument("--config", required=True)

    verify = sub.add_parser("verify-run", help="Verify an immutable RTHP run directory and its hash ledger.")
    verify.add_argument("--run-root", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "validate-config":
        config = load_activation_config(args.config)
        pipeline = RTHPTrainActivationPipeline(config)
        result = {
            "status": "PASS",
            "run_id": config.run_id,
            "config_digest": config.config_digest,
            "source_snapshot": pipeline.source_snapshot,
            "engine_modified": False,
            "canonical_context_modified": False,
        }
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0
    if args.command == "run":
        config = load_activation_config(args.config)
        result = RTHPTrainActivationPipeline(config).run()
        print(json.dumps(result, sort_keys=True, indent=2))
        return 0 if result["status"] in {"PASS", "PASS_WITH_SKIPS"} else 2
    result = verify_run_root(Path(args.run_root))
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

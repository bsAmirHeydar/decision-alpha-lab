#!/usr/bin/env python3
import argparse
import json
from strategy_factory_qualification_v3.conformance import run_conformance

parser = argparse.ArgumentParser()
parser.add_argument("--include-synthetic-external-evidence", action="store_true")
args = parser.parse_args()
print(json.dumps(run_conformance(args.include_synthetic_external_evidence), indent=2, sort_keys=True, default=lambda x: getattr(x, "value", str(x))))

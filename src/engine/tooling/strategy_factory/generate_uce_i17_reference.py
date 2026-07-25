#!/usr/bin/env python3
from strategy_factory_portfolio_v3.conformance import run_conformance
import json
print(json.dumps(run_conformance(),indent=2,sort_keys=True))

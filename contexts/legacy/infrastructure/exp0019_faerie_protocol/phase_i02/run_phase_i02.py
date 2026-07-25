#!/usr/bin/env python3
from __future__ import annotations
from tools.repository_paths import find_repository_root

import json
import sys
from pathlib import Path

ROOT = find_repository_root(__file__)
PYROOT = ROOT / "contexts/legacy/infrastructure/exp0019_faerie_protocol/phase_i02/python"
if str(PYROOT) not in sys.path:
    sys.path.insert(0, str(PYROOT))

from fp_i02_kernel.conformance import run_conformance

if __name__ == "__main__":
    report = run_conformance()
    print(json.dumps(report, indent=2, sort_keys=True))
    raise SystemExit(0 if report["passed"] else 1)

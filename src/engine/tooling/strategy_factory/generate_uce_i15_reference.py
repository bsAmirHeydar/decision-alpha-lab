#!/usr/bin/env python3
from tools.repository_paths import find_repository_root
from pathlib import Path
import sys
from dataclasses import asdict
ROOT=find_repository_root(__file__);sys.path.insert(0,str(ROOT/'src/engine/packages'))
from strategy_factory_tournament_v3.golden import golden_run
from strategy_factory_tournament_v3.canonical import canonical_json
x=golden_run();data={'inventory':asdict(x[0]),'tournament_freeze':asdict(x[5]),'tournament_report':asdict(x[6]),'paper_report':asdict(x[8]),'decision':asdict(x[9])}
out=ROOT/'tests/fixtures/legacy/strategy_factory/v3/uce_i15_reference_tournament.json';out.write_text(canonical_json(data)+'\n');print(out)

from __future__ import annotations
from tools.repository_paths import find_repository_root
import json
from pathlib import Path
ROOT=find_repository_root(__file__)
CONTEXT=ROOT/'contexts/legacy/strategy_factory/generated/rthp_cross_symbol_cycle_divergence/ai_input'
REGISTRY=ROOT/'registry/strategy_factory/contexts/rthp/v1'
FIXTURE=CONTEXT/'fixtures/rthp_ai_smoke_records.jsonl'
def records(): return [json.loads(x) for x in FIXTURE.read_text(encoding='utf-8').splitlines() if x.strip()]
def load(name): return json.loads((CONTEXT/name).read_text(encoding='utf-8'))

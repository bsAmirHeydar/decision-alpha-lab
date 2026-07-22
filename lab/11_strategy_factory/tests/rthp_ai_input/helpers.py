from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
CONTEXT=ROOT/'lab/11_strategy_factory/generated_contexts/rthp_cross_symbol_cycle_divergence/ai_input'
REGISTRY=ROOT/'registry/strategy_factory/contexts/rthp/v1'
FIXTURE=CONTEXT/'fixtures/rthp_ai_smoke_records.jsonl'
def records(): return [json.loads(x) for x in FIXTURE.read_text(encoding='utf-8').splitlines() if x.strip()]
def load(name): return json.loads((CONTEXT/name).read_text(encoding='utf-8'))

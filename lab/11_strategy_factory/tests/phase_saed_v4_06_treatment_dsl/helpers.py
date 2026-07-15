from __future__ import annotations
import json
from dataclasses import replace
from pathlib import Path
from saed_v4_treatment_dsl.catalog import institutional_capability_profile, institutional_policy, institutional_registry
from saed_v4_treatment_dsl.parser import parse_program
from saed_v4_treatment_dsl.service import TreatmentDslService
ROOT=Path(__file__).resolve().parents[4]
EX=ROOT/'lab/11_strategy_factory/examples/saed_v4_06'
V405=ROOT/'lab/11_strategy_factory/examples/saed_v4_05'
def load(name): return json.loads((EX/name).read_text(encoding='utf-8'))
def graph(): return json.loads((V405/'golden_semantic_temporal_hypergraph.json').read_text(encoding='utf-8'))
def handoff(): return json.loads((V405/'v4_05_to_v4_06_handoff.json').read_text(encoding='utf-8'))
def source(name='golden_treatment_program_source.json'): return parse_program(load(name))
def sources(): return (source(),source('system_skip_program_source.json'),source('system_abstain_program_source.json'))
def build(srcs=None,g=None,h=None,registry=None,policy=None,profile=None):
 return TreatmentDslService().build_package(graph=g or graph(),handoff=h or handoff(),registry=registry or institutional_registry(),policy=policy or institutional_policy(),capability_profile=profile or institutional_capability_profile(),sources=srcs or sources())

from __future__ import annotations
import json
from pathlib import Path

def root(): return Path(__file__).resolve().parents[4]

def test_required_phase_files_exist():
    r=root(); required=[
      "mql5/Include/AlphaLab/StrategyFactory/ContextPackage/UCE02_All.mqh",
      "mql5/Experts/StrategyFactoryTests/UCE_I02_ContextPackageSelfTest.mq5",
      "lab/11_strategy_factory/python/strategy_factory_contexts_v3/__init__.py",
      "lab/11_strategy_factory/schemas/v3/context_package_manifest.schema.json",
      "docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i02/00_UCE_I02_MOC.md",
    ]
    for rel in required: assert (r/rel).is_file(),rel

def test_schema_registry_matches_files():
    d=root()/"lab/11_strategy_factory/schemas/v3"; registry=json.loads((d/"context_package_schema_registry.json").read_text())
    for name in registry["schemas"]: assert (d/name).is_file(),name
    assert "context_package_manifest.schema.json" in registry["schemas"]

def test_json_files_parse():
    r=root(); paths=list((r/"lab/11_strategy_factory/schemas/v3").glob("*.json"))+list((r/"lab/11_strategy_factory/examples/uce_i02").glob("*.json"))
    assert paths
    for p in paths: json.loads(p.read_text())

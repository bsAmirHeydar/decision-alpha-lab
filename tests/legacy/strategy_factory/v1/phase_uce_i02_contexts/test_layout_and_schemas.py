from __future__ import annotations
from tools.repository_paths import find_repository_root
import json
from pathlib import Path

def root(): return find_repository_root(__file__)

def test_required_phase_files_exist():
    r=root(); required=[
      "mql5/Include/AlphaLab/StrategyFactory/ContextPackage/UCE02_All.mqh",
      "mql5/Tests/Experts/StrategyFactory/UCE_I02_ContextPackageSelfTest.mq5",
      "src/engine/packages/strategy_factory_contexts_v3/__init__.py",
      "schemas/legacy/strategy_factory/v3/context_package_manifest.schema.json",
      "docs/history/systems/ucee/implementation_program/phase_deliveries/uce_i02/00_UCE_I02_MOC.md",
    ]
    for rel in required: assert (r/rel).is_file(),rel

def test_schema_registry_matches_files():
    d=root()/"schemas/legacy/strategy_factory/v3"; registry=json.loads((d/"context_package_schema_registry.json").read_text())
    for name in registry["schemas"]: assert (d/name).is_file(),name
    assert "context_package_manifest.schema.json" in registry["schemas"]

def test_json_files_parse():
    r=root(); paths=list((r/"schemas/legacy/strategy_factory/v3").glob("*.json"))+list((r/"examples/legacy/strategy_factory/uce_i02").glob("*.json"))
    assert paths
    for p in paths: json.loads(p.read_text())

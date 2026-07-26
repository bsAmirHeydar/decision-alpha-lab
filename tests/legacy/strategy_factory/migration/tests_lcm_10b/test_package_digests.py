import json
from .conftest import ROOT,jl
from src.engine.tooling.strategy_factory.lcm.lcm_10b.canonical import digest_object
def test_every_package_digest_is_valid():
 for r in jl("registries/treatment_package_registry.jsonl"):
  p=json.loads((ROOT/r["package_path"]).read_text());assert p["package_digest"]==digest_object(p,"package_digest");assert p["submission_capability_default"] is False

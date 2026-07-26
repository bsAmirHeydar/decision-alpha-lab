from .conftest import ROOT,j
from src.engine.tooling.strategy_factory.lcm.lcm_10b.canonical import file_digest
def test_manifest_binds_every_generated_file():
 m=j("output_manifest.json");assert m["file_count"]>=900
 for x in m["files"]:assert file_digest(ROOT/x["path"])==x["sha256"]

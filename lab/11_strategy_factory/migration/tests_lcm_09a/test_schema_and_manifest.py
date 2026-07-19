from .conftest import REPO,ROOT,j
def test_schemas_are_draft_2020_12():
 import json
 files=sorted((REPO/"registry/legacy_context_migration/lcm_09a/schemas/v1").glob("*.schema.json")); assert len(files)>=14; assert all(json.loads(p.read_text())["$schema"]=="https://json-schema.org/draft/2020-12/schema" for p in files)
def test_output_manifest_matches_files():
 from tools.strategy_factory.lcm.lcm_09a.canonical import file_digest
 m=j("output_manifest.json"); assert m["file_count"]==len(m["files"]); assert all((ROOT/x["path"]).stat().st_size==x["size_bytes"] and file_digest(ROOT/x["path"])==x["sha256"] for x in m["files"])

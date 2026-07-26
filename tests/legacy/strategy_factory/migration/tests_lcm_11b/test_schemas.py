import json
def test_schemas(repo_root):
 files=list((repo_root/"registry/history/lcm/lcm_11b/schemas/v1").glob("*.schema.json"));assert len(files)>=10
 for p in files:assert json.loads(p.read_text())["$schema"]=="https://json-schema.org/draft/2020-12/schema"

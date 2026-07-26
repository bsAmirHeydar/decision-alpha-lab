from src.engine.tooling.strategy_factory.lcm.lcm_05.io import read_jsonl
from src.engine.tooling.strategy_factory.lcm.lcm_05.target_mapper import map_artifact,map_identity
from src.engine.tooling.strategy_factory.lcm.lcm_05.upstream import load

def test_identity_mapping_replay(repo_root,topology_root):
    up=load(repo_root);expected=read_jsonl(topology_root/'mappings/identity_target_map.jsonl');actual=[map_identity(x) for x in up['identities']];assert [x['mapping_digest'] for x in actual]==[x['mapping_digest'] for x in expected]
def test_artifact_mapping_sample_replay(repo_root,topology_root):
    up=load(repo_root);ib={x['source_artifact_path']:x for x in up['identities']};expected=read_jsonl(topology_root/'mappings/artifact_target_map.jsonl');indices=[0,1,100,1000,10000,len(expected)-1]
    for i in indices:assert map_artifact(up['classifications'][i],ib)['mapping_digest']==expected[i]['mapping_digest']

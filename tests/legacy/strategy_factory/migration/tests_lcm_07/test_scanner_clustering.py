from tools.repository_paths import find_repository_root
from tools.strategy_factory.lcm.lcm_07.clustering import cluster,select
from tools.strategy_factory.lcm.lcm_07.io import read_json
from pathlib import Path

def test_exact_cluster_fixture():
    root=find_repository_root(__file__);records=read_json(root/"tests/legacy/strategy_factory/migration/fixtures/lcm_07/scanner/reference_functions.json")["records"]
    c=cluster(records);assert len(c)==1;assert c[0]["distinct_artifact_count"]==2;assert select(c)[0]["candidate_id"]==c[0]["candidate_id"]
def test_cluster_determinism():
    root=find_repository_root(__file__);records=read_json(root/"tests/legacy/strategy_factory/migration/fixtures/lcm_07/scanner/reference_functions.json")["records"]
    assert cluster(records)==cluster(list(reversed(records)))

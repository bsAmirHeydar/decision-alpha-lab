import json
from tools.strategy_factory.lcm.roadmap_refinement.validator import validate

def test_roadmap_registry(repo_root):
    root=repo_root/'registry/legacy_context_migration/roadmaps/LCM_ROADMAP_R1_BALANCED_PARTITION'
    result=validate(repo_root,root)
    assert result['passed']
    assert result['subphase_count']==22
    assert result['next_subphase']=='LCM-08A'

def test_balanced_partition(repo_root):
    d=json.loads((repo_root/'registry/legacy_context_migration/roadmaps/LCM_ROADMAP_R1_BALANCED_PARTITION/master_phase_partition_registry.json').read_text(encoding='utf-8'))
    assert set(d['masters'])=={f'LCM-{i:02d}' for i in range(8,17)}
    assert all(len(v['parts']) in (2,3) for v in d['masters'].values())

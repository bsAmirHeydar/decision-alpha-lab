import copy
import pytest
from saed_v4_conformal_ood_selective_control.service import run
from saed_v4_conformal_ood_selective_control.canonical import content_hash
@pytest.mark.parametrize('index,delta', [(0,1.0),(5,-1.0),(12,0.5),(27,-0.7),(41,2.0)])
def test_future_outcome_mutation_does_not_change_decisions(config, upstream, records, outputs, index, delta):
    mutated = copy.deepcopy(records)
    selection_indices = [i for i, record in enumerate(mutated) if record['role'] == 'selection_validation']
    mutated[selection_indices[index]]['realized_value'] += delta
    changed = run(config, upstream, mutated)
    assert changed['selective_decisions'] == outputs['selective_decisions']
    assert changed['conformal_bounds'] == outputs['conformal_bounds']
    assert changed['selection_ood_evaluations'] == outputs['selection_ood_evaluations']
    assert content_hash(changed['retrospective_coverage']) != content_hash(outputs['retrospective_coverage'])

import pytest
from saed_v4_conformal_ood_selective_control.conformal import downside_residual
@pytest.mark.parametrize('predicted,realized,expected', [(1,1,0),(1,0.5,0.5),(0,1,0),(-1,-2,1),(0.2,0.1,0.1)])
def test_downside_residual(predicted, realized, expected): assert downside_residual({'predicted_value': predicted, 'realized_value': realized}) == pytest.approx(expected)
def test_calibrator(outputs):
    value = outputs['conformal_calibrator']; assert value['pooled_count'] == 90 and len(value['groups']) == 3 and value['pooled_quantile'] >= 0
@pytest.mark.parametrize('index', range(30))
def test_lower_bound_has_no_outcome_dependency(outputs, index):
    value = outputs['conformal_bounds'][index]
    assert value['value_lower_bound'] <= value['predicted_value'] and value['uses_outcome_at_decision'] is False
    assert value['quantile_source'] in {'mondrian', 'pooled_fallback'} and value['calibration_count'] >= 20
@pytest.mark.parametrize('index', range(20))
def test_retrospective_coverage_rows(outputs, index): assert isinstance(outputs['retrospective_coverage']['rows'][index]['covered'], bool)

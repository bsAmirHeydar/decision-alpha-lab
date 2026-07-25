def test_adversary_bounded(result,config):
 a=result['adversary_report'];assert a['bounded'] and a['shock_bound']==config['adversary']['shock_bound'] and len(a['trace'])==config['adversary']['steps']
def test_stability_complete(result):
 s=result['stability_report'];assert len(s['rows'])==result['scenario_set']['scenario_count'];assert s['research_only']
def test_radius_monotone(result):assert result['radius_sensitivity']['monotone_nonincreasing']

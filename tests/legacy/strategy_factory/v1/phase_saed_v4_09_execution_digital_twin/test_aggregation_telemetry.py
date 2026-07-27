from .helpers import built
from saed_v4_execution_twin.aggregation import build_summary
from saed_v4_execution_twin.telemetry import build_telemetry

def test_summary_has_every_scenario_without_ranking():
    _,_,p,t=built();s=build_summary(t);assert len(s['scenario_summaries'])==len(p.scenarios);assert s['ranking_semantics']=='none'

def test_telemetry_counts_are_consistent():
    *_,t=built();x=build_telemetry(t);assert x['twin_row_count']==len(t['rows']);assert x['complete_exposure']

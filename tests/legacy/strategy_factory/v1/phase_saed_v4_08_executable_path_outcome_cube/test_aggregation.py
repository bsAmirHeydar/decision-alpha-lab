from .helpers import cube
from saed_v4_outcome_cube.aggregation import summarize
def test_summary_is_descriptive_only():
 s=summarize(cube());assert s['descriptive_only'];assert not s['ranking_authority'];assert s['row_count']==38

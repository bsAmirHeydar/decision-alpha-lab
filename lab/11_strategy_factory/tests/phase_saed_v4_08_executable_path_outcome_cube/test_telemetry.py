from helpers import cube
from saed_v4_outcome_cube.telemetry import telemetry
def test_telemetry_counts():
 t=telemetry(cube());assert t['rows']==38;assert t['path_events']>0;assert not t['production_authorization']

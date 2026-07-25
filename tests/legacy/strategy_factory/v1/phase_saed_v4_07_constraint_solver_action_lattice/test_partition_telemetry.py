from helpers import solve,load
from saed_v4_action_lattice.partition import build_partition_manifest
from saed_v4_action_lattice.telemetry import build_telemetry
from saed_v4_action_lattice.exposure import build_exposure_ledger
def test_partition_exact():assert build_partition_manifest(solve()['action_lattice'],8)==load('golden_lattice_partition_manifest.json')
def test_telemetry_exact():
 o=solve();assert build_telemetry(o['solver_result'],o['action_lattice'])==load('golden_lattice_telemetry.json')
def test_exposure_complete():
 r=solve()['solver_result'];x=build_exposure_ledger(r);assert x['complete_accounting'] and x['exposure_count']==74

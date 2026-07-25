from __future__ import annotations
import json
from _common import AR
load=lambda n:json.loads((AR/n).read_text())
inv=load("GOLDEN_INVARIANT_VERIFICATION_REPORT.JSON"); temp=load("GOLDEN_BOUNDED_TEMPORAL_VERIFICATION_REPORT.JSON"); mutation=load("GOLDEN_MUTATION_SCORECARD.JSON"); proofs=load("GOLDEN_PROOF_DISCHARGE_LEDGER.JSON"); graph=load("GOLDEN_REACHABILITY_GRAPH.JSON")
assert inv["passed"] and temp["passed"] and mutation["passed"] and mutation["survivor_count"]==0 and mutation["score"]==1.0
assert proofs["all_discharged"] and proofs["discharged_count"]==proofs["total_count"]
assert graph["complete_for_reachable_finite_state_space"] and graph["state_count"]>=6
print("V4-31 formal verification evidence validation passed")

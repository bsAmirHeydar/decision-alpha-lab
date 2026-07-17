from __future__ import annotations
from _common import reference_result
r=reference_result()
assert r["certificate"]["all_gates_passed"] and r["certificate"]["accepted_reference"]
assert r["capabilities"]["deny_by_default"] and r["separation"]["self_approval_denied"]
assert r["memory"]["cross_agent_write_denied"] and r["exposure"]["future_suffix_exposures"]==0
assert r["contradictions"]["suppressed_count"]==0 and r["incidents"]["counterexamples_preserved"]
assert r["quorum"]["single_agent_decisions"]==0 and r["authority"]["agents_have_zero_live_authority"]
assert all(v is False for v in r["authority"]["authority"].values())
print("V4-32 governance validation passed")

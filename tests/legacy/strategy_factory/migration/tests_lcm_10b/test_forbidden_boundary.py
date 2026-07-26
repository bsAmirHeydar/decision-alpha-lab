from src.engine.tooling.strategy_factory.lcm.lcm_10b.boundary import scan_canonical_boundary
from .conftest import REPO,j
def test_new_canonical_surface_has_no_broker_mutation_calls():assert scan_canonical_boundary(REPO)["passed"] and j("reports/forbidden_api_boundary_report.json")["canonical_forbidden_hit_count"]==0

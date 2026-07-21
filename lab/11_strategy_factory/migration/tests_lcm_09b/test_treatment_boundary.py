from .conftest import jl
def test_every_setup_seeds_lcm10_dependency_without_execution_semantics():
 rows=jl("dependencies/treatment_dependency_inventory_seed.jsonl");assert len(rows)==60;assert all(x["dependency_state"]=="PENDING_LCM10" for x in rows);assert all("ORDER_ROUTING" in x["forbidden_in_setup_core"] for x in rows)

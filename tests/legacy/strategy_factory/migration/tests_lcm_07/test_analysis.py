from tools.repository_paths import find_repository_root
from src.engine.tooling.strategy_factory.lcm.lcm_07.clustering import cluster
from src.engine.tooling.strategy_factory.lcm.lcm_07.analysis_engine import variance,equivalence,design,adapters,governance,decision
from src.engine.tooling.strategy_factory.lcm.lcm_07.io import read_json
from pathlib import Path

def c():
 root=find_repository_root(__file__);return cluster(read_json(root/"tests/legacy/strategy_factory/migration/fixtures/lcm_07/scanner/reference_functions.json")["records"])[0]
def test_reference_design_never_materializes():
 x=c();e=equivalence(x);d=design(x,e);assert e["extraction_authorized"] is False;assert d["materialized"] is False;assert d["extraction_authorized"] is False
def test_adapters_never_write():
 x=c();d=design(x,equivalence(x));assert all(a["write_performed"] is False for a in adapters(x,d))
def test_governance_blocks_unknown_owner():
 x=c();e=equivalence(x);d=design(x,e);g=governance(x,d,e);assert g["named_owner"]=="UNKNOWN_BLOCKING";assert g["approval_state"]=="PENDING_HUMAN_APPROVAL"
def test_decision_blocks_materialization():
 x=c();e=equivalence(x);d=design(x,e);g=governance(x,d,e);q=decision(x,e,d,g);assert q["materialization_authorized"] is False;assert q["merge_authorized"] is False
def test_variance_has_signature_dimensions():
 dims={x["dimension"] for x in variance(c())["dimensions"]};assert {"FUNCTION_NAME","RETURN_TYPE","PARAMETER_ARITY","PARAMETER_TYPES"}<=dims

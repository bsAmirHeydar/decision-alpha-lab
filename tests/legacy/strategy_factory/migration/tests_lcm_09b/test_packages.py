from .conftest import ROOT,j
from tools.strategy_factory.lcm.lcm_09b.contracts import validate_package
def test_all_packages_validate_and_fail_closed():
 for row in j("canonical_setup_registry.json")["packages"]:
  p=j(row["package_path"]);assert validate_package(p)==[]
  if p["package_status"]=="REFERENCE_BLOCKED":assert p["executable_reference"] is False and p["blocker_ids"]
def test_no_package_owns_context_clock_or_treatment_semantics():
 for row in j("canonical_setup_registry.json")["packages"]:
  p=j(row["package_path"]);assert p["context_binding"]["independent_context_clock"] is False;assert p["context_binding"]["context_recomputation"] is False;assert p["treatment_binding"]["treatment_semantics_in_setup_core"] is False

from .conftest import j,jl
def test_every_frozen_identity_has_one_package():
 r=j("canonical_setup_registry.json");assert r["package_count"]==60;assert len(r["packages"])==60;assert len({x["setup_id"] for x in r["packages"]})==60
def test_all_packages_are_explicitly_disposed():
 r=j("reports/portfolio_closure_report.json");assert r["unaccounted_count"]==0;assert r["reference_ready_count"]+r["explicitly_blocked_count"]==60

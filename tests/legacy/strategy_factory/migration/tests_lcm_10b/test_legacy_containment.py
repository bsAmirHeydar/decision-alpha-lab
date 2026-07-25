from .conftest import j
def test_legacy_broker_paths_are_contained_not_erased():
 r=j("reports/forbidden_api_boundary_report.json");assert r["legacy_contained_path_count"]==184;assert not r["repository_wide_legacy_absence_claimed"];assert all(x["containment_state"]=="LEGACY_UNMOVED_BLOCKS_CUTOVER" for x in r["legacy_contained_paths"])

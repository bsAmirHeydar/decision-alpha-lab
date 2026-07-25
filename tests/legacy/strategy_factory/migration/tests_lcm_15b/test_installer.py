def test_installer(load,loadl):
 r=load("installer_locator_registry.json");rows=loadl(r["records_path"]);assert len(rows)==1 and rows[0]["legacy_locator_retained"] and rows[0]["external_automation_state"].startswith("UNKNOWN")

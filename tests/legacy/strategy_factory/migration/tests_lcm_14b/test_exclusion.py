def test_exclusion(load):
 x=load("active_path_exclusion_registry.json")
 assert x["compile_discovery_excluded"] and x["runtime_discovery_excluded"] and x["mql5_payload_count"]==0 and x["python_payload_count"]==0

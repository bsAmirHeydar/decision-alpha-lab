def test_one_object_namespace_anchor_lifecycle_file_per_object(inventory_root,inventory):
    count=len(inventory['objects'])
    assert len(list((inventory_root/'objects').glob('*.json')))==count
    assert len(list((inventory_root/'namespaces').glob('*.json')))==count
    assert len(list((inventory_root/'visual_anchor_contracts').glob('*.json')))==count
    assert len(list((inventory_root/'visual_lifecycle_contracts').glob('*.json')))==count

def test_inventory_is_nontrivial_and_accounted(inventory):
    counts=inventory['counts']
    assert counts['visual_object_count']==len(inventory['objects'])
    assert counts['visual_object_count']>=100
    assert counts['chart_object_count']>=50
    assert counts['indicator_buffer_count']>=20
    assert counts['report_projection_count']>=1
    assert counts['active_visual_object_count']>=100

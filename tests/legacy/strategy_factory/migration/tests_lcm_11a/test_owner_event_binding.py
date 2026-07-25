def test_active_objects_have_owner_and_event_or_blocker(inventory):
    active=[x for x in inventory['objects'] if x['active_status']=='ACTIVE_OR_REFERENCED']
    assert active
    for item in active:
        assert item['owner']
        assert item['source_event_type']!='UNKNOWN_CANONICAL_EVENT' or item['blocker_ids']

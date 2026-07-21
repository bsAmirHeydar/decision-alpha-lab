import json
def test_unknown_queue_preserves_blockers(inventory_root,inventory):
    queue=json.loads((inventory_root/'unknowns/visual_unknown_queue.json').read_text())
    assert queue['blocking_count']==len(queue['blockers'])
    ids={x['blocker_id'] for x in queue['blockers']}
    for item in inventory['objects']:
        assert set(item['blocker_ids']).issubset(ids)

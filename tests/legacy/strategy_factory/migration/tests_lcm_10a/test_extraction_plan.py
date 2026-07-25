from .conftest import j
def test_extraction_order_is_disabled_and_sorted():
 d=j('plans/treatment_extraction_order.json');assert d['extraction_item_count']==483;assert not d['live_adapter_activation_allowed'] and not d['source_move_allowed'];assert [x['priority'] for x in d['ordered_items']]==sorted(x['priority'] for x in d['ordered_items'])

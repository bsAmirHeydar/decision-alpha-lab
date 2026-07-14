from fp_i14_diagnostic import *
def test_buffer_inventory(runs): assert runs[ProductKind.INDICATOR].inventory.buffer_values==((0,14.0),)
def test_visual_inventory(runs): assert runs[ProductKind.INDICATOR].inventory.visual_ids==('SEM-15',)
def test_signal_inventory(runs): assert runs[ProductKind.INDICATOR].inventory.signal_ids==('SEM-8','SEM-9')
def test_ww_inventory(runs): assert runs[ProductKind.INDICATOR].inventory.ww_context_ids==('SEM-10',)
def test_quota_inventory(runs): assert runs[ProductKind.INDICATOR].inventory.quota_winner_ids==('SEM-13',)

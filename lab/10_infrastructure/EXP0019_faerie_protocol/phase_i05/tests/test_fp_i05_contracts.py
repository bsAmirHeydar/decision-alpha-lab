import pytest
from fp_i02_kernel.enums import LookbackPolicy,WindowKind,PriceSide,ReferenceState
from fp_i05_reference.contracts import WindowStoreConfig,WindowDescriptor,CalendarDaySelectionItem
from fp_i05_reference.enums import SelectorDisposition
from fp_i05_reference.errors import FPI05Error

def test_config_is_hash_stable():
 c=WindowStoreConfig('FP-CONTEXT-001','PAIR','a'*64,'b'*64)
 assert c.config_hash==c.config_hash and len(c.config_hash)==64

def test_only_calendar_day_depth_is_accepted():
 c=WindowStoreConfig('FP-CONTEXT-001','PAIR','a'*64,'b'*64)
 assert c.lookback_policy is LookbackPolicy.CALENDAR_DAY_DEPTH

def test_invalid_depth_rejected():
 with pytest.raises(FPI05Error):WindowStoreConfig('FP-CONTEXT-001','PAIR','a'*64,'b'*64,0)

def test_invalid_coverage_rejected():
 with pytest.raises(FPI05Error):WindowStoreConfig('FP-CONTEXT-001','PAIR','a'*64,'b'*64,1,0)

def test_w_descriptor_requires_week_id():
 with pytest.raises(FPI05Error):WindowDescriptor('x','PAIR',WindowKind.W,'2026-01-01','NYDAY-1','',0,60000,1,'a'*64,'source')

def test_selected_item_requires_window_identity():
 with pytest.raises(FPI05Error):CalendarDaySelectionItem(1,'2026-01-01',WindowKind.N,SelectorDisposition.SELECTED,'','','x','a'*64)

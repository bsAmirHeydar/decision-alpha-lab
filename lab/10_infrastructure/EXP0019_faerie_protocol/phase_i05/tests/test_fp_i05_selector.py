from dataclasses import replace
from datetime import date,timedelta
from fp_i02_kernel.enums import WindowKind
from fp_i05_reference.golden import golden_completed_n_window
from fp_i05_reference.selector import select_prior_n_calendar_days
from fp_i05_reference.enums import SelectorDisposition,WindowBuildState

def _windows():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 out=[]
 for offset in (1,3):
  d=replace(desc,trading_date=(date.fromisoformat('2026-07-14')-timedelta(days=offset)).isoformat(),descriptor_id=f'd{offset}')
  left=replace(agg.left,descriptor_id=d.descriptor_id)
  right=replace(agg.right,descriptor_id=d.descriptor_id)
  out.append(replace(agg,descriptor=d,left=left,right=right,pair_window_id=f'w{offset}'))
 return out

def test_selector_does_not_compress_missing_calendar_date():
 s=select_prior_n_calendar_days('2026-07-14',3,_windows(),'a'*64)
 assert [i.offset for i in s.items]==[1,2,3]
 assert s.items[1].disposition is SelectorDisposition.DATE_MISSING

def test_selector_keeps_exact_target_dates():
 s=select_prior_n_calendar_days('2026-07-14',3,_windows(),'a'*64)
 assert [i.target_date for i in s.items]==['2026-07-13','2026-07-12','2026-07-11']

def test_selected_windows_are_only_complete_n_windows():
 s=select_prior_n_calendar_days('2026-07-14',3,_windows(),'a'*64)
 assert s.items[0].disposition is SelectorDisposition.SELECTED

def test_incomplete_window_is_evidence_not_skipped():
 ws=_windows();ws[0]=replace(ws[0],left=replace(ws[0].left,state=WindowBuildState.INCOMPLETE))
 s=select_prior_n_calendar_days('2026-07-14',1,ws,'a'*64)
 assert s.items[0].disposition is SelectorDisposition.WINDOW_INCOMPLETE

def test_selector_identity_is_stable():
 a=select_prior_n_calendar_days('2026-07-14',3,_windows(),'a'*64);b=select_prior_n_calendar_days('2026-07-14',3,_windows(),'a'*64)
 assert a.selection_id==b.selection_id and a.evidence_hash==b.evidence_hash

def test_invalid_anchor_date_fails_closed():
 import pytest
 from fp_i05_reference.errors import FPI05Error
 with pytest.raises(FPI05Error): select_prior_n_calendar_days('not-a-date',3,(),'a'*64)

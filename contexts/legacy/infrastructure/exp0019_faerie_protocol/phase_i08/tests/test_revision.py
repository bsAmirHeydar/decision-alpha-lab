from fp_i08_weekly.revision import assess_revision
from helpers import context

def test_confirmed_context_preserved_under_revision():
 c=context();r=assess_revision((c,),'REV-2',c.source_signal.first_hunt_minute_utc_ms,c.confirmed_utc_ms+60000);assert c.ww_context_id in r.preserved_confirmed_context_ids
def test_unrelated_revision_no_impact():
 c=context();r=assess_revision((c,),'REV-2',0,60000);assert not r.preserved_confirmed_context_ids

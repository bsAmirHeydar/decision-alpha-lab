from .contracts import *
from .constants import ALLOWED_CHART_TIMEFRAMES
from .canonical import sha256,stable_id
from .replay import run_incremental

def verify_timeframe_invariance(fixture,instance,chart_timeframes=ALLOWED_CHART_TIMEFRAMES):
    runs=tuple(run_incremental(fixture,instance,tf,chunk_size=17) for tf in chart_timeframes)
    semantic_hashes=tuple(sha256({'semantic':r.inventory.semantic_payloads,'chain':r.inventory.event_chain_hash,'alerts':r.inventory.alert_ids,'exports':r.inventory.export_ids}) for r in runs)
    mismatches=() if len(set(semantic_hashes))==1 else ('semantic_inventory',)
    status=ParityStatus.PASS if not mismatches else ParityStatus.FAIL
    body={'fixture':fixture.fixture_id,'timeframes':tuple(chart_timeframes),'host':fixture.resolved_host_timeframe_minutes,'hashes':semantic_hashes,'mismatches':mismatches}
    return TimeframeParityReport(stable_id('FPTF',body),fixture.fixture_id,tuple(chart_timeframes),fixture.resolved_host_timeframe_minutes,status,semantic_hashes,tuple(r.run_id for r in runs),mismatches,sha256(body))

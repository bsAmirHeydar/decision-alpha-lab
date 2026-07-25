from fp_i14_diagnostic import *
def changed(run,field,value):
    es=list(run.events);e=es[4];kw={x:getattr(e,x) for x in ('sequence','event_time_utc_ms','product','event_type','semantic_id','payload_hash','config_hash','source_revision_id','state','relation','direction','owner_session_id','buffer_index','numeric_value','reason_codes','event_id')};kw[field]=value;es[4]=TraceEvent(**kw);return build_run(run.manifest,run.fixture_id,tuple(es))
def test_payload_mismatch(runs):
    a=runs[ProductKind.INDICATOR];b=changed(runs[ProductKind.DIAGNOSTIC_EA],'payload_hash',sha256('x'));assert any(m.kind==MismatchKind.PAYLOAD_MISMATCH for m in compare_runs(a,b).mismatches)
def test_state_mismatch(runs):
    a=runs[ProductKind.INDICATOR];b=changed(runs[ProductKind.DIAGNOSTIC_EA],'state','INVALIDATED');assert any(m.kind==MismatchKind.STATE_MISMATCH for m in compare_runs(a,b).mismatches)
def test_semantic_id_mismatch(runs):
    a=runs[ProductKind.INDICATOR];b=changed(runs[ProductKind.DIAGNOSTIC_EA],'semantic_id','DIFFERENT');assert any(m.kind==MismatchKind.SEMANTIC_ID_MISMATCH for m in compare_runs(a,b).mismatches)
def test_missing_right(runs):
    a=runs[ProductKind.INDICATOR];r=runs[ProductKind.DIAGNOSTIC_EA];b=build_run(r.manifest,r.fixture_id,r.events[:-1]);assert any(m.kind==MismatchKind.EVENT_MISSING_RIGHT for m in compare_runs(a,b).mismatches)
def test_config_mismatch(runs,config_hash):
    a=runs[ProductKind.INDICATOR];m=build_manifest(ProductKind.DIAGNOSTIC_EA,sha256('other'));es=tuple(TraceEvent(e.sequence,e.event_time_utc_ms,m.product,e.event_type,e.semantic_id,e.payload_hash,m.config_hash,m.source_revision_id,e.state,e.relation,e.direction,e.owner_session_id,e.buffer_index,e.numeric_value,e.reason_codes) for e in runs[ProductKind.DIAGNOSTIC_EA].events);b=build_run(m,'FIX-I14',es);assert any(x.kind==MismatchKind.CONFIG_MISMATCH for x in compare_runs(a,b).mismatches)

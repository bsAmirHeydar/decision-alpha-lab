from .canonical import stable_id,content_hash
def build_telemetry(twin_id,journal,watermarks,projections,known_time):
    payload={'phase':'SAED_V4_03','twin_id':twin_id,'known_time':known_time,'event_count':len(journal.all_events()),'journal_root':journal.journal_root(),'stream_heads':{m.stream_id:journal.head(m.stream_id) for m in journal.registry.all()},'watermarks':[{'stream_id':w.stream_id,'watermark_time':w.watermark_time,'accepted_events':w.accepted_events,'late_events':w.late_events} for w in watermarks.all_states()],'projection_hashes':sorted(p.state_hash for p in projections),'authority':{'order':False,'broker':False,'network':False,'risk':False,'runtime':False}}
    return {**payload,'telemetry_id':stable_id('evttelemetry',payload),'telemetry_hash':content_hash(payload)}

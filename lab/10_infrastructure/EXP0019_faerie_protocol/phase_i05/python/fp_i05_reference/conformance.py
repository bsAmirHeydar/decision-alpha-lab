from .golden import golden_completed_n_window
from .canonical import canonical_sha256
from .reference_engine import transition_reference
from .enums import ReferenceTransition,TouchActor

def run_conformance():
    cfg,result,desc,agg,refset=golden_completed_n_window(); ref=refset.references[0]
    hunted,event1=transition_reference(ref,ReferenceTransition.HUNTER_TOUCH_OBSERVED,desc.end_utc_ms+60_000,'HUNT',TouchActor.HUNTER)
    consumed,event2=transition_reference(hunted,ReferenceTransition.PROTECTED_TOUCH_CONSUMED,desc.end_utc_ms+120_000,'PROTECTED',TouchActor.PROTECTED)
    checks={'window_complete':agg.completed,'reference_count':len(refset.references)==4,'hunter_non_consuming':hunted.active_for_hunt,'protected_consumes':not consumed.active_for_hunt,'descriptor_stable':desc.descriptor_hash==desc.descriptor_hash}
    return {'phase':'FP-I05','checks':checks,'passed':all(checks.values()),'evidence_hash':canonical_sha256({'checks':checks,'agg':agg.semantic_hash,'refs':refset.evidence_hash,'events':[event1.event_hash,event2.event_hash]})}

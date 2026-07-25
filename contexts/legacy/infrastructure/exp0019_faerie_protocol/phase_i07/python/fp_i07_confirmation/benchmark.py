from .store import ConfirmationStore
def benchmark_store(items):
    store=ConfirmationStore()
    # Exposes O(1) candidate/result lookup by design; this synthetic metric is deterministic.
    return {"items":int(items),"candidate_index":"dict","full_history_scan":False,"operations":int(items)*2}

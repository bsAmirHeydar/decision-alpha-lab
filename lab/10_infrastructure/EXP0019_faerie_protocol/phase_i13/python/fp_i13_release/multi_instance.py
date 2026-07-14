from .contracts import *
from .canonical import sha256,stable_id
from .replay import run_incremental

def verify_multi_instance(fixture,instances,chart_timeframe_minutes=5):
    runs=tuple(run_incremental(fixture,x,chart_timeframe_minutes,chunk_size=13) for x in instances)
    groups={'instance_ids':tuple(x.instance_id for x in instances),'namespaces':tuple(x.object_namespace for x in instances),'checkpoint_keys':tuple(x.checkpoint_key for x in instances),'export_keys':tuple(x.export_file_key for x in instances)}
    collisions=[]
    for name,values in groups.items():
        if len(values)!=len(set(values)):collisions.append(name)
    semantic_hashes=tuple(sha256({'semantic':r.inventory.semantic_payloads,'chain':r.inventory.event_chain_hash}) for r in runs)
    if len(set(semantic_hashes))!=1:collisions.append('semantic_divergence')
    status=IsolationStatus.PASS if not collisions else IsolationStatus.FAIL
    body={**groups,'semantic_hashes':semantic_hashes,'collisions':tuple(collisions)}
    return MultiInstanceReport(stable_id('FPISO',body),groups['instance_ids'],groups['namespaces'],groups['checkpoint_keys'],groups['export_keys'],semantic_hashes,status,tuple(collisions),sha256(body))

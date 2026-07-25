from dataclasses import asdict
def plugin_manifest(d,r):
    descriptor={**asdict(d),"kind":d.kind.value,"capability_mask":int(d.capability_mask),"update_scope_mask":int(d.update_scope_mask),"queue_overflow_policy":d.queue_overflow_policy.value,"descriptor_hash":d.descriptor_hash}
    req=[]
    for x in r.items:req.append({**asdict(x),"kind":x.kind.value,"strength":x.strength.value})
    return {"schema":"alpha_lab.strategy_factory/plugin_manifest@1.0.0","descriptor":descriptor,"requirements_hash":r.requirements_hash,"requirements":req}

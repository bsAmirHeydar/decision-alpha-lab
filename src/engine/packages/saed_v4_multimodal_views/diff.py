from .models import ViewDiff
def diff_views(left,right):
    l={x.feature_id:x for x in left.features};r={x.feature_id:x for x in right.features}
    common=set(l)&set(r);changed=tuple(sorted(k for k in common if l[k].semantic_payload()!=r[k].semantic_payload()))
    return ViewDiff(left.view_hash,right.view_hash,changed,tuple(sorted(set(r)-set(l))),tuple(sorted(set(l)-set(r))),left.status!=right.status,left.support!=right.support)

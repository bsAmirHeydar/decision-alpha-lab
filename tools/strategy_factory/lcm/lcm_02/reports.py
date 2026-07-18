from __future__ import annotations
from collections import Counter,defaultdict

def summarize(records):
    return {'role_counts':dict(sorted(Counter(r['artifact_role'] for r in records).items())),'disposition_counts':dict(sorted(Counter(r['primary_disposition'] for r in records).items())),'activity_counts':dict(sorted(Counter(r['activity_status'] for r in records).items())),'family_counts':dict(sorted(Counter(r['family_candidate'] for r in records).items())),'security_sensitive_count':sum(r['security_sensitive'] for r in records),'protected_platform_count':sum(r['protected_platform_asset'] for r in records),'owner_pending_count':sum(bool(r['ownership_blockers']) for r in records),'unknown_role_count':sum(r['artifact_role']=='UNKNOWN_ROLE' for r in records),'unknown_activity_count':sum(r['activity_status']=='UNKNOWN_ACTIVITY' for r in records),'generated_projection_count':sum(r['artifact_role']=='GENERATED_PROJECTION' for r in records),'active_candidate_count':sum(r['activity_status'] in {'ACTIVE_PLATFORM','ACTIVE_RUNTIME_CANDIDATE','ACTIVE_RESEARCH'} for r in records),'active_unowned_blocked_count':sum(r['activity_status'] in {'ACTIVE_PLATFORM','ACTIVE_RUNTIME_CANDIDATE','ACTIVE_RESEARCH'} and not r['ownership_is_human_approved'] for r in records)}
def family_rows(records):
    g=defaultdict(list)
    for r in records:g[r['family_candidate']].append(r)
    out=[]
    for fam,rs in sorted(g.items()):
        out.append({'family':fam,'artifact_count':len(rs),'role_counts':dict(sorted(Counter(r['artifact_role'] for r in rs).items())),'disposition_counts':dict(sorted(Counter(r['primary_disposition'] for r in rs).items())),'activity_counts':dict(sorted(Counter(r['activity_status'] for r in rs).items())),'security_sensitive_count':sum(r['security_sensitive'] for r in rs),'protected_platform_count':sum(r['protected_platform_asset'] for r in rs),'unknown_role_count':sum(r['artifact_role']=='UNKNOWN_ROLE' for r in rs),'human_owner_approval_complete':False})
    return out

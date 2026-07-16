from .canonical import content_hash,stable_id

def audit(envelopes,config,candidate,policy):
    domain=[x for x in envelopes if x['source_plane']=='domain'];foundation=[x for x in envelopes if x['source_plane']=='foundation'];by={x['view_name']:x for x in domain}
    missing_required=[n for n in config.required_view_names if n not in by or not by[n]['available']]
    missing_critical=[n for n in config.critical_view_names if n not in by or not by[n]['available']]
    stale_required=[n for n in config.required_view_names if n in by and by[n]['age_seconds']>config.max_view_age_seconds]
    corrupt=[x['view_name'] for x in envelopes if len(x['embedding'])!=config.common_dim or not x.get('envelope_hash')]
    available_domain=[x for x in domain if x['available']];available_foundation=[x for x in foundation if x['available']]
    reasons=[];action='fuse';supported=True
    if corrupt:reasons.append('corrupt_view');action=policy.corrupt_action;supported=False
    elif missing_critical:reasons.append('missing_critical_view');action=policy.missing_critical_action;supported=False
    elif missing_required:reasons.append('missing_required_view');action=policy.missing_required_action;supported=False
    elif stale_required:reasons.append('stale_required_view');action=policy.stale_required_action;supported=False
    elif len(available_domain)<candidate.min_domain_views:reasons.append('insufficient_domain_views');action='abstain';supported=False
    elif candidate.requires_foundation_views and len(available_foundation)<candidate.min_foundation_views:reasons.append('insufficient_foundation_views');action=policy.foundation_missing_action;supported=False
    doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'supported':supported,'action':action,'reasons':reasons,'available_domain_views':[x['view_name'] for x in available_domain],'available_foundation_views':[x['view_name'] for x in available_foundation],'missing_required_views':missing_required,'missing_critical_views':missing_critical,'stale_required_views':stale_required,'corrupt_views':corrupt,'domain_available_count':len(available_domain),'foundation_available_count':len(available_foundation),'production_eligible':False}
    doc['audit_hash']=content_hash(doc);doc['audit_id']=stable_id('v415support',doc);return doc

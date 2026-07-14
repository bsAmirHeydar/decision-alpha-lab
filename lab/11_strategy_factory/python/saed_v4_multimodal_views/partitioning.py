def shard_key(twin_id,view_kind,known_as_of,partitions=64):
    import hashlib
    raw=f'{twin_id}|{view_kind}|{known_as_of[:10]}'.encode();return int(hashlib.sha256(raw).hexdigest()[:16],16)%partitions
def cache_key(specification_hash,known_as_of,event_as_of,evidence_role,source_hashes):
    from .canonical import content_hash
    return content_hash({'specification_hash':specification_hash,'known_as_of':known_as_of,'event_as_of':event_as_of,'evidence_role':evidence_role,'source_hashes':sorted(source_hashes)})

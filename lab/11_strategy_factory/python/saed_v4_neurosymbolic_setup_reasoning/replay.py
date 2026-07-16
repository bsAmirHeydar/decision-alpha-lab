from __future__ import annotations
from .canonical import content_hash

def replay_hash(bundle):return content_hash(bundle)
def verify(expected_hash,bundle):return replay_hash(bundle)==expected_hash

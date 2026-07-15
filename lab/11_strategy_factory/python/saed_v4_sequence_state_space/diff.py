from __future__ import annotations
from .canonical import content_hash,stable_id,normalise

def semantic_diff(a,b):
    na=normalise(a);nb=normalise(b);material={'equal':na==nb,'left_hash':content_hash(na),'right_hash':content_hash(nb),'changed_paths':[] if na==nb else ['$']}
    return {**material,'diff_id':stable_id('seqdiff',material),'diff_hash':content_hash(material)}

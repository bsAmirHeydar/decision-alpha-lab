from __future__ import annotations
from .canonical import content_hash,stable_id

def replay_receipt(first,second):
    h1=content_hash(first);h2=content_hash(second);material={'first_hash':h1,'second_hash':h2,'bit_exact':h1==h2,'environment_class':'local_cpu_reference','external_gpu_reproduction':False}
    return {**material,'replay_id':stable_id('seqreplay',material),'replay_hash':content_hash(material)}

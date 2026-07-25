from .canonical import stable_id,canonical_sha256
from .contracts import VisualObjectSpec,Anchor,Style
from .enums import *
def object_id(namespace,kind,semantic_id):
 ns=canonical_sha256(namespace)[:8]; sem=canonical_sha256({'kind':kind.value,'semantic_id':semantic_id})[:16]
 return f'FP19::{ns}::{kind.value[:4]}::{sem}'
def make_spec(*,namespace,semantic_id,kind,layer,state,anchor,style,text='',tooltip='',immutable=False,semantic_hash,reason_codes=()):
 oid=object_id(namespace,kind,semantic_id)
 projection_hash=canonical_sha256({'object_id':oid,'kind':kind.value,'layer':int(layer),'state':state.value,'anchor_hash':anchor.anchor_hash,'style_hash':style.style_hash,'text':text,'tooltip':tooltip,'immutable':immutable,'semantic_hash':semantic_hash,'reason_codes':tuple(sorted(set(reason_codes)))})
 return VisualObjectSpec(oid,semantic_id,kind,layer,state,anchor,style,text,tooltip,immutable,semantic_hash,projection_hash,tuple(sorted(set(reason_codes))))

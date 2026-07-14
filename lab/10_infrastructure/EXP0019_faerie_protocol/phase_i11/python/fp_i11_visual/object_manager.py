from .contracts import *
from .enums import Mutation
from .canonical import canonical_sha256
from .errors import FPI11ImmutableViolation,FPI11Error
class ObjectManager:
 def __init__(self,instance_id): self.instance_id=instance_id; self._objects={}
 def inventory(self):
  vals=tuple(sorted(self._objects.values(),key=lambda x:x.object_id)); return ObjectInventory(self.instance_id,vals,canonical_sha256({'instance_id':self.instance_id,'objects':vals}))
 def diff(self,next_specs,max_objects):
  nxt={x.object_id:x for x in next_specs}
  if len(nxt)>max_objects: raise FPI11Error('FP_VIS_OBJECT_LIMIT_EXCEEDED','projection exceeds max objects')
  creates=[];updates=[];deletes=[];unchanged=[];mut=[]
  for oid,s in sorted(nxt.items()):
   prior=self._objects.get(oid)
   if prior is None: creates.append(s);mut.append(MutationRecord(Mutation.CREATE,oid,'',s.projection_hash,'FP_VIS_OBJECT_CREATE'))
   elif prior.projection_hash==s.projection_hash: unchanged.append(oid);mut.append(MutationRecord(Mutation.NOOP,oid,prior.projection_hash,s.projection_hash,'FP_VIS_OBJECT_UNCHANGED'))
   else:
    if prior.immutable and prior.semantic_hash!=s.semantic_hash: raise FPI11ImmutableViolation('FP_VIS_IMMUTABLE_OBJECT_CHANGED',oid)
    updates.append(s);mut.append(MutationRecord(Mutation.UPDATE,oid,prior.projection_hash,s.projection_hash,'FP_VIS_OBJECT_UPDATE'))
  for oid,prior in sorted(self._objects.items()):
   if oid not in nxt:
    if prior.immutable: unchanged.append(oid);mut.append(MutationRecord(Mutation.NOOP,oid,prior.projection_hash,prior.projection_hash,'FP_VIS_IMMUTABLE_RETAINED'))
    else: deletes.append(oid);mut.append(MutationRecord(Mutation.DELETE,oid,prior.projection_hash,'','FP_VIS_OBJECT_DELETE'))
  payload={'creates':[x.object_id for x in creates],'updates':[x.object_id for x in updates],'deletes':deletes,'unchanged':unchanged,'mutations':mut}
  return DirtySet(tuple(creates),tuple(updates),tuple(deletes),tuple(unchanged),tuple(mut),canonical_sha256(payload))
 def apply(self,dirty):
  for oid in dirty.deletes:self._objects.pop(oid,None)
  for s in dirty.creates+dirty.updates:self._objects[s.object_id]=s
  return self.inventory()

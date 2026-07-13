from __future__ import annotations
from .contracts import LedgerEntry
from .canonical import canonical_sha256,stable_id
from .enums import Stage
from .errors import TournamentError
ZERO='0'*64
class TournamentLedger:
 def __init__(self,entries=()):self._entries=list(entries);self.verify()
 @property
 def entries(self):return tuple(self._entries)
 @property
 def tail_hash(self):return self._entries[-1].entry_hash if self._entries else ZERO
 def append(self,stage:Stage,event_type:str,payload,timestamp_ms:int,actor_id:str='system'):
  entry=LedgerEntry(stable_id('uce15_ledger',{'n':len(self._entries),'p':payload,'prev':self.tail_hash}),len(self._entries),stage,event_type,canonical_sha256(payload),self.tail_hash,timestamp_ms,actor_id)
  self._entries.append(entry);return entry
 def verify(self):
  prev=ZERO
  for i,e in enumerate(self._entries):
   if e.sequence!=i or e.previous_hash!=prev:raise TournamentError('ledger_chain_broken','ledger sequence/hash broken',{'sequence':i})
   prev=e.entry_hash
  return True

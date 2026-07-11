from __future__ import annotations
from .models import TransactionRecord
from .enums import TransactionType
from .hashing import stable_id, chain_hash

class AppendOnlyTransactionLedger:
    def __init__(self) -> None:
        self._rows: list[TransactionRecord] = []

    @property
    def rows(self) -> tuple[TransactionRecord,...]: return tuple(self._rows)

    @property
    def tail_hash(self) -> str: return self._rows[-1].chain_hash if self._rows else "GENESIS"

    def append(self, transaction_type: TransactionType, entity_id: str, event_time_utc_msc: int,
               payload_hash: str, message: str) -> TransactionRecord:
        sequence=len(self._rows)+1
        canonical="|".join((str(sequence),str(int(transaction_type)),entity_id,str(event_time_utc_msc),payload_hash,message))
        txid=stable_id("xtxn",canonical)
        previous=self.tail_hash
        ch=chain_hash(previous,canonical)
        row=TransactionRecord(txid,sequence,transaction_type,entity_id,event_time_utc_msc,previous,payload_hash,ch,message)
        self._rows.append(row)
        return row

    def validate_chain(self) -> bool:
        previous="GENESIS"
        for row in self._rows:
            canonical="|".join((str(row.sequence),str(int(row.transaction_type)),row.entity_id,
                str(row.event_time_utc_msc),row.payload_hash,row.message))
            if row.previous_chain_hash != previous or row.chain_hash != chain_hash(previous,canonical): return False
            previous=row.chain_hash
        return True

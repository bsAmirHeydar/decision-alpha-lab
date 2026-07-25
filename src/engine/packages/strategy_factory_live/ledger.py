from __future__ import annotations
from .models import LiveTransactionRecord
from .enums import LiveTransactionType
from .hashing import stable_id, chain_hash

class AppendOnlyLiveLedger:
    def __init__(self, maximum_records: int = 4096) -> None:
        if maximum_records<=0: raise ValueError("maximum_records")
        self.maximum_records=maximum_records; self.records: list[LiveTransactionRecord]=[]; self.tail_hash="GENESIS"
    def append(self, transaction_type: LiveTransactionType, entity_id: str, event_time_utc_msc: int,
               payload_hash: str, message: str) -> LiveTransactionRecord:
        if len(self.records)>=self.maximum_records: raise OverflowError("live ledger capacity")
        seq=len(self.records)+1
        canonical=f"{seq}|{int(transaction_type)}|{entity_id}|{event_time_utc_msc}|{self.tail_hash}|{payload_hash}|{message}"
        ch=chain_hash(self.tail_hash,canonical); tid=stable_id("ltx",canonical)
        row=LiveTransactionRecord(tid,seq,transaction_type,entity_id,event_time_utc_msc,self.tail_hash,payload_hash,ch,message)
        self.records.append(row); self.tail_hash=ch; return row
    def validate_chain(self) -> bool:
        previous="GENESIS"
        for row in self.records:
            canonical=f"{row.sequence}|{int(row.transaction_type)}|{row.entity_id}|{row.event_time_utc_msc}|{previous}|{row.payload_hash}|{row.message}"
            if row.previous_chain_hash!=previous or row.chain_hash!=chain_hash(previous,canonical): return False
            previous=row.chain_hash
        return previous==self.tail_hash

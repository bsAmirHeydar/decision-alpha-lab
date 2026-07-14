from __future__ import annotations
from .models import EvidenceDebtItem
from .enums import DebtSeverity
from .errors import ContractError
class EvidenceDebtLedger:
    def __init__(self):self._items={}
    def open(self,item:EvidenceDebtItem):
        old=self._items.get(item.debt_id)
        if old and old!=item:raise ContractError('debt rebind')
        self._items[item.debt_id]=item;return item.debt_id
    def resolve(self,debt_id,resolution_hash):
        old=self._items.get(debt_id)
        if not old:raise ContractError('unknown debt')
        if len(resolution_hash)!=64:raise ContractError('resolution hash required')
        self._items[debt_id]=EvidenceDebtItem(old.twin_id,old.debt_key,old.description,old.severity,old.source_ref,old.opened_known_time,True,resolution_hash)
    def active(self,twin_id):return tuple(sorted((x for x in self._items.values() if x.twin_id==twin_id and not x.resolved),key=lambda x:x.debt_id))
    def blocking(self,twin_id):return tuple(x for x in self.active(twin_id) if x.severity==DebtSeverity.BLOCKING)

from __future__ import annotations
from dataclasses import dataclass, field
from .models import *
from .retcodes import classify_retcode
from .hashing import stable_id, cfloat

@dataclass
class DeterministicDryRunBroker:
    check_retcode: int = 0
    send_retcode: int = 10009
    check_api_ok: bool = True
    send_api_ok: bool = True
    order_ticket_seed: int = 180000
    deal_ticket_seed: int = 280000
    checked: list[NormalizedBrokerRequest] = field(default_factory=list)
    sent: list[NormalizedBrokerRequest] = field(default_factory=list)
    def check(self, request: NormalizedBrokerRequest, now_utc_msc: int) -> BrokerCheckResult:
        self.checked.append(request); cls=classify_retcode(self.check_retcode)
        canonical=f"{request.request_id}|{int(self.check_api_ok)}|{self.check_retcode}|{now_utc_msc}"
        h=stable_id("lchk",canonical)
        return BrokerCheckResult(request.request_id,self.check_api_ok,self.check_retcode,cls,100000,100000,100,99900,
            "dry-run check",now_utc_msc,h)
    def send(self, request: NormalizedBrokerRequest, now_utc_msc: int) -> BrokerSendResult:
        self.sent.append(request); cls=classify_retcode(self.send_retcode); n=len(self.sent)
        canonical=f"{request.request_id}|{int(self.send_api_ok)}|{self.send_retcode}|{n}|{now_utc_msc}"
        h=stable_id("lsnd",canonical)
        return BrokerSendResult(request.request_id,self.send_api_ok,self.send_retcode,cls,self.order_ticket_seed+n,
            self.deal_ticket_seed+n,request.volume,request.price,request.price,request.price,"dry-run send",now_utc_msc,h)

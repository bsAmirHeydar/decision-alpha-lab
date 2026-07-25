from decimal import Decimal
import pytest
from strategy_factory_economics_v3 import *
def test_idempotent_reservation_and_restart():
    q,s,a,g,r,b,m=fixture(); e=MaximumLossSolver().solve(g,q,s,a,m,b); l=ReservationLedger(); x=l.reserve(e,a.account_id,'strat','grp',1,1,'same'); y=l.reserve(e,a.account_id,'strat','grp',1,1,'same'); assert x.event_hash==y.event_hash and len(l.events)==1
    r=ReservationLedger().replay(tuple(l.events)); assert r.head_hash==l.head_hash and r.total_open_cash==l.total_open_cash
def test_consume_and_release_cannot_exceed_open():
    q,s,a,g,r,b,m=fixture(); e=MaximumLossSolver().solve(g,q,s,a,m,b); l=ReservationLedger(); ev=l.reserve(e,a.account_id,'strat','grp',1,1); rid=ev.reservation_id; l.consume(rid,e.maximum_loss_cash/2,2,2); l.release(rid,e.maximum_loss_cash/2,3,3); assert l.records[rid].open_cash==0
    with pytest.raises(Exception): l.release(rid,Decimal('1'),4,4)

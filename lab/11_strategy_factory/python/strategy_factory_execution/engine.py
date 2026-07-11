from __future__ import annotations
from dataclasses import replace
from .models import *
from .enums import *
from .hashing import stable_id, cfloat
from .ledger import AppendOnlyTransactionLedger

class PaperExecutionEngine:
    """Deterministic, no-send paper/shadow execution engine.

    The engine consumes immutable Phase-16 execution intents and quote observations. It never
    calls broker APIs. Every state transition is appended to a hash-chained transaction ledger.
    """
    def __init__(self, run_id: str, policy: PaperExecutionPolicy, *, maximum_orders: int = 512) -> None:
        if not run_id: raise ValueError("run_id required")
        policy.validate()
        self.run_id=run_id; self.policy=policy; self.maximum_orders=maximum_orders
        self.orders: dict[str,PaperOrder]={}
        self.intent_hashes: dict[str,str]={}
        self.intents: dict[str,ExecutionIntentRecord]={}
        self.fills: list[FillRecord]=[]
        self.positions: dict[str,PositionRecord]={}
        self.ledger=AppendOnlyTransactionLedger()
        self._duplicates=0; self._stale_quotes=0; self._rejected=0

    def submit(self, intent: ExecutionIntentRecord, now_utc_msc: int) -> PaperOrder:
        try: intent.validate()
        except ValueError:
            return self._reject(intent,now_utc_msc,RejectReason.INVALID_INTENT)
        self.ledger.append(TransactionType.INTENT_RECEIVED,intent.intent_id,now_utc_msc,intent.intent_hash,"intent received")
        if intent.intent_id in self.intent_hashes:
            self._duplicates += 1
            if self.intent_hashes[intent.intent_id] != intent.intent_hash:
                return self._reject(intent,now_utc_msc,RejectReason.DUPLICATE_HASH_CONFLICT)
            return self.orders[intent.intent_id]
        if len(self.orders) >= self.maximum_orders:
            return self._reject(intent,now_utc_msc,RejectReason.CAPACITY_EXCEEDED)
        if now_utc_msc > intent.expires_at_utc_msc:
            return self._reject(intent,now_utc_msc,RejectReason.EXPIRED_INTENT)
        if not intent.paper_eligible and not self.policy.allow_research_only_intents:
            return self._reject(intent,now_utc_msc,RejectReason.RESEARCH_ONLY_AUTHORITY)
        oid=stable_id("pord",f"{self.run_id}|{intent.intent_id}|{intent.intent_hash}|{self.policy.derived_hash()}")
        order=PaperOrder(oid,intent.intent_id,intent.intent_hash,intent.symbol,intent.direction,intent.order_kind,
            OrderState.WORKING,intent.volume,0.0,intent.volume,intent.entry_price,0.0,intent.stop_price,
            intent.target_price,intent.has_target,now_utc_msc,now_utc_msc,intent.expires_at_utc_msc)
        order.refresh_hash(); self.orders[intent.intent_id]=order; self.intent_hashes[intent.intent_id]=intent.intent_hash
        self.intents[intent.intent_id]=intent
        self.ledger.append(TransactionType.ORDER_ACCEPTED,oid,now_utc_msc,order.order_hash,"paper order accepted")
        self.ledger.append(TransactionType.ORDER_WORKING,oid,now_utc_msc,order.order_hash,"paper order working")
        return order

    def _reject(self, intent: ExecutionIntentRecord, now: int, reason: RejectReason) -> PaperOrder:
        oid=stable_id("pord",f"{self.run_id}|{getattr(intent,'intent_id','invalid')}|reject|{int(reason)}|{now}")
        symbol=getattr(intent,'symbol','INVALID'); direction=getattr(intent,'direction',1)
        kind=getattr(intent,'order_kind',OrderKind.MARKET); volume=max(float(getattr(intent,'volume',0.0)),0.0)
        order=PaperOrder(oid,getattr(intent,'intent_id','invalid'),getattr(intent,'intent_hash','invalid'),symbol,direction,
            kind,OrderState.REJECTED,volume,0.0,volume,max(float(getattr(intent,'entry_price',0.0)),0.0),0.0,
            max(float(getattr(intent,'stop_price',0.0)),0.0),max(float(getattr(intent,'target_price',0.0)),0.0),
            bool(getattr(intent,'has_target',False)),now,now,max(int(getattr(intent,'expires_at_utc_msc',now)),now),-1,reason)
        order.refresh_hash(); self.orders[order.intent_id]=order; self.intent_hashes[order.intent_id]=order.intent_hash
        self._rejected += 1
        self.ledger.append(TransactionType.ORDER_REJECTED,oid,now,order.order_hash,f"rejected:{int(reason)}")
        return order

    def cancel(self, intent_id: str, now_utc_msc: int) -> bool:
        order=self.orders.get(intent_id)
        if order is None or order.state not in (OrderState.WORKING,OrderState.PARTIALLY_FILLED): return False
        order.state=OrderState.CANCELED; order.updated_at_utc_msc=now_utc_msc; order.refresh_hash()
        self.ledger.append(TransactionType.ORDER_CANCELED,order.order_id,now_utc_msc,order.order_hash,"paper order canceled")
        return True

    def on_quote(self, quote: QuoteObservation, now_utc_msc: int | None = None) -> None:
        quote.validate(); now=quote.time_utc_msc if now_utc_msc is None else now_utc_msc
        if now-quote.time_utc_msc > self.policy.maximum_quote_age_milliseconds:
            self._stale_quotes += 1; return
        for intent_id in sorted(self.orders):
            order=self.orders[intent_id]
            if order.symbol != quote.symbol: continue
            if order.last_quote_sequence >= quote.sequence: continue
            order.last_quote_sequence=quote.sequence
            if order.state in (OrderState.WORKING,OrderState.PARTIALLY_FILLED):
                if now > order.expires_at_utc_msc:
                    order.state=OrderState.EXPIRED; order.updated_at_utc_msc=now; order.refresh_hash()
                    self.ledger.append(TransactionType.ORDER_EXPIRED,order.order_id,now,order.order_hash,"paper order expired")
                    continue
                if self._entry_triggered(order,quote): self._entry_fill(order,quote)
        self._evaluate_positions(quote)

    def _entry_triggered(self, order: PaperOrder, q: QuoteObservation) -> bool:
        if order.order_kind == OrderKind.MARKET: return True
        if order.order_kind == OrderKind.LIMIT:
            return q.ask <= order.requested_price if order.direction == 1 else q.bid >= order.requested_price
        return q.ask >= order.requested_price if order.direction == 1 else q.bid <= order.requested_price

    def _entry_price(self, order: PaperOrder, q: QuoteObservation) -> float:
        adverse=self.policy.adverse_slippage_points*self.policy.point
        if order.order_kind == OrderKind.MARKET:
            base=q.ask if order.direction==1 else q.bid
        elif order.order_kind == OrderKind.LIMIT:
            base=min(order.requested_price,q.ask) if order.direction==1 else max(order.requested_price,q.bid)
        else:
            base=max(order.requested_price,q.ask) if order.direction==1 else min(order.requested_price,q.bid)
        return base+adverse if order.direction==1 else base-adverse

    def _entry_fill(self, order: PaperOrder, q: QuoteObservation) -> None:
        cap=self.policy.max_fill_volume_per_quote
        fill_volume=order.remaining_volume if cap<=0.0 else min(order.remaining_volume,cap)
        if not self.policy.allow_partial_fills and fill_volume<order.remaining_volume: return
        price=self._entry_price(order,q); old=order.filled_volume
        order.filled_volume += fill_volume; order.remaining_volume=max(0.0,order.requested_volume-order.filled_volume)
        order.average_fill_price=(order.average_fill_price*old+price*fill_volume)/order.filled_volume
        order.state=OrderState.FILLED if order.remaining_volume<=1e-12 else OrderState.PARTIALLY_FILLED
        order.updated_at_utc_msc=q.time_utc_msc; order.refresh_hash()
        pid=stable_id("ppos",f"{self.run_id}|{order.intent_id}")
        reason={OrderKind.MARKET:FillReason.ENTRY_MARKET,OrderKind.LIMIT:FillReason.ENTRY_LIMIT,OrderKind.STOP:FillReason.ENTRY_STOP}[order.order_kind]
        commission=fill_volume*self.policy.commission_per_lot_per_side
        proxy=abs(price-(q.ask if order.direction==1 else q.bid))*fill_volume
        canonical="|".join((order.order_id,pid,str(int(reason)),cfloat(fill_volume),cfloat(price),str(q.sequence),str(q.time_utc_msc)))
        fid=stable_id("pfil",canonical)
        fill=FillRecord(fid,order.order_id,order.intent_id,pid,order.symbol,order.direction,reason,fill_volume,price,
            commission,proxy,q.sequence,q.time_utc_msc,fid)
        self.fills.append(fill)
        tx=TransactionType.ORDER_FILLED if order.state==OrderState.FILLED else TransactionType.ORDER_PARTIAL_FILL
        self.ledger.append(tx,order.order_id,q.time_utc_msc,fill.fill_hash,"entry fill")
        if pid not in self.positions:
            p=PositionRecord(pid,order.intent_id,order.symbol,order.direction,PositionState.OPEN,fill_volume,price,
                order.stop_price,order.target_price,order.has_target,q.time_utc_msc,commission_cash=commission)
            p.refresh_hash(); self.positions[pid]=p
            self.ledger.append(TransactionType.POSITION_OPENED,pid,q.time_utc_msc,p.position_hash,"paper position opened")
        else:
            p=self.positions[pid]; total=p.volume+fill_volume
            p.average_entry_price=(p.average_entry_price*p.volume+price*fill_volume)/total; p.volume=total
            p.commission_cash += commission; p.refresh_hash()
            self.ledger.append(TransactionType.POSITION_INCREASED,pid,q.time_utc_msc,p.position_hash,"paper position increased")

    def _evaluate_positions(self, q: QuoteObservation) -> None:
        for pid in sorted(self.positions):
            p=self.positions[pid]
            if p.symbol!=q.symbol or p.state!=PositionState.OPEN: continue
            stop=(q.bid<=p.stop_price) if p.direction==1 else (q.ask>=p.stop_price)
            target=p.has_target and ((q.bid>=p.target_price) if p.direction==1 else (q.ask<=p.target_price))
            if stop: self._close_position(p,q,FillReason.EXIT_STOP,p.stop_price)
            elif target: self._close_position(p,q,FillReason.EXIT_TARGET,p.target_price)

    def _close_position(self,p: PositionRecord,q: QuoteObservation,reason: FillReason,trigger: float) -> None:
        adverse=self.policy.adverse_slippage_points*self.policy.point
        market=q.bid if p.direction==1 else q.ask
        if reason==FillReason.EXIT_STOP:
            price=min(trigger,market)-adverse if p.direction==1 else max(trigger,market)+adverse
        elif reason==FillReason.EXIT_TARGET:
            price=max(trigger,market)-adverse if p.direction==1 else min(trigger,market)+adverse
        else: price=market-adverse if p.direction==1 else market+adverse
        commission=p.volume*self.policy.commission_per_lot_per_side
        canonical="|".join((p.position_id,str(int(reason)),cfloat(p.volume),cfloat(price),str(q.sequence),str(q.time_utc_msc)))
        fid=stable_id("pfil",canonical)
        fill=FillRecord(fid,"",p.intent_id,p.position_id,p.symbol,-p.direction,reason,p.volume,price,commission,
            abs(price-market)*p.volume,q.sequence,q.time_utc_msc,fid)
        self.fills.append(fill)
        p.state=PositionState.CLOSED; p.closed_at_utc_msc=q.time_utc_msc; p.average_exit_price=price
        p.realized_gross_price_units=(price-p.average_entry_price)*p.direction*p.volume
        p.commission_cash += commission; p.close_reason=reason; p.refresh_hash()
        tx={FillReason.EXIT_STOP:TransactionType.POSITION_CLOSED_STOP,FillReason.EXIT_TARGET:TransactionType.POSITION_CLOSED_TARGET}.get(reason,TransactionType.POSITION_CLOSED_MANUAL)
        self.ledger.append(tx,p.position_id,q.time_utc_msc,p.position_hash,"paper position closed")

    def report(self, now_utc_msc: int) -> ExecutionReport:
        orders=tuple(self.orders[k] for k in sorted(self.orders))
        positions=tuple(self.positions[k] for k in sorted(self.positions))
        telemetry=ExecutionTelemetry(len(self.intent_hashes),sum(o.state!=OrderState.REJECTED for o in orders),
            sum(o.state==OrderState.REJECTED for o in orders),sum(o.state in (OrderState.WORKING,OrderState.PARTIALLY_FILLED) for o in orders),
            sum(o.state==OrderState.FILLED for o in orders),sum(o.state==OrderState.EXPIRED for o in orders),
            sum(o.state==OrderState.CANCELED for o in orders),len(self.fills),sum(p.state==PositionState.OPEN for p in positions),
            sum(p.state==PositionState.CLOSED for p in positions),self._duplicates,self._stale_quotes)
        canonical="|".join((self.run_id,str(int(self.policy.mode)),self.policy.derived_hash(),str(now_utc_msc),
            ','.join(o.order_hash for o in orders),','.join(f.fill_hash for f in self.fills),
            ','.join(p.position_hash for p in positions),self.ledger.tail_hash))
        rh=stable_id("xrep",canonical)
        return ExecutionReport(rh,self.run_id,self.policy.mode,self.policy.derived_hash(),now_utc_msc,orders,
            tuple(self.fills),positions,self.ledger.rows,telemetry,rh)

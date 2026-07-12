from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR
from strategy_factory_treatments_v3.enums import TradeSide
from .contracts import QuoteSnapshot,SymbolEconomicsSpec,ExecutablePriceRequest,ExecutablePriceResult
from .enums import ExecutionRole,OrderKind
from .errors import StaleEconomicInput
from .utils import stable_id,dec,round_tick
class ExecutablePriceKernel:
    VERSION='3.0.0'
    EXIT_ROLES={ExecutionRole.STOP_EXIT,ExecutionRole.TARGET_EXIT,ExecutionRole.TRAIL_EXIT,ExecutionRole.MANAGEMENT_EXIT,ExecutionRole.LIQUIDATION}
    def compute(self,request:ExecutablePriceRequest,quote:QuoteSnapshot,spec:SymbolEconomicsSpec,max_quote_age_ms:int=2000)->ExecutablePriceResult:
        if quote.age_ms(request.decision_time_ms)>max_quote_age_ms: raise StaleEconomicInput('stale_quote','quote too old',{'age_ms':quote.age_ms(request.decision_time_ms)})
        is_entry=request.role is ExecutionRole.ENTRY
        if request.order_kind is OrderKind.MARKET or request.logical_price is None:
            if is_entry: base=quote.ask if request.side is TradeSide.LONG else quote.bid
            else: base=quote.bid if request.side is TradeSide.LONG else quote.ask
        else: base=request.logical_price
        slip=request.adverse_slippage_points*spec.point
        adverse_sign=Decimal('1') if ((is_entry and request.side is TradeSide.LONG) or ((not is_entry) and request.side is TradeSide.SHORT)) else Decimal('-1')
        px=base+adverse_sign*slip
        rounding=ROUND_CEILING if adverse_sign>0 else ROUND_FLOOR
        px=round_tick(px,spec.tick_size,rounding)
        side='ask' if ((is_entry and request.side is TradeSide.LONG) or ((not is_entry) and request.side is TradeSide.SHORT)) else 'bid'
        return ExecutablePriceResult(stable_id('ucepxreq',request.to_dict()),quote.quote_id,base,abs(px-base),px,quote.spread,side,True,'ok')

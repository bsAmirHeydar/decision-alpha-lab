from __future__ import annotations
from dataclasses import dataclass,field,replace
from decimal import Decimal
from typing import Mapping,Any
from strategy_factory_treatments_v3.enums import TradeSide
from .enums import *
from .utils import dec,stable_id,safe_id,canonical_value

@dataclass(frozen=True,slots=True)
class QuoteSnapshot:
    symbol:str; bid:Decimal; ask:Decimal; source_time_ms:int; known_time_ms:int; source_id:str='terminal'; sequence:int=0
    def __post_init__(self):
        safe_id(self.symbol,'symbol'); object.__setattr__(self,'bid',dec(self.bid)); object.__setattr__(self,'ask',dec(self.ask))
        if self.bid<=0 or self.ask<=0 or self.ask<self.bid: raise ValueError('invalid bid/ask quote')
        if self.known_time_ms<self.source_time_ms: raise ValueError('known_time before source_time')
    @property
    def spread(self): return self.ask-self.bid
    @property
    def quote_id(self): return stable_id('uceq',self.to_dict())
    def age_ms(self,decision_time_ms:int): return max(0,decision_time_ms-self.known_time_ms)
    def to_dict(self): return {'symbol':self.symbol,'bid':self.bid,'ask':self.ask,'source_time_ms':self.source_time_ms,'known_time_ms':self.known_time_ms,'source_id':self.source_id,'sequence':self.sequence}

@dataclass(frozen=True,slots=True)
class CurrencyConversionQuote:
    from_currency:str; to_currency:str; bid:Decimal; ask:Decimal; source_time_ms:int; known_time_ms:int; source_id:str='terminal'
    def __post_init__(self):
        safe_id(self.from_currency,'from_currency'); safe_id(self.to_currency,'to_currency'); object.__setattr__(self,'bid',dec(self.bid)); object.__setattr__(self,'ask',dec(self.ask))
        if self.bid<=0 or self.ask<self.bid: raise ValueError('invalid conversion quote')
    def conservative_rate(self,amount_sign:int=1)->Decimal: return self.bid if amount_sign>=0 else self.ask
    @property
    def conversion_id(self): return stable_id('ucefx',self.to_dict())
    def to_dict(self): return {'from_currency':self.from_currency,'to_currency':self.to_currency,'bid':self.bid,'ask':self.ask,'source_time_ms':self.source_time_ms,'known_time_ms':self.known_time_ms,'source_id':self.source_id}

@dataclass(frozen=True,slots=True)
class SymbolEconomicsSpec:
    symbol:str; base_currency:str; profit_currency:str; margin_currency:str; digits:int; point:Decimal; tick_size:Decimal;
    tick_value_profit:Decimal; tick_value_loss:Decimal; contract_size:Decimal; volume_min:Decimal; volume_max:Decimal; volume_step:Decimal;
    stops_level_points:int=0; freeze_level_points:int=0; trade_status:TradeStatus=TradeStatus.ENABLED; allowed_order_kinds:tuple[OrderKind,...]=(OrderKind.MARKET,OrderKind.LIMIT,OrderKind.STOP);
    allowed_filling_modes:tuple[str,...]=('fok','ioc','return'); margin_mode:MarginMode=MarginMode.LEVERAGE; leverage:Decimal=Decimal('100'); margin_rate:Decimal=Decimal('0'); margin_per_lot:Decimal=Decimal('0');
    spec_time_ms:int=0; known_time_ms:int=0; broker_id:str='fixture'; version:str='1.0.0'
    def __post_init__(self):
        safe_id(self.symbol,'symbol'); safe_id(self.version,'version')
        for n in ('point','tick_size','tick_value_profit','tick_value_loss','contract_size','volume_min','volume_max','volume_step','leverage','margin_rate','margin_per_lot'): object.__setattr__(self,n,dec(getattr(self,n)))
        if min(self.point,self.tick_size,self.contract_size,self.volume_step)<=0: raise ValueError('non-positive symbol unit')
        if self.volume_min<0 or self.volume_max<self.volume_min: raise ValueError('invalid volume bounds')
        if self.tick_value_loss<=0 or self.tick_value_profit<=0: raise ValueError('tick values must be positive')
    @property
    def definition_id(self): return stable_id('ucespec',self.to_dict())
    def age_ms(self,decision_time_ms:int): return max(0,decision_time_ms-self.known_time_ms)
    def value_per_price_unit_per_lot(self,loss:bool=True)->Decimal:
        return (self.tick_value_loss if loss else self.tick_value_profit)/self.tick_size
    def to_dict(self):
        return {'symbol':self.symbol,'base_currency':self.base_currency,'profit_currency':self.profit_currency,'margin_currency':self.margin_currency,'digits':self.digits,'point':self.point,'tick_size':self.tick_size,'tick_value_profit':self.tick_value_profit,'tick_value_loss':self.tick_value_loss,'contract_size':self.contract_size,'volume_min':self.volume_min,'volume_max':self.volume_max,'volume_step':self.volume_step,'stops_level_points':self.stops_level_points,'freeze_level_points':self.freeze_level_points,'trade_status':self.trade_status.value,'allowed_order_kinds':[x.value for x in self.allowed_order_kinds],'allowed_filling_modes':list(self.allowed_filling_modes),'margin_mode':self.margin_mode.value,'leverage':self.leverage,'margin_rate':self.margin_rate,'margin_per_lot':self.margin_per_lot,'spec_time_ms':self.spec_time_ms,'known_time_ms':self.known_time_ms,'broker_id':self.broker_id,'version':self.version}

@dataclass(frozen=True,slots=True)
class AccountEconomicSnapshot:
    account_id:str; currency:str; balance:Decimal; equity:Decimal; free_margin:Decimal; margin_used:Decimal; peak_equity:Decimal;
    daily_realized_pnl:Decimal=Decimal('0'); daily_unrealized_pnl:Decimal=Decimal('0'); open_planned_risk:Decimal=Decimal('0'); reserved_risk:Decimal=Decimal('0');
    account_time_ms:int=0; known_time_ms:int=0; symbol_risk:Mapping[str,Decimal]=field(default_factory=dict); strategy_risk:Mapping[str,Decimal]=field(default_factory=dict); group_risk:Mapping[str,Decimal]=field(default_factory=dict)
    def __post_init__(self):
        safe_id(self.account_id,'account_id'); safe_id(self.currency,'currency')
        for n in ('balance','equity','free_margin','margin_used','peak_equity','daily_realized_pnl','daily_unrealized_pnl','open_planned_risk','reserved_risk'): object.__setattr__(self,n,dec(getattr(self,n)))
        if min(self.balance,self.equity,self.free_margin,self.peak_equity)<0: raise ValueError('negative account base value')
    @property
    def drawdown_fraction(self): return Decimal('0') if self.peak_equity<=0 else max(Decimal('0'),(self.peak_equity-self.equity)/self.peak_equity)
    @property
    def daily_loss(self): return max(Decimal('0'),-(self.daily_realized_pnl+self.daily_unrealized_pnl))
    @property
    def snapshot_id(self): return stable_id('uceacct',self.to_dict())
    def to_dict(self): return {'account_id':self.account_id,'currency':self.currency,'balance':self.balance,'equity':self.equity,'free_margin':self.free_margin,'margin_used':self.margin_used,'peak_equity':self.peak_equity,'daily_realized_pnl':self.daily_realized_pnl,'daily_unrealized_pnl':self.daily_unrealized_pnl,'open_planned_risk':self.open_planned_risk,'reserved_risk':self.reserved_risk,'account_time_ms':self.account_time_ms,'known_time_ms':self.known_time_ms,'symbol_risk':canonical_value(self.symbol_risk),'strategy_risk':canonical_value(self.strategy_risk),'group_risk':canonical_value(self.group_risk)}

@dataclass(frozen=True,slots=True)
class ExecutablePriceRequest:
    side:TradeSide; role:ExecutionRole; order_kind:OrderKind; decision_time_ms:int; logical_price:Decimal|None=None; adverse_slippage_points:Decimal=Decimal('0'); latency_ms:int=0
    def __post_init__(self):
        if self.logical_price is not None: object.__setattr__(self,'logical_price',dec(self.logical_price))
        object.__setattr__(self,'adverse_slippage_points',dec(self.adverse_slippage_points))
    def to_dict(self): return {'side':self.side.value,'role':self.role.value,'order_kind':self.order_kind.value,'decision_time_ms':self.decision_time_ms,'logical_price':self.logical_price,'adverse_slippage_points':self.adverse_slippage_points,'latency_ms':self.latency_ms}

@dataclass(frozen=True,slots=True)
class ExecutablePriceResult:
    request_id:str; quote_id:str; base_executable_price:Decimal; slippage_amount:Decimal; executable_price:Decimal; spread_amount:Decimal; used_quote_side:str; accepted:bool; reason_code:str='ok'
    @property
    def result_id(self): return stable_id('ucepx',self.to_dict())
    def to_dict(self): return {'request_id':self.request_id,'quote_id':self.quote_id,'base_executable_price':self.base_executable_price,'slippage_amount':self.slippage_amount,'executable_price':self.executable_price,'spread_amount':self.spread_amount,'used_quote_side':self.used_quote_side,'accepted':self.accepted,'reason_code':self.reason_code}

@dataclass(frozen=True,slots=True)
class CommissionRule:
    rule_id:str; basis:CommissionBasis; amount:Decimal=Decimal('0'); minimum:Decimal=Decimal('0'); maximum:Decimal|None=None; applies_entry:bool=True; applies_exit:bool=True; currency:str=''
    def __post_init__(self): object.__setattr__(self,'amount',dec(self.amount)); object.__setattr__(self,'minimum',dec(self.minimum)); object.__setattr__(self,'maximum',None if self.maximum is None else dec(self.maximum)); safe_id(self.rule_id,'rule_id')
    def to_dict(self): return {'rule_id':self.rule_id,'basis':self.basis.value,'amount':self.amount,'minimum':self.minimum,'maximum':self.maximum,'applies_entry':self.applies_entry,'applies_exit':self.applies_exit,'currency':self.currency}

@dataclass(frozen=True,slots=True)
class SlippageRule:
    rule_id:str; kind:SlippageModelKind; entry_long_points:Decimal=Decimal('0'); entry_short_points:Decimal=Decimal('0'); exit_long_points:Decimal=Decimal('0'); exit_short_points:Decimal=Decimal('0'); volatility_multiplier:Decimal=Decimal('0'); percentile:Decimal=Decimal('0.99')
    def __post_init__(self):
        for n in ('entry_long_points','entry_short_points','exit_long_points','exit_short_points','volatility_multiplier','percentile'): object.__setattr__(self,n,dec(getattr(self,n)))
    def points(self,side:TradeSide,is_entry:bool,volatility_points:Decimal=Decimal('0')):
        base=(self.entry_long_points if side is TradeSide.LONG else self.entry_short_points) if is_entry else (self.exit_long_points if side is TradeSide.LONG else self.exit_short_points)
        return max(Decimal('0'),base+self.volatility_multiplier*dec(volatility_points))
    def to_dict(self): return {'rule_id':self.rule_id,'kind':self.kind.value,'entry_long_points':self.entry_long_points,'entry_short_points':self.entry_short_points,'exit_long_points':self.exit_long_points,'exit_short_points':self.exit_short_points,'volatility_multiplier':self.volatility_multiplier,'percentile':self.percentile}

@dataclass(frozen=True,slots=True)
class FinancingRule:
    basis:FinancingBasis=FinancingBasis.NONE; long_amount:Decimal=Decimal('0'); short_amount:Decimal=Decimal('0'); triple_day:int=3
    def __post_init__(self): object.__setattr__(self,'long_amount',dec(self.long_amount)); object.__setattr__(self,'short_amount',dec(self.short_amount))
    def to_dict(self): return {'basis':self.basis.value,'long_amount':self.long_amount,'short_amount':self.short_amount,'triple_day':self.triple_day}

@dataclass(frozen=True,slots=True)
class CostModelDescriptor:
    model_id:str; version:str; spread_source:SpreadSource=SpreadSource.OBSERVED; spread_floor_points:Decimal=Decimal('0'); spread_percentile_points:Decimal=Decimal('0');
    commission_rules:tuple[CommissionRule,...]=(); slippage_rule:SlippageRule=field(default_factory=lambda:SlippageRule('none',SlippageModelKind.FIXED_POINTS)); financing_rule:FinancingRule=field(default_factory=FinancingRule);
    tax_bps:Decimal=Decimal('0'); conversion_cost_bps:Decimal=Decimal('0'); reserve_multiplier:Decimal=Decimal('1'); max_quote_age_ms:int=2000; max_spec_age_ms:int=86400000; tags:Mapping[str,str]=field(default_factory=dict)
    def __post_init__(self):
        safe_id(self.model_id,'model_id'); safe_id(self.version,'version')
        for n in ('spread_floor_points','spread_percentile_points','tax_bps','conversion_cost_bps','reserve_multiplier'): object.__setattr__(self,n,dec(getattr(self,n)))
    @property
    def exact_key(self): return f'{self.model_id}@{self.version}'
    @property
    def definition_id(self): return stable_id('ucecost',self.to_dict())
    def to_dict(self): return {'model_id':self.model_id,'version':self.version,'spread_source':self.spread_source.value,'spread_floor_points':self.spread_floor_points,'spread_percentile_points':self.spread_percentile_points,'commission_rules':[x.to_dict() for x in self.commission_rules],'slippage_rule':self.slippage_rule.to_dict(),'financing_rule':self.financing_rule.to_dict(),'tax_bps':self.tax_bps,'conversion_cost_bps':self.conversion_cost_bps,'reserve_multiplier':self.reserve_multiplier,'max_quote_age_ms':self.max_quote_age_ms,'max_spec_age_ms':self.max_spec_age_ms,'tags':canonical_value(self.tags)}

@dataclass(frozen=True,slots=True)
class RiskGeometry:
    treatment_id:str; side:TradeSide; order_kind:OrderKind; logical_entry_price:Decimal; logical_stop_price:Decimal; logical_target_price:Decimal|None=None; entry_transactions:int=1; exit_transactions:int=1; expected_holding_days:Decimal=Decimal('0'); gap_reserve_points:Decimal=Decimal('0'); volatility_points:Decimal=Decimal('0')
    def __post_init__(self):
        for n in ('logical_entry_price','logical_stop_price','expected_holding_days','gap_reserve_points','volatility_points'): object.__setattr__(self,n,dec(getattr(self,n)))
        if self.logical_target_price is not None: object.__setattr__(self,'logical_target_price',dec(self.logical_target_price))
        if self.side is TradeSide.LONG and self.logical_stop_price>=self.logical_entry_price: raise ValueError('long stop must be below entry')
        if self.side is TradeSide.SHORT and self.logical_stop_price<=self.logical_entry_price: raise ValueError('short stop must be above entry')
    @property
    def geometry_id(self): return stable_id('ucegeo',self.to_dict())
    def to_dict(self): return {'treatment_id':self.treatment_id,'side':self.side.value,'order_kind':self.order_kind.value,'logical_entry_price':self.logical_entry_price,'logical_stop_price':self.logical_stop_price,'logical_target_price':self.logical_target_price,'entry_transactions':self.entry_transactions,'exit_transactions':self.exit_transactions,'expected_holding_days':self.expected_holding_days,'gap_reserve_points':self.gap_reserve_points,'volatility_points':self.volatility_points}

@dataclass(frozen=True,slots=True)
class CostBreakdown:
    spread_cash:Decimal; entry_slippage_cash:Decimal; exit_slippage_cash:Decimal; commission_cash:Decimal; financing_cash:Decimal; tax_cash:Decimal; conversion_cash:Decimal; gap_reserve_cash:Decimal
    @property
    def total_cash(self): return sum((self.spread_cash,self.entry_slippage_cash,self.exit_slippage_cash,self.commission_cash,self.financing_cash,self.tax_cash,self.conversion_cash,self.gap_reserve_cash),Decimal('0'))
    def to_dict(self): return {'spread_cash':self.spread_cash,'entry_slippage_cash':self.entry_slippage_cash,'exit_slippage_cash':self.exit_slippage_cash,'commission_cash':self.commission_cash,'financing_cash':self.financing_cash,'tax_cash':self.tax_cash,'conversion_cash':self.conversion_cash,'gap_reserve_cash':self.gap_reserve_cash,'total_cash':self.total_cash}

@dataclass(frozen=True,slots=True)
class CapitalRequest:
    request_id:str; account_id:str; treatment_id:str; strategy_id:str; symbol:str; correlation_group:str; decision_time_ms:int; confidence:Decimal=Decimal('0.5'); expected_win_probability:Decimal=Decimal('0.5'); expected_win_loss_ratio:Decimal=Decimal('1'); volatility_fraction:Decimal=Decimal('0'); tags:Mapping[str,str]=field(default_factory=dict)
    def __post_init__(self):
        for n in ('confidence','expected_win_probability','expected_win_loss_ratio','volatility_fraction'): object.__setattr__(self,n,dec(getattr(self,n)))
        safe_id(self.request_id,'request_id')
    def to_dict(self): return {'request_id':self.request_id,'account_id':self.account_id,'treatment_id':self.treatment_id,'strategy_id':self.strategy_id,'symbol':self.symbol,'correlation_group':self.correlation_group,'decision_time_ms':self.decision_time_ms,'confidence':self.confidence,'expected_win_probability':self.expected_win_probability,'expected_win_loss_ratio':self.expected_win_loss_ratio,'volatility_fraction':self.volatility_fraction,'tags':canonical_value(self.tags)}

@dataclass(frozen=True,slots=True)
class CapitalBudget:
    request_id:str; policy_definition_ids:tuple[str,...]; requested_cash:Decimal; approved_cash:Decimal; reductions:Mapping[str,Decimal]; accepted:bool; reason_code:str='ok'
    @property
    def budget_id(self): return stable_id('ucebudget',self.to_dict())
    def to_dict(self): return {'request_id':self.request_id,'policy_definition_ids':list(self.policy_definition_ids),'requested_cash':self.requested_cash,'approved_cash':self.approved_cash,'reductions':canonical_value(self.reductions),'accepted':self.accepted,'reason_code':self.reason_code}

@dataclass(frozen=True,slots=True)
class EconomicEnvelope:
    treatment_id:str; geometry_id:str; quote_id:str; symbol_spec_id:str; cost_model_definition_id:str; capital_budget_id:str; side:TradeSide;
    entry_executable_price:Decimal; stop_executable_price:Decimal; target_executable_price:Decimal|None; normalized_volume:Decimal; raw_volume:Decimal;
    price_loss_cash:Decimal; costs:CostBreakdown; maximum_loss_cash:Decimal; target_gross_cash:Decimal; target_net_cash:Decimal; margin_required:Decimal;
    risk_budget_cash:Decimal; cash_risk_utilization:Decimal; accepted:bool; reason_code:str; adjustments:tuple[str,...]=(); decision_time_ms:int=0; metadata:Mapping[str,Any]=field(default_factory=dict)
    @property
    def envelope_id(self): return stable_id('uceecon',self.to_dict())
    def to_dict(self): return {'treatment_id':self.treatment_id,'geometry_id':self.geometry_id,'quote_id':self.quote_id,'symbol_spec_id':self.symbol_spec_id,'cost_model_definition_id':self.cost_model_definition_id,'capital_budget_id':self.capital_budget_id,'side':self.side.value,'entry_executable_price':self.entry_executable_price,'stop_executable_price':self.stop_executable_price,'target_executable_price':self.target_executable_price,'normalized_volume':self.normalized_volume,'raw_volume':self.raw_volume,'price_loss_cash':self.price_loss_cash,'costs':self.costs.to_dict(),'maximum_loss_cash':self.maximum_loss_cash,'target_gross_cash':self.target_gross_cash,'target_net_cash':self.target_net_cash,'margin_required':self.margin_required,'risk_budget_cash':self.risk_budget_cash,'cash_risk_utilization':self.cash_risk_utilization,'accepted':self.accepted,'reason_code':self.reason_code,'adjustments':list(self.adjustments),'decision_time_ms':self.decision_time_ms,'metadata':canonical_value(self.metadata)}

@dataclass(frozen=True,slots=True)
class ReservationEvent:
    sequence:int; action:LedgerAction; reservation_id:str; account_id:str; treatment_id:str; symbol:str; strategy_id:str; correlation_group:str; amount_cash:Decimal; event_time_ms:int; known_time_ms:int; prior_hash:str; reason:str=''; metadata:Mapping[str,Any]=field(default_factory=dict)
    @property
    def event_hash(self): return stable_id('ucerlev',self.to_dict(include_hash=False),64)
    def to_dict(self,include_hash=True):
        d={'sequence':self.sequence,'action':self.action.value,'reservation_id':self.reservation_id,'account_id':self.account_id,'treatment_id':self.treatment_id,'symbol':self.symbol,'strategy_id':self.strategy_id,'correlation_group':self.correlation_group,'amount_cash':self.amount_cash,'event_time_ms':self.event_time_ms,'known_time_ms':self.known_time_ms,'prior_hash':self.prior_hash,'reason':self.reason,'metadata':canonical_value(self.metadata)}
        if include_hash: d['event_hash']=self.event_hash
        return d

@dataclass(frozen=True,slots=True)
class ReservationRecord:
    reservation_id:str; account_id:str; treatment_id:str; symbol:str; strategy_id:str; correlation_group:str; reserved_cash:Decimal; consumed_cash:Decimal; released_cash:Decimal; state:ReservationState; last_sequence:int; last_event_hash:str
    @property
    def open_cash(self): return max(Decimal('0'),self.reserved_cash-self.consumed_cash-self.released_cash)
    def to_dict(self): return {'reservation_id':self.reservation_id,'account_id':self.account_id,'treatment_id':self.treatment_id,'symbol':self.symbol,'strategy_id':self.strategy_id,'correlation_group':self.correlation_group,'reserved_cash':self.reserved_cash,'consumed_cash':self.consumed_cash,'released_cash':self.released_cash,'open_cash':self.open_cash,'state':self.state.value,'last_sequence':self.last_sequence,'last_event_hash':self.last_event_hash}

@dataclass(frozen=True,slots=True)
class StressScenario:
    scenario_id:str; version:str; kind:StressKind; magnitude:Decimal; expected_direction:str='non_improving'; enabled:bool=True
    def __post_init__(self): object.__setattr__(self,'magnitude',dec(self.magnitude)); safe_id(self.scenario_id,'scenario_id')
    @property
    def definition_id(self): return stable_id('ucestress',self.to_dict())
    def to_dict(self): return {'scenario_id':self.scenario_id,'version':self.version,'kind':self.kind.value,'magnitude':self.magnitude,'expected_direction':self.expected_direction,'enabled':self.enabled}

@dataclass(frozen=True,slots=True)
class StressResult:
    scenario_definition_id:str; baseline_envelope_id:str; stressed_envelope_id:str; baseline_max_loss:Decimal; stressed_max_loss:Decimal; baseline_volume:Decimal; stressed_volume:Decimal; passed_monotonicity:bool; accepted:bool; reason_code:str
    def to_dict(self): return {'scenario_definition_id':self.scenario_definition_id,'baseline_envelope_id':self.baseline_envelope_id,'stressed_envelope_id':self.stressed_envelope_id,'baseline_max_loss':self.baseline_max_loss,'stressed_max_loss':self.stressed_max_loss,'baseline_volume':self.baseline_volume,'stressed_volume':self.stressed_volume,'passed_monotonicity':self.passed_monotonicity,'accepted':self.accepted,'reason_code':self.reason_code}

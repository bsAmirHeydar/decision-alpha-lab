from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass(frozen=True)
class PatternSpec:
    code: str
    expression: re.Pattern[str]
    authority_class: str | None = None
    severity: str = "EVIDENCE"

# Patterns describe legacy source text. Their presence is evidence, not authority.
def _p(code: str, expression: str, authority: str | None = None, severity: str = "EVIDENCE") -> PatternSpec:
    return PatternSpec(code, re.compile(expression, re.IGNORECASE), authority, severity)

TREATMENT_PATTERNS = (
    _p("ENTRY_MARKET", r"\b(?:market[_ ]?entry|entry[_ ]?market|\.Buy\s*\(|\.Sell\s*\()"),
    _p("ENTRY_LIMIT", r"\b(?:BuyLimit|SellLimit|limit[_ ]?order|ORDER_TYPE_(?:BUY|SELL)_LIMIT)\b"),
    _p("ENTRY_STOP", r"\b(?:BuyStop|SellStop|stop[_ ]?order|ORDER_TYPE_(?:BUY|SELL)_STOP)\b"),
    _p("ENTRY_PRICE", r"\b(?:entry_price|entryprice|planned_entry|signal\.entry|plan\.entry)\b"),
    _p("STOP_LOSS", r"\b(?:stop[_ ]?loss|stoploss|stop_price|stopdistance|sl_points|signal\.sl|plan\.sl|\bSL\b)"),
    _p("TAKE_PROFIT", r"\b(?:take[_ ]?profit|takeprofit|target_price|profit_target|tp_points|signal\.tp|plan\.tp|\bTP\b)"),
    _p("CANCELLATION", r"\b(?:cancel(?:lation|led)?|OrderDelete|delete_pending|cancel_order)\b"),
    _p("EXPIRY", r"\b(?:expir(?:y|ation|ed)|ORDER_TIME_(?:DAY|SPECIFIED|SPECIFIED_DAY)|time[_ ]?in[_ ]?force)\b"),
    _p("VOLUME_SIZING", r"\b(?:position[_ ]?siz|volume_step|lot[_ ]?size|lots?\b|risk[_ ]?(?:pct|percent|fraction)|NormalizeVolume|calc(?:ulate)?_volume)"),
    _p("PARTIAL_EXIT", r"\b(?:PositionClosePartial|partial[_ ]?(?:close|exit)|scale[_ ]?out)\b"),
    _p("BREAKEVEN", r"\b(?:break[_ ]?even|breakeven|move[_ ]?to[_ ]?be)\b"),
    _p("TRAILING", r"\b(?:trailing|trail[_ ]?(?:stop|distance|step)|update[_ ]?trail)\b"),
    _p("TIME_EXIT", r"\b(?:time[_ ]?exit|max[_ ]?hold|holding[_ ]?period|close[_ ]?after|exit[_ ]?time)\b"),
    _p("RECONCILIATION", r"\b(?:reconcil|PositionSelect|PositionsTotal|HistorySelect|HistoryDeal|HistoryOrder|OrderSelect)\b"),
    _p("DUPLICATE_GUARD", r"\b(?:duplicate[_ ]?(?:order|decision|signal)|already[_ ]?(?:open|submitted)|magic(?:_number)?|expert_magic)\b"),
    _p("SPREAD_PRICING", r"\b(?:spread|slippage|deviation_points|tick_size|trade_tick_size|SYMBOL_POINT|SYMBOL_DIGITS)\b"),
    _p("SESSION_GATE", r"\b(?:session[_ ]?(?:gate|filter|start|end)|trading[_ ]?hours|market[_ ]?open|trade[_ ]?allowed)\b"),
)

CAPABILITY_PATTERNS = (
    _p("BROKER_REQUEST_BUILD", r"\b(?:MqlTradeRequest|OrderCheck)\b", "CREATE_REQUEST_INTENT", "HIGH"),
    _p("BROKER_SUBMIT_RAW", r"\bOrderSend(?:Async)?\s*\(", "SUBMIT_ORDER", "CRITICAL"),
    _p("BROKER_SUBMIT_CTRADE", r"(?:\b|\.)(?:Buy|Sell|BuyLimit|SellLimit|BuyStop|SellStop|BuyStopLimit|SellStopLimit)\s*\(", "SUBMIT_ORDER", "CRITICAL"),
    _p("BROKER_POSITION_OPEN", r"\bPositionOpen\s*\(", "SUBMIT_ORDER", "CRITICAL"),
    _p("BROKER_POSITION_MODIFY", r"\bPositionModify\s*\(", "MODIFY_POSITION", "CRITICAL"),
    _p("BROKER_ORDER_MODIFY", r"\bOrderModify\s*\(", "MODIFY_ORDER", "CRITICAL"),
    _p("BROKER_ORDER_CANCEL", r"\bOrderDelete\s*\(", "CANCEL_ORDER", "CRITICAL"),
    _p("BROKER_POSITION_CLOSE", r"\bPositionClose(?:Partial)?\s*\(", "CLOSE_POSITION", "CRITICAL"),
    _p("BROKER_STATE_POSITION", r"\b(?:PositionSelect|PositionGet|PositionsTotal)\w*\s*\(", "RECONCILE_BROKER_STATE", "HIGH"),
    _p("BROKER_STATE_ORDER", r"\b(?:OrderSelect|OrderGet|OrdersTotal)\w*\s*\(", "RECONCILE_BROKER_STATE", "HIGH"),
    _p("BROKER_STATE_HISTORY", r"\b(?:HistorySelect|HistoryDeal|HistoryOrder)\w*\s*\(", "RECONCILE_BROKER_STATE", "HIGH"),
    _p("BROKER_SYMBOL_STATE", r"\bSymbolInfo(?:Double|Integer|String|Tick)\s*\(", "READ_BROKER_CONSTRAINTS", "MEDIUM"),
    _p("BROKER_ACCOUNT_STATE", r"\bAccountInfo(?:Double|Integer|String)\s*\(", "READ_ACCOUNT_STATE", "HIGH"),
    _p("FILE_LEDGER_READ", r"\bFileOpen\s*\(|\b(?:read_text|read_bytes|open)\s*\(", "READ_FILE_LEDGER", "MEDIUM"),
    _p("FILE_LEDGER_WRITE", r"\b(?:FileWrite|FileWriteString|FileDelete|FileMove|write_text|write_bytes|unlink|replace)\s*\(", "MUTATE_FILE_LEDGER", "HIGH"),
    _p("NETWORK_EXTERNAL", r"\b(?:WebRequest|SocketCreate|socket\.|requests\.|httpx\.|urllib\.)", "NETWORK_EXTERNAL", "CRITICAL"),
    _p("DYNAMIC_LIBRARY", r'#import\s+"|\b(?:ctypes|LoadLibrary|ShellExecute|WinExec)\b', "NATIVE_OR_PROCESS_EXTERNAL", "CRITICAL"),
)

RISK_PATTERNS = (
    _p("POINT_CONVERSION", r"\b(?:_Point|Point\s*\(|SYMBOL_POINT|points_to_price|price_to_points)\b"),
    _p("TICK_SIZE", r"\b(?:SYMBOL_TRADE_TICK_SIZE|tick_size|trade_tick_size)\b"),
    _p("TICK_VALUE", r"\b(?:SYMBOL_TRADE_TICK_VALUE|tick_value)\b"),
    _p("VOLUME_MIN", r"\b(?:SYMBOL_VOLUME_MIN|volume_min|min_lot)\b"),
    _p("VOLUME_MAX", r"\b(?:SYMBOL_VOLUME_MAX|volume_max|max_lot)\b"),
    _p("VOLUME_STEP", r"\b(?:SYMBOL_VOLUME_STEP|volume_step|lot_step)\b"),
    _p("STOP_LEVEL", r"\b(?:SYMBOL_TRADE_STOPS_LEVEL|stops_level|stop_level)\b"),
    _p("FREEZE_LEVEL", r"\b(?:SYMBOL_TRADE_FREEZE_LEVEL|freeze_level)\b"),
    _p("SPREAD_ASSUMPTION", r"\b(?:spread|SYMBOL_SPREAD|ask\s*-\s*bid)\b"),
    _p("SLIPPAGE_DEVIATION", r"\b(?:slippage|deviation_points|SetDeviationInPoints)\b"),
    _p("DUPLICATE_DECISION", r"\b(?:duplicate|idempot|already[_ ]?(?:sent|open)|decision[_ ]?key)\b"),
    _p("SESSION_ASSUMPTION", r"\b(?:session|market[_ ]?hours|trade[_ ]?session|daylight|DST)\b"),
    _p("LONG_SHORT_ASYMMETRY", r"\b(?:sell[_ ]?stop[_ ]?spread|long[_ ]?only|short[_ ]?only|buy[_ ]?only|sell[_ ]?only)\b"),
)

MODE_PATTERNS = (
    ("TESTER", re.compile(r"\b(?:MQL_TESTER|IsTesting|tester|backtest|pytest|unittest|tests?/)\b", re.IGNORECASE)),
    ("DRY_RUN", re.compile(r"\b(?:dry[_ -]?run|no[_ -]?send|preview[_ -]?only)\b", re.IGNORECASE)),
    ("PAPER", re.compile(r"\b(?:paper[_ -]?trade|paper[_ -]?broker|simulation[_ -]?broker)\b", re.IGNORECASE)),
    ("SHADOW", re.compile(r"\bshadow(?:[_ -]?mode|[_ -]?run)?\b", re.IGNORECASE)),
    ("LIVE", re.compile(r"\b(?:live[_ -]?mode|real[_ -]?execution|production[_ -]?trade)\b", re.IGNORECASE)),
)

BROKER_CAPABILITY_CODES = frozenset(spec.code for spec in CAPABILITY_PATTERNS if spec.authority_class in {
    "CREATE_REQUEST_INTENT", "SUBMIT_ORDER", "MODIFY_POSITION", "MODIFY_ORDER", "CANCEL_ORDER", "CLOSE_POSITION",
    "RECONCILE_BROKER_STATE", "READ_BROKER_CONSTRAINTS", "READ_ACCOUNT_STATE"
})
ORDER_MUTATION_CODES = frozenset(spec.code for spec in CAPABILITY_PATTERNS if spec.authority_class in {
    "SUBMIT_ORDER", "MODIFY_POSITION", "MODIFY_ORDER", "CANCEL_ORDER", "CLOSE_POSITION"
})

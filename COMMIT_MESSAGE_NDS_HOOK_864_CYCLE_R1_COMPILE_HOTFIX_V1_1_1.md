fix(nds): use canonical paper-limit trade action in backtest stats

Replace the stale FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT_READY reference with
FP_NDS_HOOK_TRADE_ACTION_PAPER_LIMIT in FP_NDSBacktestUpdateStats.

Add repository-wide QA that resolves every FP_NDS_HOOK_TRADE_ACTION_* reference
against the canonical enum in FP_NDSHookTradeTypes.mqh.

No setup, Phase04 closure, first-arrival, order, risk, broker, persistence, or
capital behavior changes.

Repository Phase 55 bounded QA passes. Windows MetaEditor compilation remains
an external acceptance gate.

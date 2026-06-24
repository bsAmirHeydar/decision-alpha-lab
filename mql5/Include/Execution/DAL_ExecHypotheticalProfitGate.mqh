#ifndef __DAL_EXEC_HYPOTHETICAL_PROFIT_GATE_MQH__
#define __DAL_EXEC_HYPOTHETICAL_PROFIT_GATE_MQH__

// Decision Alpha Lab — reusable two-layer hypothetical profit gate.
// Pure MQL5. No Python. No external scripts.
//
// Purpose:
// - Layer 1 is a hypothetical/shadow trade stream.
// - Layer 2 is the real execution stream.
// - When the gate is closed, valid signals are NOT traded live. The first valid
//   signal is tracked hypothetically with the same entry, SL and TP.
// - If the hypothetical trade wins, the gate opens and the NEXT signals are allowed live.
// - If the hypothetical trade loses, the gate stays closed and waits for the next
//   hypothetical trade to win.
// - When the gate is open, real trades are allowed. A real winning trade keeps the
//   gate open. A real losing or flat trade closes the gate again.
//
// The module does not create entries, calculate stops, size positions, or send orders.
// It only decides whether the next signal may pass to live execution.

struct DALExecHypotheticalProfitGateConfig
{
   bool enabled;
   bool start_open;
   bool persist_state;
   string state_key;
   bool print_logs;
};

struct DALExecHypotheticalProfitGateState
{
   bool initialized;
   bool live_allowed;
   bool active_virtual;
   int cycle_id;
   int virtual_direction;
   datetime virtual_signal_time;
   datetime virtual_open_time;
   double virtual_entry;
   double virtual_stop;
   double virtual_take_profit;
   double last_virtual_net_r;
   double last_real_profit;
   ulong last_real_deal_ticket;
   string last_reason;
};

string DAL_ExecHypoGateBoolToString(const bool v)
{
   return (v ? "true" : "false");
}

void DAL_ExecHypoGateDefaults(DALExecHypotheticalProfitGateConfig &cfg)
{
   cfg.enabled = true;
   cfg.start_open = false;
   cfg.persist_state = true;
   cfg.state_key = "default";
   cfg.print_logs = false;
}

void DAL_ExecHypoGateResetState(DALExecHypotheticalProfitGateState &st)
{
   st.initialized = false;
   st.live_allowed = false;
   st.active_virtual = false;
   st.cycle_id = 0;
   st.virtual_direction = 0;
   st.virtual_signal_time = 0;
   st.virtual_open_time = 0;
   st.virtual_entry = 0.0;
   st.virtual_stop = 0.0;
   st.virtual_take_profit = 0.0;
   st.last_virtual_net_r = 0.0;
   st.last_real_profit = 0.0;
   st.last_real_deal_ticket = 0;
   st.last_reason = "not_initialized";
}

string DAL_ExecHypoGatePrefix(const DALExecHypotheticalProfitGateConfig &cfg)
{
   long login = (long)AccountInfoInteger(ACCOUNT_LOGIN);
   string key = cfg.state_key;
   if(key == "")
      key = "default";
   return "DAL_HYPO_GATE_" + IntegerToString((int)login) + "_" + key;
}

void DAL_ExecHypoGateSave(const DALExecHypotheticalProfitGateConfig &cfg, const DALExecHypotheticalProfitGateState &st)
{
   if(!cfg.persist_state)
      return;

   string p = DAL_ExecHypoGatePrefix(cfg);
   GlobalVariableSet(p + "_initialized", st.initialized ? 1.0 : 0.0);
   GlobalVariableSet(p + "_live_allowed", st.live_allowed ? 1.0 : 0.0);
   GlobalVariableSet(p + "_active_virtual", st.active_virtual ? 1.0 : 0.0);
   GlobalVariableSet(p + "_cycle_id", (double)st.cycle_id);
   GlobalVariableSet(p + "_virtual_direction", (double)st.virtual_direction);
   GlobalVariableSet(p + "_virtual_signal_time", (double)st.virtual_signal_time);
   GlobalVariableSet(p + "_virtual_open_time", (double)st.virtual_open_time);
   GlobalVariableSet(p + "_virtual_entry", st.virtual_entry);
   GlobalVariableSet(p + "_virtual_stop", st.virtual_stop);
   GlobalVariableSet(p + "_virtual_take_profit", st.virtual_take_profit);
   GlobalVariableSet(p + "_last_virtual_net_r", st.last_virtual_net_r);
   GlobalVariableSet(p + "_last_real_profit", st.last_real_profit);
   GlobalVariableSet(p + "_last_real_deal_ticket", (double)st.last_real_deal_ticket);
}

bool DAL_ExecHypoGateLoad(const DALExecHypotheticalProfitGateConfig &cfg, DALExecHypotheticalProfitGateState &st)
{
   if(!cfg.persist_state)
      return false;

   string p = DAL_ExecHypoGatePrefix(cfg);
   if(!GlobalVariableCheck(p + "_initialized"))
      return false;

   st.initialized = (GlobalVariableGet(p + "_initialized") > 0.5);
   st.live_allowed = (GlobalVariableGet(p + "_live_allowed") > 0.5);
   st.active_virtual = (GlobalVariableGet(p + "_active_virtual") > 0.5);
   st.cycle_id = (int)GlobalVariableGet(p + "_cycle_id");
   st.virtual_direction = (int)GlobalVariableGet(p + "_virtual_direction");
   st.virtual_signal_time = (datetime)GlobalVariableGet(p + "_virtual_signal_time");
   st.virtual_open_time = (datetime)GlobalVariableGet(p + "_virtual_open_time");
   st.virtual_entry = GlobalVariableGet(p + "_virtual_entry");
   st.virtual_stop = GlobalVariableGet(p + "_virtual_stop");
   st.virtual_take_profit = GlobalVariableGet(p + "_virtual_take_profit");
   st.last_virtual_net_r = GlobalVariableGet(p + "_last_virtual_net_r");
   st.last_real_profit = GlobalVariableGet(p + "_last_real_profit");
   st.last_real_deal_ticket = (ulong)GlobalVariableGet(p + "_last_real_deal_ticket");
   st.last_reason = "loaded";

   return st.initialized;
}

bool DAL_ExecHypoGateInit(DALExecHypotheticalProfitGateConfig &cfg, DALExecHypotheticalProfitGateState &st)
{
   DAL_ExecHypoGateResetState(st);

   if(DAL_ExecHypoGateLoad(cfg, st))
      return true;

   st.initialized = true;
   st.live_allowed = (!cfg.enabled ? true : cfg.start_open);
   st.active_virtual = false;
   st.cycle_id = 1;
   st.last_reason = (st.live_allowed ? "initial_open" : "initial_wait_for_hypothetical_win");

   DAL_ExecHypoGateSave(cfg, st);
   return true;
}

bool DAL_ExecHypoGateShouldTrade(const DALExecHypotheticalProfitGateConfig &cfg, const DALExecHypotheticalProfitGateState &st)
{
   if(!cfg.enabled)
      return true;
   if(!st.initialized)
      return false;
   return st.live_allowed;
}

bool DAL_ExecHypoGateHasActiveVirtual(const DALExecHypotheticalProfitGateState &st)
{
   return st.active_virtual;
}

bool DAL_ExecHypoGateOpenVirtualTrade(
   const DALExecHypotheticalProfitGateConfig &cfg,
   DALExecHypotheticalProfitGateState &st,
   const int direction,
   const double entry_price,
   const double stop_price,
   const double take_profit,
   const datetime signal_time,
   const string reason
)
{
   if(!cfg.enabled)
      return false;
   if(!st.initialized)
      return false;
   if(st.live_allowed)
      return false;
   if(st.active_virtual)
      return false;
   if(direction == 0)
      return false;
   if(entry_price <= 0.0 || stop_price <= 0.0 || take_profit <= 0.0)
      return false;

   if(direction > 0)
   {
      if(!(stop_price < entry_price && take_profit > entry_price))
         return false;
   }
   else
   {
      if(!(stop_price > entry_price && take_profit < entry_price))
         return false;
   }

   st.active_virtual = true;
   st.virtual_direction = direction;
   st.virtual_signal_time = signal_time;
   st.virtual_open_time = TimeCurrent();
   st.virtual_entry = entry_price;
   st.virtual_stop = stop_price;
   st.virtual_take_profit = take_profit;
   st.last_virtual_net_r = 0.0;
   st.last_reason = "virtual_open_" + reason;

   if(cfg.print_logs)
   {
      Print("DAL_HYPO_GATE_VIRTUAL_OPEN *** direction=", (direction > 0 ? "BUY" : "SELL"),
         "*entry=", DoubleToString(entry_price, 8),
         "*sl=", DoubleToString(stop_price, 8),
         "*tp=", DoubleToString(take_profit, 8),
         "*signalTime=", IntegerToString((int)signal_time),
         "*reason=", reason);
   }

   DAL_ExecHypoGateSave(cfg, st);
   return true;
}

int DAL_ExecHypoGateUpdateVirtual(
   const DALExecHypotheticalProfitGateConfig &cfg,
   DALExecHypotheticalProfitGateState &st,
   const string symbol
)
{
   if(!cfg.enabled)
      return 0;
   if(!st.initialized || !st.active_virtual)
      return 0;
   if(symbol == "")
      return 0;

   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   if(bid <= 0.0 || ask <= 0.0)
      return 0;

   bool hit_tp = false;
   bool hit_sl = false;

   if(st.virtual_direction > 0)
   {
      hit_sl = (bid <= st.virtual_stop);
      hit_tp = (bid >= st.virtual_take_profit);
   }
   else if(st.virtual_direction < 0)
   {
      hit_sl = (ask >= st.virtual_stop);
      hit_tp = (ask <= st.virtual_take_profit);
   }
   else
   {
      return 0;
   }

   if(!hit_tp && !hit_sl)
      return 0;

   int result = 0;
   if(hit_tp && !hit_sl)
      result = 1;
   else if(hit_sl && !hit_tp)
      result = -1;
   else
      result = -1;

   double r = MathAbs(st.virtual_entry - st.virtual_stop);
   if(r <= 0.0)
      r = 1.0;

   if(result > 0)
   {
      st.last_virtual_net_r = MathAbs(st.virtual_take_profit - st.virtual_entry) / r;
      st.live_allowed = true;
      st.last_reason = "virtual_win_gate_open_next_signal";
   }
   else
   {
      st.last_virtual_net_r = -1.0;
      st.live_allowed = false;
      st.last_reason = "virtual_loss_keep_waiting";
   }

   st.active_virtual = false;
   st.virtual_direction = 0;
   st.virtual_signal_time = 0;
   st.virtual_open_time = 0;
   st.virtual_entry = 0.0;
   st.virtual_stop = 0.0;
   st.virtual_take_profit = 0.0;

   if(cfg.print_logs)
   {
      Print("DAL_HYPO_GATE_VIRTUAL_CLOSED *** result=", (result > 0 ? "WIN_GATE_OPEN" : "LOSS_STAY_BLOCKED"),
         "*liveAllowed=", DAL_ExecHypoGateBoolToString(st.live_allowed),
         "*lastVirtualR=", DoubleToString(st.last_virtual_net_r, 2));
   }

   DAL_ExecHypoGateSave(cfg, st);
   return result;
}

void DAL_ExecHypoGateOnRealClosedDeal(
   const DALExecHypotheticalProfitGateConfig &cfg,
   DALExecHypotheticalProfitGateState &st,
   const double net_profit,
   const ulong deal_ticket
)
{
   if(!cfg.enabled)
      return;
   if(!st.initialized)
      return;
   if(deal_ticket != 0 && st.last_real_deal_ticket == deal_ticket)
      return;

   st.last_real_profit = net_profit;
   st.last_real_deal_ticket = deal_ticket;

   if(net_profit > 0.0)
   {
      st.live_allowed = true;
      st.active_virtual = false;
      st.last_reason = "real_win_keep_gate_open";
   }
   else
   {
      st.live_allowed = false;
      st.active_virtual = false;
      st.cycle_id++;
      st.last_reason = "real_loss_close_gate_wait_hypothetical_win";
   }

   if(cfg.print_logs)
   {
      Print("DAL_HYPO_GATE_REAL_CLOSED *** deal=", IntegerToString((int)deal_ticket),
         "*netProfit=", DoubleToString(net_profit, 2),
         "*liveAllowed=", DAL_ExecHypoGateBoolToString(st.live_allowed),
         "*reason=", st.last_reason);
   }

   DAL_ExecHypoGateSave(cfg, st);
}

string DAL_ExecHypoGateStateToLog(const DALExecHypotheticalProfitGateConfig &cfg, const DALExecHypotheticalProfitGateState &st)
{
   return "hypoGateEnabled=" + DAL_ExecHypoGateBoolToString(cfg.enabled)
      + "*hypoGateReason=" + st.last_reason
      + "*hypoGateLiveAllowed=" + DAL_ExecHypoGateBoolToString(DAL_ExecHypoGateShouldTrade(cfg, st))
      + "*hypoGateActiveVirtual=" + DAL_ExecHypoGateBoolToString(st.active_virtual)
      + "*hypoGateCycle=" + IntegerToString(st.cycle_id)
      + "*hypoGateVirtualDir=" + IntegerToString(st.virtual_direction)
      + "*hypoGateVirtualEntry=" + DoubleToString(st.virtual_entry, 8)
      + "*hypoGateVirtualSL=" + DoubleToString(st.virtual_stop, 8)
      + "*hypoGateVirtualTP=" + DoubleToString(st.virtual_take_profit, 8)
      + "*hypoGateLastVirtualR=" + DoubleToString(st.last_virtual_net_r, 2)
      + "*hypoGateLastRealProfit=" + DoubleToString(st.last_real_profit, 2);
}

#endif

//+------------------------------------------------------------------+
//| Decision Alpha Lab — E0006 All-Zone Touch Limit Executor          |
//| Places one limit order per live M0001 structural zone.            |
//+------------------------------------------------------------------+
#property strict
#property version   "1.02"
#property description "Execution module E0006: all M0001 live zones with per-side pending caps and open-position side blocking."

#include <Trade/Trade.mqh>
#include <DecisionAlphaLab/Market/DAL_Bars.mqh>
#include <DecisionAlphaLab/StructuralNodes/DAL_StructuralNodeEngine.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Config.mqh>
#include <DecisionAlphaLab/M0001/DAL_M0001Engine.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecRisk.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecOrders.mqh>
#include <DecisionAlphaLab/Execution/DAL_ExecReversalOneToOne.mqh>

// Symbol / timeframe.
input string InpSymbol = "";
input ENUM_TIMEFRAMES InpTimeframe = PERIOD_CURRENT;
input int InpBars = 2500;

// M0001 structure. E0006 does not rebuild zone logic; it uses M0001 live territory modules.
input int InpL = 5;
input double InpZoneRatio = 0.90;

// Execution model: all valid live zones, no trade-count cap.
input long InpMagicNumber = 6006006;
input double InpRiskCash = 100.0;
input double InpRewardR = 20.0;
input string InpOrderCommentPrefix = "DALE6";
input int InpPendingExpirationMinutes = 0;        // 0 = GTC
input int InpMaxNodesScan = 0;                    // 0 = scan all confirmed nodes
input int InpMaxBuyPendingOrders = 0;              // 0 = unlimited buy-side pending orders
input int InpMaxSellPendingOrders = 0;             // 0 = unlimited sell-side pending orders
input int InpMaxBuyOpenPositionsBeforeBlock = 0;   // 0 = off; if BUY positions >= this, delete/block BUY pending
input int InpMaxSellOpenPositionsBeforeBlock = 0;  // 0 = off; if SELL positions >= this, delete/block SELL pending
input bool InpDeleteSidePendingWhenOpenCapHit = true; // force-delete side pending orders when open-position cap is reached

// Spread adjustments requested for the exact limit model.
input double InpBuyEntrySpreadMultiplier = 1.0;    // buy limit = LOW-zone upper edge + spread * multiplier
input double InpSellStopSpreadMultiplier = 1.0;    // sell SL = HIGH-zone upper edge + spread * multiplier
input double InpSellTpSpreadMultiplier = 1.0;      // sell TP = fixed-R TP + spread * multiplier

// Risk and broker mechanics.
input bool InpAllowMinLotIfRiskTooSmall = false;
input double InpCommissionPerLotRoundTurn = 0.0;

// Sync policy. This is not a trade-count limit; it only keeps the live order grid correct.
input bool InpModifyExistingPendingOrders = true;
input bool InpDeleteStalePendingOrders = true;
input bool InpTradingEnabled = true;

// New-bar only. No tick-by-tick computation.
input bool InpRunOnInit = true;
input int InpUpdateEveryNBars = 1;
input bool InpPrintOrderLogs = false;

// Optional broker-time session gate.
input bool InpUseTradingSessionFilter = false;
input int InpTradingStartHour = 0;
input int InpTradingStartMinute = 0;
input int InpTradingEndHour = 23;
input int InpTradingEndMinute = 59;

#define DAL_E0006_BUILD "1.02"

CTrade g_trade;
datetime g_last_open_bar_time = 0;
int g_new_bar_counter = 0;

struct E0006ZoneSetup
{
   bool valid;
   string reason;
   int node_id;
   int node_index;
   ENUM_DALNodeType node_type;
   int direction;
   datetime node_time;
   datetime active_from_time;
   double node_price;
   double live_extreme;
   double zone_lower;
   double zone_upper;
   double spread;
   double entry;
   double sl;
   double tp;
   double reward_r;
   double risk_distance;
   string comment;
};

void E0006_ResetSetup(E0006ZoneSetup &s)
{
   s.valid = false;
   s.reason = "not_built";
   s.node_id = -1;
   s.node_index = -1;
   s.node_type = DAL_NODE_LOW;
   s.direction = 0;
   s.node_time = 0;
   s.active_from_time = 0;
   s.node_price = 0.0;
   s.live_extreme = 0.0;
   s.zone_lower = 0.0;
   s.zone_upper = 0.0;
   s.spread = 0.0;
   s.entry = 0.0;
   s.sl = 0.0;
   s.tp = 0.0;
   s.reward_r = 0.0;
   s.risk_distance = 0.0;
   s.comment = "";
}

string E0006_Symbol()
{
   if(InpSymbol == "")
      return _Symbol;
   return InpSymbol;
}

ENUM_TIMEFRAMES E0006_Timeframe()
{
   if(InpTimeframe == PERIOD_CURRENT)
      return (ENUM_TIMEFRAMES)_Period;
   return InpTimeframe;
}

int E0006_ClampInt(const int value, const int lo, const int hi)
{
   if(value < lo)
      return lo;
   if(value > hi)
      return hi;
   return value;
}

string E0006_TwoDigits(const int value)
{
   if(value < 10)
      return "0" + IntegerToString(value);
   return IntegerToString(value);
}

string E0006_FormatDateTime(const datetime value)
{
   MqlDateTime dt;
   TimeToStruct(value, dt);
   return StringFormat("%04d.%02d.%02d %02d:%02d:%02d", dt.year, dt.mon, dt.day, dt.hour, dt.min, dt.sec);
}

bool E0006_IsTradingSessionOpen(string &reason)
{
   if(!InpUseTradingSessionFilter)
   {
      reason = "timeFilter=OFF";
      return true;
   }

   int start_hour = E0006_ClampInt(InpTradingStartHour, 0, 23);
   int start_minute = E0006_ClampInt(InpTradingStartMinute, 0, 59);
   int end_hour = E0006_ClampInt(InpTradingEndHour, 0, 23);
   int end_minute = E0006_ClampInt(InpTradingEndMinute, 0, 59);
   int start = start_hour * 60 + start_minute;
   int finish = end_hour * 60 + end_minute;

   datetime now_time = TimeCurrent();
   MqlDateTime dt;
   TimeToStruct(now_time, dt);
   int now_minute = dt.hour * 60 + dt.min;

   bool open = false;
   if(start == finish)
      open = true;
   else if(start < finish)
      open = (now_minute >= start && now_minute < finish);
   else
      open = (now_minute >= start || now_minute < finish);

   reason = "timeFilter=ON*now=" + E0006_FormatDateTime(now_time)
      + "*window=" + E0006_TwoDigits(start_hour) + ":" + E0006_TwoDigits(start_minute)
      + "-" + E0006_TwoDigits(end_hour) + ":" + E0006_TwoDigits(end_minute)
      + "*open=" + DAL_BoolToString(open);
   return open;
}

bool E0006_HasNewOpenCandle()
{
   datetime current_open = iTime(E0006_Symbol(), E0006_Timeframe(), 0);
   if(current_open <= 0)
      return false;

   if(g_last_open_bar_time <= 0)
   {
      g_last_open_bar_time = current_open;
      return true;
   }

   if(current_open == g_last_open_bar_time)
      return false;

   g_last_open_bar_time = current_open;
   return true;
}

void E0006_BuildM0001Config(DALM0001Config &config)
{
   DAL_M0001DefaultConfig(config);
   config.L = MathMax(1, InpL);
   config.zone_ratio = InpZoneRatio;
   config.max_events = 0;
   config.min_rtv = 0.0;
}

bool E0006_LoadContext(DALBar &bars[], int &bars_count, DALLRuleNode &nodes[], int &nodes_count, string &reason)
{
   ArrayResize(bars, 0);
   ArrayResize(nodes, 0);
   bars_count = 0;
   nodes_count = 0;
   reason = "not_loaded";

   bars_count = DAL_LoadBarsChronological(E0006_Symbol(), E0006_Timeframe(), InpBars, true, bars);
   int min_required = MathMax(20, MathMax(1, InpL) * 2 + 10);
   if(bars_count <= min_required)
   {
      reason = "not_enough_closed_bars";
      return false;
   }

   nodes_count = DAL_DetectConfirmedStructuralNodes(bars, bars_count, MathMax(1, InpL), nodes);
   if(nodes_count <= 0)
   {
      reason = "no_confirmed_nodes";
      return false;
   }

   reason = "ok";
   return true;
}

string E0006_ManagedCommentPrefix()
{
   return DAL_ExecManagedCommentPrefix(InpOrderCommentPrefix);
}

string E0006_BuildComment(const E0006ZoneSetup &s)
{
   return DAL_ExecBuildCompactSetupComment(E0006_ManagedCommentPrefix(), s.reward_r, s.node_id, s.direction);
}

bool E0006_BuildZoneSetup(
   const string symbol,
   const DALBar &bars[],
   const int bars_count,
   const DALLRuleNode &node,
   const double zone_ratio,
   E0006ZoneSetup &setup
)
{
   E0006_ResetSetup(setup);

   if(!node.confirmed)
   {
      setup.reason = "node_unconfirmed";
      return false;
   }
   if(node.active_from_index < 0 || node.active_from_index >= bars_count)
   {
      setup.reason = "node_not_active_in_window";
      return false;
   }

   double extreme = 0.0, lower = 0.0, upper = 0.0;
   bool hunted = false;
   if(!DAL_ExecBuildLiveNodeTerritory(bars, bars_count, node, zone_ratio, extreme, lower, upper, hunted))
   {
      setup.reason = "live_territory_build_failed";
      return false;
   }
   if(hunted)
   {
      setup.reason = "node_hunted_invalidated";
      return false;
   }

   double spread = DAL_ExecCurrentSpreadPrice(symbol);
   double reward_r = MathMax(0.01, InpRewardR);

   setup.node_id = node.id;
   setup.node_index = node.index;
   setup.node_type = node.type;
   setup.node_time = node.time;
   setup.active_from_time = node.active_from_time;
   setup.node_price = node.price;
   setup.live_extreme = extreme;
   setup.zone_lower = lower;
   setup.zone_upper = upper;
   setup.spread = spread;
   setup.reward_r = reward_r;

   if(node.type == DAL_NODE_LOW)
   {
      setup.direction = +1;
      // Support/demand touch. Buy opens on Ask, so entry is shifted up by spread.
      setup.entry = upper + spread * MathMax(0.0, InpBuyEntrySpreadMultiplier);
      setup.sl = lower;
      setup.risk_distance = MathAbs(setup.entry - setup.sl);
      setup.tp = setup.entry + setup.risk_distance * reward_r;
   }
   else
   {
      setup.direction = -1;
      // Supply/resistance touch. Sell entry stays on lower zone edge.
      // Sell SL and TP are shifted upward by spread as requested.
      setup.entry = lower;
      setup.sl = upper + spread * MathMax(0.0, InpSellStopSpreadMultiplier);
      setup.risk_distance = MathAbs(setup.entry - setup.sl);
      setup.tp = setup.entry - setup.risk_distance * reward_r + spread * MathMax(0.0, InpSellTpSpreadMultiplier);
   }

   if(setup.risk_distance <= 0.0)
   {
      setup.reason = "zero_stop_distance";
      return false;
   }

   setup.comment = E0006_BuildComment(setup);
   setup.valid = true;
   setup.reason = "ok";
   DAL_ExecNormalizePrices(symbol, setup.entry, setup.sl, setup.tp);
   return true;
}

bool E0006_PositionCommentExists(const string symbol, const long magic, const string comment)
{
   int pos_total = PositionsTotal();
   for(int i = 0; i < pos_total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;
      if(PositionGetString(POSITION_COMMENT) == comment)
         return true;
   }
   return false;
}

bool E0006_FindPendingByComment(const string symbol, const long magic, const string comment, DALExecPendingOrder &out)
{
   DAL_ExecResetPendingOrder(out);
   for(int i = 0; i < OrdersTotal(); i++)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;
      if(OrderGetString(ORDER_COMMENT) != comment)
         continue;
      return DAL_ExecReadPendingOrder(ticket, out);
   }
   return false;
}


int E0006_OrderDirectionFromType(const ENUM_ORDER_TYPE type)
{
   if(type == ORDER_TYPE_BUY_LIMIT || type == ORDER_TYPE_BUY_STOP || type == ORDER_TYPE_BUY_STOP_LIMIT)
      return +1;
   if(type == ORDER_TYPE_SELL_LIMIT || type == ORDER_TYPE_SELL_STOP || type == ORDER_TYPE_SELL_STOP_LIMIT)
      return -1;
   return 0;
}

int E0006_CountOpenPositionsByDirection(const string symbol, const long magic, const int direction)
{
   int count = 0;
   int pos_total = PositionsTotal();
   for(int i = 0; i < pos_total; i++)
   {
      ulong ticket = PositionGetTicket(i);
      if(ticket == 0 || !PositionSelectByTicket(ticket))
         continue;
      if(PositionGetString(POSITION_SYMBOL) != symbol)
         continue;
      if((long)PositionGetInteger(POSITION_MAGIC) != magic)
         continue;

      ENUM_POSITION_TYPE type = (ENUM_POSITION_TYPE)PositionGetInteger(POSITION_TYPE);
      if(direction > 0 && type == POSITION_TYPE_BUY)
         count++;
      else if(direction < 0 && type == POSITION_TYPE_SELL)
         count++;
   }
   return count;
}

void E0006_DeletePendingOrdersByDirection(
   const string symbol,
   const long magic,
   const int direction,
   int &deleted,
   int &kept,
   int &failed
)
{
   deleted = 0;
   kept = 0;
   failed = 0;

   string prefix = E0006_ManagedCommentPrefix();
   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != magic)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;
      if(E0006_OrderDirectionFromType(type) != direction)
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(StringFind(comment, prefix, 0) != 0)
      {
         kept++;
         continue;
      }

      string reason = "";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, reason))
         deleted++;
      else
         failed++;
   }
}

bool E0006_PricesCloseEnough(const string symbol, const double a, const double b)
{
   double point = SymbolInfoDouble(symbol, SYMBOL_POINT);
   if(point <= 0.0)
      point = 0.00000001;
   return (MathAbs(a - b) <= point * 0.5);
}

bool E0006_ModifyPendingOrder(const ulong ticket, double entry, double sl, double tp, string &reason)
{
   if(ticket == 0 || !OrderSelect(ticket))
   {
      reason = "pending_ticket_not_found";
      return false;
   }

   string symbol = OrderGetString(ORDER_SYMBOL);
   DAL_ExecNormalizePrices(symbol, entry, sl, tp);

   datetime expiration = 0;
   ENUM_ORDER_TYPE_TIME type_time = ORDER_TIME_GTC;
   if(InpPendingExpirationMinutes > 0)
   {
      type_time = ORDER_TIME_SPECIFIED;
      expiration = TimeCurrent() + InpPendingExpirationMinutes * 60;
   }

   g_trade.SetExpertMagicNumber(InpMagicNumber);
   if(!g_trade.OrderModify(ticket, entry, sl, tp, type_time, expiration, 0.0))
   {
      reason = "modify_failed_retcode_" + IntegerToString((int)g_trade.ResultRetcode()) + "_" + g_trade.ResultRetcodeDescription();
      return false;
   }

   reason = "ok_modified_" + IntegerToString((int)ticket);
   return true;
}

bool E0006_UpsertLimitOrder(const E0006ZoneSetup &s, string &reason)
{
   reason = "not_sent";
   if(!s.valid)
   {
      reason = s.reason;
      return false;
   }

   string symbol = E0006_Symbol();

   if(E0006_PositionCommentExists(symbol, InpMagicNumber, s.comment))
   {
      reason = "position_exists_for_zone";
      return false;
   }

   string geometry_reason = "";
   if(!DAL_ExecCheckLimitGeometry(symbol, s.direction, s.entry, s.sl, s.tp, geometry_reason))
   {
      reason = "geometry_" + geometry_reason;
      return false;
   }

   DALExecRiskSizing risk;
   if(!DAL_ExecCalculateRiskVolume(symbol, s.entry, s.sl, InpRiskCash, InpCommissionPerLotRoundTurn, InpAllowMinLotIfRiskTooSmall, risk))
   {
      reason = "risk_" + risk.reason;
      return false;
   }

   DALExecPendingOrder existing;
   if(E0006_FindPendingByComment(symbol, InpMagicNumber, s.comment, existing))
   {
      if(existing.direction != s.direction)
      {
         string del_reason = "";
         DAL_ExecDeletePendingOrder(existing.ticket, g_trade, del_reason);
      }
      else
      {
         bool same = E0006_PricesCloseEnough(symbol, existing.price, s.entry)
            && E0006_PricesCloseEnough(symbol, existing.sl, s.sl)
            && E0006_PricesCloseEnough(symbol, existing.tp, s.tp)
            && E0006_PricesCloseEnough(symbol, existing.volume, risk.volume);

         if(same || !InpModifyExistingPendingOrders)
         {
            reason = same ? "ok_existing_same" : "existing_pending_no_modify";
            return true;
         }

         string mod_reason = "";
         if(E0006_ModifyPendingOrder(existing.ticket, s.entry, s.sl, s.tp, mod_reason))
         {
            reason = mod_reason;
            return true;
         }

         reason = mod_reason;
         return false;
      }
   }

   if(!InpTradingEnabled)
   {
      reason = "trading_disabled";
      return false;
   }

   string place_reason = "";
   bool ok = DAL_ExecPlaceLimitOrder(symbol, InpMagicNumber, s.direction, risk.volume, s.entry, s.sl, s.tp, s.comment, InpPendingExpirationMinutes, g_trade, place_reason);
   reason = place_reason;
   return ok;
}

bool E0006_StringInArray(const string value, const string &arr[])
{
   for(int i = 0; i < ArraySize(arr); i++)
   {
      if(arr[i] == value)
         return true;
   }
   return false;
}

void E0006_AppendStringUnique(string &arr[], const string value)
{
   if(value == "" || E0006_StringInArray(value, arr))
      return;
   int n = ArraySize(arr);
   ArrayResize(arr, n + 1);
   arr[n] = value;
}

void E0006_DeleteStalePendingOrders(const string &desired_comments[], int &deleted, int &kept, int &failed)
{
   deleted = 0;
   kept = 0;
   failed = 0;

   if(!InpDeleteStalePendingOrders)
      return;

   string symbol = E0006_Symbol();
   string prefix = E0006_ManagedCommentPrefix();

   for(int i = OrdersTotal() - 1; i >= 0; i--)
   {
      ulong ticket = OrderGetTicket(i);
      if(ticket == 0 || !OrderSelect(ticket))
         continue;
      if(OrderGetString(ORDER_SYMBOL) != symbol)
         continue;
      if((long)OrderGetInteger(ORDER_MAGIC) != InpMagicNumber)
         continue;

      ENUM_ORDER_TYPE type = (ENUM_ORDER_TYPE)OrderGetInteger(ORDER_TYPE);
      if(!DAL_ExecOrderIsPendingLimit(type))
         continue;

      string comment = OrderGetString(ORDER_COMMENT);
      if(StringFind(comment, prefix, 0) != 0)
         continue;

      if(E0006_StringInArray(comment, desired_comments))
      {
         kept++;
         continue;
      }

      string reason = "";
      if(DAL_ExecDeletePendingOrder(ticket, g_trade, reason))
         deleted++;
      else
         failed++;
   }
}

void E0006_ProcessNewBar(const string run_mode)
{
   string session_reason = "";
   if(!E0006_IsTradingSessionOpen(session_reason))
      return;

   DALBar bars[];
   DALLRuleNode nodes[];
   int bars_count = 0;
   int nodes_count = 0;
   string load_reason = "";
   if(!E0006_LoadContext(bars, bars_count, nodes, nodes_count, load_reason))
   {
      if(InpPrintOrderLogs)
         Print("DAL_E0006_SKIP *** build=", DAL_E0006_BUILD, "*runMode=", run_mode, "*reason=", load_reason);
      return;
   }

   DALM0001Config m1;
   E0006_BuildM0001Config(m1);

   string desired_comments[];
   ArrayResize(desired_comments, 0);

   int scanned = 0;
   int built = 0;
   int sent_or_synced = 0;
   int skipped = 0;
   int build_reject = 0;
   int order_reject = 0;
   int buy_desired = 0;
   int sell_desired = 0;
   int side_cap_skip = 0;
   int max_buy_pending = MathMax(0, InpMaxBuyPendingOrders);
   int max_sell_pending = MathMax(0, InpMaxSellPendingOrders);
   int max_buy_open_before_block = MathMax(0, InpMaxBuyOpenPositionsBeforeBlock);
   int max_sell_open_before_block = MathMax(0, InpMaxSellOpenPositionsBeforeBlock);
   int open_buy_positions = E0006_CountOpenPositionsByDirection(E0006_Symbol(), InpMagicNumber, +1);
   int open_sell_positions = E0006_CountOpenPositionsByDirection(E0006_Symbol(), InpMagicNumber, -1);
   bool buy_side_blocked_by_open_cap = (max_buy_open_before_block > 0 && open_buy_positions >= max_buy_open_before_block);
   bool sell_side_blocked_by_open_cap = (max_sell_open_before_block > 0 && open_sell_positions >= max_sell_open_before_block);
   int side_block_deleted_buy = 0, side_block_kept_buy = 0, side_block_failed_buy = 0;
   int side_block_deleted_sell = 0, side_block_kept_sell = 0, side_block_failed_sell = 0;

   if(InpDeleteSidePendingWhenOpenCapHit && buy_side_blocked_by_open_cap)
      E0006_DeletePendingOrdersByDirection(E0006_Symbol(), InpMagicNumber, +1, side_block_deleted_buy, side_block_kept_buy, side_block_failed_buy);
   if(InpDeleteSidePendingWhenOpenCapHit && sell_side_blocked_by_open_cap)
      E0006_DeletePendingOrdersByDirection(E0006_Symbol(), InpMagicNumber, -1, side_block_deleted_sell, side_block_kept_sell, side_block_failed_sell);

   for(int i = nodes_count - 1; i >= 0; i--)
   {
      DALLRuleNode node = nodes[i];
      if(!node.confirmed)
      {
         skipped++;
         continue;
      }

      scanned++;
      if(InpMaxNodesScan > 0 && scanned > InpMaxNodesScan)
         break;

      E0006ZoneSetup setup;
      if(!E0006_BuildZoneSetup(E0006_Symbol(), bars, bars_count, node, m1.zone_ratio, setup))
      {
         build_reject++;
         continue;
      }

      built++;

      if(setup.direction > 0 && buy_side_blocked_by_open_cap)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_OPEN_SIDE_BLOCK_SKIP *** build=", DAL_E0006_BUILD,
               "*nodeId=", setup.node_id,
               "*side=BUY",
               "*openBuyPositions=", open_buy_positions,
               "*maxBuyOpenBeforeBlock=", max_buy_open_before_block,
               "*deletedBuyPending=", side_block_deleted_buy);
         continue;
      }
      if(setup.direction < 0 && sell_side_blocked_by_open_cap)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_OPEN_SIDE_BLOCK_SKIP *** build=", DAL_E0006_BUILD,
               "*nodeId=", setup.node_id,
               "*side=SELL",
               "*openSellPositions=", open_sell_positions,
               "*maxSellOpenBeforeBlock=", max_sell_open_before_block,
               "*deletedSellPending=", side_block_deleted_sell);
         continue;
      }

      if(setup.direction > 0 && max_buy_pending > 0 && buy_desired >= max_buy_pending)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIDE_CAP_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*side=BUY*maxBuyPending=", max_buy_pending);
         continue;
      }
      if(setup.direction < 0 && max_sell_pending > 0 && sell_desired >= max_sell_pending)
      {
         side_cap_skip++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIDE_CAP_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*side=SELL*maxSellPending=", max_sell_pending);
         continue;
      }

      if(setup.direction > 0)
         buy_desired++;
      else if(setup.direction < 0)
         sell_desired++;

      E0006_AppendStringUnique(desired_comments, setup.comment);

      string order_reason = "";
      if(E0006_UpsertLimitOrder(setup, order_reason))
      {
         sent_or_synced++;
         if(InpPrintOrderLogs)
         {
            int digits = (int)SymbolInfoInteger(E0006_Symbol(), SYMBOL_DIGITS);
            Print("DAL_E0006_ALL_ZONE_LIMIT *** build=", DAL_E0006_BUILD,
               "*runMode=", run_mode,
               "*action=UPSERT_OK",
               "*nodeId=", setup.node_id,
               "*side=", DAL_NodeTypeToString(setup.node_type),
               "*dir=", setup.direction,
               "*zoneLower=", DoubleToString(setup.zone_lower, digits),
               "*zoneUpper=", DoubleToString(setup.zone_upper, digits),
               "*entry=", DoubleToString(setup.entry, digits),
               "*sl=", DoubleToString(setup.sl, digits),
               "*tp=", DoubleToString(setup.tp, digits),
               "*rewardR=", DoubleToString(setup.reward_r, 2),
               "*spread=", DoubleToString(setup.spread, digits),
               "*comment=", setup.comment,
               "*reason=", order_reason);
         }
      }
      else
      {
         order_reject++;
         if(InpPrintOrderLogs)
            Print("DAL_E0006_SIGNAL_SKIP *** build=", DAL_E0006_BUILD, "*nodeId=", setup.node_id, "*reason=", order_reason);
      }
   }

   int stale_deleted = 0, stale_kept = 0, stale_failed = 0;
   E0006_DeleteStalePendingOrders(desired_comments, stale_deleted, stale_kept, stale_failed);

   if(InpPrintOrderLogs)
   {
      Print("DAL_E0006_AUDIT *** build=", DAL_E0006_BUILD,
         "*runMode=", run_mode,
         "*bars=", bars_count,
         "*nodes=", nodes_count,
         "*scanned=", scanned,
         "*built=", built,
         "*synced=", sent_or_synced,
         "*skipped=", skipped,
         "*buildReject=", build_reject,
         "*orderReject=", order_reject,
         "*sideCapSkip=", side_cap_skip,
         "*buyDesired=", buy_desired,
         "*sellDesired=", sell_desired,
         "*maxBuyPending=", max_buy_pending,
         "*maxSellPending=", max_sell_pending,
         "*openBuyPositions=", open_buy_positions,
         "*openSellPositions=", open_sell_positions,
         "*maxBuyOpenBeforeBlock=", max_buy_open_before_block,
         "*maxSellOpenBeforeBlock=", max_sell_open_before_block,
         "*buySideBlockedByOpenCap=", DAL_BoolToString(buy_side_blocked_by_open_cap),
         "*sellSideBlockedByOpenCap=", DAL_BoolToString(sell_side_blocked_by_open_cap),
         "*sideBlockDeletedBuy=", side_block_deleted_buy,
         "*sideBlockDeletedSell=", side_block_deleted_sell,
         "*sideBlockFailedBuy=", side_block_failed_buy,
         "*sideBlockFailedSell=", side_block_failed_sell,
         "*desired=", ArraySize(desired_comments),
         "*staleDeleted=", stale_deleted,
         "*staleKept=", stale_kept,
         "*staleFailed=", stale_failed,
         "*rewardR=", DoubleToString(InpRewardR, 2),
         "*mode=ALL_LIVE_M0001_ZONES_NO_TRADE_COUNT_LIMIT_NEW_BAR_ONLY");
   }
}

int OnInit()
{
   g_trade.SetExpertMagicNumber(InpMagicNumber);

   Print("DAL_E0006_BUILD_SANITY *** build=", DAL_E0006_BUILD,
      "*symbol=", E0006_Symbol(),
      "*tf=", EnumToString(E0006_Timeframe()),
      "*module=EXECUTION_E0006_ALL_ZONE_TOUCH_LIMIT_FIXED_R",
      "*source=M0001_LIVE_TERRITORY",
      "*entry=LIMIT_ON_TOUCH_EDGE",
      "*buyEntry=LOW_ZONE_UPPER_PLUS_SPREAD",
      "*sellEntry=HIGH_ZONE_LOWER",
      "*sellSL=HIGH_ZONE_UPPER_PLUS_SPREAD",
      "*sellTP=FIXED_R_TP_PLUS_SPREAD",
      "*rewardR=", DoubleToString(InpRewardR, 2),
      "*maxBuyPending=", InpMaxBuyPendingOrders,
      "*maxSellPending=", InpMaxSellPendingOrders,
      "*maxBuyOpenBeforeBlock=", InpMaxBuyOpenPositionsBeforeBlock,
      "*maxSellOpenBeforeBlock=", InpMaxSellOpenPositionsBeforeBlock,
      "*deleteSidePendingWhenOpenCapHit=", DAL_BoolToString(InpDeleteSidePendingWhenOpenCapHit),
      "*openSideBlockPolicy=CHECK_EVERY_NEW_CANDLE_DELETE_PENDING_AND_BLOCK_SIDE",
      "*newBarOnly=true");

   if(InpRunOnInit)
      E0006_ProcessNewBar("init_backfill_sync");

   return INIT_SUCCEEDED;
}

void OnDeinit(const int reason)
{
   Comment("");
}

void OnTick()
{
   if(!E0006_HasNewOpenCandle())
      return;

   g_new_bar_counter++;
   int every = MathMax(1, InpUpdateEveryNBars);
   if((g_new_bar_counter % every) != 0)
      return;

   E0006_ProcessNewBar("new_closed_candle_sync");
}

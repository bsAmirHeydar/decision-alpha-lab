#ifndef __CGX_TYPES_MQH__
#define __CGX_TYPES_MQH__

#include <IntermarketDivergenceExecution/CG/CGC_Types.mqh>

enum ECGXRuntimeMode
{
   CGX_RUNTIME_BACKTEST_ONLY = 0,
   CGX_RUNTIME_PAPER_ONLY    = 1,
   CGX_RUNTIME_LIVE_ENABLED  = 2
};

enum ECGXTradeLeg
{
   CGX_TRADE_PROTECTED_SYMBOL = 0,
   CGX_TRADE_HUNTER_SYMBOL    = 1
};

enum ECGXEntryModel
{
   CGX_ENTRY_MARKET_ON_CLOSED_CANDLE = 0
};

enum ECGXStopModel
{
   CGX_STOP_BEHIND_CONFIRMATION_CANDLE = 0
};

enum ECGXTargetModel
{
   CGX_TARGET_ATR_MULTIPLE = 0
};

enum ECGXVolumeModel
{
   CGX_VOLUME_RISK_PERCENT_EQUITY = 0,
   CGX_VOLUME_FIXED_LOTS          = 1
};

enum ECGXPositionPolicy
{
   CGX_POSITION_EVERY_SIGNAL            = 0,
   CGX_POSITION_ONE_OWN_POSITION_SYMBOL = 1
};

enum ECGXNettingPolicy
{
   CGX_NETTING_SKIP_WHEN_POSITION_EXISTS = 0,
   CGX_NETTING_ALLOW_POSITION_MERGE       = 1
};

struct SCGXExecutionConfig
{
   ECGXRuntimeMode runtime_mode;
   ECGXTradeLeg trade_leg;
   ECGXEntryModel entry_model;
   ECGXStopModel stop_model;
   ECGXTargetModel target_model;
   ECGXVolumeModel volume_model;
   ECGXPositionPolicy position_policy;
   ECGXNettingPolicy netting_policy;
   bool   require_hedging_account;

   double stop_buffer_points;
   int    atr_period;
   double atr_multiplier;

   double risk_percent_equity;
   double fixed_lots;
   bool   allow_minimum_volume_risk_overflow;

   long   magic_base;
   int    deviation_points;
   double max_spread_points;
   int    max_quote_age_seconds;

   bool   process_existing_closed_bar_on_init;
   bool   print_execution_events;
   bool   enable_audit_csv;
   bool   audit_use_common_files;
   string audit_file_name;
   int    max_signal_registry_records;
};

struct SCGXClosedCandle
{
   bool     ready;
   string   symbol;
   ENUM_TIMEFRAMES timeframe;
   datetime open_time_broker;
   datetime close_time_broker;
   double   open;
   double   high;
   double   low;
   double   close;
   long     tick_volume;
   string   error_text;
};

struct SCGXTradePlan
{
   bool     valid;
   string   rejection_reason;
   string   signal_id;
   string   group_name;
   int      group_minutes;
   int      group_index;
   ECGCSignalDirection direction;
   ECGXTradeLeg trade_leg;
   string   hunter_symbol;
   string   protected_symbol;
   string   trade_symbol;
   datetime confirmation_time_broker;
   ENUM_TIMEFRAMES confirmation_timeframe;
   datetime candle_open_time_broker;
   double   candle_high;
   double   candle_low;
   double   candle_close;
   double   quote_bid;
   double   quote_ask;
   double   planned_entry_price;
   double   stop_loss;
   double   atr_value;
   double   take_profit;
   double   risk_money;
   double   risk_per_lot;
   double   volume;
   long     magic_number;
   string   order_comment;
};

struct SCGXExecutionResult
{
   bool   attempted;
   bool   sent;
   bool   paper_only;
   ulong  order_ticket;
   ulong  deal_ticket;
   uint   retcode;
   double result_price;
   string message;
};

#endif

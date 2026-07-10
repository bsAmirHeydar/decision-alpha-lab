#ifndef __CGX_AUDIT_MQH__
#define __CGX_AUDIT_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_Utilities.mqh>
#include <IntermarketDivergenceExecution/CG/Execution/CGX_TradeEntitlement.mqh>

class CCGX_Audit
{
private:
   SCGXExecutionConfig m_config;

   int FileFlags()
   {
      int flags=FILE_CSV|FILE_READ|FILE_WRITE|FILE_ANSI|FILE_SHARE_READ|FILE_SHARE_WRITE;
      if(m_config.audit_use_common_files)
         flags|=FILE_COMMON;
      return flags;
   }

   string OneShotAuditFileName()
   {
      string file_name=m_config.audit_file_name;
      if(file_name=="")
         return "EXP0017_Phase14_OneShot_Gate_Audit.csv";
      int length=StringLen(file_name);
      if(length>=4 && StringSubstr(file_name,length-4)==".csv")
         return StringSubstr(file_name,0,length-4)+"_OneShot_Gate.csv";
      return file_name+"_OneShot_Gate.csv";
   }

public:
   void Configure(const SCGXExecutionConfig &config)
   {
      m_config=config;
   }

   void WriteOneShotSuppression(const SCGCFinalSignal &signal,
                                const datetime observation_close_broker,
                                const string entitlement_key,
                                const string reason)
   {
      if(m_config.print_execution_events)
      {
         Print(StringFormat("EXP0017 CGX one-shot gate | SUPPRESSED | %s | %s | side=%s | observation=%s | key=%s | reason=%s",
                            signal.group_name,
                            signal.signal_id,
                            CGX_EntitlementSideText(signal.side),
                            TimeToString(observation_close_broker,TIME_DATE|TIME_SECONDS),
                            entitlement_key,
                            reason));
      }

      if(!m_config.enable_audit_csv)
         return;

      string file_name=OneShotAuditFileName();
      ResetLastError();
      int handle=FileOpen(file_name,FileFlags(),',');
      if(handle==INVALID_HANDLE)
      {
         Print("EXP0017 CGX one-shot audit open failed: ",GetLastError());
         return;
      }
      if(FileSize(handle)==0)
      {
         FileWrite(handle,
                   "event_time_broker","observation_close_broker","trade_entitlement_key","signal_id","cg","group_minutes","side",
                   "trading_day_start_ny","current_cycle_start_ny","reference_cycle_start_ny","hunter_symbol","protected_symbol","gate_state","reason");
      }
      FileSeek(handle,0,SEEK_END);
      string gate_state=(reason=="one_shot_entitlement_already_consumed" ? "SUPPRESSED_ALREADY_CONSUMED" : "SUPPRESSED_GATE_REJECTED");
      FileWrite(handle,
                TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                TimeToString(observation_close_broker,TIME_DATE|TIME_SECONDS),
                entitlement_key,
                signal.signal_id,
                signal.group_name,
                IntegerToString(signal.group_minutes),
                CGX_EntitlementSideText(signal.side),
                TimeToString(signal.trading_day_start_ny,TIME_DATE|TIME_SECONDS),
                TimeToString(signal.current_cycle_start_ny,TIME_DATE|TIME_SECONDS),
                TimeToString(signal.reference_cycle_start_ny,TIME_DATE|TIME_SECONDS),
                signal.hunter_symbol,
                signal.clean_symbol,
                gate_state,
                reason);
      FileFlush(handle);
      FileClose(handle);
   }

   void Write(SCGXTradePlan &plan,SCGXExecutionResult &result)
   {
      string status=(plan.valid ? "PLAN_VALID" : "PLAN_REJECTED");
      if(result.paper_only) status="PAPER_ACCEPTED";
      else if(result.sent) status="ORDER_SENT";
      else if(result.attempted) status="ORDER_FAILED";

      if(m_config.print_execution_events)
      {
         Print(StringFormat("EXP0017 CGX | %s | %s | %s | %s | entitlement=%s symbol=%s entry=%s sl=%s tp=%s target=%s risk_model=%s budget=%.2f planned_loss=%.2f volume=%s hedge=%s result=%s",
                            plan.group_name,
                            CGX_DirectionText(plan.direction),
                            CGX_TradeLegText(plan.trade_leg),
                            status,
                            plan.trade_entitlement_key,
                            plan.trade_symbol,
                            DoubleToString(plan.planned_entry_price,CGX_PriceDigits(plan.trade_symbol)),
                            DoubleToString(plan.stop_loss,CGX_PriceDigits(plan.trade_symbol)),
                            DoubleToString(plan.take_profit,CGX_PriceDigits(plan.trade_symbol)),
                            CGX_TargetModelText(plan.target_model),
                            CGX_VolumeModelText(plan.volume_model),
                            plan.risk_budget_money,
                            plan.planned_loss_at_stop,
                            DoubleToString(plan.volume,4),
                            (m_config.enable_hedging ? "ON" : "OFF"),
                            (plan.valid ? result.message : plan.rejection_reason)));
      }

      if(!m_config.enable_audit_csv || m_config.audit_file_name=="")
         return;

      ResetLastError();
      int handle=FileOpen(m_config.audit_file_name,FileFlags(),',');
      if(handle==INVALID_HANDLE)
      {
         Print("EXP0017 CGX audit open failed: ",GetLastError());
         return;
      }
      if(FileSize(handle)==0)
      {
         FileWrite(handle,
                   "event_time_broker","confirmation_time_broker","trade_entitlement_key","signal_id","cg","direction","trade_leg","hunter_symbol","protected_symbol","trade_symbol","status","rejection_reason",
                   "target_model","volume_model","hedging_enabled","entry","stop_loss","spread_price","spread_points","stop_distance","atr","take_profit","target_distance",
                   "risk_budget_money","risk_per_lot","planned_loss_at_stop","volume","magic","attempted","sent","paper_only","order_ticket","deal_ticket","retcode","result_price","message");
      }
      FileSeek(handle,0,SEEK_END);
      FileWrite(handle,
                TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                TimeToString(plan.confirmation_time_broker,TIME_DATE|TIME_SECONDS),
                plan.trade_entitlement_key,
                plan.signal_id,
                plan.group_name,
                CGX_DirectionText(plan.direction),
                CGX_TradeLegText(plan.trade_leg),
                plan.hunter_symbol,
                plan.protected_symbol,
                plan.trade_symbol,
                status,
                plan.rejection_reason,
                CGX_TargetModelText(plan.target_model),
                CGX_VolumeModelText(plan.volume_model),
                (m_config.enable_hedging ? "true" : "false"),
                DoubleToString(plan.planned_entry_price,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.stop_loss,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.spread_price,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.spread_points,2),
                DoubleToString(plan.stop_distance,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.atr_value,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.take_profit,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.target_distance,CGX_PriceDigits(plan.trade_symbol)),
                DoubleToString(plan.risk_budget_money,2),
                DoubleToString(plan.risk_per_lot,2),
                DoubleToString(plan.planned_loss_at_stop,2),
                DoubleToString(plan.volume,4),
                IntegerToString((int)plan.magic_number),
                (result.attempted ? "true" : "false"),
                (result.sent ? "true" : "false"),
                (result.paper_only ? "true" : "false"),
                IntegerToString((long)result.order_ticket),
                IntegerToString((long)result.deal_ticket),
                IntegerToString((int)result.retcode),
                DoubleToString(result.result_price,CGX_PriceDigits(plan.trade_symbol)),
                result.message);
      FileFlush(handle);
      FileClose(handle);
   }
};

#endif

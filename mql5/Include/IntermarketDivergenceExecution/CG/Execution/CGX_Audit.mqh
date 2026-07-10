#ifndef __CGX_AUDIT_MQH__
#define __CGX_AUDIT_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_OrderRouter.mqh>

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

public:
   void Configure(const SCGXExecutionConfig &config)
   {
      m_config=config;
   }

   void Write(SCGXTradePlan &plan,SCGXExecutionResult &result)
   {
      string status=(plan.valid ? "PLAN_VALID" : "PLAN_REJECTED");
      if(result.paper_only) status="PAPER_ACCEPTED";
      else if(result.sent) status="ORDER_SENT";
      else if(result.attempted) status="ORDER_FAILED";

      if(m_config.print_execution_events)
      {
         Print(StringFormat("EXP0017 CGX | %s | %s | %s | %s | symbol=%s entry=%s sl=%s tp=%s target=%s risk_model=%s budget=%.2f planned_loss=%.2f volume=%s hedge=%s result=%s",
                            plan.group_name,
                            CGX_DirectionText(plan.direction),
                            CGX_TradeLegText(plan.trade_leg),
                            status,
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
                   "event_time_broker","confirmation_time_broker","signal_id","cg","direction","trade_leg","hunter_symbol","protected_symbol","trade_symbol","status","rejection_reason",
                   "target_model","volume_model","hedging_enabled","entry","stop_loss","spread_price","spread_points","stop_distance","atr","take_profit","target_distance",
                   "risk_budget_money","risk_per_lot","planned_loss_at_stop","volume","magic","attempted","sent","paper_only","order_ticket","deal_ticket","retcode","result_price","message");
      }
      FileSeek(handle,0,SEEK_END);
      FileWrite(handle,
                TimeToString(TimeCurrent(),TIME_DATE|TIME_SECONDS),
                TimeToString(plan.confirmation_time_broker,TIME_DATE|TIME_SECONDS),
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

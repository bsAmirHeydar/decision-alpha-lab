#ifndef __CGX_ENGINE_MQH__
#define __CGX_ENGINE_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_SignalSource.mqh>
#include <IntermarketDivergenceExecution/CG/Execution/CGX_Audit.mqh>
#include <IntermarketDivergenceExecution/CG/Execution/CGX_ExecutionVisuals.mqh>

class CCGX_Engine
{
private:
   SCGXExecutionConfig m_execution_config;
   CCGX_SignalSource   m_signal_source;
   CCGX_TradePlanner   m_planner;
   CCGX_SignalRegistry m_registry;
   CCGX_OrderRouter    m_router;
   CCGX_Audit          m_audit;
   CCGX_ExecutionVisuals m_visuals;
   bool                m_clock_primed;
   datetime            m_last_processed_close;

   bool PrimeClockAndLifecycle(const datetime latest_closed)
   {
      datetime boundaries[];
      if(!m_signal_source.CollectCurrentTradingDayClosedBoundaries(latest_closed,boundaries))
         return false;

      int count=ArraySize(boundaries);
      int replay_count=count;
      if(m_execution_config.process_existing_closed_bar_on_init && replay_count>0)
         replay_count--;

      for(int i=0;i<replay_count;i++)
      {
         SCGCFinalSignal replay_signals[];
         int replay_group_indices[];
         datetime replay_day_start=0;
         int signal_count=m_signal_source.BuildConfirmedSignals(boundaries[i],replay_signals,replay_group_indices,replay_day_start);
         m_registry.EnsureTradingDay(replay_day_start);
         for(int j=0;j<signal_count;j++)
         {
            string registry_reason="";
            m_registry.RegisterAttempt(replay_signals[j].signal_id,registry_reason);
         }
      }

      m_clock_primed=true;
      if(m_execution_config.process_existing_closed_bar_on_init)
      {
         if(count>=2)
            m_last_processed_close=boundaries[count-2];
         else
            m_last_processed_close=0;
      }
      else
         m_last_processed_close=latest_closed;

      if(m_execution_config.print_execution_events)
         Print(StringFormat("EXP0017 CGX warmup complete | closed_boundaries=%d | replayed=%d | latest=%s",count,replay_count,TimeToString(latest_closed,TIME_DATE|TIME_SECONDS)));
      return true;
   }

   bool ValidateConfig(string &reason)
   {
      if(m_execution_config.target_model==CGX_TARGET_ATR_MULTIPLE)
      {
         if(m_execution_config.atr_period<1)
         {
            reason="atr_period_must_be_positive";
            return false;
         }
         if(m_execution_config.atr_multiplier<=0.0)
         {
            reason="atr_multiplier_must_be_positive";
            return false;
         }
      }
      if(m_execution_config.target_model==CGX_TARGET_RISK_MULTIPLE && m_execution_config.risk_reward_multiple<=0.0)
      {
         reason="risk_reward_multiple_must_be_positive";
         return false;
      }
      if(m_execution_config.magic_base<=0)
      {
         reason="magic_base_must_be_positive";
         return false;
      }
      if(m_execution_config.enable_hedging && m_execution_config.require_hedging_account && !CGX_IsHedgingAccount())
      {
         reason="hedging_account_required_when_hedging_enabled";
         return false;
      }
      if(m_execution_config.volume_model==CGX_VOLUME_FIXED_RISK_MONEY && m_execution_config.fixed_risk_money<=0.0)
      {
         reason="fixed_risk_money_must_be_positive";
         return false;
      }
      if(m_execution_config.volume_model==CGX_VOLUME_RISK_PERCENT_EQUITY && m_execution_config.risk_percent_equity<=0.0)
      {
         reason="risk_percent_must_be_positive";
         return false;
      }
      if(m_execution_config.volume_model==CGX_VOLUME_FIXED_LOTS && m_execution_config.fixed_lots<=0.0)
      {
         reason="fixed_lots_must_be_positive";
         return false;
      }
      reason="ok";
      return true;
   }

public:
   bool Init(SCGTTimeConfig &time_config,SCGCConfirmationConfig &confirmation_config,SCGXExecutionConfig &execution_config,bool &enabled[])
   {
      m_execution_config=execution_config;
      string reason="";
      if(!ValidateConfig(reason))
      {
         Print("EXP0017 CGX init rejected: ",reason);
         return false;
      }

      m_signal_source.Configure(time_config,confirmation_config,enabled);
      m_planner.Configure(m_execution_config);
      m_registry.Configure(m_execution_config.max_signal_registry_records);
      m_router.Configure(m_execution_config);
      m_audit.Configure(m_execution_config);
      m_visuals.Configure(m_execution_config);
      m_clock_primed=false;
      m_last_processed_close=0;

      Print(StringFormat("EXP0017 CGX initialized | runtime=%s | leg=%s | target=%s | volume=%s | fixed_risk=%.2f %s | hedge=%s | draw=%s | magic_base=%d",
                         CGX_RuntimeText(m_execution_config.runtime_mode),
                         CGX_TradeLegText(m_execution_config.trade_leg),
                         CGX_TargetModelText(m_execution_config.target_model),
                         CGX_VolumeModelText(m_execution_config.volume_model),
                         m_execution_config.fixed_risk_money,
                         AccountInfoString(ACCOUNT_CURRENCY),
                         (m_execution_config.enable_hedging ? "ON" : "OFF"),
                         (m_execution_config.draw_executed_signals ? "ON" : "OFF"),
                         m_execution_config.magic_base));
      return true;
   }

   void Pulse()
   {
      datetime closed_at=m_signal_source.LastClosedCandleCloseBroker();
      if(closed_at<=0)
         return;

      if(!m_clock_primed)
      {
         if(!PrimeClockAndLifecycle(closed_at))
            return;
         if(!m_execution_config.process_existing_closed_bar_on_init)
            return;
      }
      if(closed_at==m_last_processed_close)
         return;
      if(closed_at<m_last_processed_close)
         return;

      m_last_processed_close=closed_at;

      SCGCFinalSignal signals[];
      int group_indices[];
      datetime trading_day_start_ny=0;
      int count=m_signal_source.BuildConfirmedSignals(closed_at,signals,group_indices,trading_day_start_ny);
      m_registry.EnsureTradingDay(trading_day_start_ny);

      for(int i=0;i<count;i++)
      {
         string registry_reason="";
         if(!m_registry.RegisterAttempt(signals[i].signal_id,registry_reason))
            continue;

         SCGXTradePlan plan;
         bool planned=m_planner.Build(signals[i],group_indices[i],plan);
         SCGXExecutionResult result;
         result.attempted=false;
         result.sent=false;
         result.paper_only=false;
         result.order_ticket=0;
         result.deal_ticket=0;
         result.retcode=0;
         result.result_price=0.0;
         result.message="";
         if(planned)
         {
            m_router.Execute(plan,result);
            m_visuals.DrawAcceptedExecution(signals[i],plan,result);
         }
         else
            result.message="plan_rejected_"+plan.rejection_reason;
         m_audit.Write(plan,result);
      }
   }

   void Clear()
   {
      m_registry.Clear();
      m_visuals.Clear();
   }
};

#endif

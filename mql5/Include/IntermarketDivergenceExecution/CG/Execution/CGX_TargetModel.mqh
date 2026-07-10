#ifndef __CGX_TARGET_MODEL_MQH__
#define __CGX_TARGET_MODEL_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelRiskMultiple.mqh>

class CCGX_TargetModel
{
private:
   CCGX_TargetModelATR          m_atr;
   CCGX_TargetModelRiskMultiple m_risk_multiple;

public:
   bool Build(const SCGXExecutionConfig &config,
              const string symbol,
              const ENUM_TIMEFRAMES timeframe,
              const datetime confirmation_close,
              const ECGCSignalDirection direction,
              const double entry_price,
              const double stop_loss,
              double &atr_value,
              double &take_profit,
              string &reason)
   {
      atr_value=0.0;
      take_profit=0.0;

      if(config.target_model==CGX_TARGET_ATR_MULTIPLE)
         return m_atr.Build(config,symbol,timeframe,confirmation_close,direction,entry_price,atr_value,take_profit,reason);

      if(config.target_model==CGX_TARGET_RISK_MULTIPLE)
         return m_risk_multiple.Build(config,symbol,direction,entry_price,stop_loss,take_profit,reason);

      reason="unsupported_target_model";
      return false;
   }
};

#endif

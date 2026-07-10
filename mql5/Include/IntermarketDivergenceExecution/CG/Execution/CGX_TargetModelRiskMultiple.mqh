#ifndef __CGX_TARGET_MODEL_RISK_MULTIPLE_MQH__
#define __CGX_TARGET_MODEL_RISK_MULTIPLE_MQH__

#include <IntermarketDivergenceExecution/CG/Execution/CGX_TargetModelATR.mqh>

class CCGX_TargetModelRiskMultiple
{
public:
   bool Build(const SCGXExecutionConfig &config,
              const string symbol,
              const ECGCSignalDirection direction,
              const double entry_price,
              const double stop_loss,
              double &take_profit,
              string &reason)
   {
      take_profit=0.0;
      if(config.risk_reward_multiple<=0.0)
      {
         reason="risk_reward_multiple_not_positive";
         return false;
      }

      double stop_distance=MathAbs(entry_price-stop_loss);
      if(stop_distance<=0.0)
      {
         reason="risk_multiple_stop_distance_not_positive";
         return false;
      }

      double target_distance=stop_distance*config.risk_reward_multiple;
      if(direction==CGC_DIRECTION_BUY)
         take_profit=entry_price+target_distance;
      else if(direction==CGC_DIRECTION_SELL)
         take_profit=entry_price-target_distance;
      else
      {
         reason="invalid_direction_for_target";
         return false;
      }

      take_profit=CGX_NormalizePrice(symbol,take_profit);
      reason="ok";
      return true;
   }
};

#endif
